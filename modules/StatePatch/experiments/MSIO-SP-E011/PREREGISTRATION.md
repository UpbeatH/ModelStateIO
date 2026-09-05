# MSIO-SP-E011 generated-text static lifecycle receipt

Run the same three arms as E010R3, but freeze extraction of generated text as
the lines after the echoed `> <prompt>` line and before the first `[ Prompt:`
telemetry line. Store raw stdout/stderr and the extracted text separately.
All other artifacts, CPU-only setting, prompt, seed, temperature, token bound,
timeouts, and `none -> attached -> none-after` order are unchanged.

PASS requires all arms exit zero, extracted base-only hashes match exactly,
attached extracted text differs, no residual llama process, and no GPU action.
This remains a new-process static contract only.
