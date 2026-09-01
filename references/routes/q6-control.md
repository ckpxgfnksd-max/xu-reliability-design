# Q6 — Bounded control and soft-fault propagation

Principles: P6, P7. Default provenance: `XU-SYNTHESIS` from `xu-077`, `xu-083`, `xu-014`,
`xu-012`, `xu-026`, `xu-030`, `xu-034`, `xu-006`, `xu-065`, `xu-056`, `xu-089`, `xu-046`,
`xu-047`, `xu-088`.

## Guideline

For every controller, autoscaler, traffic manager, tuner, or remediation agent, state:

- objective and hard safety constraints;
- authoritative observation source, delay, and uncertainty;
- maximum step, rate, concurrency, affected population, and capacity guard;
- priority/conflict arbitration for shared observations or actuators;
- LKG/fallback, stop condition, recovery, and write exclusivity where needed.

For every dependency, distinguish `down`, `slow`, `intermittent`, `wrong`, `stale`, `duplicate`, and
`success after timeout`. Trace queue/thread/connection retention and downstream amplification. Bound
deadlines, retries, concurrency, and backlog; cancel useless work and isolate slow work. Generic
retry-budget formulas are `COMPANION`; the need to treat slow/interaction faults separately is
`XU-SYNTHESIS`.

## Worked example

A traffic controller clips each move, validates remaining target capacity, serializes with other
traffic tools through one priority pipeline, stops on stale/unhealthy telemetry, and restores LKG
on validation failure. A slow target is not treated as green merely because TCP accepts connections.

## Acceptance

- delay one dependency while connectivity/health remains green;
- inject intermittent completion, wrong-but-schema-valid data, stale telemetry, and late success;
- run two controllers concurrently against the shared actuator;
- exhaust target capacity and remove a fault domain during a move;
- observe useful goodput, backlog, shed work, and recovery after the fault ends;
- prove the controller stays within step/rate/radius bounds and stops when evidence is insufficient.

Choose latency multipliers from measured operating distributions. `10×` or `100×` is only an
illustrative stress point, not a Xu-derived universal threshold.
