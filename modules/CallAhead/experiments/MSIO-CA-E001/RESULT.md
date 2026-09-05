# MSIO-CA-E001 result

Status: **NO-GO** for the present CallAhead foreground-harm/pacing mechanism.
Executed once on g130 on 2026-09-05. Evidence level: preregistered
single-host causal death gate, not a paper-level or cross-context result.

## Integrity and execution

- All 18 frozen trials completed: six counterbalanced blocks and three arms
  per block. Each trial retained all 160 scheduled foreground requests.
- All 2,880 foreground responses and all 18 background probes passed their
  correctness/return-code checks. Every non-none trial read exactly
  830,472,192 bytes; paced trials stayed at the frozen 256 MiB/s ceiling.
- Every trial began at 0% measured background-file residency; prepared trials
  ended at 74.34% full-file residency. Cleanup left no model process, no lock
  and 0 MiB GPU allocation.
- Raw receipt: 1,131,091 bytes, SHA-256
  `391502489abc49abf4a25488c61a308fff962116be06e0815e8f8d43496937aa`,
  retained outside Git at
  `D:\Temp\ModelStateIO-CallAhead\MSIO-CA-E001\receipts.json` and at the
  g130 private runtime path documented below.
- The executed runner SHA-256 was
  `58be13a1d2d68c628dc1ed75efe32072b443367aca0743bd96f2b6660af9dbf2`;
  the frozen analyzer SHA-256 was
  `e24a2d604e2eca71975db989d250952a592e03085533b646a94a8ab3200bfc28`.

## Confirmatory result

| frozen outcome | observation | threshold | decision |
|---|---:|---:|---|
| median eager relative foreground p95 harm | 0.12% | at least 10% | FAIL |
| paired-block bootstrap 95% interval | [-3.01%, 5.90%] | lower bound above 0 | FAIL |
| blocks with positive eager excess | 3/6 | descriptive only | unstable affected set |
| median pacing recovery among positive-excess blocks | 175.2% | at least 50% | not decision-relevant after harm failure |
| median eager readiness benefit | 0.402 s | positive | observed |
| median paced readiness benefit | 0.400 s | at least half of eager | PASS (99.5% retained) |

Eager preparation transferred about 830 MB at 1.89--2.13 GB/s and produced a
stable background readiness opportunity, but it did not create the required
foreground p95 externality. The confidence interval is also entirely below
the preregistered 10% material-harm target at its upper end.

## Decision and claim boundary

The causal premise for a foreground-harm-aware pacing controller is absent in
this platform/workload/model pair. Per the frozen stopping rule, E002--E006 of
the present design do not run. Increasing model size, adding memory pressure,
changing foreground load/rate/window, or adding repetitions after this result
would be post-hoc rescue and cannot reopen E001.

The positive readiness result supports a different, narrower future question:
under finite model capacity and genuine branch uncertainty, can a controller
choose *which* full model to prepare while charging wrong-path bytes and
eviction/reload debt? That is not evidence for the current CallAhead system.
It may re-enter only as a new candidate after (1) a stronger source-level
conflict audit against PBKV, ServerlessLLM, HydraServe and SYMPHONY and (2) a
real, provenance-complete three-model program trace with pre-arrival branch
notices and capacity conflict. Without both, the modification is merely a
KV-to-weight transfer and remains No-Go.

Raw g130 evidence remains outside Git at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CA-E001/`.
