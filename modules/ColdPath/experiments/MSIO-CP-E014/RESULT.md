# MSIO-CP-E014 result

## Established observation

The frozen natural-warm-state run completed 18/18 valid trials (six per mode) on the isolated g130 V100S/Qwen2.5-0.5B setup. The hash-pinned analyzer returned `PASS`: robust CV was 0.0403 for `mmap`, 0.1280 for `none`, and 0.0483 for `dio`, all within the prespecified 0.15 threshold.

## Decision

**PASS for measurement qualification only.** This establishes that the three paths can be measured under the frozen bounded setup. It does not establish an optimization gain, a cross-workload ranking, cold-start behavior, or generalization. The next gate must use the 18 valid receipts to freeze an effect-size/uncertainty decision before any controller claim.

## Evidence boundary

Raw receipts, logs, and checksum manifest remain outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E014/`. The checked-in compact result is a derived artifact only.
