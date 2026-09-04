# MSIO-ST-I001 single-node runtime enablement

Target: `g127-chenhao`. This task is authorized for ModelStateIO only and is
independent of `PFSOpt/environment/HPC-STACK`, which applies to Lustre/PFS
work. Do not install or change Lustre clients, mounts, kernel modules, or
system services.

## Objective

Prepare an isolated user-owned runtime capable of exposing at least two
effective model-loading paths (for example mmap and non-mmap/direct I/O) and a
second approved model footprint. Installation is not evidence of a performance
benefit.

## Pre-install audit (read-only)

Record hostname, GPU/driver, CUDA toolkit/runtime, compiler/CMake, available
disk and RAM, current processes, existing llama.cpp source/binaries, model
artifacts and hashes, and user-owned paths. Stop if the target is busy or any
system/Lustre change would be required.

## Allowed changes

- Create directories below `/mnt/nvme3n1/chenhao/modelstateio-runtime/` and
  `/home/chenhao/modelstateio-runtime/`.
- Build or install a user-local llama.cpp/runtime under those directories.
- Copy only user-approved model artifacts into the isolated model directory,
  preserving source URL/path and SHA-256.

## Forbidden changes

No apt/conda system installation, driver/CUDA upgrade, Ollama service change,
Lustre client/mount change, kernel/module change, deletion, or overwrite of
existing artifacts. If a required dependency is absent, stop and report it.

## Acceptance

Pass only if the runtime and model identities are recorded, two loading modes
have effective-setting/readback receipts, and a correctness smoke succeeds.
Otherwise record `BLOCKED` or `PARTIAL`; do not claim a controllable path.

