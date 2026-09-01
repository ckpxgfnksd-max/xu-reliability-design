# xu-reliability-design

An evidence-backed agent skill for reliability and system-design reviews, synthesized from Tianyin Xu's 97-entry publication inventory.

The skill turns recurring findings across configuration, controllers, distributed state, recovery, fault injection, observability, formal methods, and production evidence into reusable design principles. It is intended for architecture reviews, design proposals, failure analysis, control-plane reviews, and reliability acceptance criteria.

## What is included

- `SKILL.md` — compact entry point and task router.
- `references/principles.md` — 14 corpus-wide principles. Every principle includes a guideline, acceptance criterion, example, counterexample, and full-text evidence anchors.
- `references/routes/` — seven task-specific routes covering intent, state, change, seams, correctness, control, and evidence.
- `references/checklists.md` — review and acceptance checklists.
- `references/examples.md` — worked design-review examples.
- `references/formal-verification.md` — guidance for choosing specifications, model checking, testing, and runtime checks.
- `references/paper-ledger.md` — the 97-paper evidence ledger.
- `EVALS.md` — evaluation protocol, results, limitations, and the gate for future automated optimization.

## Research coverage

| Measure | Result |
|---|---:|
| Publication inventory | 97 unique entries |
| Full-text audited | 94 |
| Metadata-only because full text was unavailable | 3 |
| Direct system-design evidence | 54 |
| Adjacent evidence | 39 |
| No general design claim extracted | 4 |
| Synthesized principles | 14 |

The repository does **not** include paper PDFs. It contains original synthesis, structured citations, and links or bibliographic identifiers. Metadata-only papers are explicitly marked and are never used as unqualified direct evidence.

## The 14 principles

1. Make invalid or dangerous intent unrepresentable, rejectable, and repairable at the boundary.
2. Model observed state as partial, stale, and capable of moving backward.
3. Treat every change and operation as a crashable, resumable state transition.
4. Make interactions and management semantics explicit contracts.
5. Judge correctness by end-to-end behavior and relational oracles.
6. Put adaptive control inside an explicit safety envelope.
7. Design for silent, slow, latent, and propagating faults—not only crashes.
8. Exercise recovery and rare paths at a risk-calibrated cadence, realism, and radius.
9. Minimize the control surface and make feedback usable.
10. Treat recovery as a controlled workflow that must not worsen the incident.
11. Include progress, stability, and model–implementation conformance in correctness.
12. Preserve evidence, provenance, and counterfactuals as system features.
13. Place observation and enforcement where semantic ground truth lives.
14. Calibrate design assumptions with real distributions and deployment relationships.

## Install

Clone the repository into the skill directory used by your agent environment:

```bash
git clone https://github.com/ckpxgfnksd-max/xu-reliability-design.git path/to/skills/xu-reliability-design
```

The folder must remain intact so that `SKILL.md` can route to the supporting references.

## Use

Invoke it explicitly when reviewing a system, design document, incident, or reliability proposal:

```text
Use $xu-reliability-design to review this controller design. Identify violated principles,
required evidence, failure scenarios, and testable acceptance criteria.
```

The skill distinguishes three attribution levels:

- `XU-DIRECT` — explicitly supported by a cited Xu-coauthored paper.
- `XU-SYNTHESIS` — a cross-paper abstraction supported by multiple Xu-coauthored papers.
- `COMPANION` — useful external practice, not evidence about Xu's research program.

## Validation status

- Package and frontmatter validation: pass.
- Independent release review: GO.
- Attribution probe: 5/5 after preserving and correcting the original 4/5 failure case.
- Automated optimization: intentionally not started; a protocol-compliant per-case routed baseline has not yet been certified.

See [EVALS.md](EVALS.md) for the complete evaluation protocol and limitations.

## Attribution

This is an independent synthesis of publicly described research. It is not authored, endorsed, or maintained by Tianyin Xu or his coauthors. Cite the original papers for research claims; use the ledger to locate the relevant source.

## License

MIT. The license applies to this repository's original skill text and supporting artifacts, not to the cited papers or third-party materials.
