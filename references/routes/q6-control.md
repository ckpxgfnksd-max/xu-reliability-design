# Q6 — Bounded control and soft-fault propagation

Principles: P6, P7. Default provenance: `XU-SYNTHESIS`; anchors Taiji `xu-077`, Maelstrom
`xu-083`, Slooo fail-slow support `xu-065`, DepFast `xu-056`, Kscaler `xu-014`.

## Guideline

For every controller, autoscaler, traffic manager, tuner, or remediation agent, state:

- objective and hard safety constraints;
- authoritative observation source, its delay and uncertainty, and what the controller does when
  telemetry is stale, missing, or contradictory;
- maximum step, rate, concurrency, affected population, and capacity guard;
- priority or conflict arbitration for shared observations or actuators, including manual tools
  and operator overrides (this question owns arbitration between automated actuator writers;
  concurrent runs of one non-controller job, and identity or staleness generally, are Q2);
- LKG or fallback, stop condition, recovery, and write exclusivity where needed;
- restart behavior: after a crash or redeploy the controller re-observes before acting and never
  replays a decision computed from pre-restart telemetry.

For every dependency, distinguish `down`, `slow`, `intermittent`, `wrong`, `stale`, `duplicate`, and
`success after timeout`. Trace queue, thread, and connection retention and downstream amplification.
Bound deadlines, retries, concurrency, and backlog; cancel useless work and isolate slow work. When
the controller pushes to targets that can be unreachable for long periods (devices, edge nodes,
remote regions), bound per-target retry, total backlog, and backlog age, and state what happens at
the bound and what a late-reconnecting target receives. Generic retry-budget formulas are
`COMPANION`; the need to treat slow and interaction faults separately is `XU-SYNTHESIS`.

## Worked example

A traffic controller clips each move, validates remaining target capacity, serializes with other
traffic tools through one priority pipeline, stops on stale or unhealthy telemetry, and restores LKG
on validation failure. A slow target is not treated as green merely because TCP accepts connections.

## Acceptance

- delay one dependency while connectivity and health remain green;
- inject intermittent completion, wrong-but-schema-valid data, stale telemetry, and late success;
- run two controllers, or a controller and a manual tool, concurrently against the shared actuator;
- restart the controller mid-action from its durable state; it must re-observe, not re-apply;
- disconnect a large cohort of targets for longer than the retry horizon; backlog stays bounded and
  a reconnecting target does not receive superseded intent;
- exhaust target capacity and remove a fault domain during a move;
- abandon a caller mid-work: deadlines propagate, and work completing after abandonment is cancelled
  or accounted for and cannot silently commit twice (`P7`);
- hold a dependency slow until retries and hedges spend their end-to-end budget: total attempts stay
  within it, queues and worker/connection pools stay bounded, and the dependency cannot monopolize
  every worker or quorum wait or spread failure beyond the stated domain (`P7`; retry-budget mechanics may use
  `COMPANION` guidance);
- observe useful goodput, occupied resources, retry work, backlog age, shed work, and time to recover
  after the fault ends (`P7`);
- prove the controller stays within step, rate, and radius bounds and stops when evidence is
  insufficient.

Choose latency multipliers from measured operating distributions. `10×` or `100×` is only an
illustrative stress point, not a Xu-derived universal threshold.

Failure signal: the safety argument is "the value is stored atomically" or "we retry until it
succeeds"; nothing says what happens on restart, on a second writer, or when the backlog never
drains.
