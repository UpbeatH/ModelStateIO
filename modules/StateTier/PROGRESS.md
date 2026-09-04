# StateTier progress

- 2026-09-04: this branch activated StateTier locally; ColdPath is owned by another branch.
- 2026-09-04: read-only audits of g127/g128 completed. g127 is provisionally preferred for a future StateTier gate because its V100S GPU had no compute process and `/mnt/nvme3n1` had about 1.3 TB free. g128 was not selected because Milvus streamingnode was using about 159% CPU and multiple data services were active.
- Evidence: current node observation plus hypothesis only; no StateTier performance result.
- E000 preflight reached `NOT_RUN`: no verified multi-state trace was found and `/mnt/nvme3n1` is shared with active Kubernetes/MinIO services. No scientific hypothesis was tested.
- Follow-up inspection of the only candidate JSONL confirmed it is a generic `idx/ttft/metric/text` result (SHA-256 recorded in `RESULT.md`), not a StateTier trace.
- T001 collection qualification also reached `NOT_RUN`: observation tools and Ollama are present, but the proposed external directory is absent, root-owned shared storage is ambiguous, and no workload was started.
- After explicit directory authorization, two `qwen2.5:7b` collection probes both timed out at 90 seconds with empty output (exit 124). Classified as technical failure; no scientific evidence was obtained.
- An API-based diagnostic succeeded: cold request ~7.98 s (load ~7.86 s), warm request ~0.26 s, both correct. Classified `PARTIAL` because only weight residency was observed; no second state class was exposed.
- T002 API context probe succeeded: model residency and a 32,768-token context limit were visible; a second request returned in ~0.21 s. No KV byte/residency/eviction signal was exposed, so the multi-state hypothesis remains untested.
- T003 passed the single-state residency capability gate: three `keep_alive=0` versus `5m` pairs were correct, with cold totals 4.665–5.408 s and warm totals 0.218–0.223 s. This is not a CCF B result; larger model/pressure/baseline validation remains required.
- T004 model-footprint expansion is `BLOCKED_INPUT`: Ollama currently contains only qwen2.5:7b; no second model was downloaded or run.
- T005 passed same-model footprint execution (context 2048/8192, 12 successful API requests). Cold totals were ~5.2–5.9 s and established warm totals ~0.21–0.25 s; no context-dependent residency effect was established.
- T006 passed a bounded externality probe: a concurrent read-only 1 GiB model-blob read produced 0.212–0.243 s foreground totals versus 0.205–0.232 s for two valid warm controls; the first control was a reload and excluded. Capability evidence only, not CCF B.
- Final validation decision: `NO-GO` for CCF-B evidence on the current g127 Ollama platform. T004–T006 exhausted the available single-model, single-interface evidence; further repetitions would be pseudo-replication. See `WEIGHT_RESIDENCY_DECISION.md`.
- I001 audit corrected: CUDA toolkits 11.2/12.2/12.8/12.9 are installed on 127 but `nvcc` is absent from PATH; `/usr/local/cuda` points to 12.8. No dependency or service change was performed. Building with an absolute toolkit path is feasible; the second-model input remains missing.
- Final decision 2026-09-04: `NO-GO` for the unified multi-state StateTier route under the current Ollama/V100S platform. The preregistered stop condition was met: no second independently controllable state class was observable after the T001/T002 probes. This is a scientific scope decision, not a claim that typed state management is impossible elsewhere.
- Downgrade path: retain a separately scoped single-state cold/warm weight-residency study only if a new protocol and contribution are authored; do not call it StateTier multi-state evidence.
- I001 re-entry environment result: a user-local CUDA llama.cpp build and a
  second 0.5B GGUF footprint are now available on g127. `mmap` versus `none`
  have distinct syscall-level loading receipts and GPU correctness smokes; the
  requested `dio` path did not produce observed `O_DIRECT` and is excluded.
  This reopens only the separately scoped single-state WeightResidency study,
  not the prior unified multi-state StateTier route.
- Next exact gate: freeze and run the smallest two-model, `mmap` versus `none`,
  equal-budget WeightResidency falsification protocol after a new host audit.
