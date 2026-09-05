# MSIO-CA-E000M2 result

## Established observations

The exact pinned official-CDN object was downloaded from byte zero into the
new temporary path. It was 1,055,609,536 bytes with SHA-256
`decd2598bc2c8ed08c19adc3c8fdd461ee19ed5708679d1c54ef54a5a30d4f33`.
After the mandatory checks it was renamed within `incoming/` to
`smollm2-1.7b-instruct-q4_k_m.gguf`; owner `chenhao`, group `chenhao`, mode
`664`, size and digest passed again. Postflight GPU use was 0 MiB.

## Decision

**PASS.** The artifact is an independent model family from the official
HuggingFaceTB repository at revision
`2d4a76a30b4af41ecd395c35725ac11688d4cfe4`, which declares Apache-2.0.
Together with the provenance-complete Qwen 0.5B and Qwen 1.5B files, E000 now
has three full-model states and at least two materially different footprints.
The older 7B artifact remains excluded from this count because its local
acquisition receipt is incomplete.

No model was launched; this is material identity evidence only.

