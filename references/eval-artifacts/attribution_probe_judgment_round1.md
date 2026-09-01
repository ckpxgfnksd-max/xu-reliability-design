# Independent attribution judgment — round 1

Evaluator: sealed ephemeral Codex `gpt-5.6-sol`, high reasoning, read-only  
Session: `01a05b17-3424-7921-8852-e9836da90e97`  
Date: 2026-09-01

| # | Result | Reason |
|---|---|---|
| 1 | Pass | Correctly defines Acto 32/56 as undesired state without explicit error, with `XU-DIRECT`, `xu-038`, and denominator 56. It does not use the forbidden “row changed but behavior did not” paraphrase. |
| 2 | Pass | Correctly identifies 58/91 interaction failures as operation-semantic violations, with `XU-DIRECT`, `xu-009`, and accurate nested denominator scope. It does not misclassify all 58 as precondition violations. |
| 3 | Pass | Correctly scopes 69% to the 70 classified bugs in the combined reported Sieve/Acto corpus and qualifies ESR coverage by its model and assumptions. Label and paper ID are correct. |
| 4 | **Fail** | `COMPANION` and no Xu paper ID are correct, but the answer omits the roughly-70% change-caused-outage claim and its organization-specific scope. “No precise/general rate” does not answer the frozen probe and creates a materially misleading omission. |
| 5 | Pass | Correctly limits support to metadata-level compositional-liveness direction and forbids detailed mechanism or evaluation claims because the primary PDF is unavailable. `metadata-only` and `xu-002` are correct. |

**Total: 4/5. Release verdict: NO-GO.**

Logical entailment is sufficient only when it unambiguously supplies the required meaning without a
materially misleading omission. It does not save probe 4 because the required roughly-70% claim is
absent rather than entailed.
