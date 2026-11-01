# Q3 — Crashable change and controlled recovery

Principles: P3, P10. Default provenance: `XU-SYNTHESIS`; anchors Sieve `xu-054`, Acto `xu-038`,
Stratus `xu-012`, Maelstrom `xu-083`, Mux `xu-019`.

## Guideline

Represent each multi-effect mutation, migration, backfill, failover, mitigation, rollback, restore,
or credential rotation as a durable state machine:

1. preconditions and invariants;
2. committed effect and idempotency identity;
3. externally meaningful intermediate states;
4. durable progress and resume rule after every prefix;
5. late-success resolution after caller timeout;
6. abort, compensation, or last-known-good restore;
7. externally visible postcondition oracle;
8. emergency path that is not queued behind the wedged normal operation;
9. for every intermediate and final state, which versions can still read and write it: the old
   binary after a killed installer, the mixed fleet during rollout, the new code against
   untransformed rows.

For automated remediation, use Transactional No-Regression only where states have a declared health
ordering and effects are reversible or compensatable. Incomparable or irreversible actions require a
smaller radius, sandbox or canary, or approval, not a fictional rollback guarantee. Redeploying old
code is not a rollback once state has been transformed; say what forward repair or dual-read/write
period replaces it.

## Worked example

Credential rotation persists phases: create generation N+1, prove real authentication, move one
reader cohort, expand, revoke N, then garbage-collect. A timeout is reconciled against authority
before retry. Restart from any prefix advances safely or returns to the last-known-good generation;
revocation is not allowed until every required reader has demonstrated N+1 behavior.

## Acceptance

- interrupt after each externally visible effect and restart: it must converge, compensate, or enter
  a named guarded terminal state; compare normalized final behavior;
- duplicate every request and return success after the caller timeout;
- race forward action, retry, and rollback;
- run the old version against the migrated state and the new version against the unmigrated state;
- wedge the normal queue and invoke the emergency recovery path;
- inject insufficient target capacity, an unhealthy dependency, stale recovery intent, executor
  crash, and undo failure into recovery itself, and prove durable resume;
- expand a recovery exercise from a safe slice; a health regression pauses or restores rather than
  continuing on a fixed schedule;
- run recovery often enough to expose runbook, dependency, permission, and capacity drift, and
  update the executable contracts with what it finds;
- for TNR, show the exact health vector, comparison rule, undo bound, and stop condition.

Failure signal: "rerun the reverse script", process exit, a database phase flag, or "redeploy the
old build" is the only evidence of recovery correctness.
