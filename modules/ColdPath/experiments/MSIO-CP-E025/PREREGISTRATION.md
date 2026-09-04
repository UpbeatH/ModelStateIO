# MSIO-CP-E025 adversarial early-arrival concurrency gate

Status: frozen before execution. Date: 2026-09-05.

## Question

When a 1.1-second announced preparation opportunity is wrong and the request
arrives after only 0.1 second, is the qualified 75%-prefix preparation still
concurrent at arrival, and does it impose foreground harm versus no preparation?

## Frozen protocol

The action sees only the 1.1-second announcement and always triggers the
75%-prefix sequential read. The true 0.1-second arrival is hidden from it and
is below E024's 0.300-second median preparation duration. Six AB/BA paired
blocks (12 trials) compare `none` and `fixed75`. Every trial uses file-scoped
`POSIX_FADV_DONTNEED`, two-second settling and at most 20% residency. Model,
binary, command, exact-OK condition, timeout and cleanup are hash-pinned to
E024. No global cache action, download, installation, retry or expansion.

## Decision

Record leads, worker state, bytes/residency at arrival, worker duration,
arrival-to-OK, trigger-to-OK, correctness and cleanup. Technical concurrency
passes only if all trials are correct/clean and all six fixed75 workers are
active with less than 70% residency at arrival. The paired latency contrast is
descriptive only: this is not robust control or general performance evidence.
