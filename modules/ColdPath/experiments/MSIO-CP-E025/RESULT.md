# MSIO-CP-E025 result

## Established observations

All 12 frozen trials exited zero and emitted exactly one `OK`; the final audit
found no `llama-cli` process and zero CUDA allocation. Raw receipts are at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E025/receipts.json`,
SHA-256 `64562545079f976112b246c88c6d71ccc7c71ff950eaf69255f3bf7d83be23b7`.

All six fixed75 trials had an active worker at the true 0.1-second arrival and
less than 70% residency (14.5%--42.7%; median 37.6%). Thus E025 realizes the
adversarial missed-deadline concurrent state that E024 did not.

## Descriptive foreground result

The fixed75-minus-none paired arrival-to-OK median was -0.122 s, with five of
six contrasts negative (none and fixed medians 2.457 and 2.350 s). This small
single-host sample is descriptive. It says this concurrent fill did not show
front-end harm under the frozen 0.1-second miss; it does not establish robust
forecast-error tolerance, total-work improvement, or a controller benefit.

## Decision

**PASS: adversarial concurrency qualification.** The action's arrival-time
state is directly observed under a material announcement error. The broader
conservative-policy performance claim remains closed by E024's failed
confirmation; E025 must not be used to reopen it.
