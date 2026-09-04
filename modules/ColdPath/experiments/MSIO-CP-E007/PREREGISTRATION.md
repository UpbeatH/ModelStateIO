# MSIO-CP-E007 warm-state measurement qualification

Frozen: 2026-09-04. Execution authorized by the user.

## Question

Is process-start-to-first-exact-`OK` measurable with sufficient repeatability to justify a later loading-path study for the verified `mmap`, `none`, and `dio` modes?

This gate evaluates the measurement contract, not which loading mode is better. The model is already naturally warm in the host page cache. No cold-cache claim is allowed, and no global cache eviction is permitted.

## Frozen design

- Host/write boundary: `g130-chenhao`; only `/mnt/nvme1/chenhao/modelstateio-runtime/` may be written.
- Binary and model identities are the E006-verified SHA-256 values.
- Six three-arm blocks, one observation per mode per block, with fixed counterbalanced order:
  1. `mmap, none, dio`
  2. `none, dio, mmap`
  3. `dio, mmap, none`
  4. `mmap, dio, none`
  5. `dio, none, mmap`
  6. `none, mmap, dio`
- Common invocation is identical to E006 except for `--load-mode`. A Python wrapper observes monotonic process start, the first complete stdout line exactly equal to `OK`, and normal process exit. Each trial has a 120-second timeout, 1 MiB stdout/stderr cap, deterministic prompt/token settings, no stdin, and a two-second inter-trial quiet period.
- Primary qualification metric: `time_to_ok_s`. Secondary diagnostic metric: `time_to_exit_s`. Program-reported token rates are ignored.
- Raw stdout/stderr and per-trial receipts remain outside Git. Only the frozen protocol, code, and compact aggregate may enter Git.

## Admission and correctness

- Require no E007 lock or owned `llama-cli`, GPU memory at most 16 MiB, at least 2 GiB free NVMe, matching binary/model hashes, private CUDA 11.6 loader resolution, and Python 3.
- Every trial must exit 0, contain exactly one `OK` line and `Exiting...`, remain below output caps, and leave no residual `llama-cli`.
- Any timeout, cap violation, wrong output, input/loader mismatch, GPU contention, or residual process stops the experiment. Do not retry E007.

## Prospective analysis and decision

- For each mode, compute the median `time_to_ok_s`, median absolute deviation (MAD), and robust coefficient of variation `1.4826 * MAD / median` across six observations.
- Measurement PASS requires 18/18 valid trials and robust CV at most 0.15 for every mode. No trial exclusion, threshold adjustment, or automatic repetition is permitted.
- PASS authorizes design of a separate, cold/warm-aware loading-path comparison. No-Go means first redesign the instrumentation or state-control method.
- Arm medians and ratios are exploratory diagnostics only: the naturally warm state, one small model, one host, and qualification purpose prohibit a performance or optimizer claim.

