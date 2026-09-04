# MSIO-CP-E009 warm-state repeated measurement gate

Frozen: 2026-09-04. Execution authorized by the user.

## Question and boundary

Can the qualified `mmap`, `none`, and `dio` modes produce 18 complete warm-state observations under an instrumented cleanup contract? This is measurement qualification only: no cold-cache claim, global cache eviction, or performance ranking is allowed.

## Frozen design

- Host/write boundary: `g130-chenhao`; only `/mnt/nvme1/chenhao/modelstateio-runtime/` may be written.
- Recheck E006 binary/model hashes and exact hashes of the reused E007 measurement/analyzer scripts.
- Six counterbalanced blocks: `mmap,none,dio`; `none,dio,mmap`; `dio,mmap,none`; `mmap,dio,none`; `dio,none,mmap`; `none,mmap,dio`.
- Record process-start to first exact `OK`, exit status, output sizes, correctness, and structured before/after PID-command-GPU guard receipts. After each trial allow at most three one-second cleanup snapshots.
- PASS requires 18/18 valid trials and robust CV `1.4826*MAD/median <= 0.15` for each mode. Any timeout, wrong output, hash/loader mismatch, residual process after settle, or missing sample is No-Go; never retry this ID.

## Evidence boundary

All observations are naturally warm on one host and one model. They cannot establish a mode ranking, optimizer benefit, or systems-performance claim.

