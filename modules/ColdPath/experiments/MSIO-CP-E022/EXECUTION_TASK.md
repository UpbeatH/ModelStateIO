# MSIO-CP-E022 execution task

After a fresh g130 audit verifies no GPU work, the pinned runtime/model/measure
hashes, and a fresh E022 log root, run the tracked script once. It may write
only under its stated external log root. Return receipts hash, all rows, and
final GPU/process cleanup. Stop without retry on any failure code.
