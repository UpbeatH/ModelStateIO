# MSIO-CA-E000-A0 read-only audit result

Audit time: 2026-09-05T11:29:47Z. Host: `g130`. Evidence level: current
observation and prior hash-pinned receipt comparison; no performance evidence.

## Established observations

- The allowed root is owned by `chenhao`, mode `775`, on
  `/mnt/nvme1n1p1`. The audit reported 2,838,334,951,424 bytes available.
- The V100S 32 GB GPU reported 0 MiB allocated before the audit; no
  user-owned `llama`, `ollama`, `modelstate` or `prefetch` workload was found.
- `python3`, `gcc`, `taskset`, `ionice` and `systemd-run` are available.
  `fio`, `stress-ng` and `cgexec` were not found through the audited PATH.
- The isolated CUDA-compatible build contains `llama-cli` and
  `llama-server`. The extracted llama.cpp source tree is present.
- Two distinct complete GGUF weights were found in `incoming/`:
  Qwen2.5-0.5B-Instruct Q4_K_M (491,400,032 bytes) and
  Qwen2.5-7B-Instruct Q4_K_M (4,683,073,952 bytes). Their sizes match the
  previously hash-pinned ColdPath receipts. A full rehash was intentionally
  forbidden in A0 because it would perturb page-cache residency.
- StatePatch adapters, seed variants, vocabulary test GGUFs and a converted
  copy of the same 0.5B base are not independent full-model states and do not
  count toward the three-state requirement.
- Frozen E031 source evidence already establishes the inspectable llama.cpp
  queue/LRU boundary. A0 found no third provenance-complete full-model state
  and no already-installed private interference tool.

The first shell packet ended after the evidence above because a CRLF-affected
loop produced a shell syntax error. Follow-up read-only commands captured the
tool and asset observations. This execution issue did not launch a model or
change remote state.

## Requirement status

| Requirement | Status | Basis |
|---|---|---|
| 1. mechanism-level novelty gap | conditional PASS | `PRIOR_ART_MATRIX.md`; margin depends on debt/harm necessity, not a KV-to-weight port |
| 2. three provenance-complete full models | FAIL/MATERIAL | two distinct full models; 7B receipt remains incomplete; no third model |
| 3. inspectable router path | PASS | E031 source audit plus present source/binaries |
| 4. safe user-scoped cold/residency control | PASS | frozen ColdPath E017 applied file-scoped `POSIX_FADV_DONTNEED` and `mincore` to the exact owned 0.5B GGUF, observed 100% -> 0% -> 100% residency, and left no process/GPU residue; the mechanism is reusable but the old samples are not CallAhead performance data |
| 5. bounded foreground and interference harness | UNESTABLISHED | required primitives exist, but no CallAhead-specific bounded harness and receipt schema has passed qualification |

## E000 decision

**MATERIAL_BLOCKED, not scientific NO-GO.** Requirement 1 survives only in the
narrow debt-and-harm form; requirements 3 and 4 pass. Requirements 2 and 5 are
not established. E001 is forbidden until separate material/capability subgates
supply those facts without changing E001 thresholds.

No server/model was launched; no file, cache, source, system setting, CUDA,
driver, service, PFS/Lustre state or other host was modified.
