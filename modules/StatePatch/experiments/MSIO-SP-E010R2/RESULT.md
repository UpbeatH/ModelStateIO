# MSIO-SP-E010R2 result: incomplete three-arm execution

**Technical No-Go; incomplete.** The first base-only arm completed with zero
stderr, but neither attached nor final base-only receipt exists and no parent
failure receipt identifies the interruption. E010R2 must not be resumed or
used for output comparison. Its sole observation is that the current CLI emits
interactive UI text to stdout, so a successor must use a documented single-run
output mode and isolate generated text from UI/telemetry before hashing.
