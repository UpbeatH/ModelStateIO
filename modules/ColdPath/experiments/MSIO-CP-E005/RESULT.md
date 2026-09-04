# MSIO-CP-E005 result

## Established observation

- The one-shot non-interactive contract passed once on 2026-09-04 on the isolated `g130-chenhao` runtime. `smoke.exit` is `0`; the wrapper emitted `E005_PASS` and the completion sentinel exists.
- The runner rechecked the frozen binary SHA-256 `39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24` and staged Qwen2.5-0.5B Q4_K_M SHA-256 `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db` before invocation. Its CUDA loader receipt is recorded outside Git.
- The process used the frozen `--single-turn --simple-io` interface. Its stdout contains the predefined prompt, `OK`, and `Exiting...`; stdout is 1,009 bytes and stderr is 0 bytes, both below the 1 MiB ceiling. The raw-output SHA-256 is `21d00b2dd56dbf99aad71754224a1d994c5e837c5c398c06dbcbb70c1209eb6d`.
- GPU receipts show 0 MiB and 1% utilization immediately before and after; the E005 lock was removed and no residual `llama-cli` process was found after completion.

## Scope and limitation

This is a single technical interface/cleanup qualification. It establishes neither model-state I/O performance nor a loading-mode comparison, throughput/latency effect, optimizer benefit, or result reproducibility. The displayed prompt-rate line is program output and is not a preregistered performance metric.

Raw logs, loader receipt, GPU receipts, and checksums remain outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E005/`; the model remains at the separately isolated `incoming/` path. No PFS, Lustre, g129, system CUDA, driver, service, cache, or global path was modified.

## Decision

E005 closes the non-interactive CLI qualification defect identified by E004. Before any comparison, freeze a distinct, bounded loading-path measurement protocol with an equal-information/equal-runtime baseline, explicit repetitions, a cold/warm-state policy, correctness check, and a stop rule. It requires separate user authorization; do not automatically start it.
