# Q5 — Behavioral correctness, progress, and conformance

Principles: P5, P11. Default provenance: `XU-SYNTHESIS` from `xu-054`, `xu-038`, `xu-068`,
`xu-076`, `xu-043`, `xu-049`, `xu-026`, `xu-020`, `xu-031`, `xu-021`, `xu-004`, `xu-011`.

## Guideline

Define executable oracles for:

- safety/conservation: what must never happen, be lost, duplicated, or over-granted;
- progress: under named fault/fairness assumptions, what must eventually happen;
- stability: after matching intent, what remains matched until intent changes;
- effective behavior: what a real client can do through caches, replicas, and gateways;
- relations: perturbed vs clean, before vs after, declared vs effective, good vs bad;
- model–implementation conformance when a formal model is used.

For a reconciliation loop, ESR is a useful starting contract: if desired state eventually stops
changing and named dependencies/faults eventually satisfy their assumptions, actual state
eventually matches and stays matched. Specialize it when bounded convergence or domain safety is
needed. A watchdog observes re-divergence; it is not a proof.

## Worked example

“Suspend tenant” is tested with real requests through every authorization cache. The safety oracle
requires all scoped requests denied and unrelated tenants unchanged; progress is bounded cache
convergence under stated availability; stability requires no re-allow until intent changes. A
before/after request-decision diff explains every changed outcome.

## Acceptance

- perturb stale/unobserved state and compare evolution with a clean execution;
- generate legal operation sequences, including recovery, and test state relations;
- exercise real clients instead of inspecting rows or return codes;
- map model variables/actions to implementation state/transitions;
- replay implementation traces against the model without weakening invariants to obtain green;
- turn every minimized counterexample into an executable regression.

Welder (`xu-002`) is `metadata-only`; do not claim a verified compositional-liveness theorem.
Treat interacting controllers as a seam/control risk until primary evidence is available.
