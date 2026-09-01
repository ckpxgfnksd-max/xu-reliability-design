# Sealed fresh-context attribution probe prompt — round 2

Generator: ephemeral Codex `gpt-5.6-sol`, high reasoning, read-only  
Session: `01a05b19-9e5f-75e3-a2fd-5ee45c41c961`  
Date: 2026-09-01

The generator was instructed not to call tools, read files, browse, load skills, or add commentary,
and to use only these primary-evidence-derived statements:

- Acto reports 56 bugs; 32 were undesired-state bugs where the operator failed to reach desired
  state without explicit error.
- OAT reports 58 of 91 operator-application interaction failures as operation-semantic violations;
  the 91 are nested within 215 external-interaction defects from 412 closed cases across 11
  operator projects.
- Anvil authors classified 70 bugs from the combined reported Sieve and Acto corpus; 69 percent
  were violations ESR would preclude under the verified model and stated environment, fault, and
  fairness assumptions.
- A Google SRE rule of thumb says roughly 70 percent of outages are caused by changes to a live
  system; it is organization-specific non-Xu companion evidence and no finer denominator is supplied.
- Welder primary PDF was unavailable; only official title/artifact metadata indicates compositional
  liveness verification of cluster control planes.

Each answer was required to state both the correct claim and the forbidden generalization: Acto is
not row-changed-but-behavior-did-not; OAT operation-semantic violations are not all precondition
violations; Anvil is not an arbitrary-controller rate; Google is `COMPANION`, not Xu, and the
roughly-70-percent wording stays approximate; Welder has no auditable mechanism or evaluation detail.

Output contract: exactly one JSON object with a `probes` array of five objects containing `probe`,
`answer`, `evidence_label`, `paper_ids`, and `denominator_scope`; no self-assigned pass/fail.
