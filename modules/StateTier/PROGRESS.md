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
- Final decision 2026-09-04: `NO-GO` for the unified multi-state StateTier route under the current Ollama/V100S platform. The preregistered stop condition was met: no second independently controllable state class was observable after the T001/T002 probes. This is a scientific scope decision, not a claim that typed state management is impossible elsewhere.
- Downgrade path: retain a separately scoped single-state cold/warm weight-residency study only if a new protocol and contribution are authored; do not call it StateTier multi-state evidence.
- Next exact gate: obtain a provenance-verified trace with at least two state classes, or stop/re-scope to a bounded single-state experiment.
