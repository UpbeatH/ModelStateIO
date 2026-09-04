# MSIO-ST-T006 foreground externality probe

Target: `g127-chenhao`; Ollama `qwen2.5:7b`, already resident before each
measurement. Compare three control requests with three requests concurrent
with a background read of 1 GiB from the existing model blob to `/dev/null`.
Use the same API prompt, `stream:false`, `num_predict:1`, `keep_alive:"5m"`,
and 30-second bounds. Background command is read-only (`dd if=<verified
model-blob> of=/dev/null bs=4M count=256 iflag=direct`). Do not write model or
system data, change configuration, or alter mounts. Save JSON, exit codes,
timestamps, background status, and SHA-256 under the existing user-owned root.

Primary observation: API `total_duration`; secondary: `load_duration`, response
correctness, GPU/process state, and background exit code. Stop on competing
GPU work, service impact, or any unexpected write. This is an externality
capability probe, not a CCF-B result.

