# MSIO-CP-E022 result

## Established completed-preparation evidence

All 18 trials were correct and cleanup ended with no `llama-cli` and 0 MiB GPU use. The completed 75% arm had 75.03% median residency at arrival and no active worker. Its arrival-to-OK median was 2.424 s versus 2.800 s for no prefetch. Five of six completed-minus-none block contrasts were negative; their median was −0.378 s with fixed-seed 95% bootstrap interval −0.547 to −0.076 s.

**PASS: completed preparation replicates a request-visible benefit on this exact host/model.**

## Concurrent-fill instrumentation failure

The runner recorded `prefetch_active_at_arrival` only after `worker.join()`, so all concurrent rows falsely report inactive even though their request-time outcome was measured. The concurrent arm therefore cannot establish or refute a concurrent-fill mechanism. This is a technical evidence failure, not a completed-preparation performance failure.

E022 is closed and must not be rerun. E022R1 may change only the timing of the active-worker snapshot, retain all identities and schedule structure, and separately report concurrent-fill evidence. Raw receipts remain at `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E022/`.
