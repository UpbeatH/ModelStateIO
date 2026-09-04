# MSIO-LS-E000 execution task

Run only the tracked `run_e000.py` at its committed revision after a fresh
g127 audit. It may create files only in its declared external log root.
Return exit status, raw root, SHA-256 of `receipts.json`, all receipt rows,
the `strace` Direct-I/O receipt, and final GPU/process cleanup state. Do not
retry or extend the matrix after any stop condition.
