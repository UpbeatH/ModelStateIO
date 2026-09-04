# MSIO-CP-E021 asynchronous lead-time gate

Status: frozen; no result yet. Date: 2026-09-04 (Asia/Shanghai).

## Question

Can a fixed 75%-prefix asynchronous prefetch retain request-visible readiness
benefit when the actual request arrives before, during, or after preparation?
This is the first timing-sensitivity gate after E018 (completed preparation)
and E019 (fractional residency).

## Frozen design

- Host, binary, model, prompt, mmap mode, correctness, timeout, and file-scoped
  cold-state method are the E019 identities on g130.
- Arms: `none`; `lead0` (launch immediately after prefetch starts); `lead300`
  (0.300 s actual lead); `lead700` (0.700 s actual lead).
- Active arms start one buffered sequential read of the first 75% of the owned
  GGUF. The read uses no GPU. At request arrival, record `mincore` residency
  and whether the prefetch worker is still alive; then launch foreground mmap
  inference. All active arms finish their same 75%-byte background action.
- Six counterbalanced four-arm blocks yield 24 trials. Each begins with only
  file-scoped `POSIX_FADV_DONTNEED`, a two-second settle, and required <=20%
  cold residency. No global cache operation, system change, retry, or sample
  extension is allowed.

## Outcomes and decision

Primary: arrival-to-first-exact-OK. Secondary: trigger-to-OK, resident fraction
at arrival, background duration/completion, correctness, and cleanup.

`lead700` passes timing qualification only if all trials are correct and clean,
at least five of six paired `lead700 - none` request-latency contrasts are
negative, and its paired median reduction is at least 10%. Otherwise No-Go for
this 75%-prefix timing mechanism. Regardless of outcome, do not call this a
predictor, controller, total-work speedup, or cross-model result.
