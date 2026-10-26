# Worked reliability-design examples

These examples demonstrate the skill's reasoning shape. Adapt the obligations to the actual system;
do not copy domain details blindly.

## Example 1 — Credential rotation controller

### Proposal

A controller rotates tenant signing keys: create a new secret, update services, verify, and revoke
the old secret. Desired state is stored in PostgreSQL; services cache keys for five minutes.

### Question routing

| Question | Judgment |
|---|---|
| Q1 intent | Rotation request needs unique target generation, authorization, non-duplicate key, and “old key is still active” precondition. (`P1`) |
| Q2 state | PostgreSQL is intent authority; secret store, service caches, controller checkpoint, and audit log are partial views. Names are insufficient; use key ID + generation. (`P2`) |
| Q3 transition | `stage-new → distribute → verify-real-auth → activate → revoke-old → collect`; every stage is durable and idempotent. (`P3`, `P10`) |
| Q4 seams | DB↔secret store, controller↔service config, gateway↔key caches, and audit system have explicit late-success/version semantics. (`P4`) |
| Q5 oracle | A real request signed by new key succeeds everywhere; old key fails everywhere only after activation; clean and crash runs normalize to one active generation. (`P5`, `P11`) |
| Q6 propagation | Distribution is bounded by cohort; failure pauses before revoke; no controller may activate a second generation concurrently. (`P6`, `P7`) |
| Q7 fidelity | Candidate run uses the production role and real secret service in canary; cache behavior is compared with the test double. (`P8`, `P14`) |

### Highest risks and acceptance

| Risk | Prevention | Oracle / acceptance |
|---|---|---|
| Crash after new key creation is mistaken for completion | Durable stage and generation; completion requires behavior oracle | Crash after every stage; restart reaches exactly one active generation |
| Stale cache keeps old credential valid | Revoke has cache invalidation/TTL contract and external request probe | Request old token through each gateway/region until all reject before GC |
| Late secret-store success creates duplicate on retry | Idempotency identity plus read-after-timeout resolution | Commit then drop response; retry observes same secret ID, not a second key |
| Rollback queues behind stuck rotation | Separate fenced recovery transition | Wedge distribute stage, then prove recovery can restore LKG without concurrent activation |

### Bad design

`UPDATE keys SET active=true`; restart services; revoke old key. Readiness checks only PostgreSQL.
There is no durable stage, generation fence, cache oracle, or uncertain-result handling.

## Example 2 — Datacenter drain and traffic failover

### Proposal

Drain a degraded cell to two neighboring cells using a global traffic controller.

### Question routing

| Question | Judgment |
|---|---|
| Q1 intent | Drain target/radius and emergency override are typed; dependencies and remaining capacity are preconditions. (`P1`) |
| Q2 state | Traffic, capacity, cache warmth, queues, and service health arrive at different rates; observation age accompanies every decision. (`P2`) |
| Q3 transition | Dependency DAG executes small durable traffic steps with inverse restore. (`P3`, `P10`) |
| Q4 seams | Frontends, caches, databases, queues, auth, and observability have ownership and capacity contracts. (`P4`, `P13`) |
| Q5 oracle | Customer success, P99, error budget, queue age, and data-integrity checks—not routing weights—prove the step. (`P5`) |
| Q6 control | Maximum step/rate/radius, priority arbitration, cold-cache guard, stop and restore are explicit. (`P6`, `P7`) |
| Q7 fidelity | Regular small-radius production drains calibrate dependency and capacity models before disaster scale. (`P8`, `P14`) |

### Recovery contract

1. Verify every mandatory dependency is available in target cells and spare capacity includes
   cold-cache/backlog load.
2. Shift 2%; wait for a health-window based on observations, not a fixed sleep.
3. If guardrails hold, advance through bounded stages. If any degrades, stop and restore that stage.
4. Persist each committed stage and inverse; executor restart resumes without replaying a committed
   routing mutation.
5. If maximum safe target capacity is insufficient, shed/degrade intentionally rather than continue
   the drain.

### Acceptance

- Remove one target dependency, understate target capacity, delay health telemetry, crash the drain
  executor after every stage, and fail one inverse restore.
- The controller must not exceed the current safe radius; it either resumes, compensates, or stops
  in a guarded state with operator-visible evidence.
- A small-radius exercise must falsify a deliberately stale dependency graph.

### Bad design

Move 100% on a fixed five-minute schedule because both target cells are “green.” The transfer cools
caches and overloads shared storage; the recovery action expands the incident.

## Example 3 — Fail-slow quorum service

### Proposal

A metadata client waits for two of three replicas. A replica can remain connected while taking
30 seconds per operation.

### Question routing

| Question | Judgment |
|---|---|
| Q2 state | Liveness and replica health are partial observations; a connected channel is not a usable replica. (`P2`) |
| Q3 transition | Request identity survives retry; a late response cannot apply a second mutation. (`P3`) |
| Q4 seams | Client↔replica contract distinguishes no-send, accepted-then-timeout, slow, stale, and wrong result. (`P4`) |
| Q5 oracle | External completion, unique effect, quorum value consistency, and recovery after slowness ends. (`P5`, `P11`) |
| Q6 propagation | Two valid acknowledgements complete the request; the third is cancelled; per-request and global budgets bound work. (`P6`, `P7`) |
| Q7 fidelity | Latency distributions and fault correlation come from deployment, not a fixed lab average. (`P14`) |

### Acceptance matrix

| Injection | Required evidence |
|---|---|
| One replica 100× slower | SLO stays bounded or request sheds explicitly; slow member does not retain every worker |
| Slow replica commits after caller timeout | Idempotency resolution proves one effect before retry |
| Two replicas return conflicting versions | Quorum value rule rejects/repairs rather than selecting fastest blindly |
| Slowness stops after backlog forms | Goodput and backlog age recover within the stated bound; no metastable retry loop |
| Health endpoint remains green | Application-level probe still detects unusable latency |

### Bad design

Wait for all three because “replication is safer,” retry every timeout at two layers, and use TCP
connectivity as health. One fail-slow replica consumes the pool and spreads outage to healthy work.

## Example 4 — RBAC expansion

### Proposal

Expand a support role from tenant-specific read access to region-wide troubleshooting.

### Question routing

| Question | Judgment |
|---|---|
| Q1 intent | Scope, resource classes, break-glass duration, and ticket identity are validated before policy publish. (`P1`, `P9`) |
| Q2 state | Policy files, compiled gateway policy, application checks, caches, and access logs are distinct views. (`P2`) |
| Q3 transition | Publish and cache activation have generations; revoke/expiry is a tested recovery transition. (`P3`, `P10`) |
| Q4 seams | Identity provider, gateway, application ownership, and data relationships share explicit subject/resource semantics. (`P4`) |
| Q5 oracle | Before/after request-decision diff over production code/data explains every `deny→allow`; real revocation requests verify effect. (`P5`) |
| Q7 fidelity | The isolated test uses production authorization logic and production-shaped relational data. (`P8`, `P14`) |

### Acceptance

1. Build `(subject, resource, action, context)` cases from real access plus cross-tenant/export
   adversarial cases.
2. Run old and new policy through production authorization code against masked relationship data.
3. Block any unexplained `deny→allow`; review intended `allow→deny` impact.
4. Publish to canary generation and make real requests through each material gateway/cache.
5. Revoke and prove the old generation no longer authorizes anywhere.
6. From one suspicious production request, trace the effective policy back to change, actor, ticket,
   and generation.

### Bad design

Review a textual policy diff, publish, and assert that the policy row changed. Under incident
pressure, the on-call uses `GRANT ALL` because denial feedback cannot identify the missing relation.

## Example 5 — AI SRE remediation agent

### Proposal

An agent investigates rising latency and may restart pods, change traffic weights, or clear caches.

### Control boundary

- LLM: proposes hypotheses, evidence queries, and candidate actions.
- Deterministic orchestrator: owns action classification, authorization, preconditions, state
  transitions, write lock, budgets, TNR guardrails, postcondition oracle, undo, and stop.
- Evaluator: runs live/high-fidelity failure scenarios with noise and tool faults before expanding
  autonomy.

### Action tiers

| Tier | Examples | Gate |
|---|---|---|
| Read-only | query metrics/logs/topology | scoped credentials and evidence provenance |
| Reversible write | restart one canary pod, move 1% traffic | deterministic transaction + TNR + undo |
| Irreversible/high radius | delete data, revoke root key, drain region | no autonomous exploration; sandbox/canary and explicit human authority |

### Acceptance

- Same incident with misleading logs, partial telemetry, correlated fault, tool timeout, stale
  topology, and an already-running remediation.
- A wrong hypothesis must end as `unsafe-abstain`, `unknown`, or a fully undone canary—not a
  customer-visible regression.
- Command exit success never counts as resolution; external health and invariant oracles decide.
- Clear-cache proposal must be rejected or canaried when backend/cold-cache capacity is unknown.
- Model or tool changes rerun the suite before write permission expands.

### Bad design

The agent gets cluster-admin shell. It sees high latency, globally clears cache, causes a backend
miss storm, then tries an unrelated scale-up. Each command succeeds, so the benchmark calls it
resolved despite a larger incident.

## Example 6 — Safe extension framework

### Proposal

Tenants upload request filters that run in a high-performance host. A verifier checks filters before
load; some safe filters currently require unsafe helpers to pass.

### Question routing

| Question | Judgment |
|---|---|
| Q1 intent | Extension capabilities, resource budgets, and permitted state transitions are typed at source level. (`P1`, `P9`) |
| Q3 transition | Load/replace/unload is generation-fenced and crash safe. (`P3`) |
| Q4 seams | Source language, compiler, verifier, runtime, and host APIs share a mapped safety contract. (`P4`, `P13`) |
| Q5 oracle | Memory/type/capability invariants plus panic/timeout cleanup and reference-path differential. (`P5`, `P11`) |
| Q6 containment | CPU/memory/time and capability blast radius are hard runtime limits. (`P6`, `P7`) |
| Q7 fidelity | Representative safe and adversarial programs measure false rejection, bypass, and runtime containment. (`P8`, `P14`) |

### Acceptance

- Every verifier failure maps to a source-level object, violated contract, and safe repair.
- Representative safe filters pass without bytecode shaping or unsafe helpers.
- Unsafe escape hatches have explicit capabilities, owners, call sites, and negative tests; trend is
  reviewed.
- Inject panic, timeout, allocation exhaustion, concurrent unload, and compiler/verifier version
  change; the host remains safe and the old/new extension generation cannot overlap incorrectly.
- Post-verification fusion/optimization is checked for semantic and capability equivalence.

### Bad design

A bytecode verifier rejects a safe loop. Developers split the program and share state through an
unsafe helper. The code loads, but the helper bypasses memory/synchronization guarantees and becomes
the real unverified interface.
