# Direct prior-art pressure test

Checked 2026-09-04. This is a qualification matrix, not a full systematic review.

| Work | Established mechanism (paper/repository level) | Route threatened | Consequence |
|---|---|---|---|
| DUAL-BLADE (arXiv:2604.26557) | Dynamically chooses page-cache or NVMe-direct KV path and overlaps storage I/O with GPU DMA. | ColdPath, StateTier | Dynamic path selection and overlap cannot be claimed as new. |
| mzCache (arXiv:2609.01338) | Fine-grained weight/KV buffers, partial eviction, ordered restore, and restore/prefill overlap on mobile devices. | ColdPath, StateTier | Partial restore, ordering, and mixed memory/storage restoration are prior art. |
| Swarm (arXiv:2603.17803) | Co-activation-aware KV placement across SSDs with replication and adaptive retrieval. | StateTier | Semantic grouping and adaptive SSD placement alone are insufficient. |
| Tutti (arXiv:2605.03375) | GPU-centric SSD-backed KV object path with GPU io_uring and slack-aware scheduling. | StateTier, LoadShield | GPU-driven direct storage and slack scheduling are occupied mechanisms. |
| CoLLM (ICDCS 2026 artifact) | Collaborative parameter loading/inference across constrained devices; public llama.cpp-derived artifact requires multiple Raspberry Pi devices. | ColdPath | Parameter-loading optimization alone is not a gap. |
| Cappuccino (ICDCS 2026 artifact) | Multi-LoRA scheduling/serving; published artifact examples target newer CUDA/A100-class setups. | StateTier, LoadShield | Adapter multiplexing and batching alone are insufficient; V100 feasibility must be demonstrated separately. |

Candidate gap, still a **hypothesis**: none of the checked works establishes a portable, typed model-state contract spanning cold readiness, mixed-state lifecycle, and externality-safe admission under equal-information/action/runtime evaluation. The three routes must test that claim separately; they must not be packaged as a single oversized system before individual gates pass.

Primary entry points:

- https://arxiv.org/abs/2604.26557
- https://arxiv.org/abs/2609.01338
- https://arxiv.org/abs/2603.17803
- https://arxiv.org/abs/2605.03375
- https://github.com/jzdypo/llama.cpp-collm
- https://github.com/icloud-ecnu/Cappuccino

