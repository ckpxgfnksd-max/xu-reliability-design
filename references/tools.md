# Tool and technique catalog

Choose a tool only after defining the risk and oracle. Most Xu systems target Java/Kubernetes or
research environments; reuse the design pattern without pretending the research implementation is
a drop-in library for every stack.

`XU-DIRECT` here means the cited tool/pattern is from a Xu-coauthored paper. Generic adaptations are
`XU-SYNTHESIS`; third-party tools/practices are `COMPANION`.

## Configuration and change input

### SPEX / EnCore — constraint and context discovery (`XU-DIRECT`)

- Papers: `xu-097`, `xu-096`.
- Use for: finding value constraints, bad reactions, environment relationships, and correlated
  settings.
- Transferable pattern: infer constraints from code/use sites, inject violations, then improve the
  accepting system's reaction and feedback.
- Limit: inferred constraints and value-local checks do not prove candidate behavior in the target
  environment.

### PCheck — early latent-path probes (`XU-DIRECT`)

- Paper: `xu-087`.
- Use for: configuration only exercised during failover, recovery, backup, rotation, or another
  late path.
- Adaptation (`XU-SYNTHESIS`): execute a safe canary of the late-use path during a deploy gate using
  the production runtime identity. A regex or permission-list lookup is weaker than the real action.
- Limit: scope the empirical numbers to the paper's evaluated systems/samples.

### openctest / Ctest4J — candidate configuration in affected code (`XU-DIRECT`)

- Repositories: [openctest](https://github.com/xlab-uiuc/openctest),
  [Ctest4J](https://github.com/xlab-uiuc/ctest4j).
- Papers: `xu-068`, `xu-033`; selection/prioritization in `xu-063`, `xu-048`.
- Use for: running existing tests under proposed production configuration and selecting tests that
  read changed parameters.
- Adaptation: make settings injectable, record parameter reads per test, and execute intersecting
  tests with candidate values. Preserve a full-suite fallback for mapping drift.

### ConfFuzz — parameter-aware configuration fuzzing (`XU-DIRECT`)

- Paper: `xu-001`.
- Use for: configurable modules where conventional mutation explores irrelevant values or misses
  parameter/code interaction paths.
- Transferable pattern: use unit tests as drivers and parameter-read/code coverage as feedback.
- Limit: fuzzing does not replace environment probes, semantic preconditions, or end-to-end oracles.

### Ciri — LLM configuration validation (`XU-DIRECT`, auxiliary only)

- Repository: [xlab-uiuc/ciri](https://github.com/xlab-uiuc/ciri).
- Paper: `xu-025`.
- Use for: a PR comment or hypothesis source on configuration changes.
- Boundary: the paper's evaluated best average file-level F1 was 0.79 and parameter-level 0.65.
  Do not make it the sole merge/deploy gate.

## State, operation, and controller testing

### Sieve — partial-history perturbation (`XU-DIRECT`)

- Repository: [sieve-project/sieve](https://github.com/sieve-project/sieve).
- Paper: `xu-054`.
- Use for: reconciliation controllers and workflows with externally visible intermediate states.
- Perturbations: crash/restart after effective updates, stale/time-travel views, and unobserved
  transient states.
- Oracle: compare normalized state evolution and end state between clean and perturbed runs.
- Adaptation boundary: inject at meaningful external-update boundaries, not blindly after every
  memory or database write in arbitrary code.

### Acto — operation-sequence and misoperation testing (`XU-DIRECT`)

- Repository: [xlab-uiuc/acto](https://github.com/xlab-uiuc/acto).
- Paper: `xu-038`.
- Use for: operator/admin declaration spaces, operation sequences, rollback and error-state recovery.
- Oracles: desired-state consistency, differential paths to the same intent, and recovery behavior.
- Correct interpretation: Acto's 32/56 class was failure to reach desired state without explicit
  error—not a generic “row changed but behavior did not” count.

### OAT pattern — operation/application semantic contracts (`XU-DIRECT`)

- Paper: `xu-009`.
- Use for: discovering hidden preconditions and application-internal semantics that operator
  developers cannot observe from generic APIs.
- Adaptation: maintain an executable operation contract containing application state/preconditions,
  effect oracle, failure semantics, and recovery.
- Boundary: exact OAT percentages apply to its 11-project, 412-case study only.

### Rainmaker — single REST-interaction fault testing (`XU-DIRECT`)

- Repository: [xlab-uiuc/rainmaker](https://github.com/xlab-uiuc/rainmaker).
- Paper: `xu-047`.
- Use for: SDK/API response errors, timeouts, retry behavior, and success-after-timeout ambiguity.
- Adaptation: wrap the client seam with a parameterized fault matrix and externally visible oracle.
- Limit: broader callback duplication, multi-call workflows, and schema drift are corpus-wide
  synthesis or companion cases, not all direct Rainmaker claims.

### Slooo / DepFast pattern — fail-slow as an explicit completion event

- Repository: [xlab-uiuc/slooo](https://github.com/xlab-uiuc/slooo).
- Papers: Slooo `xu-065` is `XU-DIRECT`; DepFast `xu-056` is an `XU-SYNTHESIS`
  transfer from an adjacent performance/fail-slow paper.
- Use for: quorum and dependency code where a live but slow component can hold the whole operation.
- Adaptation: expose quorum/timeout/alternative-path/cancel completion events compositionally;
  measure propagation and recovery, not timeout counts alone.

## Liveness and formal conformance

### Anvil / Verus — verified controller liveness (`XU-DIRECT`)

- Repositories: [anvil-verifier/anvil](https://github.com/anvil-verifier/anvil),
  [verus-lang/verus](https://github.com/verus-lang/verus).
- Paper: `xu-031`.
- Use for: controller code whose liveness justifies mechanized proof.
- Transferable first step: write ESR-style progress/stability plus fairness and fault assumptions.
- Boundary: Anvil's proof effort and proof-to-code ratios are three-controller results, not generic
  estimates. A production divergence watchdog is useful but does not prove ESR.

### Multi-Grained Specifications — targeted model granularity (`XU-DIRECT`)

- Paper: `xu-021`.
- Use for: model checking where fully fine-grained code models explode and fully coarse models hide
  implementation bugs.
- Pattern: compose finer models for changed/high-risk modules with coarser modules while preserving
  interactions relevant to the invariant; check code/model conformance.

### Specula / SysMoBench — AI-generated specs need independent conformance (`XU-DIRECT`)

- Papers: `xu-004`, `xu-011`.
- Use for: AI-generated TLA+/formal models.
- Required metrics: syntax, runtime, trace conformance, safety/liveness invariant correctness, and
  bug reproduction—not “model checker returned green” alone.
- Execution option (`COMPANION`): a focused single-agent Specula Lite pilot can model/check and
  reproduce candidates without the full pipeline. Lite skips implementation trace validation;
  see [specula-pilot.md](specula-pilot.md) before choosing it.
- Red flag: repairing a generated model by weakening the invariant or abstracting out the failing
  behavior.

### Welder (`metadata-only` in this research pass)

- Paper ID: `xu-002`; official title indicates compositional liveness verification of cluster
  control planes.
- The official PDF was unavailable on 2026-09-01. Do not cite theorem structure, mechanism, or
  evaluation numbers until primary text is audited.

## Access control and forensic evidence

### P-DIFF / ACtests — effective-policy differential (`XU-DIRECT`)

- Papers: `xu-076`, `xu-020`.
- Use for: IAM/RBAC/ACL/entitlement changes.
- Pattern: compare real request decisions before/after using production authorization code and
  production-shaped relational data; explain every new allow and material new deny.
- Production extension: infer/sample effective policy from behavior logs and preserve change
  provenance for drift/forensics.

### Dossier — application-semantic configuration forensics (`XU-DIRECT`)

- Paper: `xu-059`.
- Use for: configuration changes as an attack/persistence surface.
- Pattern: preserve application-level config semantics, actor, intent, time, effective value, and
  causal relation; OS audit events alone may misattribute a configuration-based attack.

## Recovery and AI SRE

### Maelstrom / Taiji patterns — bounded feedback recovery

- Papers: Maelstrom `xu-083` is `XU-DIRECT`; Taiji `xu-077` is an `XU-SYNTHESIS`
  transfer from an adjacent production traffic-control paper.
- Use for: region/cell/datacenter drains and global traffic control.
- Pattern: encode dependencies and capacity, move in bounded stages, gate on health feedback,
  persist progress, provide restore, and regularly exercise small-radius drains.

### Stratus — deterministic orchestration and TNR (`XU-DIRECT`)

- Paper: `xu-012`.
- Use for: AI/automated remediation.
- Pattern: LLMs handle evidence/data flow; deterministic state machines and exclusivity control
  mutations; Transactional No-Regression requires failed actions to be undoable without worsening
  externally visible health.
- Boundary: irreversible actions or incomparable health states require isolation/human gates, not a
  claim that TNR magically orders them.

### SREGym / ITBench — live scenario evaluation (`XU-DIRECT`)

- Papers: `xu-008`, `xu-018`.
- Use for: testing SRE/IT agents before granting production action authority.
- Pattern: real/live environments, high-fidelity failures, noise/correlated faults, automated
  evaluation, and explicit partial/unsafe/unknown outcomes.

## Companion techniques — label explicitly

The following can be useful but are not Xu research:

- TLA+/TLC, Quint, P, Alloy, Hypothesis stateful testing, deterministic simulation, and general
  formal-methods cost/selection guidance beyond the Xu papers (`COMPANION`).
- Google/AWS readiness, capacity, retry-budget, load-shedding, blast-radius, and safe-deployment
  practices in `large-system-gate.md` (`COMPANION`).
- Generic database expand/contract migration and third-party upgrade-failure studies
  (`COMPANION`).

Use `references/formal-verification.md` and `references/large-system-gate.md` only when their trigger
fires; do not present them as Xu-derived empirical findings.
