# MSIO-KVG-E001 server state round-trip capability gate

## Purpose

Build the already-configured `llama-server` target only inside the isolated
g130 ModelStateIO build tree, then establish one owned KV-slot save/restore
round trip. This is a capability gate, not a policy or performance experiment.

## Frozen scope

- Source/build root: `/mnt/nvme1/chenhao/modelstateio-runtime` only.
- Model: the existing SHA-pinned 0.5B GGUF; no model download.
- Server binds loopback only and writes slot state and raw receipts only below
  `logs/MSIO-KVG-E001/`.
- One deterministic initial request is placed in slot 1, saved, restored into
  slot 0, then the same deterministic continuation is issued on both slots.
- All responses must exit successfully; saved/restored token and byte counts
  must be positive; continuation contents must match; cleanup must leave no
  server process or GPU allocation.

## Stop conditions

Stop without repair or retry on build failure, missing endpoint, malformed
JSON, nonpositive state record, response mismatch, timeout or cleanup failure.
No comparison, pressure injection, cache eviction, system setting, global
path, installation or deletion is permitted.
