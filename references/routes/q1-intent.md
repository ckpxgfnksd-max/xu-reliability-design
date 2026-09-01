# Q1 — Intent boundary and usable repair

Principles: P1, P9. Default provenance: `XU-SYNTHESIS` from `xu-097`, `xu-096`, `xu-094`,
`xu-093`, `xu-090`, `xu-087`, `xu-086`, `xu-084`, `xu-073`, `xu-069`, `xu-068`, `xu-060`,
`xu-052`, `xu-057`, `xu-033`, `xu-017`.

## Guideline

For every configuration, policy, operator, API, scheduler, plugin, or agent input:

1. name the accepting boundary and the component that owns rejection;
2. define semantic type, cross-field/component constraints, and environment references;
3. validate with the production identity and relevant deployed versions before effects;
4. exercise affected behavior when a locally valid value can activate dormant code;
5. reject atomically with field/action, violated relationship, likely impact, and safe repair;
6. justify each knob or escape hatch; prefer constrained intent over many coupled controls.

An LLM may propose constraints or explanations, but cannot be the sole deterministic gate. Removing
a knob is justified by redundant semantics, non-use plus safe derivation, or an unsafe state-space
cost—not merely by a population statistic.

## Worked example

A failover configuration names a target replica and KMS key. Regex validation passes, but neither
path runs until disaster. The accepting service resolves both with the failover identity, verifies
replica catch-up and fencing, performs a safe encrypt/decrypt probe, and rejects before scheduling
the cutover. The response identifies the failing precondition and data-loss or lockout consequence.

## Acceptance

- mutate one value within its legal syntax but outside its environmental constraint;
- change two valid fields into an invalid relationship;
- activate a late/rare path with the candidate configuration;
- use the real runtime identity and a stale version pair;
- prove rejection occurs before external effects and gives a repairable explanation;
- compare declared policy with actual allow/deny behavior through caches and gateways.

Failure signal: validation is green while the candidate produces silent no-effect, over-grant,
late-path failure, or requires an unsafe workaround.
