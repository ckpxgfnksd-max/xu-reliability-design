# Worked reliability-design examples

These examples demonstrate the skill's reasoning shape. Adapt the obligations to the actual system;
do not copy domain details blindly.

Examples 1 to 4 are deliberately large systems. Most reviews select two to four questions; Example 5
shows that shape, Example 6 shows a decline, and Example 7 shows the Check form.

## Example 1 — Credential rotation controller

### Proposal

A controller rotates tenant signing keys: create a new secret, update services, verify, and revoke
the old secret. Desired state is stored in PostgreSQL; services cache keys for five minutes.

### Question routing

| Question | Judgment |
|---|---|
| Q1 Intent | Rotation request needs unique target generation, authorization, non-duplicate key, and “old key is still active” precondition. (`P1`) |
| Q2 State | PostgreSQL is intent authority; secret store, service caches, controller checkpoint, and audit log are partial views. Names are insufficient; use key ID + generation. (`P2`) |
| Q3 Change | `stage-new → distribute → verify-real-auth → activate → revoke-old → collect`; every stage is durable and idempotent. (`P3`, `P10`) |
| Q4 Seams | DB↔secret store, controller↔service config, gateway↔key caches, and audit system have explicit late-success/version semantics. (`P4`) |
| Q5 Correctness | A real request signed by new key succeeds everywhere; old key fails everywhere only after activation; clean and crash runs normalize to one active generation. (`P5`, `P11`) |
| Q6 Control | Distribution is bounded by cohort; failure pauses before revoke; no controller may activate a second generation concurrently. (`P6`, `P7`) |
| Q7 Fidelity | Candidate run uses the production role and real secret service in canary; cache behavior is compared with the test double. (`P8`, `P14`) |

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

## Example 2 — Fail-slow quorum service

### Proposal

A metadata client waits for two of three replicas. A replica can remain connected while taking
30 seconds per operation.

### Question routing

| Question | Judgment |
|---|---|
| Q2 State | Liveness and replica health are partial observations; a connected channel is not a usable replica. (`P2`) |
| Q3 Change | Request identity survives retry; a late response cannot apply a second mutation. (`P3`) |
| Q4 Seams | Client↔replica contract distinguishes no-send, accepted-then-timeout, slow, stale, and wrong result. (`P4`) |
| Q5 Correctness | External completion, unique effect, quorum value consistency, and recovery after slowness ends. (`P5`, `P11`) |
| Q6 Control | Two valid acknowledgements complete the request; the third is cancelled; per-request and global budgets bound work. (`P6`, `P7`) |
| Q7 Fidelity | Latency distributions and fault correlation come from deployment, not a fixed lab average. (`P14`) |

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

## Example 3 — RBAC expansion

### Proposal

Expand a support role from tenant-specific read access to region-wide troubleshooting.

### Question routing

| Question | Judgment |
|---|---|
| Q1 Intent | Scope, resource classes, break-glass duration, and ticket identity are validated before policy publish. (`P1`, `P9`) |
| Q2 State | Policy files, compiled gateway policy, application checks, caches, and access logs are distinct views. (`P2`) |
| Q3 Change | Publish and cache activation have generations; revoke/expiry is a tested recovery transition. (`P3`, `P10`) |
| Q4 Seams | Identity provider, gateway, application ownership, and data relationships share explicit subject/resource semantics. (`P4`) |
| Q5 Correctness | Before/after request-decision diff over production code/data explains every `deny→allow`; real revocation requests verify effect. (`P5`) |
| Q7 Fidelity | The isolated test uses production authorization logic and production-shaped relational data. (`P8`, `P14`) |

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

## Example 4 — AI SRE remediation agent

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

## Example 5 — Two-question review: TLS certificate replacement

### Proposal

Replace the certificate on one reverse proxy before it expires, then reload the proxy. No other
component holds the certificate.

### Question routing

| Question | Judgment |
|---|---|
| Q3 Change | Install and reload are two effects; a failed reload with the new file in place leaves the next restart broken. |
| Q8 Diagnosability | During an incident a responder must tell which certificate is actually served, not which file is on disk. |

No other component depends on the certificate and nothing acts on it automatically, so the
remaining triggers are no and the review says nothing about them. The gap between file and served
certificate matters here only as diagnostic evidence, which is why it sits under Q8.

### Risk chains

```text
Risk: reload fails after the file is swapped  (Q3, P3)
Trigger → consequence: invalid chain, reload refused → current process serves the old cert until the next restart, which then fails to start
Prevention: validate the new pair with the proxy's config check before the swap; keep the old pair beside it
Oracle: an external TLS handshake returns the new serial and expiry
Recovery: restore the old pair and reload; the handshake returns the old serial
Acceptance: install a deliberately mismatched key; check refuses before the swap; external handshake unchanged
```

```text
Risk: responder trusts the file on disk  (Q8, P12)
Trigger → consequence: new file present, old process still serving → incident triage rules out the certificate while the expired one is live
Prevention: record the served serial and expiry at the observation point responders use
Oracle: the recorded serial equals the one an external handshake returns
Recovery: compare the served serial against the file and reload or restore the pair
Acceptance: swap the file without reloading; the record still shows the old serial and differs from the file
```

## Example 6 — Decline

### Proposal

Rename a label and add a sort option to a settings page.

### Answer

No trigger is yes, so say that in one line and do the task. Do not list the questions that were not
selected.

## Example 7 — Check form during execution

### Task

An agent is closing a development port that a workstation exposed on all interfaces. The deliverable
is the closed port, so the risk lines go in the task's existing plan.

```text
Risk: rule passes locally but the port stays reachable  (Q7)
Trigger → consequence: firewall rule matches one binary or one address family → port still open from another host
Acceptance: connect from a second host over each interface and over IPv4 and IPv6, with a known-open control port; no connection to the closed port is established; the loopback use still works
Recovery: remove the added rule from the saved ruleset; tested in this session
```

Testing from the same machine would pass while the risk stands, which is why the acceptance names
an off-host observation point.
