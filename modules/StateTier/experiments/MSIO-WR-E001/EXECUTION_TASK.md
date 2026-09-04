# MSIO-WR-E001 execution task

Execute only after a fresh read-only g127 audit passes the preregistration.
This task creates files only below the declared user-owned log directory; it
does not change services, drivers, CUDA, mounts, caches, or model files.

1. Verify `nvidia-smi`, `free -h`, `df -h /mnt/nvme3n1`, model SHA-256, and
   no foreign GPU process. Abort and report if any preregistration stop rule
   applies.
2. Create a timestamped log directory under the declared E001 root.
3. Execute the six frozen runs (three paired blocks) per model in the specified AB/BA/AB order
   using `/usr/bin/time -f` and `timeout 240`; collect `nvidia-smi` before
   and after each process. Do not retry a failed sample.
4. Return only a compact CSV/JSON summary plus raw-log path and SHA-256; do
   not interpret the result as a systems-paper claim.
