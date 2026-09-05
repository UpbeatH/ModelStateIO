# MSIO-SP-E010R3 documented single-turn lifecycle contract

Only change from E010R2: use help-confirmed `--single-turn --simple-io
--log-disable --no-display-prompt --color off` to force one non-interactive
turn and remove UI/prompt telemetry from stdout. Preserve all artifacts,
CPU-only setting, prompt, seed, temperature, token bound, arm order, timeout,
and hash rule. Complete receipts for all three arms are mandatory.
