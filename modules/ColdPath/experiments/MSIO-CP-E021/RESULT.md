# MSIO-CP-E021 result: asynchronous lead-time gate

Status: **GO for timing qualification only.** Date: 2026-09-04.

## Established observations

The remote runner SHA-256 matched the tracked script:
`a3473491207b481c1b6fc3d9a6ff569a337ce447785f950396cc49762a669576`.
All 24 trials completed with exact output, exit zero, and no residual
`llama-cli`; final GPU use was 0 MiB. Every trial began at <=20% foreground
model residency. The 0.3-second arrivals had about 36%--38% resident pages;
the 0.7-second arrivals had about 75% resident pages and their prefetch worker
had completed.

| Block | None (s) | lead700 (s) | lead700 - none (s) |
|---|---:|---:|---:|
| b1 | 2.769 | 2.492 | -0.277 |
| b2 | 2.769 | 2.488 | -0.281 |
| b3 | 2.685 | 2.713 | +0.028 |
| b4 | 2.842 | 2.442 | -0.400 |
| b5 | 2.812 | 2.469 | -0.344 |
| b6 | 2.738 | 2.428 | -0.311 |

Five of six paired contrasts were negative. Median request time was 2.769 s
for none and 2.478 s for lead700: a 10.50% reduction. The fixed-seed
(20260904), 10,000-resample block-bootstrap interval for the median contrast
was [-0.372, -0.124] s. `receipts.json` SHA-256 is
`0fa9ced5d918d2d0c0ce1f0613c88de0caf619ca270e9e45d091ea5e8e82fb88`.

## Decision and limitation

The preregistered lead700 timing gate passes. This establishes only that a
75%-prefix buffered read completed before a 0.7-second request can lower the
request-visible latency on this exact host/model. It does not establish an
arrival predictor, controller, total-work speedup, cross-model result, or a
CCF-B contribution.

`lead0` also had zero model residency at arrival yet often reduced latency.
That is an unplanned observation consistent with concurrent page-cache filling,
but it cannot be used as a confirmatory controller claim. The next gate must
separate completed-preparation benefit from concurrent-fill behavior and test a
held-out model or storage context under a newly frozen protocol.
