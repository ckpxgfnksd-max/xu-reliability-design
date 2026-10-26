# Judge rubric

You receive one design prompt, its gold record from `evals.json`, and one or more responses labeled
A, B, … You are not told which skill version or condition produced each response, and you may be
able to infer it from label vocabulary or output format. Score content, never format or vocabulary.
Judge every response independently against the gold, then compare.

## 1. Routing (report only; do not score)

Report the raw set of questions each response treated as selected: use `meta.selected_questions`
when a meta file is provided; otherwise extract the set from the response's triage list or section
headings. Do not compute precision or recall and do not apply any label mapping: routing is scored
mechanically by `evals/aggregate.py`, which applies the partition rule (every question not listed
as material or optional is a false positive) and the cross-version label map.

If a response selects a question outside the gold's material and optional sets and names a
concrete trigger from the prompt for it, list it under `justified_fp` with the quote. This is
advisory; the mechanical score stays strict.

## 2. Risk chains

For the top three material risks the response raises, check each contains all six elements:
trigger, consequence/invariant, prevention, behavioral oracle, recovery, falsifiable acceptance.
Report `complete_chains` as `k/3`: the denominator is always 3 when the gold has a material
question, and a response that raises fewer than three material risks scores the missing ones as
incomplete. A chain whose oracle is "add tests", a green mock, a row change, no exception, or a
model-checker exit code is incomplete. When the gold has no material question, report `n/a`.

## 3. Decision quality (0–2 each, max 10)

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| mechanism | names symptoms only | names the mechanism for most material risks | every material risk has the concrete state/transition/seam that fails |
| oracle | inspection of rows/returns | at least one externally observable oracle | every material risk has an externally observable or relational oracle |
| recovery/control | none or "rollback" | recovery or bound stated | recovery/bound stated with the condition under which it stops or worsens the incident |
| acceptance | "add tests" | some injections named | injection, observation point, expected relation, and guardrail for the top risks |
| proportionality | template dump or misses the main risk | roughly proportional | length and question count match the prompt's actual risk; nothing generic |

For a case with no material question, mechanism, oracle, recovery/control, and acceptance are
`n/a`; score proportionality only (2 when the response answers the task without the protocol) and
report `total` as `n/a`. The aggregator excludes such cases from the decision-quality mean.

## 4. Coverage

For each `must_cover` item: hit / miss with a quote. For each `must_not` item: violated / clean,
with a quote either way.

## 5. Boundary safety

Flag any absolute misuse: TNR or rollback assumed for irreversible actions, mocks or simulators
promoted to release evidence, formal methods demanded by default, continuous production recovery
exercise demanded, knob deletion from a usage statistic alone, automation banned outright.

## 6. Provenance (only if the response cites research)

Check labels and denominators against the gold's attribution notes and `research-map.md` if
provided. Any wrong label, wrong denominator, or mechanism claimed for a metadata-only paper is a
critical error. If `research-map.md` was not provided, report `unverified` rather than pass.

## Output

One JSON object:

```json
{
  "case": "H5",
  "responses": {
    "A": {"selected": ["Q4","Q8"], "justified_fp": [{"q": "Q2", "quote": "..."}],
          "complete_chains": "3/3",
          "decision": {"mechanism": 2, "oracle": 2, "recovery_control": 1, "acceptance": 2, "proportionality": 2, "total": 9},
          "must_cover": {"hit": ["..."], "miss": ["..."]},
          "must_not_violated": [], "must_not_clean": ["..."],
          "boundary_flags": [],
          "provenance": "clean | unverified | error: ...",
          "words": 850}
  },
  "preference": "A|B|tie",
  "reason": "one sentence"
}
```
