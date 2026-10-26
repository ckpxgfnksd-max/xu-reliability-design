# Evaluation contract

This suite tests transfer, routing, provenance, and decision quality. It is not a paper-recall quiz
or a copy of the worked examples.

## Frozen objective

Optimize **decision-quality uplift per loaded context**. A candidate is better only if it improves
held-out design judgment without increasing attribution error, boundary misuse, or irrelevant
protocol loading.

## Evaluation protocol

Run the same model and effort in three blinded conditions, with case order randomized:

1. **No skill** — prompt only.
2. **Main only** — prompt plus `SKILL.md`.
3. **Routed** — prompt plus `SKILL.md`; the generator then reads only the route files its own
   triage selects. Run it against a copy of the skill directory with `EVALS.md`, `evals/`,
   `references/examples.md`, and `references/eval-artifacts/` removed. Each generator writes a
   meta file with `selected_questions`, `unknown_questions`, and every file it read; a routed run
   that loaded a route file for a question it neither selected nor marked unknown is flagged.

A separate fresh-context judge receives the response, `evals/rubric.md`, and the case gold. The
judge is not told which condition or skill version produced a response. Record loaded word count
for every run. Prompts, golds, and expectations are machine-readable in `evals/evals.json`; the
judge output schema is in `evals/rubric.md`. `references/examples.md` is removed from the measured
copy because its worked reviews overlap the case set; measured context therefore understates
shipped context by that file whenever a generator would have loaded it.

## Rules for any optimization round

- Cases, golds, and the rubric are frozen for the duration of a round. A gold may change only
  between rounds, with a logged rationale, and never for a case whose number that round reports.
  The one carve-out is a pure taxonomy relabel (`kind: relabel` in `gold_history`) that renames a
  label without changing required content. Every entry carries `recorded_on` (when it was
  written) and `effective_from` (the first round it applies to); `aggregate.py --as-of` errors
  when a reported case has any other in-force gold change recorded on or after the round date.
- Stop after three consecutive rounds without held-out improvement.
- Reject any change that improves the mean by weakening provenance, the hard boundary cases, or
  the context gate, even if every other metric rises.
- The 2026-09-01 NO-GO stands until a protocol-compliant per-case routed baseline exists and
  either the evaluator's no-skill ceiling leaves at least one point of headroom or repeated
  production failures show what the skill misses. Do not optimize label agreement when mechanism,
  oracle, recovery, acceptance, and proportionality are already correct.
- Log every candidate, metric delta, kept or reverted change, and drift check.

## Metrics and gates

| Metric | Computation | Gate before autoresearch |
|---|---|---|
| Routing precision/recall | computed mechanically by `evals/aggregate.py` from the generator's recorded selections: material selected = TP, optional = neither, anything else = FP; macro-averaged per case; empty-gold cases score 1.0 when nothing is selected | both ≥90% overall and ≥85% on boundary cases |
| Complete risk chains | top three material risks containing trigger, consequence/invariant, prevention, behavioral oracle, recovery, falsifiable acceptance | ≥85% |
| Decision-quality score | 0–2 each for mechanism, oracle, recovery/control, acceptance, proportionality; max 10 | routed mean ≥8.0 and ≥1.0 above no-skill, valid only when the no-skill mean is ≤8.5; a higher no-skill mean voids the gate and means the case set lacks headroom |
| Provenance | correct `XU-DIRECT` / `XU-SYNTHESIS` / `COMPANION`, denominators and metadata limits | 100%; zero critical error |
| Boundary safety | no absolute misuse of TNR, mocks, formal methods, recovery exercise, knob deletion, or automation | zero critical misuse |
| Context | words in actually loaded skill/reference files | median ≤4,000; p90 ≤7,000 |

An answer may omit paper citations when research attribution is not decision-relevant. Do not reward
paper-name density.

## Case sets

Three sets with different evidential status. Never report a dev-set number as held-out.

| Set | Cases | Status |
|---|---|---|
| Dev | H1, H4, H6, H9, B1, B2, B3 | Used to design the 2026-09-09 restructure; the H4, H9, and B2 misses were fed back into `q6`/`q7`, `q6`, and `q3`. The skill text may be changed in response to these cases; their golds stay frozen like every other gold. |
| Seen | H2, H3, H5, H7, H8, H10, B4, B5, B6 | Authored 2026-09-01; read by the 2026-09-09 designer while restructuring but not fed back. Report separately from Held-out. |
| Held-out | N1–N6 | Authored 2026-09-09 by the same designer after the restructure was written, and not used to edit the skill. They are designer-authored, and their label golds use the 2026-09-09 taxonomy, so they are the least contaminated set available, not a clean one. A set authored by a context that has never seen the triage table is required before any held-out transfer claim. |

When a held-out case is used to fix the skill, move it to Dev and author a replacement.

Question labels follow the 2026-09-09 taxonomy: Q7 Fidelity (P8, P14) and Q8 Diagnosability
(P12). Golds authored under the earlier seven-question taxonomy were relabeled where the required
content moved between labels (H5, B5); the required content is unchanged. H8's added Q8 optional
is a content change dated 2026-09-10, not a relabel.

`evals/evals.json` is the authoritative gold set; the case list below is a rendered view of it,
and its `gold_history` entries record every gold change with a rationale and the round it takes
effect. Partition rule: every question not listed as material or optional is a false positive.
The mechanical score is strict; a judge may list a `justified_fp` with a prompt quote, which is
reported alongside but never replaces the strict number.

Label map for cross-version comparison: a response produced under the seven-question taxonomy
cannot emit `Q8`. When gold `Q8` is material, `evals/aggregate.py` lets a selected `Q7` also
satisfy it, and that `Q7` leaves the false-positive set only if `Q7` is not itself material or
optional; when gold `Q8` is merely optional, a selected `Q7` is untallied (neither TP nor FP);
there is no other stand-in, and a no-skill response gets no map. The map is applied mechanically
from the recorded version, never by the judge: a judge
can usually infer the version from label vocabulary and output format, so it reports raw
selections and content scores only. Every applied gold change is stored in `gold_history` with
its previous and current sets and an `effective_from` date; `aggregate.py --as-of DATE` replays
the golds as they stood on that date. A change derived while a round is open, or one that would
touch a held-out case, is stored under `proposed_gold_changes` and is not in force until applied
before a later round (applying one to a held-out case moves that case to Dev). `must_cover_history`
records wording changes; the scorer warns when the replayed wording differs from what the judges
scored and does not rescore coverage.

## Transfer cases

### H1 — Online schema migration with mixed binaries (dev)

Prompt: "Add a non-null `owner_id` to a 4-TB table. Old and new binaries coexist for a week; two
services write the row; backfill can restart. The rollback plan is redeploy old code."

Gold: Q2/Q3/Q4/Q5. Must expose dual-writer/version semantics, durable backfill cursor, old/new read
and write compatibility, conservation oracle, retry/restart, and the fact that code rollback cannot
undo transformed state. Q7 is acceptable only if production-data distribution changes a decision.

### H2 — At-least-once payment webhook (seen)

Prompt: "A provider retries callbacks for 72 hours. Our handler writes an order, emits a shipment
event, and returns 200. A timeout may happen after either effect."

Gold: Q2/Q3/Q4/Q5. Proposed for the next round, not applied: Q6 acceptable optional as a
bounded-wait note for a slow-but-connected event bus. Must define provider/event identity,
partial-effect state machine,
duplicate/late success, authoritative conservation relation, compensation/manual recovery, and
crash-prefix tests. Do not mandate double-entry without deriving the domain invariant.

### H3 — Feature flag with stale edge caches (seen)

Prompt: "A boolean flag disables checkout in one country. Admin UI validates type; edge caches have
unknown TTL and can miss invalidations."

Gold: Q1/Q2/Q5. Must distinguish declared/effective state, generation or bounded freshness,
end-to-end country behavior, repairable unsafe intent, and stale/omitted invalidation tests. Q3 is
optional only if rollout has multiple committed effects.

### H4 — Live storage tuning (dev)

Prompt: "A controller changes compaction concurrency every minute from latency telemetry. Operators
can override it. The value is atomically stored."

Gold: Q1/Q6/Q7; Q2, Q3, and Q5 acceptable optional (Q5 from 2026-09-10: the Q5 reconciliation
clause can read as yes for a controller). Must cover semantic ground truth, stale/noisy
telemetry, competing writers (operator override vs controller, arbitrated under Q6), step/rate/
stop/LKG, crash/restart with re-observation before acting, and behavioral/capacity calibration.
Atomic storage alone is weak. (Q2 and Q3 demoted to optional, effective 2026-09-10: arbitration
is Q6 content and no must-cover item is a multi-effect workflow.)

### H5 — Intermittent DNS degradation diagnosis (seen)

Prompt: "Only one customer cohort sees 3-second pauses. Aggregate latency is normal; logs record
request timeout but not resolver path or config generation."

Gold: Q2/Q4/Q8 (the 2026-09-01 gold with Q7 relabeled to Q8). Proposed for the next round, not
applied: Q2 and Q4 to optional, because every must-cover item is Q8 content and the prompt does
not establish a resolver-cache authority problem. Must design affordable cross-layer and
relational evidence, effective config/version, a cohort comparator, resolver/dependency outcomes,
and a test that separates at least two plausible causes. Do not turn this into a mutation/recovery
review. (Relabeled 2026-09-09 from Q2/Q4/Q7: the diagnosability content moved from Q7 to Q8; no
question was demoted for the round that reports this case.)

### H6 — Sandboxed runtime plugin (dev)

Prompt: "Plugins are verified bytecode, but safe source programs are often rejected. Teams use an
unsafe host-call helper to ship on time."

Gold: Q1/Q4/Q5; Q7 optional for workload calibration, Q6 optional from 2026-09-10 for runtime
containment as blast radius. Must treat false rejection and workaround as assurance risk, map
source/compiler/verifier/runtime contracts, narrow the unsafe boundary, and test both safe
expressiveness and runtime containment.

### H7 — Restore from object-store backup (seen)

Prompt: "Nightly backups report success. Restore was last attempted 18 months ago; credentials and
encryption keys have since changed. Testing on production data is prohibited."

Gold: Q1/Q3/Q5/Q7. Must use safe representative/redacted data, real restore identity/key path,
durable stages, integrity/behavior oracle, risk-calibrated rehearsal, and narrow the recovery claim
to the evidenced radius. Never insist on raw production data or continuous production restores.

### H8 — Cached authorization change (seen)

Prompt: "A support role gains a new regional action. CI diffs policy text; five gateways cache
decisions independently. Denial messages cause operators to request admin."

Gold: Q1/Q2/Q5/Q7. Q7 stays material because the CI policy-text diff is a surrogate for effective
decisions: the review must compare before/after effective decisions with production code and
production-shaped data. Must also explain new allow/deny outcomes, test cache convergence/replay,
preserve policy provenance, and improve repair feedback without over-grant. Q3 is optional if
activation is staged; Q8 is acceptable optional for policy provenance from 2026-09-10.

### H9 — Intermittently connected device fleet (dev)

Prompt: "A device-management service pushes firmware intent over unreliable mobile links. Devices
may reconnect weeks later with old desired state and repeat acknowledgements."

Gold: Q2/Q3/Q4/Q6; Q7 acceptable optional for real-link distribution calibration. Must cover
generation/authority, late/replayed messages, resumable device transition, version compatibility,
partial success, bounded server retry and backlog with a stated behavior at the bound, and
effective firmware behavior as the oracle. Proposed for the next round, not applied: Q5 to
optional, because the oracle item is Q5 content.

### H10 — ML autoscaler using a simulator (seen)

Prompt: "A learned autoscaler is trained in a simulator and moves 20% traffic per decision. Offline
reward is high; two manual traffic tools also exist."

Gold: Q4/Q6/Q7; Q5 acceptable optional from 2026-09-10 for a stability statement. Must cover
shared actuator/arbitration, hard capacity/radius bounds, stop/LKG,
simulator decision-fidelity calibration, correlated faults, and a canary/production guardrail. Do
not ban learning or require formal proof by default.

## Hard boundary cases

These distinguish routing from template dumping.

### B1 — Small CRUD service with one read cache (dev)

Prompt: "Review a five-endpoint internal CRUD service. One process owns Postgres; Redis caches
reads for 30 seconds. Deploys are ordinary rolling restarts."

Gold: Q2 is material; Q4/Q5 are acceptable optional if kept compact. Q1/Q3/Q6/Q7/Q8 are false
positives unless the answer discovers a concrete trigger; "ordinary rolling restarts" is not a Q3
trigger, and a write followed by a TTL-repaired cache invalidation is Q2, not Q3. Proposed for the
next round, not applied: Q6 acceptable optional as one paragraph on timeouts or bulkheads for a
slow Redis. Passing answer names cache-authority/staleness and does not emit an eight-question
protocol.

### B2 — One-host SQLite migration (dev)

Prompt: "A desktop app adds one indexed column to local SQLite. One process, no network, and the
installer can be killed."

Gold: Q3/Q5; Q2 optional for schema/version identity. Passing answer is a compact transaction/
restart/old-version compatibility review (the old binary must still open a half-migrated or
migrated file, or refuse explicitly), not a distributed-systems treatise.

### B3 — Advisory configuration linter (dev)

Prompt: "A CLI reads a YAML file and prints suggestions. It cannot write files or call production.
False positives waste developer time."

Gold: Q1 only. Must address semantic validation and usable feedback; must not demand rollback,
TNR, controller arbitration, blast radius, or production recovery.

### B4 — Stateless batch formatter (seen)

Prompt: "A local command converts Markdown headings to sentence case and writes a new output file;
the original stays untouched."

Gold: no material question. Answer the task normally; do not invoke the reliability protocol.

### B5 — Read-only performance dashboard (seen)

Prompt: "Design a dashboard to help distinguish application slowdown from storage slowdown. It has
read-only access to metrics and traces."

Gold: Q8 material (relabeled 2026-09-09 from "Q7 with P12"). Q2/Q4 are optional when they identify
evidence relations. No mutation state machine, rollback, TNR, or controller safety envelope.

### B6 — Pure mathematical simulation (seen)

Prompt: "Write a notebook that compares two queueing formulas on synthetic data. It makes no claim
about a deployed service."

Gold: no material question. If the user later claims production validity, Q7 becomes relevant; do
not preemptively run the full skill.

## Held-out cases (authored 2026-09-09, never used for design)

### N1 — Cross-region session revocation

Prompt: "Logging a user out must make their session unusable everywhere within 60 seconds. Sessions
are signed tokens that 12 edge services validate locally. A revocation list is pushed over a
message bus; each edge caches it with a five-minute TTL and re-fetches on a miss."

Gold: Q2/Q5 material; Q4 acceptable optional for the bus delivery contract. Known tension, recorded
as a proposal and not applied: the shipped Q6 trigger fires on the miss-time re-fetch, a
caller-waited dependency; an independently authored set should settle it. Must expose the conflict
between the 60-second claim and the five-minute cache, distinguish declared from effective
revocation, define the oracle as a real request through every edge, and test bus omission, replay,
and a token issued just before revocation. Do not demand a controller envelope, TNR, or a formal
model.

### N2 — Nightly backfill with a cursor

Prompt: "A cron job runs at 02:00, reads `last_processed_at` from a table, aggregates events newer
than it, writes the aggregates, then advances the cursor. A slow run can overlap the next one. The
job exits 0 when the upstream event table is empty."

Gold: Q2/Q3/Q5 material; Q8 acceptable optional for making a silent no-op visible. Must treat the
cursor as a checkpoint with two possible writers, the write-then-advance pair as an interruptible
multi-effect transition, exit-0-on-empty as a fired-but-not-finished hazard needing a progress or
conservation oracle (events in versus events aggregated), and idempotent reprocessing. Do not demand
a controller envelope or capacity gate.

### N3 — Auto-merge bot on green CI

Prompt: "A bot merges dependency-update pull requests automatically when CI reports green. CI runs
unit tests; integration suites are skipped when the Docker daemon is unavailable, and skipped suites
report as passed."

Gold: Q1/Q7 material; Q5 and Q6 acceptable optional. Must treat "green" as a surrogate with a known
discrepancy (skipped counts as passed), require a deterministic gate that distinguishes pass, fail,
and skipped, bound what may be auto-merged, and give a repairable rejection. Do not demand a
multi-step state machine for a single merge, and do not ban automation.

### N4 — Lag-aware read router

Prompt: "A database proxy routes read queries to the replica reporting the lowest replication lag.
Each replica reports its own lag every ten seconds. When every replica reports more than 30 seconds
of lag, all reads go to the primary."

Gold: Q2/Q6 material; Q5 acceptable optional for read-your-writes. Proposed, not applied: Q7
optional for the uncalibrated 30-second threshold, and Q2 to optional because the route text
assigns telemetry staleness to Q6; both are known tensions for an independently authored set to
settle. Must treat lag as a stale
self-report, treat the all-to-primary step as an unbounded traffic move needing hysteresis, step,
and capacity bounds, cover a replica that is slow yet reports low lag and the case where reports
stop arriving, and define goodput and recovery observation. Do not demand a formal model or TNR.

### N5 — EXIF rename script

Prompt: "Write a script that renames the image files in a folder to a date-based scheme from their
EXIF data, writing the renamed copies to a new folder and leaving the originals untouched."

Gold: no material question. Answer the task normally; do not invoke the reliability protocol.

### N6 — Zone-scoped latency regression after a kernel upgrade

Prompt: "After a kernel upgrade rolled out to one availability zone, p99 write latency doubled there
only. Metrics are per service with no per-host or per-zone breakdown. The upgrade also changed the
default I/O scheduler."

Gold: Q8 material; Q4 and Q7 acceptable optional. Must design a zone and host comparator, join
per-host effective kernel version and scheduler to latency, propose a query or experiment that
separates scheduler change from kernel change from a coincident deploy, and keep collection
affordable. Do not turn this into a rollout or recovery review.

## Attribution probes

All must pass; any error is critical.

1. Acto `32/56`: undesired state/no explicit error, not "row changed but behavior did not."
2. OAT `63.7%`: operation-semantic violations among 91 operator–application interaction cases, not
   all precondition violations.
3. Anvil `69%`: 70 bugs classified from the combined reported Sieve/Acto corpus under ESR's model
   and assumptions, not an arbitrary-controller rate.
4. Google roughly-70% change/outage statement: `COMPANION`, not a Xu corpus result.
5. Welder: primary PDF unavailable in this snapshot; no mechanism/evaluation detail may be asserted.

## Baseline and optimization log

### 2026-09-01 baseline (seven-question taxonomy)

| Field | Result |
|---|---|
| Evaluator / date | fresh `gpt-5.6-sol` high-reasoning generator + separate blinded judge, 2026-09-01 |
| No-skill metrics | blinded-judge routing P/R 44.0% (11/25)/26.2% (11/42); decision 9.69/10; chains 100% |
| Main-only metrics | routing P/R 77.3%/81.0%; boundary P/R 100%/80%; decision 9.56/10; chains 100% (seven-question taxonomy and pre-change golds: not comparable to post-restructure runs; any delta needs both arms rerun under current golds) |
| Main + all-routes ablation | routing P/R 81.4%/83.3%; boundary P/R 100%/80%; decision 9.81/10; chains 100%; the historical filename said "routed," but the condition is relabeled here by actual loading behavior |
| Protocol-compliant per-case routed baseline | not run / not certified; the all-routes ablation must not be presented as this condition |
| Attribution probes | 5/5 pass in a separate fresh generation plus independent judgment; raw prompt/response and both 4/5→5/5 judgments ship in `references/eval-artifacts/` |
| Critical errors | 0 observed provenance or boundary-safety errors |
| Context | main 1,196 words; all-routes ablation main+all routes 3,164 words; exact routed median/p90 not measured |
| Repeated failure cluster | taxonomy-label over/under-selection; H4 restart/calibration, H9 server backlog, B2 old-version compatibility |
| Autoresearch decision | **NO-GO**: the required per-case routed baseline is absent; the all-routes ablation adds only +0.13 over a 9.69 no-skill ceiling and still misses routing gates |

The all-routes ablation is diagnostic evidence, not a protocol-compliant routed baseline. The
no-skill ceiling of 9.69 also shows that the H/B prompts are too close to textbook cases for this
judge to measure the skill's contribution; the N cases were written to be less generic, and the next
evaluator revision should draw cases from real repository changes and incident histories.

Attribution audit history is append-only: round 1 scored 4/5 because the Google answer omitted the
roughly-70% live-change/outage wording even though its label was correct. Round 2 tightened only the
probe output contract, preserved that failure, and scored 5/5 under a new sealed independent judge.

### 2026-09-09 restructure (eight-question taxonomy)

Changes, all in the layer loaded at generation time: `SKILL.md` keeps one taxonomy (the P1–P14
table moved out; `principles.md` remains the reference); Q7 split into Q7 Fidelity and Q8
Diagnosability so P12 has one home and diagnosis prompts stop routing into recovery reviews; triage
triggers rewritten as questions answerable from the artifact instead of taxonomy labels; output
reduced to three required items with a per-risk block instead of a seven-column table; corpus
bookkeeping and the Welder paragraph moved out of the main file; route headers cite named anchors
instead of bare ID lists; the three 2026-09-01 misses fed back as guideline items, acceptance
probes, and failure signals in `q3` (old-version compatibility), `q6` (restart re-observation,
bounded backlog toward disconnected targets), and `q7` (calibration of gains). Main file 1,196 →
1,223 words: the removed bookkeeping was replaced by longer triggers, so the file did not shrink;
loaded context for a typical 3-question review is about 2,200 words.

#### Independent review of the change

`~/bin/opus-review` (fresh-context adversary, sees only the diff) ran three rounds on this change.
Round 1: FAIL, 4 high / 6 medium / 2 low. Round 2: FAIL, 3 high / 8 medium / 2 low. Every finding
was either fixed or recorded here with a reason; the substantive ones were the deleted anti-gaming
rules, the overclaimed held-out set, a judge-applied label map, writer arbitration owned by three
places, a closed Q3 list, missing single-dependency fail-slow in Q6, the unsatisfiable decision
gate, and gold inconsistencies (H4, H5, H8, H9, N4, B1). Round 3: FAIL, 2 high / 7 medium / 3 low,
all on the eval machinery: a declared Q2 stand-in the scorer did not implement, B1's must-cover
contradicting its Q3 false positive, gold changes with no stored previous sets or replay flag,
gates the scorer never reported, prose-regex selection fallback, and the Q6 fail-slow clause
firing on H2/N1/N2. Fixed by the `gold_history` contract with `--as-of`, the strict stand-in rule,
gate aggregates, meta-or-judge selections only, the caller-waited scope on the Q6 clause, and the
B1/H2/H4 gold entries. Round 4: FAIL, 4 high / 8 medium / 3 low: `must_cover` wording changed with
the routes but not versioned; golds changed for cases the same round reported; summary pooled
across sets; N1's Q6 false positive contradicted the shipped trigger; response-controlled chain
denominator; a second (Q2) stand-in; precision undefined when only optional questions were
selected; undefined decision scores on empty-gold cases; H4/N4 disagreeing on telemetry
staleness; B1's Q3 optional contradicting the Q3 exclusion; Explain mode not loading the
principles. Fixed by `must_cover_history`, reverting the reported cases' changes to
`proposed_gold_changes`, per-set summaries, N1/N4 gold entries, a fixed denominator of 3, a single
Q7 stand-in, P = 0 when nothing material is selected, decision `n/a` on empty-gold cases, and
Explain mode loading `principles.md`. Round 5: FAIL, 6 high / 6 medium / 1 low: a stale Q2
stand-in in the docstring and this file; proposals rendered as live golds; H5's Q2 demotion dated
inside the reported round; N1/N4 held-out golds edited toward the shipped triggers; unresolvable
`files_read` paths counted as zero; the Q2 and Q6 parentheticals contradicting each other for
automation-written state; dead `must_cover` replay; expectations granting an escape the strict
scorer ignores; the preference row called blind. Fixed by removing the Q2 stand-in everywhere,
rendering proposals as proposals, moving the H5 demotion and the N1/N4 edits to proposals and
rescoring, failing on missing paths, narrowing the Q2 parenthetical to controllers and shared
actuators, a replay warning instead of silent versioning, unconditional expectations, and
relabeling the preference row. Round 6: FAIL, 1 high / 4 medium / 3 low: the scorer could not
represent the no-skill and main-only conditions the protocol mandates; the label map penalized an
old-arm `Q7` when `Q8` was only optional; the Q5 reconciliation clause fired on feedback
controllers that H4/H10 score as false positives; silent drops from gated denominators; no
mechanical guard for the frozen-gold rule; `blind_wins` naming. Fixed by a `condition` field with
per-(condition, version, set) summaries and the decision-gate computation, the untallied rule,
scoping the Q5 clause and adding Q5-optional entries on H4/H10, printed warnings and denominators,
the relabel carve-out with an `--as-of` guard, and `preference_wins`. Round 7 verdict is recorded
at the end of this section. Round 7: **PASS**, 0 blocking, 5 medium / 3 low. The eight
non-blocking findings were applied after the pass and are not covered by it: H4/H10/H6 rendered
golds now carry their Q5/Q6 optional entries; the H8 relabel entry is marked `relabel`; the
frozen-gold guard distinguishes `recorded_on` from `effective_from`; the decision gate is computed
per set and guards a missing no-skill mean; a routed run that loaded route files for unselected
questions is flagged; the future-dated warning fires only without `--as-of`. Round 8 was run on
the result as a confirmation; its verdict is the last line of this section.

#### Smoke comparison, 2026-09-09

Old (2026-09-01 seven-question) and new (2026-09-09 eight-question) skill copies, each stripped of
`EVALS.md`, `evals/`, `references/examples.md`, and `references/eval-artifacts/`, run under the
Routed condition by fresh `claude-fable-5-1` subagents on nine cases: B1, B2, B4, B5 (boundary),
H2, H5 (seen), H9 (dev), N2, N6 (held-out). One generation per arm per case; no repeats, so no
variance estimate. A separate fresh judge per case scored both arms under `evals/rubric.md` with
A/B labels assigned at random; routing was scored mechanically by `evals/aggregate.py` against the
golds replayed with `--as-of 2026-09-09`. Gold changes that would have touched the nine reported
cases (H2 Q6, H5 Q2/Q4, H9 Q5, B1 Q6) and the held-out cases (N1 Q6, N4 Q2/Q7) are stored as
`proposed_gold_changes` and not applied; H4's changes carry `effective_from` 2026-09-10 and H4 is
not in this round. `must_cover` wording sharpened while feeding back the H9/B2/B1 misses is dated
2026-09-10 in `must_cover_history`, so the replay warns for H9, B1, and B2: the judges scored the
current wording, and the three old-arm misses (B1 compact, B2 compact, H9 bounded retry) are
misses under the 2026-09-01 wording as well. The B1 new-arm run was repeated
after the Q3
trigger gained the stateless-restart exclusion; the first run had also selected only Q2, so the
repeat changed the wording under test, not the outcome. The H9 new-arm
meta file was lost to a rate limit and its selected set was reconstructed from the review's own
triage section.

| Metric (`--as-of 2026-09-09`, macro per case) | Old, all 9 | New, all 9 | Old / New dev (B1, B2, H9) | Old / New seen (B4, B5, H2, H5) | Old / New held-out (N2, N6) | Gate |
|---|---|---|---|---|---|---|
| Routing precision | 0.79 | 0.90 | 0.75 / 0.92 | 0.88 / 1.00 | 0.67 / 0.67 | ≥0.90 |
| Routing recall | 0.94 | 0.84 | 0.92 / 0.75 | 0.92 / 0.83 | 1.00 / 1.00 | ≥0.90 |
| Boundary precision / recall (B1, B2, B4, B5) | 0.75 / 1.00 | 1.00 / 0.88 | | | | ≥0.85 |
| Complete risk chains (denominator 3 per case with a material question) | 22/24 = 0.92 | 23/24 = 0.96 | 9/9 / 8/9 | 7/9 / 9/9 | 6/6 / 6/6 | ≥0.85 |
| Decision quality (judge, max 10; empty-gold B4 excluded) | 8.62 | 10.0 | 8.67 / 10 | 8.33 / 10 | 9.0 / 10 | ceiling: see below |
| must_cover misses / must_not violations | 3 / 2 | 0 / 0 | 3 / 1 vs 0 / 0 | 0 / 0 vs 0 / 0 | 0 / 1 vs 0 / 0 | 0 critical |
| Boundary-safety flags | 0 | 0 | | | | 0 |
| Provenance | 9 unverified | 9 unverified | | | | 100%: not measured |
| Judge preference (cases won; unblinded in practice, since the version is inferable from label vocabulary) | 0 | 9 | 0 / 3 | 0 / 4 | 0 / 2 | |
| Loaded context, median / p90 words (context denominators: old 9 runs, new 8) | 2,304 / 11,672 | 2,646 / 7,163 | | | | ≤4,000 / ≤7,000 |
| Response length, mean words | 1,973 | 1,704 | | | | |

The all-9 columns pool three sets and are shown for the comparison only. Routing, chains, and
decision quality are gated on the per-set columns; boundary, context, provenance, and safety rows
are reported pooled and are not per-set gate evidence. The held-out pair (N2, N6) is too small to
gate on. Provenance was not
measured: the judges were not given `research-map.md`, so every citation is `unverified`, not a
pass. The old arm's N2 `Q7` is untallied because N2's `Q8` is only optional. The no-skill and
main-only conditions were not run, so the decision-quality gate is not evaluated for this round.
Loaded-context counts are computed against the final skill copy, which is up to
about 50 words longer per run than the copy each executor read. The new arm breaches the p90
context gate on N6, where it loaded `principles.md` and `research-map.md` for a diagnosis; the
`Conditional references` section now says a review does not need them, which is untested here.

What moved and why:

- The two old-arm `must_not` violations were the template dump on B1 (Q3 false positive plus the
  full protocol at twice the length) and N6 turned into a rollout/rollback review; both are the
  failure shapes the restructure targeted, and the new arm stayed inside the diagnosis on N6 and
  inside one question on B1.
- B5 and H5 routed exactly to the new Q8 while the old arm spread across Q2/Q4/Q6/Q7 and left two of
  three H5 chains without recovery.
- Old-arm reviews on H2 and N2 pasted the route headers' bare paper-ID lists into the user-facing
  review; the named-anchor headers removed that.
- New-arm recall losses are label-level: B2 carried the Q5 invariant under Q3, H9 covered bounded
  retry and backlog (Q6 content) under Q3/Q4 and marked Q6 `unknown` because the prompt names no
  rollout controller, and on H5 both arms miss Q4 while the new arm also misses Q2 (it treated
  resolver caching as part of the diagnosis). Both arms over-select on N6 (new: Q1, Q3; the Q3
  pick predates the stateless-restart exclusion).
- The decision-quality judge saturates at 10 on every new-arm case, so this evaluator cannot show
  further quality headroom; the next revision needs harder, repository-grounded cases, as the
  2026-09-01 NO-GO already required.

Verdict for this round: on the dev and seen sets the restructure improves routing precision,
chain completeness, proportionality, and boundary behavior at lower response length, with a
modest context increase and one p90 breach; recall is below gate on label agreement only. The
held-out pair ties on precision and is directional evidence, not a measurement. The NO-GO on content autoresearch
stands until the evaluator has headroom. Raw outputs and judge JSON are in the session scratchpad
(`run/out`, `run/judge`); rerun with
`python3 evals/aggregate.py --run-dir <run> --evals evals/evals.json --as-of 2026-09-09`.

Round 8 independent review (confirmation after the post-pass fixes): **PASS**, 0 blocking,
4 medium / 2 low. Those six were applied afterwards without a further review round: the case-sets
prose no longer claims H5's Q2 demotion is applied; H8's Q8 entry is a dated content change, not a
relabel; the decision gate pairs cases scored in both conditions and refuses unequal sets;
`recorded_on` is required on every non-relabel gold entry; the routed-integrity flag honours
`unknown_questions`; an empty `files_read` yields no context count. Rescoring after these edits
reproduced every number in the table above.


## 2026-10-22 — source-grounded ownership pilot extension

This is a focused execution/evidence update, not content autoresearch. The prior
NO-GO and all existing golds, partitions, scores and historical findings remain
unchanged. No new decision-quality uplift or held-out transfer claim is made.

Five new development prompts are in `evals/ownership-pilot.json`: runner death
versus writer authority, detached descendants after timeout, Lite conformance
limits, static UI non-triggering, and dependency/host boundaries. These were
authored from observed pilot behavior and inspected by the lead; they are not
blinded generator runs or independent behavioral benchmark results. Skill behavior
has not been forward-tested against OWN-1 through OWN-5.

The live pilot used Specula Lite upstream commit
`39b4a0150a2eb313f3d9abbc78fb41a0d756067f` and an unchanged job-runner source
snapshot with SHA-256
`cfb6091ea2465d9d144773e3fe06378bcbbd5684706a7f687f7dfffa70118ca1`.
A project-local dependency checksum pin was updated after matching the
official TLC release API digest (same-origin asset identity, not independent build
provenance); the original mismatch and patch are recorded
in the owning run. No global Specula installation or production runtime fix ran.

| Verification | Observed result | Evidence boundary |
|---|---|---|
| SANY parse | completed, exit 0 | model syntax only |
| Structural check | completed, 12 distinct states | TypeOK only |
| Ordinary environment model control | completed, 22 distinct states, both target invariants | no crash/detached writer |
| Crash ownership hunt | 6-state violating trace | model candidate, then real CLI reproduction |
| Detached timeout ownership hunt | 10-state violating trace | documented limitation, then real CLI reproduction |
| Timeout quiescence hunt | 7-state violating trace | same detached-process mechanism, not a third defect |
| Real-process fixtures | 4 scenarios passed their consequence/control assertions | two unsafe paths reproduced; no deployment incident claimed |
| Additional lock control | second live runner refused, exit 2 | runner exclusion only |
| Fixture cleanup | no live owned fixture process; output stable | isolated pilot resources only |

Implementation trace validation: **NOT PERFORMED**, per Lite. Bounds: one job,
two attempts, at most one runner crash. No liveness/unbounded proof. Raw models,
configs, counterexamples, unchanged source, executed reproductions and review
receipts remain with the owning task run, not embedded in this public skill.
The canonical private run pointer belongs in the local overlay/context index.


## 2026-10-26 — ownership development-case forward execution and dependency correction

This follow-up actually executed all five existing OWN-1–OWN-5 prompts. It does not reopen content autoresearch or change the earlier NO-GO, golds, partitions or historical scores. The earlier statement that these five prompts were not forward-tested is historical; this section supplies the later execution evidence.

The comparison is pre-2026-10-22 skill versus the 2026-10-26 candidate (Oct22 extension plus the narrow checksum/provenance clarification below). Both arms used the registered Codex lane, requested `gpt-6-astra`, effort `high`, in two fresh CLI contexts per arm. Each context received all five original prompts without golds, expected dispositions or earlier findings. The second repetition reversed the request order in both arms. These are suite-batched response tasks, not five isolated-context process experiments. Observed CLI success does not identify model weights; no temperature or model seed control was exposed.

The lead read every complete response and proposed semantic judgments with verbatim evidence. The lead knows the version mapping and is not a blinded independent judge. Version-masked artifacts are retained for audit; their wording can reveal treatment, and masking alone does not establish blindness. Required independent review is recorded by the owning run before activation. This is a small development-set measurement, not held-out transfer, statistical significance or a general reliability uplift estimate.

| Metric | Before | After | Denominator |
|---|---:|---:|---|
| Correct requested disposition | 10 | 10 | 5 prompts × 2 repetitions per arm |
| Required semantic coverage | 26 | 28 | 14 items × 2 repetitions per arm |
| Fully covered, safe answers | 8 | 10 | 10 answers per arm |
| Forbidden-claim/action violations | 0 | 0 | 10 answers per arm; all listed must-not criteria checked |
| Coverage plus disposition score | 36 | 38 | 38 possible points per arm |
| Mean response length | 1,018 | 913 | Unicode characters across 10 answers per arm |

Both repetitions yielded 18/19 before and 19/19 after. The only scored gap was OWN-3: both old responses correctly refused conformance and unbounded-restart claims, but could not explicitly establish that Lite omits implementation trace validation from their supplied snapshot. Both new responses stated that limitation. Do not describe this as old outputs granting unsafe conformance. OWN-1 received semantic credit in the old arm for observing accepted shared-resource writes during a continuous-writer/crash/resume test even without the exact word “interleaved”; no vocabulary-matching penalty was used. OWN-2, OWN-4 and OWN-5 also passed in both arms. On OWN-5 both new answers explicitly distinguish a same-origin replacement hash from independent authentication and exclude prior unresolved-tool checker outputs from passing assurance evidence. These observations do not establish broader supply-chain safety.

Dependency correction: the earlier project-local TLC JAR differed from the pinned digest. The archived publisher asset response from the original 2026-10-22 pilot contains the matching digest; this follow-up compares that saved response with the cached bytes. It supplies historical same-origin metadata only, not a fresh publisher verification or independent authentication. The official README explains that 1.8.0 is a rolling pre-release, which diagnoses drift but does not authenticate the replacement. The cached JAR has no embedded signature entries; the fixed-digest GitHub attestation query returned 404. Neither observation proves authentication is impossible; no independent trust anchor was obtained in this follow-up. The JAR was inspected without executing it and remained unchanged.

The unresolved replacement is now **blocked for dependent execution**. Historical SANY/TLC outputs from that replacement remain preserved observations, labelled **provenance-unverified and inconclusive for assurance**, and are excluded from this follow-up's passing evidence. The historical table above records what happened; its checker results must not be read as currently accepted assurance. Independently reproduced real-process failures and regression evidence stand separately. The skill now says to stop on checksum failure, require an independently trusted signature/attestation/digest channel to resume, and report a blocker otherwise. No same-origin repin or “record the limit and proceed” path is permitted. No global cache was deleted and no other agent's dependency setup was changed.

Canonical private paths, raw answers, exact snapshot/producer hashes, runtime attempt IDs, commands, scores, review results and dependency HTTP responses live in the local context record, not this generic skill. The source signatures/build provenance remain unresolved; the operational error was addressed by fail-closed use and corrected acceptance classification, not by claiming a verified binary.
