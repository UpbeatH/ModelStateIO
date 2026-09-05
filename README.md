# ModelStateIO

ModelStateIO studies how a single system stores, restores, moves, and protects model state across HBM, DRAM, and NVMe.

The original three-paper portfolio was organized by system problem rather than model technique:

1. `ColdPath`: cold-start and restoration data paths for model parameters.
2. `StateTier`: lifecycle-aware residency for weights, experts, adapters, and KV cache.
3. `LoadShield`: safe multi-tenant orchestration of model-state I/O.

Current status: the original ColdPath, StateTier/WeightResidency, LoadShield,
KVGuard, LayerReadyIO and StatePatch paper routes are closed under their
recorded evidence and scopes. `CallAhead` also stopped at its preregistered
E001 causal gate: full-model preparation improved background readiness, but
did not create a stable material foreground p95 harm for pacing to control.
PFSOpt remains the only cluster-active PFS line.

Start with [PORTFOLIO_DECISION.md](planning/PORTFOLIO_DECISION.md), the
[CallAhead design](modules/CallAhead/DESIGN.md), and its
[experiment plan](modules/CallAhead/EXPERIMENT_PLAN.md). The older
[THREE-PAPER-ROADMAP.md](planning/THREE-PAPER-ROADMAP.md) is retained as the
historical portfolio rationale.
