# ColdPath progress

- 2026-09-04: local design and Q0 protocol qualification completed.
- 2026-09-04: E000-A1 selected g129 after a four-host read-only audit.
- 2026-09-04: E001-A0 requests completed but its JSONL recorder was malformed; A1 reconstructed the ten raw responses without rerunning them. Frozen materiality threshold passed: 2235.43 ms median unloaded-model load versus 27.03 ms resident load (82.72x).
- Evidence boundary: one model/runtime/host; process/model residency only, with Linux page cache uncontrolled. No loading-path improvement has been demonstrated.
- Next exact gate: E002 loading-path implementation feasibility and storage-cold protocol design.
