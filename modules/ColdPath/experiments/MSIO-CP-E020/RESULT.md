# MSIO-CP-E020 result

## Established observation

All 24 trials completed correctly and cleanup left no `llama-cli` process and 0 MiB GPU use. At an equal 50% byte budget, median request latency was 2.583 s for prefix, 2.603 s for suffix, and 2.675 s for striped placement; no-prefetch control was 2.726 s.

For the two preregistered contrasts, suffix versus prefix had a paired median relative difference of +1.53% with 99% bootstrap interval −11.20% to +3.96%; striped versus prefix was −1.00% with interval −6.97% to +4.49%. Both intervals crossed zero and neither reached the 5% materiality threshold.

## Decision

**NO-GO for byte-position/content-placement as an independent action family on this setup.** Do not build a GGUF tensor-aware selector from these data. E019's fraction/timing action remains open because this gate did not invalidate its dose-response evidence.

This negative result is limited to one GGUF/model, equal 50% bytes, and prefix/suffix/8 MiB striped layouts. Raw evidence remains outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E020/`.
