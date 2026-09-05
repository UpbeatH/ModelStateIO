# CallAhead progress

- 2026-09-05: candidate created as a design-only successor informed by, but
  scientifically separate from, the closed ColdPath controller.
- Established input evidence: ColdPath fixed preparation and concurrent fill
  can reduce request-visible latency on the tested g130 models; the old
  announced-lead controller, total-cost generalization and interference claim
  remain No-Go.
- Current hypothesis: program-visible future-call structure may enable safe
  model warming only when transition debt and foreground harm are included in
  admission and pacing.
- 2026-09-05: E000 closed PASS. The official, hash-pinned model set now
  contains Qwen2.5 0.5B, Qwen2.5 1.5B and SmolLM2 1.7B; the prior-art matrix
  narrows novelty to transition-debt/foreground-harm-aware pacing.
- 2026-09-05: E000H1 technical harness qualification passed: 4/4 foreground
  requests completed while an exact 830,472,192-byte, 256 MiB/s preparation
  ran; file residency changed 0% -> 100%, and cleanup left no process or GPU
  residue. This is not performance evidence.
- Current evidence level: E000 material/runtime/harness qualification only.
  No causal harm, pacing recovery, real program notice or controller advantage
  has been established.
- 2026-09-05: E001 completed 18/18 trials and closed the present mechanism as
  NO-GO. Median eager relative foreground p95 harm was 0.12%, bootstrap 95%
  interval [-3.01%, 5.90%], failing both the 10% effect and positive-interval
  requirements. Eager/paced preparation improved background readiness by
  about 0.402/0.400 s, but pacing had no stable material harm to control.
- Current decision: stop E002--E006. Do not rescue E001 with a larger model,
  pressure, changed load/rate/window or extra repetitions. A new branch-debt
  admission candidate requires direct novelty clearance and a real
  three-model program trace with capacity conflict before any new run.
- 2026-09-06: E200 source audit is a material No-Go. The audited public router
  benchmarks expose per-query model outcomes/costs but no non-oracular program
  frontier, arrival, state-residency or capacity-conflict trace. They cannot
  be relabelled as CallAhead input.
- 2026-09-06: E201 independently expanded the search to real serving and
  agent traces (FineServe, TraceLab, AgentTrace and agent-llm-traces). Each
  lacks at least the prospective physical-state capacity contract; CallAhead
  remains material No-Go and no replay/controller execution is opened.
