# ColdPath progress

- 2026-09-04: local design and Q0 protocol qualification completed.
- 2026-09-04: E000-A1 selected g129 after a four-host read-only audit.
- 2026-09-04: E001-A0 requests completed but its JSONL recorder was malformed; A1 reconstructed the ten raw responses without rerunning them. Frozen materiality threshold passed: 2235.43 ms median unloaded-model load versus 27.03 ms resident load (82.72x).
- Evidence boundary: one model/runtime/host; process/model residency only, with Linux page cache uncontrolled. No loading-path improvement has been demonstrated.
- E002 read-only inspection found only Ollama's opaque runtime; no supported second loading path with effective-setting readback. Technical NO-GO under the frozen gate.
- ColdPath is paused pending approved existing source/runtime or isolated dependency installation; no second performance experiment was started.
- E003 isolated-install authorization selected g130 and preserved g129; source acquisition is blocked only by g130 GitHub reachability and Windows-to-g130 SCP stalling. No build has begun.
