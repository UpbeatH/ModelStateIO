# MSIO-CP-E014 guarded performance-comparison protocol

## Question and scope

On one g130 V100S host and one Qwen2.5-0.5B GGUF, does the loading path (`mmap`, `none`, `dio`) change time-to-first-exact-OK under natural warm-state execution? This is a bounded single-host result, not a cold-start or universal claim.

## Frozen design

- 18 trials: six per mode, six counterbalanced blocks; fixed model/binary hashes from E012.
- Equal information, actions, and wall-clock budget across modes; no adaptive stopping or post-hoc exclusions.
- Primary metric: time-to-first-exact-OK. Secondary: exit code, stdout bytes, GPU memory, residual process/lock, and correctness.
- Before/after exact process guard (`pgrep -x llama-cli`), private CUDA 11.6 library, bounded timeout, stdout cap, and cleanup verification.
- Report median, robust CV, paired/block effect sizes, and uncertainty intervals; preserve every failure.

## Decision gates

Go only if all 18 trials are valid, no correctness or cleanup failure occurs, and the predeclared robust-CV threshold (0.15) is met for the compared condition. Otherwise record No-Go or Abstain and do not claim an optimization win.

## Execution boundary

This file freezes design only. Running E014 requires a separate explicit execution authorization and a fresh read-only host/GPU audit.
