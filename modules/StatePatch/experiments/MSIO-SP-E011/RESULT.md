# MSIO-SP-E011 result: static lifecycle text contract

## Decision

**Technical GO for the narrow static contract.** The extracted base-only texts
are byte-identical before and after the separate attached process; the
seed-43 attached text differs. All three commands exited zero and the recorded
GPU allocation was 0 MiB.

## Exact extracted texts

- Base-only (both arms): `Storage tuning involves optimizing the performance
  and efficiency of data storage systems`
- Seed-43 attached: `Storage tuning involves optimizing the performance and
  capacity of a storage system`

## Boundary

This proves only a new-process CLI attach and clean-restart disable contract.
It is not in-process attach/detach, adapter reuse, concurrent admission,
capacity, isolation, task-quality, I/O, total-cost, or performance evidence.
