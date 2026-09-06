# BranchDebt progress

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
