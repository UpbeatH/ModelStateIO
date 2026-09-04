# MSIO-CP-E006 result

## Established observation

- E006 passed once on 2026-09-04 on the isolated g130 runtime. The `mmap`, `none`, and `dio` arms all exited `0`, emitted one exact `OK` line followed by `Exiting...`, and produced 1,009-byte stdout plus empty stderr.
- The three model-path open traces were bounded to 504, 504, and 513 bytes. `mmap` and `none` opened the verified model with `O_RDONLY`; the `dio` trace additionally records an `O_RDONLY|O_DIRECT` open of that same path.
- The runner rechecked the frozen binary SHA-256 `39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24` and model SHA-256 `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db` before execution.
- GPU receipts immediately before and after the three-arm sequence both report 0 MiB and 1% utilization. The completion sentinel exists, the E006 lock was released, and no residual `llama-cli` process was found.

## Inference and boundary

For this binary, model, ext4/NVMe path, and host, three documented load-mode contracts are executable with identical smoke correctness, and `dio` reaches an actual `O_DIRECT` file open. This supersedes E002's runtime-specific claim that the then-current platform exposed no supported second path.

This is not evidence that any mode is faster, more efficient, or preferable. The fixed single-pass order, warm page-cache state, `strace` instrumentation, and absence of repeated trials prohibit a performance comparison. No timing or token-rate value from this gate is a research result.

Raw stdout/stderr, open traces, loader receipt, GPU samples, input hashes, and receipt hashes remain outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E006/`. No model, raw log, trace, checkpoint, or system/PFS setting is committed or modified.

## Decision

The next candidate gate is a prospective measurement-qualification experiment: freeze one readiness definition, separately treat naturally warm and explicitly cold-compatible states without global cache eviction, randomize/counterbalance mode order, repeat sufficiently to estimate variability, and preserve correctness/resource receipts. It must first prove that the measurement is stable enough to justify a larger path-selection study.

