# StatePatch candidate decision

## Final decision: Research No-Go

The frozen current candidate is **No-Go as an independent CCF-B systems-paper
line**. E009/E011 establish artifact compatibility and a static new-process
LoRA attach/clean-restart contract, but that is a runtime capability rather
than a defensible systems mechanism.

## Established evidence

- Exact Apache-2.0 base plus two declared adapters were acquired, hash-verified
  and converted (E003/E009).
- A private, user-local conversion runtime was built and qualified (E007R2/E008).
- E011 shows deterministic base restoration and an attached-output change for
  one fixed prompt and one adapter with CPU-only CLI invocation.

## Why this fails the research bar

1. The control action is only startup-time `--lora`; there is no in-process
   attach/detach or a state-management protocol beyond process replacement.
2. There is no real adapter lifecycle/reuse trace, request stream, admission
   policy, capacity conflict, concurrent tenant, or isolation/harm measure.
3. No equal-information/action/runtime baseline, total cost accounting,
   task-quality oracle, workload variation, held-out adapter/model, or repeated
   robustness evidence exists.
4. Therefore any claimed storage-aware state-management contribution would be
   unsupported and the observed capability is insufficiently novel by itself.

## Retained assets and non-claims

Keep E003--E011 as reusable provenance/conversion infrastructure only. Do not
call it a StatePatch paper result or revive the static-action candidate without
a new mechanism that directly addresses online state transitions, capacity or
isolation under a real workload and is frozen as a new design.
