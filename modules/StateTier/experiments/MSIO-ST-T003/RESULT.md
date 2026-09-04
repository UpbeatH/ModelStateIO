# MSIO-ST-T003 result

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Observations

Three cold/resident pairs were executed against the existing Ollama API and
`qwen2.5:7b`. All six requests returned a valid one-token response and exit
code 0.

| Pair | `keep_alive=0` total duration | `keep_alive=5m` total duration |
|---|---:|---:|
| 1 | 4.665 s | 0.220 s |
| 2 | 5.408 s | 0.218 s |
| 3 | 5.241 s | 0.223 s |

The model digest and approximately 8.21 GB VRAM residency were visible in
`/api/ps`. Raw JSON, state snapshots, ledger, and SHA-256 receipts are under
`/mnt/nvme3n1/chenhao/modelstateio-runtime/logs/MSIO-ST-T003/`.

## Decision

`PASS` for single-state residency capability: the runtime can reproducibly
distinguish an unloaded/cold request from a resident/warm request. This is not
CCF B evidence and does not establish a new policy's superiority.

## Next gate

Freeze a larger WeightResidency protocol with at least two model footprints,
cold/warm randomization, memory-pressure or competing-I/O condition, and
strong fixed-path baselines. Do not call the route paper-ready from T003.

