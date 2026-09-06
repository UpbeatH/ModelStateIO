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

VersionGuard was considered as a narrow storage-aware transaction/lease
protocol that prevents a request from observing a mixed base-version/
adapter-version pair. The source audit does not clear it: MinT already makes
adapter revisions, attribution, rollout, evaluation, serving, recovery and
rollback first-class lifecycle state, while Kiln and dLoRA cover atomic/live
transition and request/adapter orchestration. Adding a digest check or a
rollback lease to those existing lifecycle operations is an implementation
detail, not a defensible standalone CCF-B mechanism. VersionGuard is therefore
also **research No-Go** under the current scope.

## Re-entry gate

No new GPU experiment is justified. Re-entry would require a materially new
storage mechanism beyond lifecycle versioning itself (for example a proven
cross-tier commit protocol with a failure mode absent from all four systems),
not merely a new name for version checks or rollback.

Sources: [Kiln](https://github.com/ericflo/kiln),
[dLoRA OSDI'24](https://www.usenix.org/system/files/osdi24-wu-bingyang.pdf),
[S-LoRA](https://github.com/S-LoRA/S-LoRA),
[MinT arXiv:2605.13779](https://arxiv.org/abs/2605.13779).
