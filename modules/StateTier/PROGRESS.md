# StateTier progress

- 2026-09-04: this branch activated StateTier locally; ColdPath is owned by another branch.
- 2026-09-04: read-only audits of g127/g128 completed. g127 is provisionally preferred for a future StateTier gate because its V100S GPU had no compute process and `/mnt/nvme3n1` had about 1.3 TB free. g128 was not selected because Milvus streamingnode was using about 159% CPU and multiple data services were active.
- Evidence: current node observation plus hypothesis only; no StateTier performance result.
- E000 preflight reached `NOT_RUN`: no verified multi-state trace was found and `/mnt/nvme3n1` is shared with active Kubernetes/MinIO services. No scientific hypothesis was tested.
- Follow-up inspection of the only candidate JSONL confirmed it is a generic `idx/ttft/metric/text` result (SHA-256 recorded in `RESULT.md`), not a StateTier trace.
- Next exact gate: obtain a provenance-verified trace with at least two state classes, or stop/re-scope to a bounded single-state experiment.
