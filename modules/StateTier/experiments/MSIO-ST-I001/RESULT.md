# MSIO-ST-I001 installation audit result

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Observations

- GPU: Tesla V100S-PCIE-32GB, no running GPU process at audit time; driver
  575.57.08 reports CUDA compatibility 12.9.
- Toolchain: `/usr/bin/gcc` 13.1 and CMake 4.0.2 are available; `nvcc` is
  absent. No existing `llama-cli` or `llama-server` was found in the searched
  user/storage paths.
- Models: Ollama registry contains only `qwen2.5:7b`; no second approved model
  footprint is present.
- Storage: `/mnt/nvme3n1` has about 1.2 TB free and the user-owned
  `modelstateio-runtime` directory exists, but the device is shared with
  Kubernetes/MinIO mounts.

## Decision

`BLOCKED`. A GPU-controllable llama.cpp path cannot be built from the current
toolchain without a CUDA toolkit, and a CCF-B-oriented matrix cannot be
expanded without a second model. No dependency was installed and no service
was changed. `PFSOpt/environment/HPC-STACK` was not used because it is a
Lustre/PFS-only record and does not govern this single-node line.

## Required inputs to resume

Provide a user-local CUDA toolkit/build bundle compatible with V100S, or
explicitly authorize a separately scoped user-local toolkit installation, plus
a second model artifact with provenance and SHA-256. Re-audit storage
isolation before building; do not use the shared Ollama model directory as the
experiment source.

