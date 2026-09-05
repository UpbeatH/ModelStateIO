# MSIO-CA-E000H1 result

Status: **PASS**. Executed once on g130 at 2026-09-05T11:58:34Z.
Evidence level: technical harness qualification only; not performance evidence.

## Observations

- The hash-pinned Qwen2.5 0.5B foreground server became healthy on loopback
  port 18110 and returned valid JSON with nonempty content for all four frozen
  one-token requests.
- The separate Qwen2.5 1.5B worker read exactly 830,472,192 bytes, the frozen
  75% chunk-rounded budget, in 3.094 s. Its measured rate was 268,428,997 B/s,
  below the 268,435,456 B/s ceiling and well below the 110% failure bound.
- `mincore` observed the prepared range at 0% residency immediately after the
  file-scoped eviction and 100% after preparation. All four foreground
  receipts observed the worker still active after the request.
- During the smoke, the foreground server used about 685 MiB RSS and the GPU
  snapshot reported 900 MiB allocated. The bounded server log was 4,341 bytes.
- Post-run checks found no matching server or runner, no lock, and 0 MiB GPU
  allocation.

## Decision

E000 requirement 5 **passes**: the private runner can bound and observe a
foreground service and a concurrent preparation worker without global cache,
system, CUDA, driver, service, PFS/Lustre or g129 changes.

This result does not establish foreground harm, readiness benefit, pacing
benefit or a CallAhead controller advantage. Those claims remain forbidden
until their own frozen gates pass.

Raw receipt and server log remain outside Git at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CA-E000H1/`.
