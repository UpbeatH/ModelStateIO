# MSIO-ST-T006 result

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Observation

Three control requests and three requests concurrent with a read-only 1 GiB
direct read of the Ollama model blob completed with exit code 0 and valid
responses. Control totals were 5.527 s, 0.232 s, and 0.205 s; the first is a
model reload and was excluded from the warm-state comparison. Warm control
totals were therefore 0.232 and 0.205 s. Competing-read totals were 0.243,
0.212, and 0.232 s. Background reads completed successfully.

## Decision

`PASS` for a bounded externality capability probe: the foreground API remained
correct while a 1 GiB background read ran. With only two valid warm controls
and three competition samples, this is not a CCF-B result and does not
establish robustness or a causal policy benefit.

## Next gate

Freeze a larger randomized pressure protocol only if a second approved model or
stronger controllable loading path becomes available. Otherwise the current
single-model Ollama line should be downgraded to an engineering feasibility
result rather than expanded into a CCF-B claim.

