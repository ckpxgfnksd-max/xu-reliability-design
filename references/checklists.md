# Reliability review and acceptance checklists

Load only the sections that match the system. Provenance is declared per section. Items marked
`XU-SYNTHESIS` operationalize recurring Xu-paper patterns; items marked `COMPANION` are general
engineering adaptations. Numeric stress points without a paper ID are examples to calibrate from
the target system, not Xu-derived thresholds. Paper-direct anchors are in `principles.md` and exact
scope is in `research-map.md`.

For each checked item record `pass + evidence`, `fail + consequence`, `unknown + owner/evidence`, or
`not applicable + reason`. A checked box without evidence is not a pass.

## A. Configuration and intent — `XU-SYNTHESIS` (P1/P9)

### Surface and ownership

- [ ] Every configuration, policy, admin request, scheduler decision, and agent action that can
  change behavior has an owner and semantic type.
- [ ] Each exposed knob has current usage evidence, dependencies, risk, and a retention/retirement
  decision. Rare use prompts review; it does not automatically prove deletion is safe. (`P9`)
- [ ] Constrained intent or a small enum replaces open-ended values where it preserves real use
  cases. (`P9`)
- [ ] Unknown or misspelled keys/actions in the owned namespace are rejected in the actual deploy
  path, not merely by a validator tested in another source path. (`P1`)

### Three-layer pre-effect gate

- [ ] **Value/relationship:** type, range, unit, enum, cross-field, and cross-component constraints
  are executable. (`P1`)
- [ ] **Environment:** references are resolved with the production runtime identity—credentials,
  DNS/TLS, schema/version, capacity, device, and permission—not syntax-checked only. (`P1`)
- [ ] **Affected behavior:** candidate values run the code and operations they affect, including
  failover, rotation, backup, disabled branches, and old-data/version paths. (`P1`, `P8`)
- [ ] Rejection happens before externally visible effects and reports the offending intent,
  violated relationship, likely impact, and safe next action. (`P1`, `P9`)
- [ ] An LLM/static validator is corroborating evidence, never the sole semantic gate. (`P1`)

### Acceptance probes

- [ ] Inject a value-local error, cross-field error, environment-only error, hidden operation
  precondition, unknown owned key, and candidate value that triggers a dormant bug.
- [ ] Each case fails at the earliest layer capable of knowing it and produces a distinguishable,
  repairable error.
- [ ] A valid-but-unusual candidate configuration reaches a behavioral test rather than being
  rejected only for looking unfamiliar.

## B. State, partial histories, and operations — `XU-SYNTHESIS` (P2/P3/P10)

### Authority and identity

- [ ] Every decision names its authoritative state and all derived caches, replicas, watches,
  polls, events, logs, models, and checkpoints. (`P2`)
- [ ] Each view states known/unknown staleness, omission, coalescing, replay, and time-travel
  behavior. Unknown bounds are explicit risks. (`P2`)
- [ ] Durable identity includes ID plus generation/epoch where a name can be reused. (`P2`)
- [ ] Destructive actions recheck current authority or carry a fence that rejects stale
  generations. (`P2`)
- [ ] Decisions are level-triggered over current evidence unless the design proves an event cannot
  be lost, coalesced, or replayed. (`P2`)

### Operation state machine

- [ ] Every multi-effect operation defines preconditions, ordered transitions, committed effect,
  idempotency identity, intermediate states, postcondition, and terminal/error states. (`P3`)
- [ ] Durable progress identifies the last committed state; restart does not infer completion from
  one coincidental side effect. (`P3`)
- [ ] Retry and duplicate execution are safe, or the operation exposes an explicit uncertain state
  that must be resolved before retry. (`P3`)
- [ ] Undo/compensation is itself modeled as an operation with preconditions and failure modes.
  (`P3`, `P10`)
- [ ] A stuck normal operation cannot permanently block the recovery operation. The independent
  recovery path still preserves concurrency/fencing invariants. (`P10`)

### Perturbation acceptance

- [ ] Crash or stop the executor after each externally visible update; restart must converge,
  compensate, or enter a named guarded terminal state.
- [ ] Freeze an old snapshot, restart against an older source, and then let it catch up.
- [ ] Drop/coalesce a transient event and deliver only the final current state.
- [ ] Delete and recreate a same-named object while an old action is queued.
- [ ] Reach the same declared intent through different histories and compare normalized end state
  plus external behavior.

## C. Cross-system contracts and fault semantics — `XU-SYNTHESIS` (P4/P7)

### Seam inventory

- [ ] Every internal/external arrow is classified as data-, management-, or control-plane and has
  an owner. (`P4`)
- [ ] The deployed version pair, configuration pair, serialization/unit/null/error semantics, and
  compatibility window are named. (`P4`)
- [ ] Application-management operations expose semantic preconditions instead of relying on
  runbook memory. (`P4`)
- [ ] Shared metadata, journal, invalidation, or coherence has one primary owner plus an explicit
  recovery contract. (`P13`)
- [ ] The pair is tested together under deployed configuration; isolated default-config tests are
  not used as seam evidence. (`P4`)

### Fault matrix

For each relevant seam, fill response, retry/compensation, oracle, and recovery for:

- [ ] no send / connection failure;
- [ ] timeout before the remote side commits;
- [ ] remote commit or side effect followed by lost/late response;
- [ ] slow response at and beyond the measured operating tail while health/connectivity remains green;
- [ ] intermittent completion or partial availability;
- [ ] duplicate/replayed/reordered request or callback;
- [ ] wrong but schema-valid result;
- [ ] stale result or source time travel;
- [ ] version/schema/unit/default drift;
- [ ] undocumented precondition or capacity dependency;
- [ ] emulator/mock behavior that differs from the real dependency.

### Propagation acceptance

- [ ] Deadlines propagate and work completing after caller abandonment is cancelled or accounted
  for; it cannot silently commit twice. (`P7`)
- [ ] Retries and hedges have an end-to-end budget; queues and worker/connection pools are bounded.
  (`P7`; retry-budget mechanics may use `COMPANION` guidance.)
- [ ] A slow dependency cannot monopolize every worker/quorum wait and spread failure beyond the
  stated domain. (`P7`)
- [ ] Measure goodput, occupied resources, retry work, backlog age, and time to recover after the
  injected slowness stops. (`P7`)

## D. Recovery, disaster actions, and adaptive control — `XU-SYNTHESIS` (P3/P6/P8/P10)

### Safety envelope

- [ ] Objective and hard safety invariants are distinct; optimization never overrides the latter.
  (`P6`)
- [ ] Observation source, uncertainty, maximum step/rate/concurrency/population, stop condition,
  and LKG/restore are explicit. (`P6`)
- [ ] Concurrent controllers share priority/conflict arbitration or have disjoint actuators proved
  safe. (`P6`)
- [ ] Target capacity and dependency constraints are verified before failover/drain and after each
  staged action. (`P6`, `P10`, `P14`)
- [ ] Progress is durable and resumable; executor restart does not repeat an irreversible stage.
  (`P3`, `P10`)

### Transactional no-regression

- [ ] Automated remediation has a health/guardrail vector or partial order covering availability,
  latency, data integrity, resource pressure, and blast radius. (`P10`)
- [ ] Each mutation has pre-state capture, commit predicate, undo/compensation, and undo-failure
  path. (`P10`)
- [ ] If pre/post states are incomparable or the action is irreversible, the action is canaried,
  sandboxed, or human-gated rather than falsely declared TNR-safe. (`P10`)
- [ ] The system can abstain safely when evidence is insufficient. (`P6`, `P10`)

### Recovery acceptance

- [ ] Inject insufficient target capacity, unhealthy dependency, stale recovery intent, executor
  crash, and undo failure.
- [ ] Expand exercise radius from a safe slice; health regression pauses or restores rather than
  continuing on a fixed schedule.
- [ ] Run the recovery regularly enough to expose runbook, dependency, permission, and capacity
  drift; discoveries update executable contracts.

## E. Oracles, liveness, and conformance — `XU-SYNTHESIS` (P5/P11)

### Behavioral oracles

- [ ] Each declared effect has a real-client behavior proving it through caches/gateways/replicas.
  (`P5`)
- [ ] Each crown-jewel invariant has an executable conservation, identity, reachability, or
  noninterference oracle. (`P5`)
- [ ] Perturbed and clean runs can be normalized and compared; nondeterministic fields are masked
  deliberately rather than ignored wholesale. (`P5`)
- [ ] Performance diagnosis uses comparable good/bad cohorts or event relationships where workload
  changes invalidate absolute thresholds. (`P5`, `P12`, `P14`)
- [ ] Absence of exceptions, a 2xx, or a changed row is never the only oracle. (`P5`)

### Progress and stability

- [ ] Each reconciliation/control loop states: if intent stabilizes and assumptions hold, what
  actual state eventually matches and remains matched. (`P11`)
- [ ] Fairness, eventual-response, fault-cessation, exclusive-writer, and environmental assumptions
  are explicit. (`P11`)
- [ ] Production watchdogs distinguish persistent divergence and re-divergence without new intent.
  They are monitors, not proofs. (`P11`)
- [ ] Interacting controllers are reviewed for blocking, oscillation, and conflicting writes; a
  single-loop proof is not automatically compositional. (`P6`, `P11`)

### Model/spec/test-double conformance

- [ ] A model's abstraction preserves interactions relevant to its invariants; changed/high-risk
  modules may use finer grain while others remain coarse. (`P11`)
- [ ] Implementation traces, mirrored stateful actions, or runtime invariants tie model to code.
  (`P11`)
- [ ] Syntax/runtime success of an AI-generated spec is separated from conformance and invariant
  correctness. (`P11`)
- [ ] The review never weakens invariants merely to make generated traces conform. (`P11`)
- [ ] Empirical fault tests remain for environment behavior outside the formal model. (`P11`)

## F. Effective access and security changes — `XU-SYNTHESIS` (P1/P5/P9/P12)

- [ ] Build a request corpus over `(subject, resource, action, context)` from real and adversarial
  boundary cases. (`P5`, `P9`)
- [ ] Run before/after policy using production authorization code and production-shaped relational
  data in isolation. (`P5`, `P8`)
- [ ] Every `deny → allow` transition has approved intent; every `allow → deny` has impact review.
- [ ] Revocation is tested with real requests through every material cache/proxy/region, not a
  policy or database diff only. (`P5`)
- [ ] Effective policy is reconstructed or sampled from behavior and compared with declared intent;
  provenance links suspicious access to the responsible change. (`P12`)
- [ ] Denial feedback helps repair the specific issue without encouraging global disablement or
  over-grant. (`P9`)

## G. Autonomous and AI-mediated action — `XU-SYNTHESIS` (P3/P6/P10/P12)

- [ ] Actions are classified as read-only, reversible write, irreversible, and high blast radius;
  permission increases only after scenario evidence. (`P6`, `P10`)
- [ ] Deterministic code—not the model—owns authorization, state transitions, write exclusivity,
  preconditions, time/step budgets, stop rules, and postcondition oracles. (`P3`, `P6`, `P10`)
- [ ] Agent conclusions remain hypotheses until an observation or reversible experiment
  distinguishes them. (`P12`)
- [ ] Live/high-fidelity evaluation includes noise, partial evidence, correlated faults, tool
  errors, and recovery after a wrong action. (`P8`, `P14`)
- [ ] Evaluation reports `resolved`, `regressed`, `unsafe-abstain`, and `unknown`, not command exit
  success alone. (`P5`, `P10`)
- [ ] A model/tool change re-runs the safety suite before production autonomy expands.

## H. Fidelity, ground truth, and diagnosability — `XU-SYNTHESIS` (P8/P12/P13/P14)

- [ ] For each surrogate record `decision → required truth → surrogate → discrepancy → calibration
  method/cadence`. (`P8`, `P13`, `P14`)
- [ ] Mocks/emulators are periodically differential-tested against the real service for the exact
  behaviors they are used to certify. (`P8`)
- [ ] Control signals come from the layer owning semantic truth when practical; proxy metrics have
  uncertainty and false-decision bounds. (`P13`)
- [ ] Capacity, placement, timeout, and recovery assumptions retain distribution, cohort, tail, and
  correlation evidence—not only averages. (`P14`)
- [ ] Telemetry preserves intent/change ID, effective config/version/generation, transition phase,
  dependency outcome, and external result while redacting secrets. (`P12`)
- [ ] A symptom can be compared with a healthy cohort and distinguished among failure modes that
  require different or opposite mitigations. (`P12`)
- [ ] Evidence collection is low-overhead and durable enough to be present during the real failure;
  a debug mode that cannot stay enabled is not production diagnosability. (`P12`)

## Recurring bug shapes — `XU-SYNTHESIS`

- **Silent acceptance:** invalid or context-incompatible intent is accepted and a default or partial
  effect appears successful.
- **Intermediate-state confusion:** restart sees one side effect and incorrectly infers the whole
  workflow committed.
- **Time travel:** a stale view or replayed action reaches a new object that reused an old name.
- **Unobserved transition:** correctness depends on witnessing a transient event that was coalesced.
- **Interaction discrepancy:** two individually reasonable components disagree on units, defaults,
  serialization, versions, or management preconditions.
- **Fail-slow propagation:** a living but slow component holds shared resources until unrelated work
  fails.
- **Recovery deadlock:** admission waits for stability, so the recovery operation queues behind the
  state that can never stabilize.
- **Mitigation regression:** a repair improves one symptom while worsening capacity, integrity, or
  blast radius.
- **False fidelity:** a mock/model/benchmark is self-consistent but not behaviorally conformant with
  the target.
- **Assurance workaround:** a verifier/interface is unusable, so developers route behavior through
  an unsafe escape hatch.
