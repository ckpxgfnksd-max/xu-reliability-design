# Corpus-wide system-design principles


## Evidence labels

- `XU-DIRECT`: the cited Xu-coauthored paper explicitly states the claim or implements the design.
- `XU-SYNTHESIS`: this review abstracts a recurring pattern from at least two Xu-coauthored papers.
- `COMPANION`: useful external practice, not evidence about Xu's research program.

The final skill must not phrase `XU-SYNTHESIS` as a quotation or single-paper result. A paper can be
in the 97-paper corpus without supporting a cross-paper principle; the paper ledger records that as
`adjacent` or `no-general-design-claim` rather than manufacturing a contribution.

## P1 — Make invalid or dangerous intent unrepresentable, rejectable, and repairable at the boundary

**Synthesis.** When an input can harm the system, correctness belongs at the interface that accepts
the input—not in an operator's memory or a postmortem runbook. Validation must use the value's real
execution context and relationships, then return feedback that enables the caller to repair the error.

**Evidence anchors.** SPEX (`xu-097`), EnCore (`xu-096`), configuration survey (`xu-094`), PCheck
(`xu-087`), access-denied study (`xu-086`), configuration evolution (`xu-066`), cDep (`xu-069`),
ConfigX (`xu-060`), ctest (`xu-068`), ConfFuzz (`xu-001`).

**Guideline.** For every human-, policy-, or agent-supplied input: define types and cross-field
constraints; resolve environmental references with the production identity; reject before effects;
name the offending field, violated relationship, likely impact, and safe correction. Do not treat an
LLM validator as the only gate.

**Acceptance.** Inject one value-local violation, one cross-field violation, one environment-only
failure, and one hidden operation-precondition failure; each must be rejected before side effects
with a distinct, repairable error.

**Example.** A failover request is accepted only after proving the target replica is caught up, the
old primary is fenced, capacity remains adequate, and the requested policy is compatible with the
deployed versions. The rejection names the failed precondition and the data-loss risk.

**Counterexample.** A schema-valid `promoteReplica` request is queued and executed because the
operator assumes the caller already checked replication state.

## P2 — Model observed state as partial, stale, and capable of moving backward

**Synthesis.** Components do not receive an authoritative history. They observe caches,
notifications, replicas, monitoring streams, and restarted processes, any of which can omit,
coalesce, delay, or replay state. Safety cannot depend on witnessing an event once.

**Evidence anchors.** Partial Histories (`xu-064`), Sieve (`xu-054`), P-DIFF (`xu-076`), Concord
(`xu-028`), process-state observation (`xu-030`), MVNO authority delay (`xu-080`), cellular
reliability (`xu-062`), plus Draco and Elastic Cuckoo Page Tables as scoped cache examples
(`xu-071`, `xu-074`).

**Guideline.** State every source's authority, staleness and observation gaps; drive actions from
level predicates over current evidence; give recreated objects a generation/epoch; make stale reads
safe or fence destructive actions; test delay, omission, replay, source switching, and restart.

**Acceptance.** Freeze an old snapshot, drop an intermediate event, restart against an older source,
and delete/recreate a same-named object; no stale action may affect the new generation and the
system must converge after the view catches up.

**Example.** A deletion controller acts on `(object_id, generation)` and rechecks the current owner
and desired state immediately before deletion. Replaying a prior-generation delete cannot affect a
recreated object with the same name.

**Counterexample.** “When `Deleted` is seen, remove storage named X.” The event is retried after X
has been recreated and deletes the new volume.

## P3 — Treat every change and operation as a crashable, resumable state transition

**Synthesis.** Configuration changes, controller operations, tuning, recovery, and AI mitigations
are transactions over a live system. Each prefix can be interrupted; retries and rollback are new
operations that must remain safe.

**Evidence anchors.** Sieve (`xu-054`), Acto (`xu-038`), OAT (`xu-009`), Stratus (`xu-012`), Mux
(`xu-019`), Concord (`xu-028`), Xkernel (`xu-006`), Oxbow (`xu-007`), UFC (`xu-075`), and
interruptible Android maintenance (`xu-072`).

**Guideline.** Specify preconditions, committed effects, idempotency key, intermediate states,
resume rule, undo/compensation, and postcondition oracle. Inject a crash or timeout after every
externally visible effect. For automated remediation, require transactional no-regression only
when effects are reversible or compensatable and the health states have a declared ordering;
otherwise reduce radius or require approval.

**Acceptance.** Interrupt every externally visible transition boundary, then retry, resume, abort,
and undo. Each run must reach a named terminal state with the same behavioral invariant as a clean
run or a deliberately declared degraded state.

**Example.** Credential rotation uses generations: publish new, verify real authentication, switch
readers, revoke old, then garbage-collect. Restarting from any prefix either advances safely or
reverts to the last-known-good generation.

**Counterexample.** Update the secret row, restart half the fleet, then revoke the old key; a crash
between steps has no durable phase marker and neither retry nor rollback knows which key is live.

## P4 — Make interactions and management semantics explicit contracts

**Synthesis.** Many failures exist neither inside component A nor B, but in discrepancies between
their data, versions, configuration, timing, or hidden management preconditions. Composition needs
an owned contract rather than optimistic integration.

**Evidence anchors.** CSI failures (`xu-046`), Rainmaker (`xu-047`), OAT (`xu-009`), configuration
dependencies (`xu-069`), Mux (`xu-019`), Oxbow (`xu-007`), Concord (`xu-028`), MVNO authority
delay (`xu-080`), container-image ecosystem context (`xu-084`), Maelstrom (`xu-083`), and Taiji
(`xu-077`).

**Guideline.** Inventory data-, management-, and control-plane seams; name owner, versions,
preconditions, failure semantics, capacity assumptions, and serialization rules. Test the deployed
pair/configuration, not default versions in isolation. Turn every discovered precondition into an
executable contract and regression case.

**Acceptance.** Run the deployed version/configuration pair through timeout-before-send,
success-after-timeout, slow, duplicate, stale, semantic-drift, and hidden-precondition cases; every
row needs a deterministic oracle and recovery rule.

**Example.** An object-store connector contract covers success after client timeout, duplicate
callbacks, throttling, schema drift, stale reads, and regional capacity. Contract tests run against
the production version pair and a fault-capable double.

**Counterexample.** Each service passes its own tests, while one writes decimals that the other's
serializer silently rounds under the actual deployment configuration.

## P5 — Judge correctness by end-to-end behavior and relational oracles

**Synthesis.** Internal rows, return codes, and absence of exceptions are weak evidence. Silent,
latent, or cross-system failures require oracles over externally meaningful behavior and
relationships between executions or states.

**Evidence anchors.** Sieve (`xu-054`), Acto (`xu-038`), ctest (`xu-068`), P-DIFF (`xu-076`),
relational debugging (`xu-043`), Vetter (`xu-049`), ScalaCN (`xu-026`), Rainmaker (`xu-047`),
access-control testing (`xu-020`), and OverlayChecker as a scoped user-visible oracle (`xu-081`).

**Guideline.** For each invariant and operation, define an executable behavioral oracle. Prefer
differential, metamorphic, conservation, and reachability checks; compare perturbed with clean
execution and declared with effective behavior. Preserve failing traces as regression tests.

**Acceptance.** Create a quiet failure with a successful return code and updated row but wrong
external behavior; at least one oracle must fail without depending on exceptions or error logs.

**Example.** “Suspend tenant” is verified by real requests through every cache and gateway, not by
checking a `suspended=true` row. A rollback is correct only if the final observable state matches a
clean execution from the same intent.

**Counterexample.** The controller returned 200 and emitted no error logs, so the change is called
successful even though old credentials still work through an edge cache.

## P6 — Put adaptive control inside an explicit safety envelope

**Synthesis.** Traffic managers, autoscalers, recovery systems, tuners, and AI agents are feedback
controllers. They must prioritize correctness, bound rate and scope of change, arbitrate conflicts,
fall back to known-good state, and stop when health evidence is insufficient.

**Evidence anchors.** Taiji (`xu-077`), Maelstrom (`xu-083`), Kscaler (`xu-014`), Xkernel (`xu-006`),
Stratus (`xu-012`), ScalaCN (`xu-026`), process-state control (`xu-030`), plus Chameleon, M5, and
EcoFaaS as scoped adaptive-performance controllers (`xu-015`, `xu-022`, `xu-034`).

**Guideline.** Write the controller's objective, hard safety constraints, observation source,
actuation bounds, priority/conflict rules, stop conditions, LKG fallback, and recovery path. Verify
capacity and action bounds with real load; stage expansion from small to larger blast radius.

**Acceptance.** Force stale telemetry, a conflicting controller, insufficient target capacity, and
a health regression mid-action; the controller must clip, pause, arbitrate, or restore LKG without
crossing its stated blast-radius bound.

**Example.** A traffic controller clips each move, rejects any output that would exceed remaining
datacenter capacity, stops on unhealthy telemetry, resolves all tools through one priority pipeline,
and restores LKG configuration on validation failure.

**Counterexample.** Two independent autoscalers react to the same latency spike, one adding workers
while the other moves traffic, producing oscillation and overload.

## P7 — Design for silent, slow, latent, and propagating faults—not only crashes

**Synthesis.** A dependency that is wrong, stale, or merely slow can retain connections and block
queues while appearing alive. Rare branches and dormant configuration can remain latent until the
system is already impaired.

**Evidence anchors.** fail-slow programming support (`xu-065`), ScalaCN (`xu-026`), PCheck
(`xu-087`), network checker (`xu-089`), Live Forensics (`xu-070`), cellular reliability
(`xu-062`), CSI failures (`xu-046`), Rainmaker (`xu-047`), and cross-app Android blocking
(`xu-072`).

**Guideline.** Enumerate crash, omission, delay, partial success, wrong result, overload, and stale
result separately. Make wait points and dependency propagation explicit; bound queues and retries;
isolate fault domains; probe latent branches before service; make degradation behavior intentional.

**Acceptance.** Inject latency chosen from and beyond the measured operating tail, intermittent
completion, a wrong-but-schema-valid response, and a dependency that completes after the caller
deadline. Bound occupied workers, retry work, and recovery time after the fault ends.

**Example.** A storage fan-out has per-child deadlines and concurrency budgets, returns an explicit
degraded result, and quarantines a slow shard. Tests include a shard that completes just after the
client deadline rather than only immediate failures.

**Counterexample.** Health checks pass because TCP accepts connections while requests wait forever,
exhausting the caller's workers and spreading the slowdown.

## P8 — Exercise recovery and rare paths at a risk-calibrated cadence, realism, and radius

**Synthesis.** A recovery path with no recurring evidence is likely to drift. Test environment
fidelity—including versions, identity, configuration, timing, data shape, and failure behavior—is
part of the safety argument, while cadence and production radius must match consequence and cost.

**Evidence anchors.** Maelstrom (`xu-083`), cloud-emulator fidelity (`xu-024`), genuine CXL
characterization (`xu-039`), PCheck (`xu-087`), ctest (`xu-068`), Sieve (`xu-054`), Acto
(`xu-038`), virtual-device research unit (`xu-037`, `xu-040`) and Trinity (`xu-055`), HoneyCloud
(`xu-079`), SREGym (`xu-008`), and ITBench (`xu-018`). Do not count `xu-037` and `xu-040` as two
independent research units for synthesis.

**Guideline.** Use a risk-calibrated mix of periodic rehearsal, shadowing, simulation, canaries, and
small-radius production exercise; compare doubles and emulators against real behavior; run
candidate values with production-shaped data and credentials; track fidelity gaps as risks. A test
that cannot produce the fault model is not evidence for it.

**Acceptance.** Demonstrate a differential calibration against the real dependency/substrate and
the highest safe-radius exercise justified by the risk. Any discrepancy that could reverse a
pass/fail decision must block or narrow the larger-radius claim.

**Example.** A datacenter drain begins with regular tiny-radius drains, validates dependency and
capacity models, then expands. Postmortem scenarios become permanent tests; dependency discoveries
update the model before the next exercise.

**Counterexample.** Disaster recovery is “tested” in a mock environment with no real dependencies,
instant responses, default configuration, and unlimited spare capacity.

## P9 — Minimize the control surface and make feedback usable

**Synthesis.** Flexibility transfers complexity to operators and expands the state space. Safety
mechanisms that developers cannot use correctly produce workarounds. Interfaces should expose
constrained intent, consistent semantics, and feedback with security/reliability impact.

**Evidence anchors.** Too Many Knobs (`xu-093`), configuration survey (`xu-094`), HCI configuration
view (`xu-090`), access-denied study (`xu-086`), configuration evolution (`xu-066`), field
configuration feedback (`xu-084`), Rex (`xu-017`), seccomp-eBPF and KFuse (`xu-052`, `xu-057`),
and TrafficGuard as a scoped field-default/override example (`xu-091`).

**Guideline.** Delete unjustified knobs; prefer typed intent and small enums; keep semantics
consistent across entry points; provide safe narrow APIs; return precise repair guidance and expose
who/what gains access or risk. Measure mechanism usability and watch for bypasses.

**Acceptance.** Every exposed knob has an owner, usage evidence, dependency map, and retirement
criterion; every unsafe escape hatch has an owner and negative tests; representative safe changes
can be expressed without verifier-specific workarounds.

**Example.** Instead of twelve interacting timeout/retry knobs, expose `latency_class` and
`delivery_semantics`; derive bounded internal values and show the resulting retry budget and impact.

**Counterexample.** A verifier rejects valid extension code, so developers use an unsafe escape
hatch that disables the very property the verifier was meant to guarantee.

## P10 — Treat recovery as a normal controlled workflow that must not worsen the incident

**Synthesis.** Mitigation, rollback, draining, and failover are high-risk operations under degraded
observability. They need stronger safety contracts than ordinary changes and must remain available
when normal workflows are wedged.

**Evidence anchors.** Maelstrom (`xu-083`), Acto (`xu-038`), OAT (`xu-009`), Stratus (`xu-012`),
Taiji (`xu-077`), Concord (`xu-028`), Mux (`xu-019`), Oxbow (`xu-007`), process-state control
(`xu-030`), and SpecFaaS as a scoped buffer/validate/commit example (`xu-050`).

**Guideline.** State no-regression, data-preservation and capacity invariants; provide an emergency
path that is not queued behind the failed operation; pace actions through health feedback; make
steps reversible or compensatable; continuously prove recovery prerequisites.

**Acceptance.** Inject target-capacity loss, stale recovery intent, executor crash, and undo failure.
Recovery must either resume/compensate inside guardrails or stop in an explicit guarded state; the
existence of a rollback command alone is not a pass.

**Example.** Rollback bypasses the ordinary “wait until stable” queue, but still fences the old
writer, validates compatibility, and pauses automatically when error rate rises.

**Counterexample.** The operator refuses every new operation until reconciliation completes, so
the rollback that could recover the system is permanently queued behind the stuck reconciliation.

## P11 — Correctness includes progress, stability, and model–implementation conformance

**Synthesis.** Safety assertions alone do not rule out a system that never finishes or repeatedly
undoes its own work. Formal models are useful only at a calibrated abstraction and only while tied
to executable behavior.

**Evidence anchors.** Anvil (`xu-031`), Multi-Grained Specifications (`xu-021`), Specula
(`xu-004`), SysMoBench (`xu-011`), Sieve (`xu-054`), Acto (`xu-038`), Concord (`xu-028`), Mux
(`xu-019`), ScalaCN (`xu-026`), and Vet's testing-progress oracle (`xu-061`). Welder (`xu-002`) is
a `metadata-only` note about controller composition; no theorem or evaluation detail is used here.

**Guideline.** Define progress and stability for every reconciliation/control loop; state fairness
and fault assumptions; model the smallest high-risk protocol at the granularity needed for the
invariant; preserve cross-module interactions; check traces or implementation actions against the
model; keep empirical perturbation tests for assumptions outside the model.

**Acceptance.** Check safety plus progress/stability, then replay implementation traces against the
model. Removing a necessary fairness/fault assumption must either expose a counterexample or
explicitly withdraw the guarantee; never weaken the invariant to force conformance.

**Example.** A controller contract says: if desired state remains fixed and named dependencies
eventually respond, actual state eventually matches and stays matched. Model checking covers the
crash/retry protocol; production watchdogs and trace validation check conformance.

**Counterexample.** A TLA+ model proves a coarse protocol safe, but the implementation batches two
actions whose intermediate state violates the invariant, and no trace-conformance check exists.

## P12 — Preserve evidence, provenance, and counterfactuals as system features

**Synthesis.** Diagnosis and continuous validation require knowing effective state, change history,
causal relationships, and what differs from a healthy execution. Observability that records only
symptoms cannot support reliable control.

**Evidence anchors.** live forensics (`xu-070`), configuration-attack forensics (`xu-059`), P-DIFF
(`xu-076`), relational debugging (`xu-043`), Vetter counterfactuals (`xu-049`), process-state
observation (`xu-030`), MVNO source authority (`xu-080`), RCA Copilot (`xu-036`), Eroica
(`xu-010`), and Taiji (`xu-077`).

**Guideline.** Record effective configuration and provenance, actor and intent, version/generation,
phase transitions, dependency outcomes, and a redacted result oracle. Keep a healthy baseline or
relational comparator. Make the evidence durable enough for both automated rollback and forensics.

**Acceptance.** Starting from one customer-visible symptom, reconstruct the intent, actor,
effective configuration/version, transition sequence, dependency outcomes, and a comparable healthy
execution without relying on ephemeral in-memory state.

**Example.** Every rollout emits an immutable change ID linking desired config, effective config
hash, component generations, validation results, and rollback point; incident analysis can compare
the affected cohort with a contemporaneous healthy cohort.

**Counterexample.** Logs say “request timed out” but omit the config generation, upstream attempt,
queue time, and whether the remote operation eventually committed.

## P13 — Place observation and enforcement where semantic ground truth lives

**Synthesis.** Layering is not automatically modularity. Surrogate metrics and misplaced
enforcement can hide the state needed for safe decisions. Put the decision at the layer that owns
the needed semantics; when a domain requires split responsibility, make ownership and coordination
an explicit conditional design.

**Evidence anchors.** Kscaler (`xu-014`), Oxbow (`xu-007`), Mux (`xu-019`), Xkernel (`xu-006`),
Rex (`xu-017`), seccomp-eBPF (`xu-052`), DMT/EMT and HugeGPT as scoped hardware/OS semantic-gap
examples (`xu-035`, `xu-016`, `xu-042`), and Draco (`xu-071`). MCon (`xu-003`) remains
`metadata-only` and is not an anchor.

**Guideline.** Locate measurement and enforcement at the layer with ground-truth state; assign a
single writer/owner where possible; split fast path from coordination and recovery paths without
duplicating authority; expose semantic signals instead of inferring from proxies; document the
coordination invariant at each split.

**Acceptance.** Build an ownership matrix with one primary owner per invariant; crash each component
at the shared-state boundary and prove recovery from durable state. Fast and reference paths must
produce equivalent semantic outcomes.

**Example.** CPU scaling observes scheduler runtime, idle, throttling and runqueue behavior inside
the kernel rather than inferring demand from coarse user-space utilization; a narrow interface
applies recommendations with explicit quota semantics.

**Counterexample.** A user-space controller treats “millicores” as ground truth although the kernel
enforces quota-period slices, then overreacts to throttling that its own metric cannot distinguish.

## P14 — Calibrate design assumptions with real distributions and deployment relationships

**Synthesis.** Defaults, averages, and isolated benchmarks often erase the tails and correlations
that determine reliability. Measurement is part of design when it changes fault domains, capacity,
resource policy, or debugging conclusions.

**Evidence anchors.** datacenter-network reliability (`xu-082`), Taiji (`xu-077`), Maelstrom
(`xu-083`), cellular reliability (`xu-062`), Swiftest field measurement (`xu-053`), genuine CXL
characterization (`xu-039`), cloud-storage measurement design (`xu-095`), container-image field
context (`xu-084`), relational debugging (`xu-043`), and cloud-emulator fidelity (`xu-024`).

**Guideline.** Measure the deployed population and preserve distributions, cohorts and correlations;
derive replication, fault-domain placement, timeout, spare-capacity, and tuning decisions from that
evidence; revalidate after topology/version/workload changes. Use a relational baseline, not an
unexplained global threshold.

**Acceptance.** Show the distribution, cohort, and correlation evidence behind each timeout,
capacity, placement, or fidelity threshold; repeat the calibration after one topology/version shift
and define the trigger for future recalibration.

**Example.** Replica placement and repair capacity use observed incident duration and correlated
fault-domain distributions, then are stress-tested under tail events—not designed from mean link
failure rate alone.

**Counterexample.** A fixed timeout chosen from lab averages classifies a healthy-but-slow mobile
path as failed and triggers retries that amplify congestion.

## Operational lens

The 14 principles must not become 14 mandatory sections in every review. `SKILL.md` routes them
through eight triage questions, each owning its principles exactly once:

1. Q1 Intent — what enters, and how unsafe intent is rejected and repaired (`P1`, `P9`)
2. Q2 State — what is authoritative, and what observers can miss, see late, or see twice (`P2`)
3. Q3 Change — which transitions can crash, repeat, race, or need undo (`P3`, `P10`)
4. Q4 Seams — which contracts and hidden semantics can disagree, and where enforcement sits
   (`P4`, `P13`)
5. Q5 Correctness — what behavior proves correctness, including progress and stability (`P5`,
   `P11`)
6. Q6 Control — how adaptation, fault propagation, and blast radius are bounded (`P6`, `P7`)
7. Q7 Fidelity — how realistic and calibrated the evidence and assumptions are (`P8`, `P14`)
8. Q8 Diagnosability — what recorded evidence separates competing causes (`P12`)

The skill first selects questions by observable trigger, reports only selected questions, and opens
an `unknown` when a high-impact trigger cannot be answered.
