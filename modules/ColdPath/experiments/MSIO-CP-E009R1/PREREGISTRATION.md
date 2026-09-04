# MSIO-CP-E009R1 guarded warm-state measurement

Frozen: 2026-09-04. New ID correcting only E009's self-matching process guard.

E009 stopped after 10 valid trials because `pgrep -f '[l]lama-cli'` matched the SSH inspection command containing that text. E009R1 preserves the same model, binary, prompt, modes, six counterbalanced blocks, 120-second trial bound, output/correctness checks, and robust-CV threshold, but all process guards use exact executable matching (`pgrep -x llama-cli -a`) and record structured before/after receipts. E009 remains closed and is not resumed.

PASS requires 18/18 valid trials, all cleanup guards settled, and robust CV <= 0.15 for each mode. No cache eviction or cold-state claim is permitted; this remains measurement qualification, not a performance claim.

