# MSIO-ST-T002 API context-state qualification

Task ID: MSIO-ST-T002-20260904. Target: `g127-chenhao`. Existing Ollama
service/model only; no installation, configuration write, or filesystem
parameter change.

Run at most two short `/api/generate` requests with `stream:false`,
`num_predict:1`, and `keep_alive:"5m"`; query `/api/ps` before, between, and
after. Save JSON responses and timestamps under the existing user-owned
T001 directory. Stop on competing GPU work, HTTP failure, or service impact.

This gate can establish only whether Ollama exposes a distinguishable
request-context/KV residency signal. It cannot establish a storage-tier
performance benefit. If `/api/ps` exposes only model residency and no context
state, classify `PARTIAL` and stop the unified StateTier route.

