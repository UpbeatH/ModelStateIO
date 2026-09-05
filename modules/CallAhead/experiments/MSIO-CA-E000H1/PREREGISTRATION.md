# MSIO-CA-E000H1 bounded-harness qualification

Status: frozen before implementation and execution. Date: 2026-09-05.

## Question

Can a user-private harness run a bounded foreground model service while a
separate immutable model file is prepared, enforce the declared preparation
byte/rate contract, record the metrics required by E001, and leave no process
or GPU residue?

This is a technical smoke only. It is not part of E001, cannot estimate an
effect, and cannot be pooled with later blocks.

## Frozen identities and scope

- Foreground: Qwen2.5-0.5B-Instruct Q4_K_M, size 491,400,032, SHA-256
  `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
- Background: Qwen2.5-1.5B-Instruct Q4_K_M, size 1,117,320,736, SHA-256
  `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`.
- Runtime: existing isolated llama.cpp build and private CUDA 11.6 library
  path on g130.
- One loopback-only server, one preparation worker, one deterministic
  one-token request repeated exactly four times.
- Background byte budget: exactly floor(75% of file size), rounded down to a
  whole 8 MiB chunk. Preparation rate ceiling: 256 MiB/s with token-bucket
  sleep; actual bytes may be lower only on timeout/failure and must be logged.
- Server start timeout 90 s; request timeout 30 s; whole smoke timeout 180 s.

## Required receipts

- model and binary identities; requested/effective host, port and GPU;
- foreground HTTP status, latency, response presence and four-request count;
- background start/end, requested/actual bytes, duration, achieved rate,
  before/after `mincore` residency and worker state;
- server/worker PID, process CPU/RSS samples, `/proc/meminfo`, GPU
  memory/utilization snapshots, cleanup and residual-process checks;
- stdout/stderr paths and bounded sizes.

## PASS / NO-GO

PASS only if all identity checks pass, the server becomes ready, four requests
return valid JSON successfully, background actual bytes equal the frozen
budget without exceeding 110% of the rate ceiling, residency/readback fields
are present, and cleanup leaves no task process and 0 MiB GPU memory.

Otherwise NO-GO for this harness implementation. A defect may be corrected
only under a new ID; no E001 performance block may start from a failed H1.

## Safety

Bind only to loopback and use an unoccupied high port. Use only task-owned
logs and the immutable input files. No global cache clearing, installation,
system/cgroup/service/CUDA/driver change, PFS/Lustre access, g129 access,
other-user path, pressure workload or process signal outside task-owned PIDs.

