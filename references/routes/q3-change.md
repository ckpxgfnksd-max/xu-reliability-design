# Q3 — Crashable change and controlled recovery

Principles: P3, P10. Default provenance: `XU-SYNTHESIS` from `xu-054`, `xu-038`, `xu-009`,
`xu-012`, `xu-019`, `xu-028`, `xu-030`, `xu-007`, `xu-006`, `xu-072`, `xu-075`, `xu-083`.

## Guideline

Represent each multi-effect mutation, migration, failover, mitigation, rollback, or credential
rotation as a durable state machine:

1. preconditions and invariants;
2. committed effect and idempotency identity;
3. externally meaningful intermediate states;
4. durable progress and resume rule after every prefix;
5. late-success resolution after caller timeout;
6. abort, compensation, or last-known-good restore;
7. externally visible postcondition oracle;
8. emergency path that is not queued behind the wedged normal operation.

For automated remediation, use Transactional No-Regression only where states have a declared health
ordering and effects are reversible/compensatable. Incomparable or irreversible actions require a
smaller radius, sandbox/canary, or approval—not a fictional rollback guarantee.

## Worked example

Credential rotation persists phases: create generation N+1, prove real authentication, move one
reader cohort, expand, revoke N, then garbage-collect. A timeout is reconciled against authority
before retry. Restart from any prefix advances safely or returns to the last-known-good generation;
revocation is not allowed until every required reader has demonstrated N+1 behavior.

## Acceptance

- interrupt after each externally visible effect, restart, and compare normalized final behavior;
- duplicate every request and return success after the caller timeout;
- race forward action, retry, and rollback;
- wedge the normal queue and invoke the emergency recovery path;
- inject failure into recovery itself and prove durable resume;
- for TNR, show the exact health vector, comparison rule, undo bound, and stop condition.

Failure signal: “rerun the reverse script,” process exit, or a database phase flag is the only
evidence of recovery correctness.
