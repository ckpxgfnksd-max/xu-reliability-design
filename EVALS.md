# Evaluation contract

This suite tests transfer, routing, provenance, and decision quality. It is not a paper-recall quiz
or a copy of the worked examples.

## Frozen objective

Optimize **decision-quality uplift per loaded context**. A candidate is better only if it improves
held-out design judgment without increasing attribution error, boundary misuse, or irrelevant
protocol loading.

Start autoresearch only after this evaluator has a no-skill baseline, a main-file-only baseline, and
a routed-reference baseline. Keep the cases and scorer frozen during optimization.

## Evaluation protocol

Run the same model/effort in three blinded conditions, with case order randomized:

1. **No skill** — prompt only.
2. **Main only** — prompt plus `SKILL.md`.
3. **Routed** — prompt plus `SKILL.md` and only the route files selected by its triage.

Do not load `references/examples.md`, `references/principles.md`,
`references/paper-ledger.md`, this file, or a gold answer while
generating. A separate fresh-context judge receives the response, rubric, and case gold. Record
loaded word count for every run.

## Metrics and gates

| Metric | Computation | Gate before autoresearch |
|---|---|---|
| Routing precision/recall | selected questions vs gold material questions; “acceptable optional” is neither FP nor FN | both ≥90% overall and ≥85% on boundary cases |
| Complete risk chains | top three material risks containing trigger, consequence/invariant, prevention, behavioral oracle, recovery, falsifiable acceptance | ≥85% |
| Decision-quality score | 0–2 each for mechanism, oracle, recovery/control, acceptance, proportionality; max 10 | routed mean ≥8.0 and ≥1.0 above no-skill |
| Provenance | correct `XU-DIRECT` / `XU-SYNTHESIS` / `COMPANION`, denominators and metadata limits | 100%; zero critical error |
| Boundary safety | no absolute misuse of TNR, mocks, formal methods, recovery exercise, knob deletion, or automation | zero critical misuse |
| Context | words in actually loaded skill/reference files | median ≤4,000; p90 ≤7,000 |

An answer may omit paper citations when research attribution is not decision-relevant. Do not reward
paper-name density.

## Held-out transfer cases

### H1 — Online schema migration with mixed binaries

Prompt: “Add a non-null `owner_id` to a 4-TB table. Old and new binaries coexist for a week; two
services write the row; backfill can restart. The rollback plan is redeploy old code.”

Gold: Q2/Q3/Q4/Q5. Must expose dual-writer/version semantics, durable backfill cursor, old/new read
and write compatibility, conservation oracle, retry/restart, and the fact that code rollback cannot
undo transformed state. Q7 is acceptable only if production-data distribution changes a decision.

### H2 — At-least-once payment webhook

Prompt: “A provider retries callbacks for 72 hours. Our handler writes an order, emits a shipment
event, and returns 200. A timeout may happen after either effect.”

Gold: Q2/Q3/Q4/Q5. Must define provider/event identity, partial-effect state machine, duplicate/late
success, authoritative conservation relation, compensation/manual recovery, and crash-prefix tests.
Do not mandate double-entry without deriving the domain invariant.

### H3 — Feature flag with stale edge caches

Prompt: “A boolean flag disables checkout in one country. Admin UI validates type; edge caches have
unknown TTL and can miss invalidations.”

Gold: Q1/Q2/Q5. Must distinguish declared/effective state, generation or bounded freshness,
end-to-end country behavior, repairable unsafe intent, and stale/omitted invalidation tests. Q3 is
optional only if rollout has multiple committed effects.

### H4 — Live storage tuning

Prompt: “A controller changes compaction concurrency every minute from latency telemetry. Operators
can override it. The value is atomically stored.”

Gold: Q1/Q2/Q3/Q6/Q7. Must cover semantic ground truth, stale/noisy telemetry, competing writers,
step/rate/stop/LKG, crash/restart and behavioral/capacity calibration. Atomic storage alone is weak.

### H5 — Intermittent DNS degradation diagnosis

Prompt: “Only one customer cohort sees 3-second pauses. Aggregate latency is normal; logs record
request timeout but not resolver path or config generation.”

Gold: Q2/Q4/Q7. Must design affordable cross-layer/relational evidence, effective config/version,
cohort comparator, resolver/dependency outcomes, and a test that separates at least two plausible
causes. Do not turn this into a mutation/recovery review.

### H6 — Sandboxed runtime plugin

Prompt: “Plugins are verified bytecode, but safe source programs are often rejected. Teams use an
unsafe host-call helper to ship on time.”

Gold: Q1/Q4/Q5. Must treat false rejection and workaround as assurance risk, map source/compiler/
verifier/runtime contracts, narrow the unsafe boundary, and test both safe expressiveness and
runtime containment. Q7 is optional for workload calibration.

### H7 — Restore from object-store backup

Prompt: “Nightly backups report success. Restore was last attempted 18 months ago; credentials and
encryption keys have since changed. Testing on production data is prohibited.”

Gold: Q1/Q3/Q5/Q7. Must use safe representative/redacted data, real restore identity/key path,
durable stages, integrity/behavior oracle, risk-calibrated rehearsal, and narrow the recovery claim
to the evidenced radius. Never insist on raw production data or continuous production restores.

### H8 — Cached authorization change

Prompt: “A support role gains a new regional action. CI diffs policy text; five gateways cache
decisions independently. Denial messages cause operators to request admin.”

Gold: Q1/Q2/Q5/Q7. Must compare before/after effective decisions, explain new allow/deny outcomes,
test cache convergence/replay, preserve policy provenance, and improve repair feedback without
over-grant. Q3 is optional if activation is staged.

### H9 — Intermittently connected device fleet

Prompt: “A device-management service pushes firmware intent over unreliable mobile links. Devices
may reconnect weeks later with old desired state and repeat acknowledgements.”

Gold: Q2/Q3/Q4/Q6. Must cover generation/authority, late/replayed messages, resumable device
transition, version compatibility, partial success, bounded server retry/backlog, and effective
firmware behavior. Q7 is acceptable for real-link distribution calibration.

### H10 — ML autoscaler using a simulator

Prompt: “A learned autoscaler is trained in a simulator and moves 20% traffic per decision. Offline
reward is high; two manual traffic tools also exist.”

Gold: Q4/Q6/Q7. Must cover shared actuator/arbitration, hard capacity/radius bounds, stop/LKG,
simulator decision-fidelity calibration, correlated faults, and a canary/production guardrail. Do
not ban learning or require formal proof by default.

## Hard boundary cases

These distinguish routing from template dumping.

### B1 — Small CRUD service with one read cache

Prompt: “Review a five-endpoint internal CRUD service. One process owns Postgres; Redis caches
reads for 30 seconds. Deploys are ordinary rolling restarts.”

Gold: Q2 is material; Q4/Q5 are acceptable optional if kept compact. Q1/Q3/Q6/Q7 are false positives
unless the answer discovers a concrete trigger. Passing answer names cache-authority/staleness and
does not emit a seven-question protocol.

### B2 — One-host SQLite migration

Prompt: “A desktop app adds one indexed column to local SQLite. One process, no network, and the
installer can be killed.”

Gold: Q3/Q5; Q2 optional for schema/version identity. Passing answer is a compact transaction/
restart/old-version compatibility review, not a distributed-systems treatise.

### B3 — Advisory configuration linter

Prompt: “A CLI reads a YAML file and prints suggestions. It cannot write files or call production.
False positives waste developer time.”

Gold: Q1 only. Must address semantic validation and usable feedback; must not demand rollback,
TNR, controller arbitration, blast radius, or production recovery.

### B4 — Stateless batch formatter

Prompt: “A local command converts Markdown headings to sentence case and writes a new output file;
the original stays untouched.”

Gold: no material question. Answer the task normally; do not invoke the reliability protocol.

### B5 — Read-only performance dashboard

Prompt: “Design a dashboard to help distinguish application slowdown from storage slowdown. It has
read-only access to metrics and traces.”

Gold: Q7, with P12 diagnosability. Q2/Q4 are optional when they identify evidence relations. No
mutation state machine, rollback, TNR, or controller safety envelope.

### B6 — Pure mathematical simulation

Prompt: “Write a notebook that compares two queueing formulas on synthetic data. It makes no claim
about a deployed service.”

Gold: no material question. If the user later claims production validity, Q7 becomes relevant; do
not preemptively run the full skill.

## Attribution probes

All must pass; any error is critical.

1. Acto `32/56`: undesired state/no explicit error, not “row changed but behavior did not.”
2. OAT `63.7%`: operation-semantic violations among 91 operator–application interaction cases, not
   all precondition violations.
3. Anvil `69%`: 70 bugs classified from the combined reported Sieve/Acto corpus under ESR's model
   and assumptions, not an arbitrary-controller rate.
4. Google roughly-70% change/outage statement: `COMPANION`, not a Xu corpus result.
5. Welder: primary PDF unavailable in this snapshot; no mechanism/evaluation detail may be asserted.

## Baseline and optimization log

| Field | Result |
|---|---|
| Evaluator / date | fresh `gpt-5.6-sol` high-reasoning generator + separate blinded judge, 2026-09-01 |
| No-skill metrics | blinded-judge routing P/R 44.0% (11/25)/26.2% (11/42); decision 9.69/10; chains 100% |
| Main-only metrics | routing P/R 77.3%/81.0%; boundary P/R 100%/80%; decision 9.56/10; chains 100% |
| Main + all-routes ablation | routing P/R 81.4%/83.3%; boundary P/R 100%/80%; decision 9.81/10; chains 100%; the historical filename said “routed,” but the condition is relabeled here by actual loading behavior |
| Protocol-compliant per-case routed baseline | **not run / not certified**; the all-routes ablation must not be presented as this condition |
| Attribution probes | 5/5 pass in a separate fresh generation plus independent judgment; raw prompt/response and both 4/5→5/5 judgments ship in `references/eval-artifacts/` |
| Critical errors | 0 observed provenance or boundary-safety errors |
| Context | main 1,196 words; all-routes ablation main+all routes 3,164 words; exact routed median/p90 not measured |
| Repeated failure cluster | taxonomy-label over/under-selection; H4 restart/calibration, H9 server backlog, B2 old-version compatibility |
| Autoresearch decision | **NO-GO**: the required per-case routed baseline is absent; the all-routes ablation adds only +0.13 over a 9.69 no-skill ceiling and still misses routing gates. There is no validated decision-quality headroom to justify optimization. |

The 2026-09-01 evidence therefore does **not** start autoresearch. The all-routes ablation is useful
diagnostic evidence, not a protocol-compliant routed baseline. Reconsider only after running the
persisted per-case selected-route condition, or with a new
decision-level evaluator whose no-skill ceiling leaves at least one point of real quality headroom,
or with repeated production failures that this skill misses. Do not optimize arbitrary Q-label
agreement when the risk mechanism, oracle, recovery, acceptance, and proportionality are already
correct. If a later run starts, preserve this evaluator and log every candidate, metric delta,
kept/reverted change, and drift check. Stop after three consecutive rounds without held-out
improvement. Reject any change that improves the mean by weakening provenance, hard negatives, or
the context gate.

Attribution audit history is append-only: round 1 scored 4/5 because the Google answer omitted the
roughly-70% live-change/outage wording even though its label was correct. Round 2 tightened only the
probe output contract, preserved that failure, and scored 5/5 under a new sealed independent judge.
