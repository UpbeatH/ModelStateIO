# MSIO-CP-E003 isolated llama.cpp capability build

Frozen: 2026-09-04.

## Authority and isolation

- Host: `g130-chenhao`, selected after read-only audit.
- User authorization: isolated dependency installation for the ModelStateIO line, conditional on not affecting g129 cluster control.
- Source: official GitHub archive for pinned commit `d230ddd763ffe27781c7ffd237ea78b639b36b6d`; local archive SHA-256 `2625B2172F06AB97E0B4331AC6D2FF93D76278922699212B1BE61758D27E816F`. This archive path replaces a single stalled g130 Git clone; no retry is permitted.
- Source and build roots: `/mnt/nvme1/chenhao/modelstateio-runtime/llama.cpp-d230ddd` and `/mnt/nvme1/chenhao/modelstateio-runtime/build-d230ddd-cuda116`.
- CUDA compiler: `/usr/local/cuda-11.6/bin/nvcc`; build type `Release`; CUDA backend enabled.
- Forbidden: writing `/hpc-tools`, `/usr/local`, `/etc`, system service configuration, NVIDIA driver/CUDA alternatives, Ollama configuration/model store, Lustre mounts/settings, raw devices, or another user's directory.

## Purpose and stop rules

Build an isolated `llama-cli` capable of exposing documented `--mmap`/`--no-mmap` loading modes. This is a feasibility build, not a performance experiment.

- Stop on source identity mismatch, build failure, CUDA compiler incompatibility, unexpected writes outside the two roots, non-idle GPU before smoke test, or any need for elevated privileges.
- Post-build smoke scope: `llama-cli --help` only. Do not download models or run inference in E003.
- PASS requires source identity through the official pinned archive URL plus the frozen SHA-256 above (an extracted source archive has no Git worktree metadata), successful CUDA build, `llama-cli --help` exposing mmap controls, and `ldd` with no missing libraries.
