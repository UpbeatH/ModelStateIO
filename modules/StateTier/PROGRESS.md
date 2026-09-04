# StateTier progress

- 2026-09-04: this branch activated StateTier locally; ColdPath is owned by another branch.
- 2026-09-04: read-only audits of g127/g128 completed. g127 is provisionally preferred for a future StateTier gate because its V100S GPU had no compute process and `/mnt/nvme3n1` had about 1.3 TB free. g128 was not selected because Milvus streamingnode was using about 159% CPU and multiple data services were active.
- Evidence: current node observation plus hypothesis only; no StateTier performance result.
- Next exact gate: freeze a StateTier E000 packet for the state-identity necessity test, then repeat the read-only audit immediately before any execution.
