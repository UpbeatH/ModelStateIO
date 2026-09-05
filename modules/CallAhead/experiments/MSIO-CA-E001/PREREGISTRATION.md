# MSIO-CA-E001 causal interference death gate

Status: frozen before implementation and execution. Date: 2026-09-05.

## Question and claim boundary

Does an eager, file-scoped preparation of a nonresident background model cause
repeatable p95 latency harm to a resident foreground model, and can a fixed
rate limit remove at least half that harm while retaining at least half of the
request-visible readiness benefit?

This gate tests only a causal affected set and one bounded pacing actuator. It
does not test program notice, prediction, routing or a CallAhead controller.

## Identities and arms

- Foreground service: hash-pinned Qwen2.5-0.5B-Instruct Q4_K_M on the existing
  isolated llama.cpp server, one GPU slot and loopback only.
- Background demand: hash-pinned Qwen2.5-1.5B-Instruct Q4_K_M.
- Prepared range: exactly 830,472,192 bytes (75%, rounded down to 8 MiB).
- `none`: read zero preparation bytes.
- `eager75`: read the range without an artificial rate limit.
- `paced75`: read the same range at a 256 MiB/s token-bucket ceiling.
- Each trial begins after file-scoped `POSIX_FADV_DONTNEED`, a two-second
  settle and `mincore` confirmation that background residency is at most 20%.
  Global cache clearing is forbidden.

The preparation/foreground window is four seconds. The foreground offered
load is exactly 160 sequential one-token requests with arrivals scheduled
25 ms apart. A delayed client sends overdue requests immediately; all 160 are
retained so queuing harm is not hidden. After the batch and preparation
complete, a bounded fresh one-token `llama-cli` invocation measures background
trigger-to-OK readiness while the foreground service remains resident but
idle. Preparation time and bytes are charged and never treated as free.

## Blocks and fixed order

Six counterbalanced blocks use these orders:

1. none, eager75, paced75
2. eager75, paced75, none
3. paced75, none, eager75
4. none, paced75, eager75
5. paced75, eager75, none
6. eager75, none, paced75

The block-trial is the analysis unit. Foreground trial p95 is the nearest-rank
95th percentile of all 160 latencies. No trial, request or block may be removed
for being slow. A timeout, identity/action mismatch, invalid response,
residency failure or residue is a visible gate failure.

## Receipts and bounds

Record hashes/sizes, exact commands, scheduled and actual request times,
latency/status/content presence, preparation bytes/time/rate and before/after
residency, background readiness wall time/return code, process CPU/RSS/fault
deltas, `/proc/meminfo`, GPU snapshots, nvme1n1 device-stat deltas, order,
correctness, timeouts and cleanup. Device statistics are host-level context,
not attributed causal bytes.

Server readiness timeout is 90 s; each HTTP request 30 s; each background
readiness probe 120 s; whole experiment 900 s. Raw responses and logs remain
outside Git. No installation, pressure workload, global cache, system/cgroup,
CUDA/driver/service, g129 or PFS/Lustre action is allowed.

## Confirmatory analysis

- Fixed request quantile: nearest-rank p95.
- Per-block eager relative harm: `(eager_p95 - none_p95) / none_p95`.
- Per-block pacing recovery: `(eager_p95 - paced_p95) /
  (eager_p95 - none_p95)` when the denominator is positive.
- Per-block readiness benefit of arm X: `none_ready_s - X_ready_s`.
- Preserved readiness fraction: median paced benefit / median eager benefit.
- Report the median across six paired blocks. For eager relative harm, use a
  20,000-resample paired block bootstrap with seed 20260905 and the percentile
  95% interval. No alternative endpoint or interval may replace it after data
  are opened.

## GO / NO-GO

GO only if every request/probe/action/cleanup check passes and all hold:

1. median eager relative p95 harm is at least 10%, and its fixed bootstrap
   interval excludes zero;
2. median pacing recovery is at least 50%; and
3. paced75 preserves at least 50% of eager75's median readiness benefit.

Otherwise the present CallAhead foreground-harm/pacing mechanism is **NO-GO**.
Do not add pressure, enlarge the model, change rate/window/load/thresholds or
increase repetitions after observing E001. A later re-entry requires direct
new evidence for a different mechanism, not tuning this death gate.
