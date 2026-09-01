# Q7 — Recovery evidence, fidelity, and diagnosability

Principles: P8, P12, P14. Default provenance: `XU-SYNTHESIS` from `xu-083`, `xu-082`, `xu-024`,
`xu-039`, `xu-040`, `xu-053`, `xu-095`, `xu-087`, `xu-068`, `xu-054`, `xu-038`, `xu-008`,
`xu-018`, `xu-010`, `xu-043`, `xu-049`, `xu-070`, `xu-062`.

## Guideline

For every recovery claim, emulator, simulator, mock, proxy metric, benchmark, or lab substrate,
record:

`decision → required truth → surrogate → known discrepancy → calibration method/cadence`.

Calibration cadence and blast radius are risk-based. Evidence may be periodic, shadow, simulated,
canary, or continuously production-exercised; never demand one mode universally. The test must
contain the identity, version, configuration, data shape, timing, capacity, and fault behavior that
can reverse the decision.

For production diagnosis, preserve effective config/version, cross-layer relationships, dependency
outcomes, and a healthy comparator or relational oracle. Collection must be affordable enough to
run during the incident. More logs without discriminating relations are not diagnosability.

## Worked example

A disaster-recovery plan uses frequent tiny-radius production exercises, periodic larger game days,
and simulation for destructive extremes. Each tier has a declared fidelity gap. Target capacity and
dependency constraints are refreshed from production distributions. A failed exercise records the
effective configuration, transition phase, dependency behavior, and comparable healthy cohort.

## Acceptance

- differential-test every decision-relevant emulator API against the real service on a stated cadence;
- inject a fault the surrogate cannot reproduce and show the gap is tracked rather than hidden;
- interrupt recovery at each stage and resume from durable progress;
- vary identity, versions, production-shaped data, timing, and capacity;
- show a post-incident query can distinguish at least two plausible failure modes from recorded relations;
- demonstrate at the claimed radius, or narrow the claim to the largest evidenced radius.

Failure signal: a green substitute is promoted to universal release evidence, or recovery is called
proven at a radius/fault model the environment never exercised.
