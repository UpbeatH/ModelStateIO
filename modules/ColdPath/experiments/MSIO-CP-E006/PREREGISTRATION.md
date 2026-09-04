# MSIO-CP-E006 load-mode realization gate

Frozen: 2026-09-04. Authorized by the user's instruction to continue the ModelStateIO line at five-minute checkpoints.

## Question and evidence boundary

Can the verified g130 `llama-cli` binary complete the same deterministic one-turn smoke under three documented loading modes (`mmap`, `none`, and `dio`), and does the `dio` arm expose direct-I/O open semantics? This is a path-realization qualification, not a latency or throughput comparison. Invocation duration and the program's displayed token rates are not research outcomes.

## Frozen contract

- Host/write boundary: `g130-chenhao`; only `/mnt/nvme1/chenhao/modelstateio-runtime/` may be written.
- Inputs: binary SHA-256 `39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24`; model SHA-256 `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
- Arms and order: `mmap`, `none`, then `dio`, once each. Order is fixed because no performance comparison is permitted.
- Common invocation: private CUDA 11.6 libraries; `--single-turn --simple-io --no-display-prompt --prompt 'Reply with exactly OK.' --predict 1 --seed 1 --temp 0 --n-gpu-layers 99 --ctx-size 256 --batch-size 64 --threads 4 --threads-batch 4`.
- Observation: `strace` records only `open/openat` calls involving the model path. Each arm has a 120-second timeout and 2 MiB limits for stdout, stderr, and trace output.
- No cache eviction, timing comparison, system write, installation, remount, raw-device access, or PFS action is allowed.

## Admission and decision rules

- Admit only if no E006 lock or owned `llama-cli` exists, GPU memory use is at most 16 MiB, free NVMe exceeds 2 GiB, the two input hashes match, CUDA libraries resolve from `/usr/local/cuda-11.6/lib64`, and `strace` supports path filtering.
- Per-arm correctness requires exit 0, one exact `OK` output line, `Exiting...`, bounded outputs, no interactive prompt loop, and no residual `llama-cli`.
- `dio` is realized only if its path-filtered trace includes the model path opened with `O_DIRECT`. The `mmap` and `none` arms must include a model-path open receipt and must not contain `O_DIRECT`.
- Overall PASS requires all three arms and cleanup checks to pass. Any failure is a technical No-Go; preserve evidence and do not retry the same ID.
- Even PASS establishes only three executable and distinguishable path contracts for this binary/filesystem/model combination. It cannot establish which path is faster or better.

