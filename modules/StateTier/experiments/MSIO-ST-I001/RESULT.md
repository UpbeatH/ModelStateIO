# MSIO-ST-I001 installation audit result

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Observations

- GPU: Tesla V100S-PCIE-32GB, no running GPU process at audit time; driver
  575.57.08 reports CUDA compatibility 12.9.
- Toolchain: `/usr/bin/gcc` 13.1 and CMake 4.0.2 are available. The initial
  audit checked only `PATH` and incorrectly reported `nvcc` absent. A follow-up
  read-only audit found CUDA toolkits 11.2, 12.2, 12.8, and 12.9 under
  `/usr/local`; `/usr/local/cuda` points to 12.8. No existing `llama-cli` or
  `llama-server` was found in the searched user/storage paths.
- Models: the Ollama registry still contains only `qwen2.5:7b`, but a separate
  `qwen2.5-0.5b-instruct-q4_k_m.gguf` was placed in the user-owned runtime
  model root. It is 491,400,032 bytes and has SHA-256
  `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
  Its immediate provenance is the verified user-owned source copy
  `/mnt/nvme1/chenhao/modelstateio-runtime/incoming/` on g130; the original
  slow Windows-to-g127 transfer was stopped and its 23,592,960-byte partial
  target was removed before this copy. The model begins with the `GGUF` magic.
- Storage: `/mnt/nvme3n1` has about 1.2 TB free and the user-owned
  `modelstateio-runtime` directory exists, but the device is shared with
  Kubernetes/MinIO mounts.

## User-local runtime build and smoke receipts

- Source: official ggml-org llama.cpp archive at commit
  `49c0dc82b849344f945b14ab997386bd793369ae`, downloaded from the GitHub API
  after a Git clone network failure. Archive SHA-256:
  `392836a6dfc124d0447b92dcb40992dc6e0290ac05eb75c7f02b15cd218440fe`.
- Build: `/home/chenhao/modelstateio-runtime/build/llama.cpp-cuda-12.8/`;
  CMake used `/usr/local/cuda-12.8/bin/nvcc`, `GGML_CUDA=ON`, and V100
  architecture `70-real`. `ldd` later resolved CUDA runtime libraries from
  the host's CUDA 12.2 compatibility paths; this is an observed environment
  fact, not a compatibility guarantee.
- Correctness smoke: the 0.5B model completed the prompt `Reply with exactly:
  R` using `-ngl 99` under `mmap`, `none`, and requested `dio` modes. Each
  returned `R` with exit code zero; these are capability/correctness receipts,
  not performance measurements.
- Effective-setting receipt: `strace` showed a 491,400,032-byte file-backed
  `MAP_SHARED|MAP_POPULATE` mapping for requested `mmap`, while requested
  `none` did not show a model-file mmap. Thus `mmap` and non-mmap are two
  distinguishable, usable loading paths. In contrast, requested `dio` opened
  the model as plain `O_RDONLY`, without observed `O_DIRECT`; it is therefore
  not an effective Direct-I/O treatment and is excluded from the next gate.
- Raw build and smoke logs remain outside Git at
  `/mnt/nvme3n1/chenhao/modelstateio-runtime/logs/smoke-20260904/`.

## Decision

`PARTIAL / PASS_FOR_REENTRY`. A GPU-controllable user-local llama.cpp path is
built and a distinct second model footprint plus two effective loading paths
are now available. No CUDA/system installation or service change was needed.
This clears the old environmental block only; it does not clear the scientific
CCF-B evidence gate. `PFSOpt/environment/HPC-STACK` was not used because it is
a Lustre/PFS-only record and does not govern this single-node line.

## Required inputs to resume

Freeze a new bounded WeightResidency protocol with two model footprints and
only the verified `mmap` versus `none` paths. Re-audit host contention before
execution, then compare equal-information/equal-action/equal-runtime
baselines. Do not use requested `dio` as an effective treatment and do not use
the shared Ollama model directory as the experiment source.
