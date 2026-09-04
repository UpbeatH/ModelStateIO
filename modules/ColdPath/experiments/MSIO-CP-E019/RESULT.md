# MSIO-CP-E019 result

## Established observation

All 30 trials completed correctly with no residual process and 0 MiB final GPU use. All six within-block Spearman correlations between prefetched fraction and request-visible latency were negative (`−0.9, −0.9, −0.7, −1.0, −0.6, −0.1`); their median was `−0.8`. Median time-to-first-exact-OK was 2.824 s at 0%, 2.604 s at 25%, 2.667 s at 50%, 2.508 s at 75%, and 2.440 s at 100%.

The 75% arm recovered 82.23% of the full-prefetch median benefit while reading 75% of model bytes. The 25% and 50% medians were not strictly monotonic, and block 6 had only a weak negative correlation.

## Decision

**GO for fractional residency as a ColdPath controller action space.** The preregistered direction, median-correlation, partial-recovery, correctness, and cleanup gates passed.

This is still one-host/one-model mechanism evidence. It does not establish that byte-prefix fraction is the optimal content choice, that benefits generalize, or that a controller beats strong fixed policies. The next gate should compare prefix selection with content-aware segment selection and quantify preparation time, memory occupancy, and prediction-error sensitivity.

Raw evidence remains outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E019/`.
