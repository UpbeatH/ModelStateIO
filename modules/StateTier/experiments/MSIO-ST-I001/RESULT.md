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
- Models: Ollama registry contains only `qwen2.5:7b`; no second approved model
  footprint is present.
- Storage: `/mnt/nvme3n1` has about 1.2 TB free and the user-owned
  `modelstateio-runtime` directory exists, but the device is shared with
  Kubernetes/MinIO mounts.

## Decision

`PARTIAL / BLOCKED_INPUT`. A GPU-controllable llama.cpp path can in principle
be built using an absolute CUDA toolkit path; no CUDA installation is needed.
The CCF-B-oriented matrix is still blocked by the absence of a second approved
model and by the need to select/verify a user-local build. No dependency was
installed and no service was changed. `PFSOpt/environment/HPC-STACK` was not
used because it is a Lustre/PFS-only record and does not govern this
single-node line.

## Required inputs to resume

Provide a second model artifact with provenance and SHA-256. Before building,
select one of the existing CUDA toolkits by absolute path (11.2 is the
conservative V100S baseline), verify compiler compatibility and storage
isolation, and build the runtime in the user-local directory. Do not use the
shared Ollama model directory as the experiment source.
