# Companion: risk-calibrated capacity and readiness gate

Everything in this file is **COMPANION**, not Xu-derived. Load it only when capacity, overload,
metastability, fleet rollout, SLOs, or failure-domain readiness materially changes the decision.
Treat each item as a question to calibrate, never as a universal architecture mandate.

## Structural walk

1. Map each externally visible operation to components and dependencies.
2. For each dependency, test `down / slow / wrong / stale / duplicate-or-late-success`.
3. For each component, consider duplicate authority/split brain and overload.
4. Remove each claimed fault domain—process, host, rack, zone, region—and recompute capacity.
5. Treat deployment/configuration change as a failure source with its own containment.
6. Run a premortem only as a supplement to the structural walk, not as evidence.

## Decision-calibrated questions

### Demand, SLO, and capacity

- Which customer behavior and SLO is this design protecting?
- What are expected and tail QPS, payload, state volume, growth, concurrency, and cost?
- What capacity remains after the largest claimed fault domain and during recovery?
- Which input distributions and correlations support the arithmetic, and when are they refreshed?

Numbers make assumptions falsifiable; they do not make the design correct. Avoid fixed universal
headroom or load multipliers. Choose stress points from the system's demand and failure model.

### Failure containment and overload

- What is the isolation unit and maximum affected population for hardware failure, bad deploy,
  poison input, correlated dependency failure, and controller error?
- Which work is admitted, shed, degraded, or queued first?
- Are concurrency, queues, and work age bounded, with an explicit behavior when full?
- Can retry, cache-miss, failover, garbage collection, or rework sustain overload after the trigger
  ends? What breaks each feedback loop, and how does the system recover goodput?

Retry budgets, jitter, circuit/adaptive limiting, shuffle sharding, and static stability are design
options, not mandatory patterns. Select them only after stating the failure mechanism and oracle.

### Degraded and recovery paths

For every fallback or recovery branch, choose evidence proportional to risk: unit/property tests,
simulation, shadow execution, periodic game day, canary, or continuous production use. A rarely used
fallback with no recurring evidence is a risk, but “continuously exercise or delete” is not a
universal rule.

State whether recovery depends on a control plane or just-in-time capacity. If it does, that
dependency becomes part of the recovery failure model; it is not automatically forbidden.

### Rollout and rollback

- What is the smallest production radius and expansion sequence?
- Which behavioral, integrity, capacity, and saturation signals gate each stage?
- Which states are backward/forward compatible, reversible, compensatable, or irreversible?
- When is automated rollback demonstrably safer, and when must automation stop for review?

Do not require “automatic rollback with no human” universally. A rollback can worsen the incident,
and irreversible or state-transforming changes may need forward repair, dual-read/write periods, or
approval. Apply Q3/P10.

### Irreplaceable state

Money or irreplaceable state raises consequence; it does not by itself mandate one data model.
Require a stated conservation invariant, idempotency/duplicate-effect story, authoritative record,
divergence detection, recovery, and an adequate verification method. Double-entry ledgers,
append-only logs, reconciliation jobs, runtime assertions, reference models, or model checking are
candidate mechanisms chosen by the domain and invariant.

### Formality tier

Choose the least method that closes the relevant evidence gap:

- types/schema and local invariants;
- stateful/property tests;
- deterministic simulation or executable reference model;
- model checking of a compact concurrency/recovery protocol;
- proof for a stable, high-consequence boundary.

Testability is easier when nondeterminism is abstracted early, but legacy systems can still be
incrementally wrapped and calibrated. Do not claim simulation or formality is impossible to add
later. See `formal-verification.md`.

## Acceptance template

| Claim | Input distribution / fault | Observable bound or relation | Recovery evidence | Radius | Source class |
|---|---|---|---|---|---|

Every row must say what evidence would falsify the claim. “Industry best practice” and an uncited
fixed multiplier are not acceptance criteria.

## Companion source families

If citing a specific practice, verify and link the exact primary source at use time:

- Google SRE design/production-readiness and NALSD material;
- AWS Builders' Library, operational-readiness, and static-stability material;
- Azure Safe Deployment Practices;
- metastable-failure research;
- correctness-practice reports from industrial systems.

These sources may have changed since this snapshot. Their presence here does not transfer their
assumptions to the reviewed system.
