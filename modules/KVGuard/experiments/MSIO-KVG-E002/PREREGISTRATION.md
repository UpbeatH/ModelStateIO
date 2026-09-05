# MSIO-KVG-E002 persistence versus recomputation necessity gate

## Question

For a resumed request whose previous context was evicted from active slots,
does saving and restoring owned KV state beat recomputing the full context, and
does that relationship differ between short and long contexts once save/restore
time and state bytes are charged?

## Frozen protocol

Use the existing 0.5B model and loopback server only. For each of a short and
long deterministic text prefix, run three counterbalanced repetitions. Each
block measures: (1) a fresh-slot recomputation of prefix plus suffix and
(2) a fresh base slot, save, restore into a different slot, then the same
prefix-plus-suffix continuation. The common base creation is not charged to
either resumed-request arm; save and restore are charged to persistence.
Record HTTP wall time, server prompt-token count/timing, saved/restored bytes,
response equality, all state files and cleanup. No artificial memory pressure,
global cache action, retry or sample expansion.

## Decision

The gate passes only if all 12 resumed requests are correct/clean and the
saved/restored continuation is exactly equal to its fresh recomputation. It
reports, separately by context length, the paired incremental difference:
`save_ms + restore_ms + restored-continuation wall time` minus
`recomputed-continuation wall time`. It is a necessity signal only if the
sign changes between short and long prefixes by at least 10% of the relevant
recompute median. Otherwise a fixed policy is sufficient and KVGuard stops.
