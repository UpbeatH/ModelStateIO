# MSIO-CP-E003 result

Status: PASS for isolated build capability; 2026-09-04. This is not an inference or performance result.

## Established observations

- `g129` was audited and left unchanged: no Lustre mount, MPI/I/O workload, cluster-control process, or pending ModelStateIO installation was found.
- `g130` has an idle Tesla V100S-PCIE-32GB (driver `535.104.05`), writable private NVMe storage, and no detected Lustre mount or PFS-control activity. All work stayed below `/mnt/nvme1/chenhao/modelstateio-runtime/`.
- The received official archive is `37290179` bytes and SHA-256 `2625b2172f06ab97e0b4331ac6d2ff93d76278922699212b1be61758d27e816f`, matching the frozen archive for llama.cpp commit `d230ddd763ffe27781c7ffd237ea78b639b36b6d`.
- A Release/Ninja build with `GGML_CUDA=ON`, compiler `/usr/local/cuda-11.6/bin/nvcc`, and native V100 target `CMAKE_CUDA_ARCHITECTURES=70` completed successfully. `llama-cli` SHA-256 is `39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24`.
- `llama-cli --help` exposes `--mmap, --no-mmap` (currently documented as deprecated in favor of `--load-mode`); `ldd` reported no missing library.

## Build evidence

- Source: `/mnt/nvme1/chenhao/modelstateio-runtime/llama.cpp-d230ddd/`.
- Active build: `/mnt/nvme1/chenhao/modelstateio-runtime/build-d230ddd-cuda116-sm70/`.
- Raw logs and checksums (outside Git): `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E003/`, including `configure-sm70.log`, `build-sm70.log`, `llama-cli-help.txt`, `llama-cli-ldd.txt`, and `SHA256SUMS.txt`.
- A previous default multi-architecture build was deliberately stopped after it compiled unnecessary `sm50/61/70/75/80/86` targets. Its partial build tree and log remain at `build-d230ddd-cuda116/` and `build.log` for diagnostic traceability; they are not E003 evidence.

## Limitation and exact next gate

Current observation: g130's system `/usr/local/cuda` resolves to CUDA 11.3 even though this private build used the CUDA 11.6 compiler. The binary resolves CUDA runtime libraries through that system default unless a private environment is supplied. With `LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64`, `ldd` resolves `libcudart`, `libcublas`, and `libcublasLt` to CUDA 11.6, without changing global state. No global CUDA link, driver, service, or alternative was changed.

Before any model download or inference, the next frozen gate must run the binary in a private launch environment with `/usr/local/cuda-11.6/lib64` selected explicitly, verify the resulting loader resolution, then perform one bounded model-load-only smoke test. That later test must remain separate from E003 and needs its own model/license, resource, and cache-control authorization.
