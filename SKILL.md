---
name: xu-reliability-design
description: >-
  Evidence-backed reliability and system-design review synthesized from Tianyin Xu's 97-entry
  publication inventory, with full-text audit of every available paper and explicit metadata-only
  limits. Use for configuration and policy changes, multi-step operations, controllers, caches or
  replicas, component seams, fail-slow faults, recovery, access control, test fidelity, safe
  extensions, AI-SRE action, and requests about 徐天音/Tianyin Xu's system-design principles. Do not
  trigger for pure UI/content, isolated analysis, or a simple stateless feature unless requested.
---

# Xu Reliability Design

Turn a proposal into an auditable argument that the system remains safe, makes progress, and can
recover under live change. Do not substitute paper summaries or a long checklist for design
judgment.

The research boundary is the 97 entries on Tianyin Xu's official publication page captured on
2026-09-01. Ninety-four available PDFs were full-text screened; three entries remain
`metadata-only` (`xu-002`, `xu-003`, `xu-005`). A paper may be in the inventory without supporting
a general reliability rule. See `references/paper-ledger.md` for the complete audit.

## Evidence discipline

- **XU-DIRECT** — a Xu-coauthored paper explicitly states, studies, or implements the claim.
- **XU-SYNTHESIS** — a recurring design principle derived from at least two Xu papers. Name the
  paper IDs and never phrase the synthesis as a quotation.
- **COMPANION** — useful non-Xu practice. Keep its attribution and assumptions explicit.

If a primary source was unavailable, say `metadata-only`; do not infer mechanisms from a title.
Use empirical numbers only when they change a decision, with the study population and denominator.
Exact attribution guardrails live in `references/research-map.md`.

## Fourteen corpus-wide principles

These are `XU-SYNTHESIS`. The evidence, boundaries, guidelines, and examples are in
`references/principles.md`.

| ID | Principle |
|---|---|
| P1 | Make dangerous intent unrepresentable, rejectable, and repairable at the accepting boundary. |
| P2 | Assume every observer has a partial, stale history that may omit events or move backward. |
| P3 | Treat every live change as a crashable, retryable, resumable state transition. |
| P4 | Make cross-component data and management semantics, versions, and preconditions explicit contracts. |
| P5 | Judge correctness through end-to-end behavior and relational oracles. |
| P6 | Put adaptive control inside a bounded envelope with arbitration, LKG, and stop conditions. |
| P7 | Model silent, slow, intermittent, wrong, stale, and propagating faults—not only crashes. |
| P8 | Exercise recovery and rare paths at a risk-calibrated cadence, realism, and blast radius. |
| P9 | Minimize the control surface and make safe repair usable; watch for verifier workarounds. |
| P10 | Treat recovery as a controlled workflow that must not worsen the incident. |
| P11 | Correctness includes progress, stability, and model–implementation conformance. |
| P12 | Preserve effective state, provenance, relationships, and counterfactual evidence by design. |
| P13 | Place observation and enforcement where the needed semantic ground truth lives. |
| P14 | Calibrate capacity, fault, timing, and fidelity assumptions against deployment distributions. |

Do not force fourteen headings. First select the applicable questions.

## Triage before review

Mark a question `selected` only when at least one trigger is present. For an ambiguous high-impact
trigger, mark `unknown`, name the evidence needed, risk owner, and blocked decision. Do not emit
statuses for clearly irrelevant questions.

| Question | Select when the design has… | Load |
|---|---|---|
| Q1 Intent | configuration, policy, operator/agent input, unsafe extension, or excess knobs | `references/routes/q1-intent.md` |
| Q2 State | cache/replica/events/restart, reused identity, stale authority, or change provenance | `references/routes/q2-state.md` |
| Q3 Change | multi-effect mutation, migration, failover, retry, rollback, or irreversible step | `references/routes/q3-change.md` |
| Q4 Seams | component/dependency/version boundary, hidden management semantics, or split ownership | `references/routes/q4-seams.md` |
| Q5 Correctness | nontrivial invariant, reconciliation, concurrency, conservation, or formal model | `references/routes/q5-correctness.md` |
| Q6 Control | feedback controller, autoscaling, traffic movement, automation, fail-slow propagation, or blast radius | `references/routes/q6-control.md` |
| Q7 Evidence | recovery claim, emulator/mock/proxy, production diagnosis, benchmark, or uncalibrated capacity/fault assumption | `references/routes/q7-evidence.md` |

Common selection is two to four questions. A controller platform may need all seven; a one-host
stateful migration may need only Q2/Q3/Q5. A small CRUD service with one cache does not justify the
whole protocol: select only the question whose answer can change the decision.

## Review method

### 1. Map change, state, and seams

List only what exists:

1. intent sources;
2. authoritative state and derived views;
3. mutating and recovery transitions;
4. internal/external seams and semantic owners;
5. controllers, actuators, and fault domains;
6. invariants and behavioral oracles;
7. test surrogates and calibration evidence.

For a repository, cite files, functions, and configuration paths. For a proposal, keep missing facts
as unknowns rather than filling them with a fashionable pattern.

### 2. Build risk chains

For each top risk, complete this chain:

`trigger/state → consequence/invariant → prevention → behavioral oracle → recovery → falsifiable acceptance`

Rank by consequence, reachability, observability, and recoverability. A silent, catastrophic, or
irreversible risk outranks a frequent clean failure. Every recommendation must change at least one
state boundary, transition, oracle, recovery path, or acceptance decision.

Use this compact table:

| Risk / principle | Trigger and consequence | Prevention | Oracle | Recovery | Acceptance | Provenance |
|---|---|---|---|---|---|---|

### 3. Calibrate verification

Types, runtime invariants, stateful tests, deterministic simulation, model checking, and proof are a
ladder, not a maturity badge. Load `references/formal-verification.md` only when correctness spans
concurrency, distributed coordination, crash recovery, conservation, or interacting loops.

- Formalize the smallest high-risk protocol whose interleavings escape testing.
- State safety, progress/stability, fairness, and fault assumptions.
- Preserve interactions relevant to the invariant; abstract the rest.
- Tie model actions to code through traces, mirrored actions, or runtime invariants.
- Keep fault injection and production oracles for assumptions outside the model.

Welder's controller-composition direction is `metadata-only` in this snapshot. Treat interacting
controllers through P4/P6 and as an open composition risk; do not claim a verified Welder theorem.

### 4. Make acceptance falsifiable

Specify the injection/input, observation point, expected bound or state relation, and production
guardrail. “Add tests,” a green mock, a row change, no exception, or a model checker exit code is
not an oracle. Preserve minimized failing traces as regressions.

## Conditional references

Load paper-level material only when attribution is needed:

- complete inventory and depth: `references/paper-ledger.md`;
- synthesis evidence and exact claim corrections: `references/research-map.md`;
- Xu tools and their limits: `references/tools.md`;
- full worked reviews: `references/examples.md`;
- additional reusable probes: `references/checklists.md`;
- capacity/overload/readiness beyond the Xu corpus: `references/large-system-gate.md`
  (`COMPANION`, optional, risk-calibrated).

For live degradation or diagnosis, always select Q7 and require effective configuration/version,
cross-layer relationships, a healthy comparator or relational oracle, and collection affordable
enough to run during the incident. Do not reduce diagnosability to “add logs.”

## Required output

When this skill materially changes the review, return:

1. reliability verdict and inspected scope;
2. selected questions and unresolved high-impact unknowns;
3. compact change/state/seam map when relationships need it;
4. ranked risk chains with provenance;
5. executable acceptance and production guardrails;
6. residual risks, model/fidelity limits, and liveness assumptions;
7. paper IDs and evidence labels only where research changes a decision.

Keep the response proportional. Never dump all fourteen principles, seven questions, or 97 papers
when a smaller route answers the design question.
