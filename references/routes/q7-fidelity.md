# Q7 — Fidelity of evidence and calibration of assumptions

Principles: P8, P14. Default provenance: `XU-SYNTHESIS`; anchors Maelstrom `xu-083`, Cloud
Emulator Fidelity `xu-024`, PCheck `xu-087`, datacenter network reliability `xu-082`, SREGym
`xu-008`.

## Guideline

For every recovery claim, emulator, simulator, mock, proxy metric, benchmark, offline reward, or lab
substrate, record:

`decision → required truth → surrogate → known discrepancy → calibration method and cadence`.

Cadence and blast radius are risk-based. Evidence may be periodic, shadow, simulated, canary, or
continuously production-exercised; never demand one mode universally. The test must contain the
identity, version, configuration, data shape, timing, capacity, and fault behavior that can reverse
the decision. A test that cannot produce the fault model is not evidence for it.

Every capacity, timeout, gain, threshold, or fault-correlation assumption names the deployed
population it was measured on, the cohort and tail it preserves, and the event that triggers
recalibration (topology, version, or workload change). A controller tuned on a lab average or an
offline reward has not been calibrated.

## Worked example

A disaster-recovery plan uses frequent tiny-radius production exercises, periodic larger game days,
and simulation for destructive extremes. Each tier has a declared fidelity gap. Target capacity and
dependency constraints are refreshed from production distributions. A restore rehearsal uses the
real credential and key path with redacted production-shaped data, and the recovery claim is stated
at the largest radius actually exercised.

## Acceptance

- differential-test every decision-relevant emulator or simulator API against the real service on
  a stated cadence;
- inject a fault the surrogate cannot reproduce and show the gap is tracked rather than hidden;
- interrupt the rehearsed recovery at each stage and resume from durable progress;
- vary identity, versions, production-shaped data, timing, and capacity;
- show the distribution behind each threshold or gain and repeat the calibration after one
  topology or version shift;
- demonstrate at the claimed radius, or narrow the claim to the largest evidenced radius.

Failure signal: a green substitute is promoted to universal release evidence; recovery is called
proven at a radius or fault model the environment never exercised; a controller's gains come from a
simulator whose decision-relevant behavior was never compared with production.
