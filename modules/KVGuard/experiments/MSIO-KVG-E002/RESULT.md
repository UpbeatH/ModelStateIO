# MSIO-KVG-E002 result

**Technical No-Go: recomputation baseline contaminated.** All six response
contents matched and teardown was clean, but long-prefix fresh recomputation
was 0.915 s in the first block and about 0.02--0.03 s later. The server's
default RAM prompt cache leaked prior-context information into the supposedly
fresh baseline. No action-reversal inference is admissible. E002 is closed;
its raw receipt SHA-256 is
`ef1a038da9f7dab6c705336e8ce96f37bec32fd699a9e755391c29590528c38c`.
