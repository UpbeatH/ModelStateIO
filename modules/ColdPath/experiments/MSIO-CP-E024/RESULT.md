# MSIO-CP-E024 result

## Established observations

All 27 preregistered trials exited zero, emitted exactly one `OK`, and left no
`llama-cli` process or CUDA allocation. The raw receipt set is
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E024/receipts.json`,
SHA-256 `30311c8ee6e69615092dc2d791aac090cbab5dc9b65976ed21a0d9564c10f409`.
Median 75%-prefix preparation duration was 0.300 s in this run.

The guarded policy abstained in all three insufficient-known trials
(announcement 0.6 s), and triggered in all six 1.1-s announcement trials.
All six triggered guarded trials had 75.0% observed residency and an inactive
worker at actual arrival. Thus the intended early-arrival-error case (1.1 s
announced, 0.6 s actual) still completed preparation on this run; it did not
exercise concurrent arrival. This is an observation, not evidence that future
prediction error is harmless.

## Request-visible contrasts

The median paired guarded-minus-none arrival-to-OK contrasts were +0.181 s
for insufficient-known, -0.196 s for early-arrival error, and +0.036 s for
accurate-sufficient (three pairs per case). The accurate-sufficient directional
replication therefore did not pass: only one of three paired contrasts was
negative. Fixed75-minus-none medians were -0.028, -0.065 and -0.020 s,
respectively. These small three-pair summaries are descriptive only.

## Decision

**PASS (technical policy observability); NO-GO (performance confirmation).**
The frozen controller used only announced lead, made the expected abstain/
trigger decisions, and exposed state at arrival. But E024 neither produced a
concurrent error realization nor replicated a material completed-preparation
benefit in the three accurate-sufficient pairs. It cannot support a robust
lead-time controller claim, a prediction-error robustness claim, or a
performance claim. E024 is closed and will not be rerun.
