# BranchDebt progress

## 2026-09-06 local large-artifact acquisition complete

- The frozen 7B/14B/32B set is complete locally: 11/11 independently verified
  shards, `36,933,341,696` total bytes, zero remaining `.part` files and zero
  manifest mismatch. This is acquisition evidence only.
- Both bounded automatic SCP modes were nonviable. E300 is at a technical
  transfer stop pending one Termius directory upload to g130. No GPU,
  loadability, physical-capacity or trace claim is inherited from the local
  files.

## 2026-09-06 E300 prospective-material checkpoint

- Pinned AgentTrace source commit
  `8ce41dd7f7d2a8709b17287168bc788f291ac674` supplied 400 distinct MBPP
  prompts with embedded executable assertions. Historical outputs and timings
  were not imported.
- The frozen compiler produced 300 development tasks and a hash-only receipt
  for 100 held-out tasks. Git-external receipts on g130:
  `development.jsonl` SHA-256
  `be203d6e9d2a372a14bd5b3ed5ecab5c43abbc37205f3444db8b210069ba3850`;
  `heldout-receipt.json` SHA-256
  `2ac3ecbb8aff30d27567540d827e48bc36d1684866edf333f06017dd3552953c`.
- The prospective workflow is now frozen as 7B primary plus a pre-verifier
  14B/32B repair frontier. Pass opens no repair; assertion-only failure routes
  to 14B; structural/resource failure routes to 32B. No artificial notice
  delay is permitted.
- Generated-code isolation is technically available through the existing
  immutable Docker image digest
  `sha256:261bbe628f4b438f5bf10de5a8ee05282f2697a5a2cb7ff7668f776b61b9d586`
  with Python 3.6.8. Host-Python execution is prohibited.
- The bounded verifier integration smoke passed again on g130 after the
  pre-outcome branch-entropy revision: a correct candidate returned `pass/0`,
  one failed assertion returned `assertion_minor/31`, two failed assertions
  returned `assertion_major/32`, and no `msio-bd-e300-*` container remained. The
  verifier uses an unprivileged UID, read-only bind/root, no network,
  capability drop, no-new-privileges, CPU/memory/PID limits, bounded output
  observation and forced owned-container cleanup. This is technical execution
  qualification only, not workload or performance evidence.
- Before opening any E300 task outcome, the branch contract was strengthened
  to require at least ten natural events each for no-call, 14B minor repair and
  32B major/structural repair in the first 100 tasks. This prevents a nominal
  two-candidate frontier from degenerating into an always-14B policy. Failure
  of this frozen entropy gate is E300 No-Go rather than permission to reorder
  or add tasks.
- The frozen task-structure audit at revision `3c90205` passed on all 300
  development prompts: every prompt contains exactly three independently
  executable assertion lines. No model output was opened. This qualifies the
  minor-versus-major assertion routing contract without post-hoc task
  exclusion.
- E300 is not yet PASS: the 11 frozen official model shards are still being
  acquired and must pass size/hash, per-model loadability, measured HBM and
  physical eviction/reload checks. A later preflight found the earlier
  unrelated g130 GPU process gone; every future run must still repeat the
  idle-GPU check.
- The pinned native-router smoke at code revision `eead901` passed. With three
  provenance-complete small models and `models_max=2`, the third explicit load
  evicted the first model through native LRU; status readback matched the
  expected `unloaded/loaded/loaded` state and postflight was clean. This closes
  only the technical action/readback question, not physical capacity or
  performance qualification.

- 2026-09-06: candidate created as a clean successor to CallAhead, not a
  reopened E001. `MSIO-BD-E300` is the only active ID. Existing three small
  provenance-complete models total about 2.66 GB and cannot establish physical
  conflict on a 32 GB V100. GPU execution is deferred while another user's
  process is present.
- 2026-09-06: AgentTrace source was acquired read-only at commit
  `8ce41dd7f7d2a8709b17287168bc788f291ac674` under the g130 private source
  root. Official Qwen 7B-Q4, 14B-Q4 and 32B-Q5 shard identities are frozen;
  their total 36.9 GB exceeds V100 HBM, pending acquisition and actual
  per-model load/HBM measurements.
- 2026-09-06: the first acquisition launch transferred zero bytes and exposed
  a missing wall-time bound. Its exact owned process tree was terminated and
  the empty target preserved. The runner now freezes a 20-second connect bound,
  60-second low-speed stop and 45-minute per-shard wall bound before retry.
- 2026-09-06: the bounded g130 retry also could not reach the official CDN.
  Windows proxy preflight reached the pinned object and D: has 286 GiB free;
  a checksum-equivalent isolated Windows acquisition path is frozen, without
  changing the E300 artifact set or scientific threshold.
