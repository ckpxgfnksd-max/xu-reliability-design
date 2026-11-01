# Q1 — Intent boundary and usable repair

Principles: P1, P9. Default provenance: `XU-SYNTHESIS`; anchors SPEX `xu-097`, PCheck `xu-087`,
ctest `xu-068`, Too Many Knobs `xu-093`, access-denied study `xu-086`.

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
- violate a hidden operation precondition, add an unknown owned key, and try a candidate value that
  triggers a dormant bug;
- use the real runtime identity and a stale version pair;
- prove rejection occurs at the earliest layer able to know it, before external effects, with a
  distinguishable and repairable explanation;
- compare declared policy with actual allow/deny behavior through caches and gateways.
- send a valid-but-unusual candidate through a behavioral test; it must not be rejected only for
  looking unfamiliar.

Failure signal: validation is green while the candidate produces silent no-effect, over-grant,
late-path failure, or requires an unsafe workaround.
