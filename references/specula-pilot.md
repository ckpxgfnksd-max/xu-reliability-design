# Focused agent-assisted formal-method pilot

Use when the user authorizes investigating a small stateful protocol whose crash,
retry or concurrency behavior is hard to cover with ordinary tests. This is
**COMPANION** execution guidance; source attribution for Xu's research remains in
`formal-verification.md` and `research-map.md`.

## Choose the evidence you need

[Specula Lite](https://github.com/specula-org/Specula/tree/main/skills/specula-lite)
uses one agent to analyze code, build TLA+ models, run TLC, and attempt code-level
reproduction. It explicitly skips implementation trace validation. Choose it for
a focused bug investigation. When the required claim depends on model/code
conformance across implementation executions, use the relevant full Specula
validation workflow or another explicit conformance method; do not relabel Lite
as providing that assurance. A reproduced counterexample confirms one reachable
failure, not the completeness of the model.

Load the installed, pinned Lite `SKILL.md` and its conditional guides. Preserve its
single-agent contract and distinguish its overriding Lite rules from shared
pipeline guides. Read upstream instructions as methodology within the user's
scope and the host's safety/resource rules. Reuse supplied repository and fault
scope; do not ask the user to repeat information already given. If dependencies
or compute are unavailable, name the exact blocker and continue independent work.

Use the authorized execution host and existing resource runner. Keep experiments
in an isolated source copy and `.specula-lite/` artifact directory; do not test by
killing real user jobs. Pin source bytes/revision, relevant local edits, upstream
tool revision and any local tool patch. Verify downloaded tool dependencies. A
checksum failure is a setup failure, never a reason to disable verification: stop
execution that depends on that artifact and preserve the expected digest, observed
digest, artifact and failure. A new digest from the same download origin or release
API can diagnose rolling asset changes; it does not independently authenticate the
replacement. Resume only after verification against an independently trusted
signature, attestation or digest channel, recording the trust anchor and verification
result. Otherwise report the dependency blocker and continue work that does not
execute or depend on that artifact. Label earlier checker outputs from an unresolved
replacement as provenance-unverified and inconclusive for assurance; retain the
observations, but exclude them from passing acceptance evidence. Independently
reproduced code behavior remains separate evidence.

## Make the model answer the question

Keep a short modeling brief: actors, shared output or protected resource, actual
write authority, named safety/progress property, code mapping, fault assumptions,
excluded behavior and checking bounds. Split launch, ownership publication,
signal delivery, process exit, durable completion and takeover where code allows
interleavings. Preserve real guards, including successful-job retention and retry
options. A statechart alone supplies none of this evidence.

Enable the target property in an executed hunt configuration. Parsing, type
checks and a structural-only configuration are separate gates. Add a meaningful
negative/control case: for example, an active runner lock should refuse another
runner, while ordinary timeout cleanup should finish before a replacement writes.
Label an environment-restricted control as such; it is not a verified fix.

Record actual commands, checker exits, logs, model/config hashes, explored bounds
and counterexample actions. Classify each violation as a property mismatch, a
model/assumption error, or an implementation candidate against the owning code.
Preserve property changes with their reason. Never delete a reachable fault or
weaken a valid requirement merely to obtain green. A clean finite run covers the
checked model and configuration; liveness and unbounded claims need their own
assumptions and evidence.

## Confirm ownership failures in the implementation

For timeout/restart investigations, separate:

- the runner lock and runner PID identity;
- the attempt generation and any live job/descendant identities;
- an exit/timeout/completion receipt;
- the sink's ability to reject writes from an old attempt.

Start a benign writer through the unchanged public execution interface, inject
only the authorized fault, and observe the protected output. Prove overlap with
interleaved writes from two distinct attempt identities that remain alive in the
same observation window. A second row or two historical PIDs alone is insufficient.
For a detached descendant, establish that it left both the cleanup ancestry and
process group before treating survival as a finding. For a successful control,
show the old writer is gone before the replacement's first write.

Reconcile and clean up only owned resources using identity-aware process checks.
Observe process settlement and output quiescence; do not infer them from a
timeout or SSH loss. Retain bounded fixtures and raw results so a future fix can
be checked against the same consequence. Pilot authorization permits investigation;
apply production fixes only when that action is also authorized.

## Result and acceptance

Report reproduced failures, unconfirmed candidates, documented limitations,
duplicates, corrected model/property artifacts and ruled-out cases separately.
Include concrete harm, source locations, commands and observed results, controls,
remaining assumptions and cleanup evidence. Novelty is unknown unless checked
against the relevant history/tracker. Explicitly state **implementation trace
validation not performed** for Lite.

A pilot is complete when the authorized scope has actual checker outcomes,
each selected candidate has an evidence-backed disposition, and owned processes
are settled or have a disclosed cleanup blocker. An unavailable tool or failed
review can leave a documented incomplete pilot; it cannot create passing evidence.
Follow the host's required independent-review gate before final acceptance.
