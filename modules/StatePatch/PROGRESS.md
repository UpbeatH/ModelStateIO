# StatePatch progress

- E001R1: technical lifecycle GO for one public GSM8K LoRA against the earlier
  Q4 GGUF; not a quality, isolation, capacity, or controller result.
- E002: second-adapter compatibility observation inconclusive because the
  earlier Q4 GGUF had no verifiable base revision and cleanup was signal-unsafe.
- E003: exact-base acquisition GO. The official Qwen base revision and two
  SatSec seed adapters are Apache-2.0, byte-complete and hash-verified in the
  Git-external acquisition root. This removes only the provenance blocker.
- E004: private dependency installation succeeded, but the frozen `/usr/bin/python3`
  3.8.10 cannot import the current converter because it uses Python 3.9+
  built-in generic syntax. E004 is Technical No-Go for that interpreter; raw
  logs remain outside Git in `modelstateio-runtime/logs/MSIO-SP-E004/`.
- E005: private Python 3.10.14 build succeeded, but it lacks `_sqlite3` and
  `_ctypes`, and failed the frozen complete-standard-library smoke. It is
  Technical No-Go for that broad runtime criterion; the converter-specific
  subset is not decided.
- Next gate: E006 separately qualifies the exact current llama.cpp converter
  dependencies under the E005 private Python, without claiming E005 passed.
  E006 itself is closed before installation because its frozen PyPA bootstrap
  URL returned 404. E006R1 corrected the URL and installed the dependency tree,
  but is Technical No-Go at `torch` import because E005 lacks `_ctypes`. E007
  repaired these private build prerequisites: E007R2 is Technical GO for a
  fresh Python 3.10.14 against user-local libffi and SQLite. E008 installed and
  qualified the exact converter dependency tree (both `--help` paths pass).
  E009 transferred, rehashed and converted the exact base plus two adapters;
  E011 then passed the narrow static text lifecycle contract. The candidate is
  Research No-Go: static startup-time adapter attachment has no online state
  mechanism, capacity/admission conflict, isolation, task-quality or
  equal-budget systems evidence. See `DECISION.md`.
  Afterwards, a separate protocol still needs a genuine lifecycle trace,
  capacity conflict, correctness oracle, and isolation/harm measurement before
  StatePatch can be evaluated as a paper candidate.
- 2026-09-06: upstream llama.cpp source/API inspection and g130 read-only
  audit identify a new online hot-swap capability not tested by the static
  CLI route. MSIO-SP-E200 is frozen as an idle-only technical lifecycle gate;
  it cannot inherit any paper-level Go from E011.
