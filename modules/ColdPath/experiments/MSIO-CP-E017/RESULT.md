# MSIO-CP-E017 result

## Observation

On the exact 491,400,032-byte owned GGUF, `mincore` reported 119,971/119,971 pages resident before the action, 0/119,971 after file-scoped `POSIX_FADV_DONTNEED`, and 119,971/119,971 after bounded sequential prefetch.

## Decision

**PASS for user-scoped residency control.** The preregistered cold fraction was 0.0 and prefetch fraction was 1.0, exceeding the required ≤0.20 and ≥0.80 gates. No model or inference ran, and no global cache or system setting was modified.

This is controllability evidence only. E018 must measure both request-visible latency and prefetch cost before any optimization claim.

Raw output remains outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E017/`.
