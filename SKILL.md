---
name: xu-reliability-design
description: "Reliability review for live-system changes: config/policy, caches/replicas, retried mutations, dependency failures, controllers, authz, agents on production, recovery, test doubles, production diagnosis, and scoped formal-method pilots. Also 系统可靠性、上线风险、迁移回滚、故障恢复、设计稳不稳, before or during a change to a running system. Ranked risk chains with falsifiable acceptance; research claims labeled XU-DIRECT / XU-SYNTHESIS / COMPANION from an audited Tianyin Xu (徐天音) corpus; also explains Xu's principles. Not for UI/content or stateless features unless requested."
---

# Xu Reliability Design

Turn a proposal or repository change into an auditable argument that the system stays safe, makes
progress, and can recover under live change. Do not substitute paper summaries or a long checklist
for design judgment.

Three modes:

- **Review** (default): triage below, then answer only the selected questions.
- **Check**: when you are carrying out a change and the deliverable is the work itself, not a
  review. Triage the same way, then use the short form under Output and record it in the task's
  own plan or report, or in the final message if neither exists. A full review block is more than a live hardening or migration task will
  sustain, and a short form that gets written beats a long one that does not.
- **Explain**: when the request is about Tianyin Xu's research or principles rather than a design
  under review, load `references/principles.md` and `references/research-map.md` and answer from
  the principles, threads, and audited claims. Skip triage.

A formal-method pilot is a separate optional path, described in the last section.

## Evidence discipline

- **XU-DIRECT** — a Xu-coauthored paper explicitly states, studies, or implements the claim.
- **XU-SYNTHESIS** — a recurring design principle derived from at least two Xu papers. Name the
  paper IDs and never phrase the synthesis as a quotation.
- **COMPANION** — useful non-Xu practice. Keep its attribution and assumptions explicit.

If a primary source was unavailable, say `metadata-only`; do not infer mechanisms from a title.
`xu-002` Welder, `xu-003` MCon, and `xu-005` Rex TOCS are metadata-only in this snapshot: cite no
mechanism, theorem, or number from them, and use Rex ATC `xu-017` for Rex.
Use empirical numbers only when they change a decision, with the study population and denominator.
The corpus boundary, audit depth, metadata-only entries, and audited numbers live in
`references/research-map.md`.

## Triage before review

Eight questions cover the fourteen corpus-wide principles (P1–P14, `references/principles.md`);
each route file names its principles. Mark a question `selected` only when its trigger is answered
yes from the artifact in front of you, not from what a system of this kind usually has. For a
high-impact trigger you cannot answer, mark `unknown` and name the evidence needed, the risk owner,
and the decision it blocks. Say nothing about questions whose trigger is no.

| Question | Select when you can answer yes | Load |
|---|---|---|
| Q1 Intent | Does the design accept configuration, policy, credentials, operator or agent input, or plugins where a syntactically valid value can still be wrong for the environment, only take effect on a rarely run path, or interact with other knobs? | `references/routes/q1-intent.md` |
| Q2 State | Does any decision read a cache, replica, event stream, checkpoint, or log rather than the authoritative state; can the same event or request arrive twice, late, or out of order; or can two non-controller writers (overlapping runs, old and new binaries) or a reused name target the same object? (A value written by a controller or through a shared actuator, and who else can write it: Q6.) | `references/routes/q2-state.md` |
| Q3 Change | Is there any operation with more than one externally visible effect, that can be interrupted or retried, or that contains an irreversible step? Migrations, backfills, failovers, rotations, restores, and rollouts that transform persistent state or cross incompatible versions are typical; an ordinary restart of stateless replicas is not one, and a write followed by a cache invalidation that a TTL would repair is Q2, not Q3. | `references/routes/q3-change.md` |
| Q4 Seams | Do two independently deployed components, versions, or teams have to agree on data format, units, ordering, error or partial-success semantics, hidden management preconditions, or ownership of shared state? | `references/routes/q4-seams.md` |
| Q5 Correctness | Does correctness depend on an invariant across operations (conservation, uniqueness, exactly-once, eventual and stable match), on a reconciliation loop that must converge and stay converged (a feedback controller's own loop is Q6), on concurrency, on a formal model, or on behavior a real client sees through caches and gateways rather than on a row or return code? | `references/routes/q5-correctness.md` |
| Q6 Control | Does anything act automatically on telemetry (autoscaler, tuner, traffic mover, remediation agent); do two controllers, tools, or an operator override share an actuator (concurrent runs of one non-controller job are Q2); or, on a path a caller waits on, can a dependency that is slow, intermittent, or partially failed while still connected hold this system's threads, connections, queues, or quorum waits? | `references/routes/q6-control.md` |
| Q7 Fidelity | Does a safety, capacity, or recovery claim rest on a mock, emulator, simulator, benchmark, lab substrate, a proxy metric or release gate (test-suite status, health check, offline reward), or a rehearsal smaller than the real event, or on a capacity, fault, or timing assumption never calibrated against deployment data? | `references/routes/q7-fidelity.md` |
| Q8 Diagnosability | Is the task a production diagnosis, an observability or forensics design, or does the change alter the evidence (effective configuration, version, generation, provenance, comparator) a responder would need to separate competing causes? | `references/routes/q8-diagnosability.md` |

Common selection is two to four questions. A controller platform may need most of them; a
one-host stateful change may need only Q3/Q5; a small service whose only risk is one derived view
needs one question answered in a paragraph. If no trigger is yes, say so in one line and answer the
task without this protocol.

## Review method

### 1. Map only what the selected questions need

Intent sources; authoritative state and derived views; mutating and recovery transitions; seams and
their semantic owners; controllers, actuators, and fault domains; invariants and oracles; test
surrogates and calibration evidence. For a repository, cite files, functions, and configuration
paths. For a proposal, keep missing facts as unknowns rather than filling them with a fashionable
pattern.

### 2. Build risk chains

For each top risk, complete the chain and rank by consequence, reachability, observability, and
recoverability. A silent, catastrophic, or irreversible risk outranks a frequent clean failure.
Every recommendation must change at least one state boundary, transition, oracle, recovery path, or
acceptance decision; otherwise drop it.

```text
Risk: <name>  (<question>, <principle>)
Trigger → consequence: <state or input> → <violated invariant or harm>
Prevention: <boundary, fence, contract, or bound that removes the trigger>
Oracle: <externally observable behavior or relation that fails when the risk fires>
Recovery: <path that restores safety without worsening the incident>
Acceptance: <injection or input; observation point; expected bound or relation; production guardrail>
Provenance: <XU-DIRECT xu-0NN | XU-SYNTHESIS xu-0NN, xu-0NN | COMPANION>  (only if research changed this chain)
```

### 3. Calibrate verification

Types, runtime invariants, stateful tests, deterministic simulation, model checking, and proof are a
ladder, not a maturity badge. When correctness spans concurrency, distributed coordination, crash
recovery, conservation, or interacting loops, load `references/formal-verification.md` and formalize
only the smallest high-risk protocol whose interleavings escape testing. Keep fault injection and
production oracles for assumptions outside any model. For an authorized agent-assisted TLA+
investigation, use `references/specula-pilot.md` to choose a focused Lite pilot or a conformance
workflow. A generated statechart is a starting hypothesis, not verification evidence.

### 4. Make acceptance falsifiable

Specify the injection or input, the observation point, the expected bound or state relation, and the
production guardrail. "Add tests", a green mock, a row change, no exception, or a model-checker exit
code is not an oracle. Preserve minimized failing traces as regressions.

## Conditional references

Load paper-level material only when the user asks for attribution, a research claim is contested,
or a specific technique is needed. A review that selects Q8 for a diagnosis does not need
`principles.md` or `research-map.md`; the route file is the working reference.

- synthesis evidence, audited numbers, corpus boundary, exact claim corrections:
  `references/research-map.md`;
- complete 97-entry inventory and audit depth: `references/paper-ledger.md`;
- principle text with evidence anchors, examples, and counterexamples: `references/principles.md`;
- Xu tools and their limits: `references/tools.md`;
- full worked reviews: `references/examples.md`;
- recurring bug shapes and inventory checklists: `references/checklists.md`;
- capacity, overload, and readiness beyond the Xu corpus: `references/large-system-gate.md`
  (`COMPANION`, optional, risk-calibrated).

## Output

For **Review**:

1. reliability verdict and the scope actually inspected;
2. selected questions, each with the yes-trigger that selected it, plus unresolved high-impact
   unknowns;
3. ranked risk chains in the block format above, with executable acceptance.

Only when it changes a decision: a compact change/state/seam map; residual risks, fidelity limits,
and liveness assumptions; paper IDs and evidence labels.

For **Explain**, answer the question without review blocks.

For **Check**, give each selected risk these lines:

```text
Risk: <name>  (<question>)
Trigger → consequence: <state or input> → <harm>
Acceptance: <injection or input; observation point; expected result>
Recovery: <undo path>; tested and passed | untested
```

Acceptance observes behavior from where the harm would be seen, not the step's own exit status:
section 4 still applies. Use the full block only for a risk whose step is irreversible or has no
recovery path. Most recoveries are untested at planning time, so an untested recovery stays in the
short form, marked `untested`, and testing it becomes a plan step before the step it protects. If
that step is already applied, test the undo before the next dependent step or task completion.
Rehearse on a copy or equivalent target; testing an undo on a live system needs authorization. A
recovery that fails its test, cannot be tested in time, or that a route file names as a failure
signal (such as redeploying the old build after state changed) counts as no recovery path: hold the
protected or dependent step, or task completion, until recovery is fixed or the risk owner accepts
the risk. Evidence
labels appear only when research changed a decision.

Length follows the number of selected questions, not the protocol. Never emit all eight questions,
all fourteen principles, or a paper list when a smaller route answers the design question.

## Optional: formal-method investigation

Use only when asked to run a formal-method pilot or investigate a state/concurrency failure: select
the relevant questions and load `references/formal-verification.md` plus
`references/specula-pilot.md`. This path needs a pinned Specula Lite and a checker whose provenance
verifies. If the tool is absent, install it only when that is explicitly authorized. If provenance
fails, the checksum rule in `specula-pilot.md` governs and reinstalling does not clear it. Either
way, name the blocker and continue the work that does not depend on it. Execute only the authorized target and fault scope; a review recommendation alone does not
authorize installation, experiments, or implementation fixes.

Deliver the source/tool identities, scope and bounds, selected risk chains, actual checker outcomes,
code-level reproductions, controls, cleanup, and unresolved candidates. Separate model violations
from reproduced defects and documented limitations; state whether implementation trace validation
ran.
