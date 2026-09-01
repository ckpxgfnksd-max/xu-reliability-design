# Research map and attribution guardrails

Load this file when a design decision needs paper-level justification or when checking whether a
claim belongs to Tianyin Xu's research. Use `paper-ledger.md` for the complete 97/97 inventory.

## Corpus and method

- Canonical inclusion source: [Tianyin Xu's official publications page](https://tianyin.github.io/pub.html),
  snapshot 2026-09-01, 97 entries.
- Full text was locally extracted and principle-screened for 94 papers. The first pass gave 49
  high-relevance papers a mechanism-level close read; the second pass read the remaining 45
  available papers' abstract, problem, design, limitations/threats, and conclusion. Three official
  links were unavailable in this pass:
  `xu-002` Welder, `xu-003` MCon, and `xu-005` Rex TOCS. The ATC Rex version is available as
  `xu-017`.
- Final routing judgment: `54 direct`, `39 adjacent`, `4 none`. Welder `xu-002` remains a
  metadata-only adjacent direction and is excluded from unqualified direct evidence. These are skill-contribution labels,
  not paper-quality rankings. `xu-037` and `xu-040` are one research unit and are not double-counted
  as independent support for a synthesis.
- Principles were promoted only when they changed a failure model, invariant, change/recovery path,
  acceptance check, or system boundary and recurred in at least two Xu-coauthored papers.
- Performance mechanisms without a transferable reliability judgment remain `adjacent` or `none`.
  This is deliberate pruning, not omission.

## Research threads

### 1. Configuration is an executable change surface

Core papers: SPEX `xu-097`, EnCore `xu-096`, configuration survey `xu-094`, Too Many Knobs
`xu-093`, PCheck `xu-087`, configuration evolution `xu-066`, cDep `xu-069`, ctest `xu-068`,
ConfigX `xu-060`, ctest prioritization `xu-063`, uRTS `xu-048`, Ctest4J `xu-033`, Ciri
`xu-025`, ConfFuzz `xu-001`.

Recurring conclusion: value-local validation is necessary but insufficient. Configuration meaning
depends on environment, correlated parameters, affected code, and latent paths. The accepting
system owns early rejection and useful repair feedback. Excess flexibility enlarges the state and
test space, so control-surface reduction precedes more validation.

### 2. Operations and controllers are state-transition programs

Core papers: Partial Histories `xu-064`, Sieve `xu-054`, Acto `xu-038`, Anvil `xu-031`, OAT
`xu-009`, CSI failures `xu-046`, Rainmaker `xu-047`, Mux `xu-019`, Concord `xu-028`, Android
interruptible maintenance `xu-072`, Multi-Grained Specifications `xu-021`, Welder `xu-002`
(title/artifact metadata only in this pass).

Recurring conclusion: operations, operation sequences, crashes, stale views, unobserved states,
misoperations, hidden application semantics, and other controllers are part of the input space.
Correctness needs end-to-end oracles plus progress/stability contracts, not only error checks.

### 3. Recovery and adaptive control can cause the next failure

Core papers: Maelstrom `xu-083`, Taiji `xu-077`, datacenter-network reliability `xu-082`,
Stratus `xu-012`, Acto `xu-038`, OAT `xu-009`, Xkernel `xu-006`.

Recurring conclusion: drain, failover, tuning, rollback, and remediation are live mutations under
degraded observability. They need dependency/capacity constraints, bounded steps, health feedback,
durable progress, stop conditions, restore, and no-regression guardrails.

### 4. Soft failure and real-environment fidelity are first-class

Core papers: fail-slow support `xu-065`, ScalaCN `xu-026`, DepFast `xu-056`, NChecker `xu-089`,
cellular reliability `xu-062`, Android cross-app blocking `xu-072`, Cloud Emulator Fidelity
`xu-024`, Virtual Device Farms `xu-040`, genuine CXL characterization `xu-039`, Kscaler `xu-014`.

Recurring conclusion: connected is not usable; a slow or intermittently wrong component can spread
failure farther than a crashed one. Mocks, emulators, proxy metrics, and similar hardware are useful
only relative to a decision-specific fidelity contract with real-system calibration.

### 5. Security correctness is effective behavior plus usable enforcement

Core papers: P-DIFF `xu-076`, access-control testing `xu-020`, access-denied study `xu-086`,
Dossier `xu-059`, Rex `xu-017`, kernel-verification position paper `xu-044`, seccomp-eBPF
`xu-052`, KFuse `xu-057`, Draco `xu-071`.

Recurring conclusion: declared policy or verifier acceptance is not the external security effect.
Continuously compare intended with effective decisions, preserve provenance, and align the safety
contract with the abstraction developers/operators actually use; otherwise workarounds and unsafe
escape hatches accumulate.

### 6. Diagnosability is a designed evidence relation

Core papers: Live Forensics/Kscope `xu-070`, Relational Debugging `xu-043`, Vetter `xu-049`, Dossier
`xu-059`, process-state observation `xu-030`, RCA Copilot `xu-036`, Eroica `xu-010`, fast kernel
probes `xu-032`.

Recurring conclusion: more logs are not enough. Evidence must preserve application semantics,
cross-layer relationships, effective configuration/version, and a comparable healthy baseline;
collection must be cheap enough to run where the incident occurs.

### 7. AI reliability depends on the harness around the model

Core papers: Stratus `xu-012`, SREGym `xu-008`, ITBench `xu-018`, SysMoBench `xu-011`, Specula
`xu-004`, RCA Copilot `xu-036`, Ciri `xu-025`.

Recurring conclusion: LLMs may propose hypotheses or actions, but deterministic orchestration,
authorization, executable preconditions, write exclusivity, transactional undo, postcondition
oracles, conformance checking, and live high-fidelity evals determine production safety.

### 8. Semantics-aligned placement and explicit coordination

Papers across this architecture thread: Kscaler `xu-014`, Mux `xu-019`, Oxbow `xu-007`, Xkernel
`xu-006`, Rex `xu-017`, seccomp-eBPF `xu-052`, KFuse `xu-057`, EMT/DMT `xu-016`/`xu-035`,
HugeGPT `xu-042`, and scoped cache placement in Draco `xu-071`.

Recurring architecture lesson: observe/enforce at the layer with semantic truth; preserve mature
subsystem responsibilities; make ownership, journaling, coherence, and recovery explicit where
responsibility is split. This route is conditional because many papers' main contribution is
domain-specific performance, not a universal reliability rule.

### 9. Deployment measurement is part of design, not post-hoc evaluation

Core papers: Swiftest/mobile bandwidth `xu-053`, cellular reliability `xu-062`, low-cost bandwidth
testing `xu-067`, datacenter-network reliability `xu-082`, genuine CXL characterization `xu-039`,
GPU memory envelopes `xu-041`, container-image field context `xu-084`, TrafficGuard `xu-091`,
offline-download routing `xu-092`, and cloud-storage measurement design `xu-095`.

Recurring conclusion: separate observable deployment factors from controllable design choices;
preserve distributions, cohorts, topology and correlations; state the measurement method's own
noise, coverage, cost and staleness; and feed field behavior/overrides back into thresholds,
defaults, placement and test selection. A field statistic constrains the studied population—it does
not become a universal constant.

## Audited quantitative claims

Use these only with their study scope. The skill does not need numbers to apply the principle.

| Claim | Audited wording |
|---|---|
| SPEX silent reactions | In SPEX's seven-system fault-injection corpus, 599 of 743 bad-reaction vulnerabilities were silent violation or silent ignorance. `XU-DIRECT`, `xu-097`. |
| PCheck latent incidents | In one anonymous commercial-storage customer-issue sample, latent configuration errors were 75% of high-severity configuration issues. `XU-DIRECT`, `xu-087`; do not generalize as an industry base rate. |
| Rarely used knobs | In three studied systems, 31.1–54.1% of ordinary-user parameters were changed by fewer than 1% of users. `XU-DIRECT`, `xu-093`; this supports review/hide/simplify, not automatic deletion. |
| ctest benchmark | ctest reported 62/64 detections in its real-failure benchmark; value checkers detected 0 of the 13 valid-change-triggered-bug cases. `XU-DIRECT`, `xu-068`; dataset-specific. |
| Sieve oracles | In Sieve's 46-bug Kubernetes-controller corpus, differential state-evolution oracles flagged 45; exception/crash checks flagged 5. `XU-DIRECT`, `xu-054`. |
| Acto 32/56 | Acto found 56 bugs; 32 were undesired-state bugs where the operator failed to reach desired state without an explicit error. `XU-DIRECT`, `xu-038`. Do not paraphrase this as “row changed but behavior did not.” |
| OAT interactions | In 412 closed failure cases from 11 operator projects, 215 (52.2%) were external-interaction defects; 91 of those were operator–application interactions. `XU-DIRECT`, `xu-009`. |
| OAT semantics | Of the 91 operator–application interaction failures, 58 (63.7%) were operation-semantic violations. This is not the count of precondition violations. `XU-DIRECT`, `xu-009`. |
| ESR bug analysis | Anvil authors classified 70 Sieve/Acto bugs—69% of those tools' combined reported corpus—as violations ESR would preclude under the verified model and assumptions. `XU-DIRECT`, `xu-031`; not a universal 69% controller-bug rate. |
| Anvil effort | For Anvil's three evaluated Rust/Kubernetes controllers, proof-to-code ratio was 4.5–7.4 and implementation took about 2.5 person-months per controller with reusable framework support. `XU-DIRECT`, `xu-031`; do not use as a generic formal-methods cost. |
| Cloud emulator fidelity | In the ICSE'25 study of five cloud services, 94 of 255 studied APIs showed a real-service/emulator discrepancy for the studied functional behavior. `XU-DIRECT`, `xu-024`; it did not measure all performance/fault behavior. |
| Ciri | Across its evaluated models/projects, the best average file-level F1 was 0.79 and best parameter-level average 0.65. `XU-DIRECT`, `xu-025`; use as an auxiliary signal, not sole gate. |

## Claims removed from the previous skill

- **“Xu's program covers the Google 70%.”** Google SRE's roughly-70% change-outage statement is
  organization-specific companion evidence. No Xu source proves corpus-wide coverage of that set.
- **“About half of parameters have correlations.”** cDep cites 23.4–61.2% of prior
  *misconfiguration cases* involving multiple parameters, not half of all parameters.
- **“Pinpointing messages reduce diagnosis 3–13×.”** This audit did not locate one primary source
  supporting that unified claim.
- **“Acto's largest class was row changed, behavior didn't.”** Incorrect paraphrase; use the audited
  undesired-state definition above.
- **“OAT 63.7% were precondition violations.”** The 63.7% denominator refers to operation-semantic
  violations; only a subset involved preconditions.
- **“Rainmaker directly covers every callback/schema-drift fault.”** Rainmaker directly studies
  single REST-call response/status/timeout/retry interactions; broader fault matrices are
  `XU-SYNTHESIS` or companion practice.

## Companion boundary

The following may remain as optional practice, but they are not Xu research:

- Google SRE/change-management and NALSD/PRR material;
- AWS TLA+/P and operational-readiness practices;
- the Purdue/Toronto software-upgrade-failure line;
- generic retry budgets, database migration patterns, Hypothesis, deterministic simulation, and
  language/framework-specific adaptations such as Pydantic environment-key checks.

Label them `COMPANION` and keep them out of Xu-derived empirical claims.

## Open evidence limits

- Welder `xu-002`: official title and artifact branch support compositional-liveness direction;
  primary PDF text was unavailable, so do not cite theorem/evaluation details.
- MCon `xu-003`: project/metadata available but primary PDF unavailable in this pass.
- Rex TOCS `xu-005`: use the available ATC paper `xu-017` for mechanism claims until the TOCS PDF
  can be audited.
- The 2026 corpus may change between accepted/preprint and camera-ready versions. Re-audit exact
  numbers before using them in an external publication.
