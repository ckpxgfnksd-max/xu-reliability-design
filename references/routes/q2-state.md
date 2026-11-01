# Q2 — Authority and partial histories

Principle: P2. Default provenance: `XU-SYNTHESIS`; anchors Partial Histories `xu-064`, Sieve
`xu-054`, Concord `xu-028`, MVNO authority study `xu-080`.

## Guideline

For every decision, name the authoritative state and each derived view the decision actually reads:
caches, replicas, event streams, polls, checkpoints, logs, models. For each view, state whether it
can be stale, omit or coalesce a transient, replay, reorder, move backward after a restart or source
switch, or reuse a name for a new object.

- Prefer level predicates over "event X was observed once."
- Pair stable identity with a generation or epoch for any destructive or irreversible action.
- Recheck authority at the last responsible moment; fence stale writers and readers.
- Where two non-controller writers can target one object (old and new binary, overlapping job
  runs), name the fence and which write wins; "atomically stored" says nothing about either.
  Controllers, tools, and operator overrides sharing an actuator are arbitrated under Q6.
- For job recovery, distinguish a runner lock from writer authority: identify surviving job
  processes and detached descendants before replacement. A runner exit, timeout marker, or
  recorded generation is insufficient unless old writes are stopped or rejected by the sink.
- Treat an incoming event or request as possibly duplicated, late, or reordered unless the design
  proves otherwise.

## Worked example

A deletion controller receives a replayed `Deleted(name=X)` event after X has been recreated. It
keys work by `(object_id, generation)` and rechecks current ownership before deleting storage. The
old event cannot reach the new generation.

## Acceptance

- delay, omit, coalesce, reorder, and replay observations;
- restart the observer from an old checkpoint and switch it between sources;
- delete and recreate the same human-readable name while an old action is queued;
- race a stale decision with a fresh authoritative update and with a second writer;
- show that no destructive action crosses a generation fence.
- reach the same declared intent through different histories and compare normalized end state plus
  external behavior.

Failure signal: correctness depends on seeing every transition, on an event arriving exactly once,
or on a value that two writers can set without either learning that it lost.
