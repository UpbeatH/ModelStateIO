# MSIO-KVG-E004 result - paper-level No-Go

## Established observations

The frozen 48-block matrix completed with three repetitions for each short/long x return/abandon x policy cell. All returning-A outputs were content-equal to their within-block references; every non-retain arm admitted foreground B; no server remained. Raw evidence is outside Git at /mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-KVG-E004/receipts.json (SHA-256 612aba98e7f137e4a454837ac64b1905e7d0757581ef234f9cb2bad3a6d0f832).

| state/life | controller action | controller A median (s) | best fixed admitted A median (s) | controller B median (s) | best fixed B median (s) |
| --- | --- | ---: | ---: | ---: | ---: |
| short/return | recompute | 0.021479 | save: 0.017228 | 0.008824 | recompute: 0.005357 |
| long/return | save | 0.019979 | save: 0.020930 | 0.006962 | recompute: 0.005540 |

For announced abandonment, controller dropped A and wrote zero bytes, while always-save wrote 259,004 bytes (short) or 2,227,644 bytes (long). This is a correct accounting observation, not a performance-policy result: always-recompute also writes zero bytes.

## Decision

**Paper-level No-Go on the available platform and artifacts.** The controller does not beat the strongest fixed admitted action by the preregistered 10% in either returning context class. It is worse for short return and increases B median by more than 10%; for long return it merely reproduces always-save within small-sample variation. The cancellation branch is an announced deterministic drop and adds no nontrivial choice over always-recompute.

## What remains true

E001R1 and E003R1 establish that the isolated runtime can save/restore owned KV state and that short/long costs reverse under a narrowly bounded test. They do not establish a novel controller, capacity policy, end-to-end serving benefit, tail-latency improvement, or CCF B paper contribution.

## Reopen condition

Do not rerun E004 or tune its threshold. Reopen only with a new provenance-complete application trace that supplies a non-oracular lifecycle/deadline signal, multiple live competing states, a measured capacity/eviction externality, and an equal-information comparison against production-quality prefix/KV caching baselines.
