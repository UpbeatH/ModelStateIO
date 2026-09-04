# MSIO-CP-E022R1 result

All 18 trials completed correctly; cleanup left no `llama-cli` and 0 MiB GPU use. The arrival snapshot fixed the E022 defect: all six concurrent rows recorded an active prefetch worker at arrival and zero resident model pages, while completed rows recorded no active worker and 75.03% median residency.

Completed preparation had median arrival-to-OK 2.349 s versus 2.674 s for no prefetch. Its six paired contrasts were all negative, median −0.345 s, with fixed-seed 95% bootstrap interval −0.457 to −0.161 s.

Concurrent fill had median arrival-to-OK 2.326 s; its six paired contrasts were all negative, median −0.384 s, interval −0.531 to −0.150 s.

## Decision

**PASS for mechanism separation on this host/model.** Both prepared residency and concurrent page-cache filling can reduce request-visible latency under the frozen 75% action. They are distinct mechanisms and must remain separately modeled; this does not establish a predictor, controller, total-work reduction, held-out-model result, or paper-level contribution.

Raw evidence remains outside Git at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E022R1/`.
