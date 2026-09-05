# MSIO-KVG-E000 capability result

## Established observations

Read-only source inspection of the isolated g130 llama.cpp tree found
`llama_context::state_save_file`, `state_load_file`, partial sequence-state
restore, KV offload controls, and server prompt-cache/idle-slot code. The
available isolated build, however, contains only `llama-cli`; no
`llama-server` executable is present. CLI help exposes KV type/offload,
context-checkpoint and cache-RAM options, but no owned sequence-state
save/load interface.

## Decision

**Platform-blocked, not mechanism No-Go.** The desired state lifecycle is
implemented in source but not exposed by the currently available executable.
E000 did not launch a model, server or GPU work. A future E001 requires a new
packet authorizing a user-local `llama-server` build or a minimal state API
wrapper; it must first prove exact round-trip and cleanup before any policy or
performance comparison.
