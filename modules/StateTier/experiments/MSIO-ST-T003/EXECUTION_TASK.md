# MSIO-ST-T003 weight residency capability

Target: `g127-chenhao`; existing Ollama `qwen2.5:7b`; no installation or
system/storage parameter change. Run three paired requests. In each pair,
first request with `keep_alive:0` (cold/unload policy), then request with
`keep_alive:"5m"` (resident policy). Use `stream:false`, `num_predict:1`,
fixed prompts, 30-second request bounds, and save JSON/timing under the
existing user-owned T001 root. Query `/api/ps` before and after each request.

Primary observation: total and load duration from API JSON. Record correctness,
HTTP/exit status, VRAM/model residency, and cleanup. This is a capability gate,
not a CCF B performance claim. Stop on competing GPU work, HTTP failure,
service impact, or any need to modify shared configuration.

