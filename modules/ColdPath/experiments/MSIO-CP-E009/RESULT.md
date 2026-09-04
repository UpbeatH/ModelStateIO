# MSIO-CP-E009 result

## Decision

Technical **NO-GO**. E009 is closed and must not be resumed.

## Established observation

Ten model trials completed correctly. Before the eleventh model invocation, the guard recorded the current SSH inspection command as a `llama-cli` process because it searched the full command line with `pgrep -f '[l]lama-cli'`. The schedule stopped at `b4-p2-dio` before the model was launched; the lock was released and GPU usage returned to 0 MiB.

This is a runner self-match defect, not model-state or performance evidence. A new E009R1 ID corrects only the process matching and preserves the frozen measurement design.

