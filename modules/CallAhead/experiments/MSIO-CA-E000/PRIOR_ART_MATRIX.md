# MSIO-CA-E000 mechanism-level prior-art matrix

Status: source-checked qualification evidence, 2026-09-05. This matrix is a
novelty screen, not a claim that omitted work is irrelevant. It distinguishes
the information source, physical state, action and protected resource because
changing only the state type or deployment scale is not a contribution.

| Work | Source-level mechanism checked | Overlap with CallAhead | Gap that remains, if any |
|---|---|---|---|
| ServerlessLLM, OSDI 2024 | Sections 3--6: loading-optimized checkpoint, multi-tier local checkpoint loading, locality-aware startup-time model scheduling and live migration | full-model weights, storage hierarchy, loading-cost model and locality-aware scheduling | request-triggered/distributed placement; no program-frontier notice contract or measured single-node preparation-victim harm controller |
| Parrot, OSDI 2024 | Sections 3--5: Semantic Variables expose application dataflow and request dependencies to the serving system | program/application structure is available before individual calls | optimizes request scheduling and semantic-variable dataflow, not full-weight state preparation with transition-debt/readiness accounting |
| USHER, OSDI 2024 | Sections 3--5: interference estimation plus placement/resource decisions to satisfy latency SLOs | interference-aware model-serving control and foreground protection | targets colocated GPU execution/resource allocation rather than user-space NVMe/page-cache weight warming before a future call |
| BlitzScale, OSDI 2025 | Sections 3--6: compute-network parameter transfer, O(1) host caching and layer-level live autoscaling | live weight transfer and eliminating wait for full model load | scale-out/scale-up after demand; not program-notice-driven local warming or its page-cache eviction/reload debt |
| HydraServe, NSDI 2026 | Sections 4--6: cold-start allocation, network-contention-aware placement, node prefetcher and overlapped fetch/load/initialization | proactive full-weight prefetch, explicit contention handling and SLO-aware resource choice | starts after worker allocation/cold-start demand; does not use a future program-call frontier or charge local victim reload debt |
| Agentix, NSDI 2026 | Section 4: process table, program-aware priority/preemption and locality-aware balancing; explicitly non-clairvoyant and initially DAG-agnostic | program-level context and multi-call optimization | does not predict/prepare future full-model weight state; its non-clairvoyant assumption is a useful baseline boundary |
| SYMPHONY, NSDI 2026 | advisory requests derived from user interaction/workload structure; priority/cooperative management under unreliable hints | advisory future-use signal, conservative state preparation and latency protection | manages KV cache in a disaggregated memory layer, not full-model transition bytes and eviction/reload debt; changing KV to weights alone would not be novel |
| PBKV, arXiv 2605.06472 v1 | Sections 4 and 6: predicts future workflow agent invocations; conservatively performs KV-cache eviction/prefetch under prediction error | the closest information/control analogue: future-step prediction, conservative prefetch, eviction and LRU comparison | physical object is reusable KV cache; CallAhead remains viable only if measured full-weight transition debt and foreground-harm pacing are independently necessary |
| PRESERVE, arXiv 2501.08192 / SPAA 2026 brief announcement | graph transformation inserts weight/KV prefetches that overlap off-chip reads with collectives | model-weight prefetch and graph-visible future execution | intra-inference L2 prefetch, not inter-call NVMe/DRAM/GPU state transitions or multi-model admission |
| Mooncake / IMPRESS / Bidaw / SolidAttention / mzCache | primary papers and local summaries: KV-cache tiering, admission, selective restoration/prefetch and negative-cache regimes | transition cost, selective preparation, tiering and negative regimes | the same accounting patterns are already known; they can motivate baselines but cannot establish weight-state novelty |
| llama.cpp multi-model router | frozen E031 source audit: `--models-dir`, `--models-preset`, `--models-max`, queue-on-limit and LRU eviction | inspectable local model-ID/load/queue/eviction boundary | reactive LRU only; no program-notice input or harm-bounded proactive action |

## Source pointers

- ServerlessLLM: <https://www.usenix.org/system/files/osdi24-fu.pdf>
- Parrot: <https://www.usenix.org/system/files/osdi24-lin-chaofan.pdf>
- USHER: <https://www.usenix.org/conference/osdi24/presentation/shubha>
- BlitzScale: <https://www.usenix.org/system/files/osdi25-zhang-dingyan.pdf>
- HydraServe: <https://www.usenix.org/system/files/nsdi26-lou.pdf>
- Agentix: <https://www.usenix.org/system/files/conference/nsdi26/nsdi26spring_luo_prepub.pdf>
- SYMPHONY: <https://www.usenix.org/conference/nsdi26/presentation/agarwal>
- PBKV: <https://arxiv.org/abs/2605.06472>
- PRESERVE: <https://arxiv.org/abs/2501.08192>
- Router evidence: `../../../ColdPath/experiments/MSIO-CP-E031/RESULT.md`

## Novelty qualification decision

**Conditional pass for requirement 1 only.** No checked work implements the
complete combination of (a) a pre-call program-frontier notice, (b) a
full-model NVMe/host/GPU transition, (c) measured eviction/reload debt, and
(d) pacing or abstention bounded by foreground harm on one constrained server.

The margin is narrow. Program awareness is already established by Parrot and
Agentix; conservative future-step prefetch/eviction is already established by
SYMPHONY and PBKV; full-weight prefetch and interference-aware loading are
already established by ServerlessLLM and HydraServe. Therefore CallAhead can
survive only if E001--E006 show that transition-debt and foreground-harm
accounting change actions and improve held-out outcomes. A policy that merely
ports PBKV/SYMPHONY from KV caches to weights is a scientific No-Go.

