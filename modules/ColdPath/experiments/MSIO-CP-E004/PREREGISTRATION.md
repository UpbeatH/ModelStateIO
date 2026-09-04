# MSIO-CP-E004 bounded model-load smoke

Frozen: 2026-09-04 before model download or execution.

## Question and evidence boundary

Can the E003 `llama-cli` build load one licensed GGUF with the private CUDA 11.6 runtime and complete exactly one generated token on g130? This is a technical feasibility gate only. It is not evidence of loading-path performance, an optimization benefit, or generality.

## Frozen inputs

- Host and scope: `g130-chenhao`; all new files remain below `/mnt/nvme1/chenhao/modelstateio-runtime/`.
- Binary: `/mnt/nvme1/chenhao/modelstateio-runtime/build-d230ddd-cuda116-sm70/bin/llama-cli`; expected SHA-256 `39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24`.
- Model: author-published `Qwen/Qwen2.5-0.5B-Instruct-GGUF`, Apache-2.0, revision `df5bf01389a39c743ab467d734bf501681e041c5`, file `qwen2.5-0.5b-instruct-q4_k_m.gguf`.
- Expected model size: `491400032` bytes; expected SHA-256/LFS OID: `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
- Runtime: `LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64`; four CPU threads; CUDA offload capped at 99 layers; context 256; batch 64; seed 1; temperature 0; exactly one predicted token; 180-second timeout.

## Admission and stop rules

- Stop without execution if another E004 lock/process exists, the GPU is not idle, free NVMe is below 2 GiB, binary/model identity differs, CUDA 11.6 libraries do not resolve, or elevated/global changes are needed.
- A single resumable download is allowed through the already available user proxy, with at most two bounded retries. Preserve a partial file on network failure and resume next heartbeat; do not start a parallel transfer.
- Do not drop caches, change CUDA links, drivers, services, mounts, Lustre/PFS settings, or access g129/other users.

## Decision

- PASS: exact identities; smoke exit 0 within 180 seconds; log shows successful model load and CUDA offload; no residual `llama-cli`; GPU returns idle.
- NO-GO: invalid identity, loader failure, timeout, crash, OOM, or absent CUDA offload. Preserve raw logs outside Git and do not retry the smoke automatically.

