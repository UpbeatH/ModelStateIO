# ModelStateIO

ModelStateIO studies how a single system stores, restores, moves, and protects model state across HBM, DRAM, and NVMe.

The three-paper doctoral line is deliberately organized by system problem rather than model technique:

1. `ColdPath`: cold-start and restoration data paths for model parameters.
2. `StateTier`: lifecycle-aware residency for weights, experts, adapters, and KV cache.
3. `LoadShield`: safe multi-tenant orchestration of model-state I/O.

Current status: local qualification only. No live host audit or performance run has occurred. `ColdPath` is the first local candidate; none of the three modules is cluster-active.

Start with [THREE-PAPER-ROADMAP.md](planning/THREE-PAPER-ROADMAP.md) and [MSIO-Q000](experiments/MSIO-Q000/RESULT.md).

