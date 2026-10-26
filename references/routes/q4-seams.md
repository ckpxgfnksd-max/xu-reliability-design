# Q4 — Interaction contracts and semantics-aligned placement

Principles: P4, P13. Default provenance: `XU-SYNTHESIS`; anchors CSI failures `xu-046`, Rainmaker
`xu-047`, OAT `xu-009`, Kscaler `xu-014`, Oxbow `xu-007`.

## Guideline

Inventory every data-, management-, and control-plane seam. For each, record:

- contract owner and the layer holding semantic ground truth;
- deployed version/configuration pair;
- units, nulls, ordering, serialization, error and partial-success semantics;
- hidden operation preconditions, capacity assumptions, and serialization rules;
- timeout, retry, duplication, late success, staleness, and recovery behavior;
- ownership of shared metadata, journaling, invalidation, and coherence.

Place observation and enforcement at the layer that owns the needed state. When responsibility is
split, state the coordination invariant and avoid duplicated authority. Heterogeneous ownership is
a conditional architecture pattern, not a universal rule. A fast path/reference path pair needs a
semantic differential oracle.

## Worked example

An object-store connector's management contract covers success after client timeout, duplicate
requests, throttling, stale reads, and regional capacity. Contract tests use the deployed client and
service versions plus a fault-capable double calibrated against the real service. The idempotency
authority sits where the remote operation's commit state is knowable, not in a caller cache.

## Acceptance

- run the deployed version/configuration pair rather than defaults in isolation;
- inject schema/unit/null drift and wrong-but-valid responses;
- delay success past caller timeout and duplicate the operation;
- violate each discovered precondition and require an explicit owned error;
- compare fast and reference paths on the same semantic input;
- crash at the split-ownership journal boundary and verify the coordination invariant.

Failure signal: both components pass alone while the assembled pair silently rounds, duplicates,
loses, or accepts an operation whose hidden precondition is false.
