# LoadShield progress

- 2026-09-04: candidate specified; held behind affected-set causal gate.
- MSIO-LS-E000 completed on g127 with six paired defer/overlap blocks. All
  Direct-I/O, cold-state, overlap, correctness, and cleanup receipts passed,
  but overlap did not harm foreground cold-launch latency: only 2/6 paired
  contrasts were positive and the median contrast was -0.164 s. `NO-GO` for
  this isolated storage-I/O mechanism; do not expand it by adding pressure or
  repetitions. A future LoadShield proposal needs distinct prior evidence and
  a newly frozen protocol.
