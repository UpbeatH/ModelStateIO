# MSIO-KVG-E001 execution task

First verify g130 private-directory ownership, no server process, zero GPU use,
model SHA-256 and absent E001 output. Build only the existing configured target
with `cmake --build build-d230ddd-cuda116-sm70 --target llama-server -j2`;
do not install it. Copy this runner to the private incoming directory and run
once with a 600-second bound. Return build exit, runner exit, receipt hash and
final process/GPU audit. Stop on the first failure; do not rerun or start a
performance comparison.
