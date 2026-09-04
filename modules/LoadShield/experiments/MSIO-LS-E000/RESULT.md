# MSIO-LS-E000 result: affected-set causal gate

Status: **No-Go** for the frozen isolated storage-I/O mechanism.
Date: 2026-09-04 (Asia/Shanghai). Raw root:
`/mnt/nvme3n1/chenhao/modelstateio-runtime/logs/MSIO-LS-E000/`.

## Established observations

- Identity, capacity, and process preflight passed: both isolated model hashes
  matched; no foreign GPU compute process was present; all 12 foreground runs
  exited zero and emitted the required standalone `R`.
- `strace` recorded the 7B background model file as `O_RDONLY|O_DIRECT`.
  All six overlap arms retained a live background PID at foreground start;
  all 12 background reads exited zero. No residual `llama-cli` or background
  reader remained and final GPU use was 0 MiB.
- Each foreground model was file-scoped evicted and had `mincore` cold fraction
  0.0 before launch. The background reader did not use GPU, so this gate does
  not conflate the tested storage I/O with background GPU compute.

| Block | Defer foreground (s) | Overlap foreground (s) | Overlap - defer (s) |
|---|---:|---:|---:|
| b1 | 3.108 | 2.801 | -0.307 |
| b2 | 2.957 | 2.937 | -0.020 |
| b3 | 3.106 | 2.798 | -0.307 |
| b4 | 2.912 | 3.017 | +0.105 |
| b5 | 3.104 | 2.769 | -0.335 |
| b6 | 2.893 | 2.950 | +0.058 |

Median foreground time was 3.031 s for deferred background work and 2.869 s
for overlap; paired median contrast was -0.164 s. Only 2/6 contrasts were
positive. Empirical p95 was 3.108 s (defer) versus 3.017 s (overlap).
The fixed-seed (20260904), 10,000-resample block-bootstrap interval for the
median contrast was [-0.321, +0.081] s.

`receipts.json` SHA-256:
`b67639b74913b5313fe1dc3dea0f8e570a6da5c966f0d2e8aa00a5aa7b46e6a0`.
The Direct-I/O trace SHA-256 is
`5b27a915c71347d7bac8b84e24d22bbfc8817a9b5d95c31905963174761b8371`.

## Decision

The preregistered Go criteria fail: fewer than five positive pairs, negative
paired median, negative empirical p95 contrast, and an interval crossing zero.
Do not add samples, raise background bytes, retune overlap timing, or call this
an affected-set opportunity. This result does not rule out all model-serving
externalities; it closes the specific one-node 7B Direct-I/O read versus 0.5B
cold-launch mechanism.
