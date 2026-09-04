# MSIO-CP-E022R1 concurrent-fill snapshot correction

E022 is closed. It replicated completed 75% preparation but failed to establish concurrent-fill state because `prefetch_active_at_arrival` was recorded after `join()`.

E022R1 retains the exact E022 model, binary, measurement identity, three arms (`none`, completed 75%, concurrent 75%), six counterbalanced blocks, 75% byte budget, file-scoped cold-state/readback, timeout, correctness and cleanup rules. The only change is an immutable arrival-time snapshot taken before any `mincore`, model launch or worker join: monotonic timestamp, `worker.is_alive()`, worker completion timestamp if already present, and bytes read so far.

Completed replication uses the unchanged E022 completed-minus-none gate. Concurrent-fill evidence is admissible only if its arrival snapshot is active in all concurrent trials; otherwise E022R1 is technical No-Go. E022 raw evidence is not reused.
