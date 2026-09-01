# Calibrated formal verification and conformance

Load this file when correctness spans concurrency, crash/retry, distributed coordination,
conservation, multiple controllers, or a safety-critical extension. Formal methods are one rung in a
reliability argument, not a universal mandate.

## Provenance boundary

Xu-coauthored evidence directly supports four obligations:

1. **State progress and stability, not safety alone.** Anvil (`xu-031`) defines ESR and verifies
   controllers under explicit environment/fault/fairness assumptions.
2. **Choose abstraction/granularity against the invariant and preserve interactions.**
   Multi-Grained Specifications (`xu-021`) composes fine/coarse module specifications to balance
   implementation fidelity and state space.
3. **Tie specification to implementation behavior.** `xu-021` and Specula (`xu-004`) use trace
   validation/conformance; SysMoBench (`xu-011`) separates syntax/runtime success from conformance
   and invariant correctness.
4. **Put assurance at a usable native abstraction.** Rex (`xu-017`) and the kernel-verification
   position paper (`xu-044`) show the language–verifier gap and unsafe-workaround risk.

Welder (`xu-002`) is relevant by official title/artifact metadata, but its primary PDF was
unavailable in the 2026-09-01 research pass. Treat detailed compositional-liveness claims as pending.

TLA+/TLC, Quint, P, Alloy, property-based testing, deterministic simulation, and industry practice
below are **COMPANION** techniques unless a Xu paper is explicitly named.

## First decide what assurance is needed

For each crown-jewel claim, answer:

1. **Property:** what safety/conservation, progress, and stability must hold?
2. **Assumptions:** which scheduler fairness, fault cessation, eventual response, writer
   exclusivity, capacity, and environment behaviors does the claim require?
3. **Abstraction:** which states/actions/interactions can change that property? What is deliberately
   omitted?
4. **Conformance:** how will code and environment remain connected to the artifact?

A green model checker answers only the model/property under the selected bounds and assumptions. It
does not prove performance, capacity, emulator fidelity, unmodeled libraries, or code conformance.

## Verification ladder (`COMPANION` selection framework)

Choose the lowest rung that can falsify the risk. Higher is not automatically better.

| Rung | Technique | Best use | Main blind spot |
|---|---|---|---|
| 0 | Types, schemas, DB constraints, capability-safe APIs | Illegal states and local write-time invariants | Context, sequences, concurrency |
| 1 | Runtime assertions, scheduled conservation/effective-state checks, watchdogs | Continuous drift and externally visible invariants | Rare interleavings before production |
| 2 | Property-based and stateful model-based tests | Edge inputs and wrong operation sequences | Only sampled/generated executions |
| 3 | Targeted fault injection / deterministic schedule control | Crash, retry, stale view, reorder, partition, fail-slow | Quality and completeness of the harness/oracle |
| 4 | Design model checking (TLA+/Quint/P/Alloy) | Exhaustive bounded reasoning over protocol state/interleavings | Abstraction/model–code gap; state explosion |
| 5 | Mechanized proof / verified implementation | Small stable cores needing unbounded guarantees in the modeled domain | High expert cost; trusted base and environment assumptions |

Anvil's three evaluated controllers reported proof-to-code ratios of 4.5–7.4 and about 2.5
person-months per controller with reusable framework support. This is `XU-DIRECT`, `xu-031`, but it
is not a generic cost estimate for every proof system or codebase.

## When model checking is justified

Model the smallest protocol whose risk cannot be adequately explored with lower rungs when one or
more holds:

- conservation or uniqueness must survive crash/retry/concurrency;
- two or more actors/controllers can interleave writes that affect correctness;
- recovery/reconfiguration can pass through unsafe intermediate states;
- a liveness argument needs multiple fairness/fault assumptions;
- an irreversible action depends on more than a few ordered state transitions;
- the team is already arguing correctness with an informal state machine that can be made
  executable.

Do not use an arbitrary component-count or “money means TLA+” rule. A simple transaction may be
better protected by database constraints and stateful tests; a small controller can still deserve a
model if it has deep crash/retry behavior.

## Required specification artifact

When model checking/proof is chosen, the design review includes:

### 1. Scope and mapping

- modeled actors and state variables;
- mapping from each model variable/action to code/interface/state;
- explicitly omitted behaviors and why they cannot affect the property;
- bounds used for checking and the class of behavior those bounds cover.

### 2. Initial states and actions

- legal initial states;
- normal actions and enabling preconditions;
- one meaningful externally visible effect per abstract action unless atomicity is justified;
- crash, restart, timeout, retry, duplicate, reorder, stale-read, and recovery actions relevant to
  the protocol.

### 3. Properties and assumptions

- named safety/conservation invariants;
- progress and stability/liveness;
- fairness, fault cessation, eventual response, capacity, and writer assumptions;
- an explicit statement of behavior when an assumption does not hold.

### 4. Checking and counterexamples

- tool, bounds, symmetry/abstraction decisions, and CI command;
- expected state-space/runtime envelope;
- preserved counterexamples and their translation into code/harness regression tests.

### 5. Conformance

Use at least one, preferably two independent links:

- **trace validation:** instrument implementation actions and check traces against the spec;
- **mirrored stateful actions:** drive implementation and reference/model with the same sequence and
  compare observable results;
- **runtime invariants/watchdogs:** deploy the safety/effective-state/progress symptoms;
- **counterexample replay:** translate model traces into deterministic implementation tests.

Re-run conformance when relevant code/state/action mapping changes. A spec with no owner or drift
gate is explanatory documentation, not verification evidence.

## ESR: progress plus stability (`XU-DIRECT`)

For a controller with desired description `d` and actual-state predicate `match(d)`, Anvil's ESR
informally requires:

> If desired state eventually stops changing, actual state eventually matches it and remains
> matched.

Write the domain version with assumptions:

```text
If desired_state remains D,
and [named dependencies eventually respond],
and [named faults eventually stop / fairness holds],
then actual_state eventually satisfies Match(D)
and remains Match(D) until desired_state changes.
```

Questions a review must answer:

- Does `Match(D)` describe actual external behavior, not a row or declaration only?
- Can another controller undo the match without new intent?
- Does the controller progress from every reachable intermediate state after restart?
- Which permanent faults make the premise false, and how is that visible operationally?
- Are production divergence/re-divergence watchdogs bounded symptoms rather than falsely called a
  proof of unbounded ESR?

Anvil authors classified 70 bugs in the Sieve/Acto reported corpora—69% of that combined
corpus—as ESR violations. Preserve that denominator and model/assumption scope when citing it.

## Multi-grained modeling (`XU-DIRECT`)

Fine-grained models can explode; coarse models can hide code behavior. Use this decision process:

1. Start from the invariant and the interactions that can violate it.
2. Model changed/high-risk modules at the action granularity needed to expose those violations.
3. Keep unchanged modules coarse only if their visible interactions are preserved.
4. Compose modules and trace-check the relevant implementation actions.
5. Add a finer module when a counterexample, code change, or conformance failure crosses an
   abstraction boundary.

“Only model the changed file” is not the principle; preserving interaction semantics is.

## AI-generated specifications (`XU-DIRECT` + synthesis)

An AI-generated model must pass separate gates:

- parses/typechecks;
- executes/model-checks under declared bounds;
- conforms to representative implementation traces;
- preserves independently stated safety/liveness invariants;
- reproduces known bugs or rejects known bad traces where applicable;
- turns new counterexamples into implementation tests.

Reject reward-hacking repairs that delete an action, weaken an invariant, or overfit instrumentation
only to make the current trace pass. Keep property ownership outside the same agent that is rewarded
for achieving conformance.

## Native-abstraction fit (`XU-SYNTHESIS`)

For verifier-backed extension or policy systems:

- map developer/source-language, compiler, verifier, and runtime contracts explicitly;
- express common safety obligations at source/API/type level;
- use a narrow runtime guard for properties static verification cannot practically express;
- map errors back to source intent with a safe repair;
- inventory false rejections, verifier-specific rewrites, and unsafe escape hatches;
- verify post-verification fusion/optimization preserves capability and behavior.

More rejection is not evidence of more safety if developers route around the verifier.

## Tool choice (`COMPANION`)

| Need | Candidate |
|---|---|
| State-machine design and temporal properties | TLA+/TLC or Quint |
| Event-driven async actors with monitor/code-generation ecosystem | P |
| Relational structures, authorization graphs, bounded object models | Alloy |
| Python operation sequences | Hypothesis `RuleBasedStateMachine` |
| Rust concurrency scheduling | loom/shuttle-style schedule exploration |
| Verified Rust implementation | Verus/Anvil where the domain and team fit |

Tool familiarity, maintainability, property shape, and conformance path matter more than brand.

## Worked mini-example: credential rotation

```text
State:
  desired_generation
  active_generation
  staged_generations
  reader_generation[service]
  revoked_generations

Actions:
  Stage(g), Publish(g, service), Verify(g), Activate(g),
  Revoke(old), Crash, Restart, Retry, Abort(g)

Safety:
  at most one active generation
  revoked generation never authorizes
  a generation is not revoked before new generation works for every required reader

Liveness/stability:
  if desired_generation stabilizes, dependencies eventually respond, and crashes eventually stop,
  active_generation eventually equals desired_generation and remains so until intent changes

Conformance:
  controller emits action/generation traces checked against the model;
  counterexamples become crash-boundary tests;
  real authentication probes are the postcondition oracle
```

The model does not prove secret-store availability, cache TTL fidelity, or operator permissions.
Those stay in environment probes, fail-slow/fault tests, and production behavior oracles.
