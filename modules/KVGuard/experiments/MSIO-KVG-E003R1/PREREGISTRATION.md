# MSIO-KVG-E003R1 invocation-contract correction

E003R1 is a new experiment because E003 stopped in its first block: a
suffix-only request with prompt caching disabled was not semantically
equivalent after slot restore.

Only two call-contract changes are allowed. The restored slot receives the
same full prompt as fresh recomputation, and prompt alignment is enabled for
that slot. The runtime remains `--cache-ram 0`; a newly started and stopped
server process still isolates every block, so no prompt state can cross blocks.
All E003 contexts, three repetitions per class, RP/PR/RP arm orders, warm-up,
model hash, metrics, stop conditions and 10% sign-reversal threshold are
otherwise unchanged. E003 data are not reused.

This correction restores the documented slot-save/restore interaction. It
does not permit global cache reuse, threshold changes, additional samples, or
any claim beyond the original necessity gate.
