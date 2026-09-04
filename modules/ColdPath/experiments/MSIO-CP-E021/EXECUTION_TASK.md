# MSIO-CP-E021 execution task

After a fresh g130 audit confirms an idle GPU, the three pinned artifact hashes,
and a fresh E021 log root, run the tracked script once. It may create files
only below its external log root. Return exit status, `receipts.json` hash,
all compact receipt rows, and final process/GPU cleanup evidence. Do not retry
or modify the schedule after a stop condition.
