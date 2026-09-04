# MSIO-CP-E018 result

## Established observation

All 12 trials (six counterbalanced cold/prefetch blocks) completed correctly. Every block favored completed prefetch for request-visible time-to-first-exact-OK. The paired median reduction was 13.54%; the fixed-seed block-bootstrap 95% interval was 9.88% to 20.05%, above zero. Median cold request latency was 2.898 s and median prefetched request latency was 2.500 s.

Full sequential prefetch itself required a median 0.690 s. Median preparation-plus-request latency was 3.170 s, so prefetch did not reduce total work relative to the 2.898 s cold request. Cleanup passed with no residual `llama-cli` and 0 MiB GPU use.

## Decision

**Conditional GO for deadline-aware ResidencyShaper.** E018 passes the preregistered ≥10% paired-median request-latency reduction and positive bootstrap lower-bound gates. The mechanism is useful only when preparation can begin before the request or overlap other work; it is not an on-demand end-to-end speedup.

The next falsification gate must vary available lead time/prefetch budget and test whether partial preparation yields a monotonic, reproducible latency frontier. No controller or generalization claim is yet supported.

Raw receipts remain outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E018/`; receipts SHA-256 is `11c6b53c6eb52cd5f2da88f795073abbe8fb11a9b8986c14c615eae149c1b4c6`.
