# MSIO-CP-E001 model-residency materiality gate

Frozen: 2026-09-04, before observing E001 outcomes.

## Question

Does loading an existing 14B quantized model into the existing Ollama/V100S runtime impose a stable, material readiness penalty relative to an immediately repeated resident-model request?

## Evidence boundary

This is a process/model-residency gate. Unloading the model does not evict the Linux page cache, so it is **not** a storage-cold experiment and cannot establish an advantage for mmap, buffered I/O, Direct I/O, prefetching, or any proposed ColdPath mechanism.

## Frozen platform and workload

- Host: `g129-chenhao`; observed idle V100S 32GB at E000-A1.
- Existing runtime: Ollama 0.5.13 system service.
- Existing model: `qwen2.5:14b`, Q4_K_M, reported 14.8B parameters and approximately 9GB model size.
- Prompt: `Return one token.`; `temperature=0`; `num_predict=1`; non-streaming API.
- Five paired repetitions. Each pair unloads the model, verifies no model remains in `ollama ps`, executes one process-cold request, then one resident-model request.
- No OS cache drop, model copying, download, installation, service restart, or system setting change.

## Metrics and decision

- Primary: Ollama-reported `load_duration` difference between cold and warm requests.
- Secondary: `total_duration`, prompt/eval durations, HTTP success, response presence, GPU process cleanup.
- Technical validity: ten successful JSON responses, all required duration fields numeric, every pre-pair unload verified, and final `ollama ps` empty.
- Go to implementation feasibility design if median cold `load_duration` is at least 1 second and at least 5x median warm `load_duration`.
- No-Go for this runtime/model pair if either threshold fails.
- A PASS means only that model residency has measurable cost. It does not validate a storage-path contribution.

