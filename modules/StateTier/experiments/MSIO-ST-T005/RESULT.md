# MSIO-ST-T005 result

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Observation

Twelve API requests were completed successfully for `qwen2.5:7b`: context
footprints 2048 and 8192, each with three `keep_alive=0` cold and three
`keep_alive=5m` resident requests. Cold totals ranged from 5.220 to 5.902 s
for 2048 and 5.469 to 5.571 s for 8192. After residency was established,
warm totals were approximately 0.206–0.249 s; the first warm request after a
cold unload reloaded the model and therefore remained ~5.08 s (2048) or ~5.31
s (8192). All responses were valid and exit code 0.

## Decision

`PASS` for same-model footprint execution and lifecycle logging. No reliable
context-dependent weight-residency effect was established. This is not
cross-model evidence and not a CCF-B result.

## Next gate

Freeze a bounded competing-I/O or memory-pressure protocol with a foreground
request and a background action, including a no-background control and
externality metrics. Do not infer pressure effects from T005.

