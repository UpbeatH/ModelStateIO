# MSIO-CE-D002-TR1-P1 token-budget repair

Status: frozen after P0 technical diagnosis and before P1 output.
Date: 2026-09-08.

P0 completed all 24 HTTP calls, but 17 returned `finish_reason=length` at the
frozen 900-token output cap: fourteen had no final content and three contained
truncated non-JSON content. HTTP status, returned model identity, usage, and
thinking receipts were otherwise present. P0 is preserved as
`P0_NO_GO_TO_PROMPT_EXPANSION`, driven by a technical output-budget defect.

P1 is the sole technical repair. It preserves every P0 message, run order,
model, thinking/high request, no-tools contract, stateless call, scoring rule,
and 24-call budget. The only request change is `max_tokens: 4096`. It uses a
new experiment ID and external `attempt-001` root; it does not overwrite or
selectively retry P0 rows.

The frozen P0 Go/No-Go thresholds apply unchanged. Any remaining invalid
outputs count normally. There is no further prompt, temperature, reasoning,
token-budget, parser, model, or gateway repair after P1. A Go opens immediate
real-system design; a No-Go stops this API/prompt branch.
