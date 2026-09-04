# MSIO-CP-E009R1 result

## Decision

Statistical **NO-GO** for measurement qualification. The ID is closed and must not be rerun.

## Established observation

- All 18 planned trials completed correctly: six each for `mmap`, `none`, and `dio`; every trial exited 0, emitted exactly one `OK` and `Exiting...`, and stayed within the output bound.
- The exact-executable process guard did not self-match the SSH command. Every cleanup check settled, and the final state had no lock, no `llama-cli`, and 0 MiB GPU use.
- Robust CV of `time_to_ok_s` was 0.1030 (`mmap`), 0.1601 (`none`), and 0.0483 (`dio`). Because `none` exceeds the preregistered 0.15 threshold, the qualification decision is No-Go.

## Record-integrity note

The reused analyzer wrote `experiment: MSIO-CP-E007` in its remote compact artifact; this is a provenance-label defect, not a change to the 18 receipts or their values. The checked-in compact result normalizes the ID to E009R1 while retaining the remote values. The next gate must pin an analyzer that derives the experiment ID from its output path or an explicit argument.

## Evidence boundary and next gate

The complete run shows the measurement wrapper is operational, but warm-state variability for `none` does not meet the frozen stability criterion. These values are not a mode-performance claim and do not justify selecting a winner. A new local/remote gate must first correct analyzer identity handling and decide whether the threshold should remain fixed or whether an explicit state-control mechanism is needed; no post hoc threshold change is allowed.

Raw receipts, logs, schedule, analyzer output and checksums remain outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E009R1/`.

