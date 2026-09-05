# MSIO-KVG-E003R1 result - necessity signal GO

All six independent server-process blocks completed, were content-equal, and left no llama-server process.
Raw evidence is outside Git at /mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-KVG-E003R1/receipts.json
(SHA-256 f49e84969fc8ecd1e5d66680e495742932a0bdad25dcb10923768382d763fbee).

| context | n | fresh recompute median (s) | save+restore+resume median (s) | median P-R (s) | frozen 10% threshold (s) |
| --- | ---: | ---: | ---: | ---: | ---: |
| short (26 prompt tokens) | 3 | 0.018973 | 0.021958 | +0.004285 | 0.001897 |
| long (186 prompt tokens) | 3 | 0.031249 | 0.027834 | -0.003415 | 0.003125 |

The signs reverse and both median magnitudes exceed their frozen threshold. Saved states were 259012 and 2227652 bytes; restored requests reported cached prefix lengths of 21 and 181 tokens.

## Decision

**GO - action-reversal necessity signal.** A fixed always-save or always-recompute choice is not sufficient for these two tested context costs. This warrants one capacity-specific gate.

## Limits and next gate

This is not a throughput, tail-latency, capacity-pressure, cancellation, multi-tenant, or paper-level result. It has three repetitions per class and one model/runtime. The short-arm direction is not uniform (two of three pair differences are negative despite the positive median), so no per-context threshold is claimed.

E004 must create a bounded one-slot capacity conflict and a predeclared abandonment case. It must compare always-retain, always-save, always-recompute, and a state-size/deadline-aware controller under equal observability and action budgets. It must charge save/restore bytes and time, foreground harm, correctness, cleanup, and abandoned-write cost, and stop if no conflict is induced or the controller fails its frozen threshold.
