# MSIO-SP-E202 AdapterTxn / VersionGuard prior-art death gate

Date: 2026-09-06. Status: **AdapterTxn (generic lifecycle/capacity) NO-GO;
VersionGuard remains conditional**.

## Established source evidence

- Kiln's public implementation and documentation expose bounded online-LoRA
  SFT, atomic publication, live hot-swap, evaluation endpoints, and managed
  agent trajectories. A paper claiming only online publication or hot-swap
  would duplicate this scope.
- dLoRA (USENIX OSDI 2024) explicitly orchestrates requests and adapters by
  dynamic merge/unmerge and migration between worker replicas. Its paper and
  artifact therefore close the generic “schedule/swap/migrate adapters under
  capacity” contribution.
- S-LoRA provides unified paging of many concurrent LoRA adapters and KV
  tensors over shared base weights. Generic adapter admission, paging, or
  capacity management is not a defensible new mechanism.
- MinT (arXiv:2605.13779, 2026) keeps a base resident while exporting LoRA
  revisions through rollout, update, evaluation, serving, and rollback. A
  lifecycle-only AdapterTxn claim is adjacent to an already published
  end-to-end lifecycle abstraction.
- The local E200 result proved only idle global apply/disable on two adapters;
  it did not provide request isolation, a quality oracle, finite-capacity
  admission, or tenant-harm evidence. E201 already records the Kiln/S-LoRA
  audit and this gate adds dLoRA and MinT.

## Decision

The following claims are dead and must not be implemented as a paper:

1. generic online adapter attach/detach or hot-swap;
2. adapter paging, placement, or capacity admission without a new consistency
   invariant;
3. lifecycle orchestration, rollout, evaluation, serving, and rollback alone.

The only surviving candidate is a narrow **VersionGuard** mechanism: a
storage-aware transaction/lease protocol that prevents a request from ever
observing a mixed base-version/adapter-version pair while an adapter is being
evicted, restored, or replaced, with bounded rollback and tenant-visible harm
accounting. This is a hypothesis, not evidence of novelty or performance.

## Re-entry gate

Before any GPU experiment, VersionGuard must pass a source-level design audit
showing a concrete invariant and an implementation point absent from Kiln,
dLoRA, S-LoRA, and MinT. Then a new frozen experiment must use at least two
base revisions, three adapters, request-level version binding, a task-quality
oracle, finite HBM capacity, concurrent requests, and equal-information,
equal-action, equal-runtime baselines. Failure of the invariant or absence of
observable mixed-version harm is a No-Go.

Sources: [Kiln](https://github.com/ericflo/kiln),
[dLoRA OSDI'24](https://www.usenix.org/system/files/osdi24-wu-bingyang.pdf),
[S-LoRA](https://github.com/S-LoRA/S-LoRA),
[MinT arXiv:2605.13779](https://arxiv.org/abs/2605.13779).
