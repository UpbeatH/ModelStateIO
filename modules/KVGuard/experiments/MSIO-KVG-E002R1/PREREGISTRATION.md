# MSIO-KVG-E002R1 cache-isolation correction

E002 closed because the server default RAM prompt cache contaminated fresh
recomputation. E002R1 changes only server launch to `--cache-ram 0`, retaining
the same model, prefixes, three repetitions, save/restore actions, slots,
response equality, byte accounting, run order and stop rules. A new ID is
required; no E002 measurement is reused. If short/long incremental persistence
does not reverse by the frozen threshold, KVGuard stops as a fixed-policy
problem.
