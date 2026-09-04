# MSIO-CP-E007 result

## Decision

Technical **NO-GO**. E007 stopped prospectively after 11 of 18 planned trials and must not be resumed or filled in under the same experiment ID.

## Established observations

- The preserved schedule contains four complete blocks through `b4-p2-dio`; `b4-p3-none` was never appended or started. Counts are `mmap=4`, `none=3`, and `dio=4`.
- All 11 completed trials individually satisfy the frozen correctness contract: exit 0, exactly one `OK`, `Exiting...`, 1,009-byte stdout, empty stderr, and no trial-reported failure.
- The last completed receipt, `b4-p2-dio`, records `time_to_ok_s=2.579336055` and `time_to_exit_s=3.08630317`, with exit 0 and correct output.
- After the stop, the E007 lock was absent, no `llama-cli` remained, and the GPU reported 0 MiB and 1% utilization.
- The deterministic partial analyzer returned `NO_GO`, 11/18 valid trials, and refused to calculate the preregistered six-observation per-mode statistics. The Git-external remote compact artifact has SHA-256 `41102113f570fbf4d322d59260c2c9f90666ff4956eac18fc4be27d183018c07`; the checked-in JSON is its normalized compact content.

## Failure localization and uncertainty

The runner stopped after writing the valid `b4-p2-dio` receipt and before appending the next schedule row. In the frozen script, the only substantive check at that boundary is the post-trial owned-process guard, followed by a fixed sleep. The empty driver log does not identify the exact failing command. A transient residual-process observation is therefore a plausible inference, not an established fact.

This missing stop-reason receipt is itself an instrumentation defect. No observation may be excluded and the remaining seven trials may not be appended post hoc.

## Evidence boundary and next gate

The 11 valid samples show that the monotonic first-`OK` wrapper can produce bounded observations, but they do not meet the planned sample count and cannot qualify measurement stability or compare modes. The next gate must first make every admission/post-trial failure self-identifying, capture the matching process snapshot, and define a bounded cleanup-settle policy before any new repeated measurement ID is considered.

Raw receipts, stdout/stderr, schedule, loader and GPU records remain outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E007/`. No g129, PFS/Lustre, system CUDA, driver, service, cache, or global setting was modified.
