# LoadShield design

Status: E000 No-Go for the isolated 7B Direct-I/O versus 0.5B cold-launch
mechanism; no active LoadShield experiment.

Test whether concurrent model-state I/O creates a stable affected set and predictable foreground p99 harm distinct from GPU compute saturation. Only after that causal gate may an admission/defer/throttle policy be compared with FIFO, greedy, fixed cap, shortest-load, and deadline/slack baselines under equal offered load.

The historical GPU data-pipeline study retained high GPU utilization despite NVMe interference, so generic "storage starves GPU" is not an acceptable premise. This route needs model-state-specific causal evidence.

MSIO-LS-E000 supplied a clean negative result for one such causal test: even
with verified O_DIRECT, per-file foreground cold state, and live overlap, the
background read did not produce stable foreground harm. Do not revive this
mechanism through post-hoc pressure expansion. Any future route must identify
a different state-I/O externality and freeze its own causal gate first.
