# MSIO-ST-T005 same-model footprint qualification

Target `g127-chenhao`, existing Ollama `qwen2.5:7b`. This packet authorizes
only API requests; no downloads, installs, service/configuration writes, or
system parameter changes.

Run three counterbalanced pairs across `num_ctx=2048` and `num_ctx=8192`.
Each request uses `stream:false`, `num_predict:1`, a 30-second bound, and
`keep_alive` set to `0` for cold or `5m` for resident. Record API JSON,
`/api/ps`, exit code, timestamps, and hashes under the existing user-owned
external root. Stop on GPU contention, HTTP failure, or service impact.

This gate tests same-model memory/context-footprint sensitivity only. It cannot
establish cross-model generalization or CCF-B readiness by itself.

