# MSIO-ST-T001 model-state trace collection

Task ID: MSIO-ST-T001-20260904. Required repository commit: to be recorded before execution. Target: `g127-chenhao`.

## Authority and boundary

This packet authorizes only a bounded local trace-collection qualification using the existing `qwen2.5:7b` Ollama artifact. It permits starting one short user-owned inference process only if all preflight checks pass. It forbids system/PFS parameter writes, installations, mounts, service restarts, model downloads, deletion, and changes to shared Kubernetes/MinIO data.

## Question

Can the available single-node runtime expose at least two distinguishable model-state classes (for example immutable weights plus request-scoped KV) with timestamps, sizes or access events sufficient for a StateTier trace?

## Preflight (read-only, in order)

```text
hostname; date -Is; nvidia-smi --query-gpu=name,utilization.gpu,memory.used --format=csv,noheader
free -h; uptime; pgrep -a -u chenhao || true
ollama list
ollama show qwen2.5:7b --modelfile 2>/dev/null || true
command -v strace || true; command -v perf || true; command -v iostat || true
find /mnt/nvme3n1 /home/chenhao -maxdepth 5 -type f -name '*.gguf' -printf '%p %s\n' 2>/dev/null | head -n 20
```

Stop before workload if the GPU is occupied, load exceeds 8 on 104 CPUs, the model is absent, no writable user-owned external data directory is available, or neither `strace` nor an equivalent already-installed observation path exists.

## Collection (only after preflight)

Use an external path under `/mnt/nvme3n1/chenhao/modelstateio-runtime/logs/MSIO-ST-T001/` only after verifying ownership and free space. Run at most three prompts with fixed text and one repeat, record wall-clock and exit code, and capture only process/file metadata needed to identify model loading and runtime state. Do not download models or alter Ollama configuration. Do not claim a multi-state trace unless the returned records contain at least two state classes with provenance.

## Stop rules

Stop on any competing GPU process, service impact, missing observation tool, unsupported Ollama interface, ambiguous external path, or inability to distinguish a second state class. A weights-only trace is `PARTIAL`, not a StateTier hypothesis test.

## Return package

Return exact commands, exit codes, timestamps, model identity, observation-tool versions, external paths, file sizes and SHA-256, cleanup proof, and a `PASS`, `PARTIAL`, or `NOT_RUN` decision. No raw prompts or private data should enter Git.

