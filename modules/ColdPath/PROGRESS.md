# ColdPath progress

- 2026-09-04: local design and Q0 protocol qualification completed.
- 2026-09-04: E000-A1 selected g129 after a four-host read-only audit.
- 2026-09-04: E001-A0 requests completed but its JSONL recorder was malformed; A1 reconstructed the ten raw responses without rerunning them. Frozen materiality threshold passed: 2235.43 ms median unloaded-model load versus 27.03 ms resident load (82.72x).
- Evidence boundary: one model/runtime/host; process/model residency only, with Linux page cache uncontrolled. No loading-path improvement has been demonstrated.
- E002 read-only inspection found only Ollama's opaque runtime; no supported second loading path with effective-setting readback. Technical NO-GO under the frozen gate.
- ColdPath is paused pending approved existing source/runtime or isolated dependency installation; no second performance experiment was started.
- E003 isolated-install authorization selected g130 and preserved g129; source acquisition is blocked only by g130 GitHub reachability and Windows-to-g130 SCP stalling. No build has begun.
- MSIO-CP-E018/E019 passed conditional readiness and fractional-residency
  gates; E020 rejected content placement at fixed bytes. MSIO-CP-E021 then
  passed the 75%-prefix, 0.7-second lead-time qualification on g130: 5/6
  paired improvements and 10.50% median request-latency reduction. This is
  limited to one host/model and does not validate a controller. The unplanned
  lead0 observation must not be promoted without a new protocol.
- 2026-09-05: the original controller remains closed by E024/E028. E029 tested
  separate `RiskPrefetch` re-entry material without a GPU run. The available
  public Qwen trace has event timing but no non-oracle notice, model/adapter
  identity, state size, outcome, or contention fields, so the candidate is
  inactive (NO-GO on this material). Re-entry requires a provenance-complete
  application/scheduler trace with two or more state identities and a
  user-scoped harm measurement.
- 2026-09-05: E030 closed the unmodified-runtime ArrivalSplit fallback: model
  loading and context creation share a sequential source path. E031 found a
  documented multi-model router/LRU boundary and two private GGUF files, but no
  admissible admission trace, user-scoped interference measure, or complete
  7B acquisition record. Router capability passed technically; performance and
  paper activation are NO-GO on current material.
