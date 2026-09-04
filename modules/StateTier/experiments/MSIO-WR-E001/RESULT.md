# MSIO-WR-E001 result

Status: **No-Go** for the preregistered loading-path hypothesis on g127.
Date: 2026-09-04 (Asia/Shanghai).

## Established observations

All 12 frozen runs exited zero and produced the required standalone `R`.
Raw logs are outside Git at
`/mnt/nvme3n1/chenhao/modelstateio-runtime/logs/MSIO-WR-E001/20260904T213000+0800/`.
`summary.csv` SHA-256 is
`2d754423f0b02d40d288b8c9dd10d758f9e3f75a67fdb64aec412996ac7d60dc`.

| Model | Block contrasts `none - mmap` (s) | Median contrast | Paired median wall time | Relative contrast |
|---|---:|---:|---:|---:|
| 0.5B Q4_K_M | +0.09, +0.29, +0.20 | +0.20 | 2.66 | 7.5% |
| 7B Q4_K_M | +0.19, +0.17, +0.16 | +0.17 | 3.72 | 4.6% |

The direction is consistent (`none` slower) but neither model reaches the
frozen 10% relative-median threshold. Maximum RSS also differs substantially
between modes, but this run did not predefine a causal memory analysis and did
not measure a controlled cache/pressure condition.

## Decision

**No-Go.** Do not extend repetitions, add post-hoc pressure, or claim a
general storage-management benefit from this experiment. The bounded result
only establishes that two effective loading paths are executable and produce
small same-direction cold-start differences under this host and prompt.

## Implication

The prior unified multi-state StateTier No-Go remains unchanged. For a future
single-node paper candidate, start from a new mechanism with controlled state
pressure and a stronger problem than mmap versus non-mmap loading; this E001
does not justify a controller or CCF-B claim.
