# MSIO-CP-E016 effect-size decision

## Established evidence

Using the 18 valid E014 natural-warm-state receipts and six block-paired differences, a fixed-seed (20260904), 10,000-resample block bootstrap found no stable `mmap` advantage. The mean `none - mmap` difference was +0.0409 s (95% interval −0.2186 to +0.2926 s); `dio - mmap` was +0.0502 s (−0.1755 to +0.2691 s).

## Decision

**NO-GO for the ColdPath static load-mode action hypothesis.** Both uncertainty intervals cross zero and the paired effects reverse direction by block. Do not add samples, retune thresholds, or claim an optimizer/controller benefit from `mmap`/`none`/`dio` selection on this setup.

## Scope

This is not a claim that all model-state I/O research is infeasible. It closes only the frozen single-host, natural-warm, static-load-path action family. A future route would require a distinct, independently justified mechanism and fresh protocol.
