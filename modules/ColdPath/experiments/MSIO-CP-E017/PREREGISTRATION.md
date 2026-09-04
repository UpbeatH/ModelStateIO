# MSIO-CP-E017 per-file residency control qualification

## Motivation and hypothesis

E016 closes static selection among `mmap`, `none`, and `dio`: paired effects were directionally inconsistent. The new mechanism is **ResidencyShaper**, a user-scoped preparation layer that controls and reads back residency of the owned GGUF before launch. The hypothesis for E017 is limited to controllability: file-scoped eviction followed by bounded sequential prefetch can produce measurably distinct cold and prefetched states without global cache control.

## Frozen scope

- Host: g130; exact owned model path and SHA-256 used by E014.
- No model, GPU, inference, root command, `/proc/sys` write, global `drop_caches`, installation, or filesystem modification.
- Actions: `POSIX_FADV_DONTNEED` on the read-only model descriptor; then a complete sequential read using an 8 MiB buffer.
- Readback: Linux `mincore` over a read-only private mapping; report resident pages/bytes before, after file-scoped eviction, and after prefetch.
- Safety gates: exact model SHA, regular file, current-user ownership, no `llama-cli`, sufficient free RAM, 180-second bound, and output cap.

## Decision

PASS only if eviction reduces resident pages by at least 80% of total and sequential prefetch restores at least 80% residency, with no process/GPU residue. Otherwise NO-GO for this state-control mechanism. PASS is state-control evidence only, not latency or optimization evidence.
