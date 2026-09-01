# Q2 — Authority, partial histories, and provenance

Principles: P2, P12. Default provenance: `XU-SYNTHESIS` from `xu-064`, `xu-054`, `xu-076`,
`xu-028`, `xu-030`, `xu-080`, `xu-070`, `xu-059`, `xu-043`, `xu-010`.

## Guideline

For every decision, distinguish authoritative state from caches, replicas, events, polls, logs,
models, and checkpoints. State whether each derived view can be stale, omit/coalesce a transient,
replay, reorder, move backward after restart/source-switch, or reuse a name for a new object.

- Prefer level predicates over “event X was observed once.”
- Pair stable identity with generation/epoch for destructive or irreversible actions.
- Recheck authority at the last responsible moment; fence stale writers/readers.
- Record actor/intent, desired and effective state, version/generation, transition phase, dependency
  outcomes, and a redacted behavioral result.
- Preserve a healthy comparator or relational evidence when absolute thresholds cannot separate
  workload effects from defects.

## Worked example

A deletion controller receives a replayed `Deleted(name=X)` event after X has been recreated. It
keys work by `(object_id, generation)`, rechecks current ownership before deleting storage, and
records the source event, authority read, decision, and resulting external behavior. The old event
cannot reach the new generation.

## Acceptance

- delay, omit, coalesce, reorder, and replay observations;
- restart the observer from an old checkpoint and switch it between sources;
- delete and recreate the same human-readable name;
- race a stale decision with a fresh authoritative update;
- show no destructive action crosses a generation fence;
- reproduce a diagnosis using effective config/version plus a healthy/bad relational comparison.

Failure signal: correctness depends on seeing every transition, or incident evidence records only
symptoms without enough state identity and provenance to distinguish competing causes.
