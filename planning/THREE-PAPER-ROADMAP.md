# ModelStateIO three-paper roadmap

Status date: 2026-09-04. Evidence labels are explicit below.

## Unifying dissertation question

**Hypothesis:** model state has typed lifecycles and deadlines that conventional byte-oriented paging, caching, and per-job I/O policies do not expose. A storage-aware control plane can use those semantics to reduce readiness latency and tail interference while preserving correctness and bounded resource harm.

This is not yet an established gap. Direct prior art already exploits KV semantics, partial restoration, loading order, caching, and I/O/compute overlap. The line survives only if its typed-state contract and cross-context evidence add capabilities that the strongest systems do not already provide.

## Route 1 — ColdPath

- **Question:** under changing model size, memory pressure, storage device, and reuse distance, when should a cold model use page-cache faults, explicit buffered prefetch, direct/asynchronous I/O, or a hybrid path?
- **Mechanism hypothesis:** a typed loading plan that exposes layer readiness, dependency order, memory headroom, and path setup cost can minimize p95 time-to-ready/TTFT without trading it for excessive bytes, CPU time, or foreground harm.
- **Strong baselines:** unmodified framework loading; mmap/page cache; sequential buffered read; fixed direct-I/O path where supported; oracle chosen after observing all arms.
- **Smallest real gate:** one V100S host, one verified local NVMe, two model footprints (fits and exceeds effective HBM), cold/warm states, randomized order, at least five valid repetitions per cell. Live hardware and software must be re-audited first.
- **Go:** on held-out contexts, at least 10% lower median p95 time-to-ready than the best fixed deployable baseline, 95% bootstrap interval excluding zero, no correctness failure, and no more than 5% foreground p99 harm.
- **No-Go:** benefit is explained by ordinary readahead alone; selection loses to the best fixed path under equal information/runtime; or gains fail held-out model/device-pressure groups.
- **Claim ceiling before the gate:** protocol hypothesis only.

## Route 2 — StateTier

- **Question:** can one lifecycle-aware residency contract jointly manage immutable weights/experts, small adapters, and request-scoped KV state across HBM, DRAM, and NVMe?
- **Mechanism hypothesis:** reuse horizon, recomputation cost, dirtiness, dependency position, and restore deadline define distinct state classes; enforcing per-class placement and transition rules will dominate a single generic eviction/cache policy.
- **Strong baselines:** independent LRU/LFU-style tiers; state-specific best published/reproducible policies; capacity-matched static partitions; offline oracle.
- **Zero-cluster gate:** trace/schema study must show that at least two state classes reverse their preferred action under the same capacity pressure. Otherwise the unified contract adds no necessity.
- **Smallest real gate:** replay the same request sequence and byte budget across isolated state classes, then a mixed workload; report hit/restore bytes, p95 TTFT, throughput, HBM/DRAM peak, CPU overhead, and write amplification.
- **Go:** mixed-state policy improves the primary tail metric by at least 10% over the strongest capacity-matched baseline and retains at least half that effect on held-out mixes, without correctness or endurance regression.
- **No-Go:** per-class independent policies match it; state identity is unnecessary; or profiling/transition overhead repays the gain.
- **Direct novelty threat:** DUAL-BLADE, mzCache, SolidAttention, Swarm, and Tutti already cover important parts of KV/weight placement and restore. A mere multi-tier cache is not publishable novelty.

## Route 3 — LoadShield

- **Question:** how should a node admit, defer, order, or throttle concurrent model loads, adapter swaps, KV restores, and checkpoints so that one job's state I/O does not violate another job's latency objective?
- **Mechanism hypothesis:** an affected-set contract using storage queueing, cache displacement, PCIe/DMA contention, and deadline slack can protect foreground p99 better than per-job greedy loading while maintaining useful aggregate throughput.
- **Strong baselines:** FIFO; work-conserving greedy; fixed bandwidth cap; shortest remaining load; deadline/slack scheduling; clairvoyant oracle.
- **Zero-cluster gate:** controlled local traces must demonstrate repeatable cross-job harm attributable to state I/O, not GPU compute saturation alone.
- **Smallest real gate:** one node first, with foreground inference plus one background state action; randomized pair order and equal offered load. Four-host work is out of scope until the single-node causal gate passes and each host is re-audited.
- **Go:** reduce foreground p99 violation rate by at least 30% relative to the best non-oracle baseline while retaining at least 90% aggregate useful throughput; no starvation and bounded cancellation waste.
- **No-Go:** no reproducible affected set; simple I/O capping matches the policy; or GPU compute is the dominant confounder.
- **Direct novelty threat:** admission/SLO scheduling is mature. Novelty requires model-state-specific externality attribution and a validated safe contract, not a new scheduler name.

## Portfolio order and publication logic

- First local/real candidate: `ColdPath`, because it has the cheapest causal experiment and can falsify the platform fit quickly.
- Second candidate: `LoadShield` only if ColdPath exposes reproducible externality; otherwise test `StateTier`'s state-identity necessity gate.
- `StateTier` is the broadest and highest-overlap route; it stays unactivated until its necessity test passes.
- Graduation safety target: each route must be independently publishable. A mature CCF B evidence package is preferred to premature CCF A scope expansion; venue rating must be checked against the designated local CCF directory when submission planning begins.
- Exactly one line may consume cluster time. At present that remains PFSOpt; ModelStateIO is local-only.

