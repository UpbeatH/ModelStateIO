# MSIO-ST-T002 result

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Observations

- `/api/ps` before the first request returned `{"models":[]}`.
- The first short `/api/generate` request returned `Storage` and reported
  `total_duration` 4.806 s and `load_duration` 4.748 s.
- With `keep_alive:"5m"`, `/api/ps` reported `qwen2.5:7b`, model size
  8,210,446,336 bytes, `size_vram` 8,210,446,336 bytes, and context length
  32,768.
- The second request returned `OK` in 0.213 s with `load_duration` 0.175 s.
- The API exposes model residency and token context arrays, but no actual KV
  byte size, residency tier, eviction, migration, or per-state deadline.

## Decision

`PARTIAL`. This is real model-plus-context lifecycle evidence and confirms an
API path for future instrumentation. It does not test the StateTier necessity
hypothesis because a second independently controllable state class is not
observable through the supported interface.

## Next gate

Stop expanding the Ollama-only route. Either obtain an approved runtime that
exposes KV/adapter residency events, or re-scope StateTier to cold/warm model
weight residency and explicitly drop the unified multi-state claim.

