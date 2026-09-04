# StateTier progress

- 2026-09-04: this branch activated StateTier locally; ColdPath is owned by another branch.
- 2026-09-04: read-only audits of g127/g128 completed. g127 is provisionally preferred for a future StateTier gate because its V100S GPU had no compute process and `/mnt/nvme3n1` had about 1.3 TB free. g128 was not selected because Milvus streamingnode was using about 159% CPU and multiple data services were active.
- Evidence: current node observation plus hypothesis only; no StateTier performance result.
- E000 preflight reached `NOT_RUN`: no verified multi-state trace was found and `/mnt/nvme3n1` is shared with active Kubernetes/MinIO services. No scientific hypothesis was tested.
- Follow-up inspection of the only candidate JSONL confirmed it is a generic `idx/ttft/metric/text` result (SHA-256 recorded in `RESULT.md`), not a StateTier trace.
- T001 collection qualification also reached `NOT_RUN`: observation tools and Ollama are present, but the proposed external directory is absent, root-owned shared storage is ambiguous, and no workload was started.
- After explicit directory authorization, two `qwen2.5:7b` collection probes both timed out at 90 seconds with empty output (exit 124). Classified as technical failure; no scientific evidence was obtained.
- An API-based diagnostic succeeded: cold request ~7.98 s (load ~7.86 s), warm request ~0.26 s, both correct. Classified `PARTIAL` because only weight residency was observed; no second state class was exposed.
- Next exact gate: obtain a provenance-verified trace with at least two state classes, or stop/re-scope to a bounded single-state experiment.
