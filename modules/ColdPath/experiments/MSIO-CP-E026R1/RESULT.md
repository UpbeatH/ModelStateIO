# MSIO-CP-E026R1 result

All 12 trials exited zero with exactly one `OK`; final process/GPU audit was
clean. Raw receipts: `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E026R1/receipts.json`, SHA-256
`776507331f6ff07963a0197b6a849063c08cbe6eba84024040e6308ed5681e19`.

All six fixed75 7B trials had an active worker at the hidden 0.1-second
arrival and under 70% residency (median 2.0%). Fixed75-minus-none paired
arrival-to-OK median was -1.688 s; all six contrasts were negative (medians
4.449 versus 6.094 s). **PASS: cross-model adversarial-concurrency
qualification.** This is descriptive g130 evidence only; it does not repair
E024's controller-performance No-Go, establish total-work reduction, or cure
the E023 local acquisition provenance boundary.
