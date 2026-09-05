# MSIO-CA-E000M1R2 result

## Established observations

The clean single-writer download from the official pinned resolver's CDN
completed at the new R2 path. The file was exactly 1,117,320,736 bytes and its
SHA-256 was
`6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`.
It was then renamed within the same `incoming/` directory to
`qwen2.5-1.5b-instruct-q4_k_m.gguf`; owner `chenhao`, group `chenhao`, mode
`664`, size and digest were verified again. Postflight reported 0 MiB GPU use
and no task model process.

## Decision

**PASS for one new provenance-complete full-model artifact.** Source is the
official Qwen repository at frozen revision
`a615a81362316d7b9f5a7a9c4313adfdf9b54588`, which declares Apache-2.0. This
is acquisition evidence only; loadability and performance remain untested.

