# Q8 — Diagnosability and evidence preservation

Principle: P12. Default provenance: `XU-SYNTHESIS`; anchors Kscope live forensics `xu-070`,
relational debugging `xu-043`, Vetter counterfactuals `xu-049`, P-DIFF `xu-076`, Eroica `xu-010`.
Where to place observation so that it sees semantic ground truth is P13, handled under Q4.

## Guideline

Diagnosability is a designed relation between recorded evidence and the mitigations that differ,
not a volume of logs. For a production diagnosis, an observability or forensics design, or a change
that alters incident evidence:

- start from the failure modes that need different or opposite mitigations, and design the evidence
  that separates them;
- record effective configuration and version or generation, actor and intent, transition phase,
  dependency outcomes, and a redacted behavioral result, not only the symptom;
- keep a healthy comparator (cohort, time window, or clean execution) or a relational oracle,
  because absolute thresholds cannot separate workload effects from defects;
- preserve cross-layer relationships (request → resolver → upstream attempt → queue time → commit)
  so a query can walk the path after the fact;
- make collection affordable enough to stay on during the incident; a debug mode that cannot stay
  enabled is not production diagnosability;
- preserve change provenance so a suspicious outcome links back to the responsible change.

## Worked example

One customer cohort sees 3-second pauses while aggregate latency is normal and logs say only
"request timeout". The design adds, per request: resolver path and answer source, configuration
generation, upstream attempt outcome, and queue time, all keyed by cohort. A post-incident query
compares the affected cohort with a healthy one and separates "stale resolver cache on one node"
from "new configuration generation reached this cohort first" from "upstream slow for this key
range". Collection cost is measured and left on.

## Acceptance

- from one customer-visible symptom, reconstruct intent, actor, effective configuration and version,
  transition sequence, and dependency outcomes without relying on ephemeral in-memory state;
- show a stored query that distinguishes at least two plausible causes with different mitigations;
- show the comparator (healthy cohort, prior window, or clean run) the diagnosis depends on and how
  it is kept current;
- measure the overhead of the evidence path and prove it stays enabled under incident load;
- link one suspicious outcome to its originating change, actor, and generation.

Failure signal: the incident record says what failed but not which configuration, version, path, or
comparator it failed under; the only proposal is "add more logs"; the evidence needed for diagnosis
exists only in a debug mode that is off in production.
