# MSIO-CP-E005 non-interactive CLI contract

Frozen: 2026-09-04. Execution is not authorized by this document.

## Motivation and question

E004 loaded the staged model but exposed a runner-interface defect: the command entered interactive mode and was stopped by its 180-second timeout. E005 asks a narrow technical question: can the same binary execute a single predefined turn in documented non-interactive mode and exit under a bounded-output contract? It is not a loading-path comparison or a performance experiment.

## Frozen contract

- Host and isolation: `g130-chenhao`; only `/mnt/nvme1/chenhao/modelstateio-runtime/` may be written.
- Inputs: the E004-verified binary and staged Qwen2.5-0.5B Q4_K_M model, with the E004 SHA-256 values rechecked before execution.
- Runtime: `LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64`; dynamic loader must resolve CUDA runtime libraries under that path.
- Invocation: `--single-turn --simple-io --no-display-prompt --prompt 'Reply with exactly OK.' --predict 1 --seed 1 --temp 0 --n-gpu-layers 99 --ctx-size 256 --batch-size 64 --threads 4 --threads-batch 4`.
- Bounded execution: one process, 120-second timeout, 1 MiB per-output-file limit, no stdin, and separate stdout/stderr/result files outside Git.

## Admission, success, and stop rules

- Admit only if no prior E005 lock or `llama-cli` process exists, GPU is idle, staged input hashes match, and free NVMe exceeds 2 GiB.
- PASS requires exit 0 before 120 seconds, stdout and stderr no larger than 1 MiB, no interactive prompt loop, no residual process, and GPU returned to idle after termination.
- Any timeout, nonzero exit, output-cap hit, identity mismatch, loader mismatch, GPU contention, or residual process is a technical No-Go. Preserve evidence; do not retry automatically.
- Do not download models, clear caches, modify system or PFS state, or infer a throughput/latency result from this contract.

