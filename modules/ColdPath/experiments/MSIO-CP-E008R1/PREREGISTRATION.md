# MSIO-CP-E008R1 runner-observability integration correction

Frozen: 2026-09-04. This new ID corrects only E008's shell decision-parser quoting failure; it does not rerun E007 or claim model evidence.

## Contract

Run the same three deterministic guard fixtures as E008 (`no-process`, `transient-fixture`, `persistent-fixture`) using the E008 `guard_receipt.py` and unit-test logic, but validate decisions with shell `grep` rather than embedded Python quoting. Require complete receipts, checksum output, completion sentinel, and no `llama-cli` process. No model, GPU workload, cache, system, PFS, Lustre, g129, or remote experiment is used.

## Decision

PASS requires all three expected decisions, unit tests, checksum and completion sentinel. Any missing artifact is No-Go. A PASS permits a new measurement ID; it does not resume E007/E008.

