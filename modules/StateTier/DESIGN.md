# StateTier design

Status: unactivated candidate.

Test whether state identity is causally necessary for HBM/DRAM/NVMe residency decisions. The first gate is a trace/schema counterexample: under equal capacity pressure, at least two of weights/experts, adapters, and KV state must prefer different actions because of reuse, recomputation, dirtiness, dependency, or deadline. If no reversal exists, stop; a unified controller is unnecessary.

Direct prior-art risk is high (DUAL-BLADE, mzCache, SolidAttention, Swarm, Tutti). No remote or performance work is authorized by this document.

