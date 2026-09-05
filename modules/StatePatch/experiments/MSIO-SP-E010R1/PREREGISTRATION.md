# MSIO-SP-E010R1 static lifecycle quoting correction

Only change from E010: pass the frozen prompt as one quoted argument. Keep
the same binary, E009 artifacts, `none -> seed-43 attached -> none-after`
order, seed 123, temperature zero, 12-token bound, per-arm timeout, and
CPU-only `-ngl 0`. Existing GPU users are not inspected beyond allocation and
must not be modified; the experiment claims no GPU resource.

PASS requires three zero-exit bounded outputs, matching base-only hashes,
a differing attached hash, and no residual llama process. It remains a static
new-process contract, not an in-process detach or performance result.
