# MSIO-CA-E000M1R1 direct-CDN material gate

Status: frozen before execution. Date: 2026-09-05. This is a transport-only
revision of E000M1; artifact identity and decision thresholds are unchanged.

## Frozen method

1. Resolve the exact E000M1 revision/file through the official Hugging Face
   endpoint using the existing session-scoped local proxy.
2. Pass only that resolver-issued, time-limited CDN URL to g130. No mirror or
   alternate model source is allowed.
3. On g130 use direct HTTPS with HTTP range resume against the existing
   temporary file. Require the server to report the frozen object length.
4. After completion, require exact size `1,117,320,736` and SHA-256
   `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`.
5. Only after both checks pass, rename within `incoming/` to
   `qwen2.5-1.5b-instruct-q4_k_m.gguf` and verify owner, size and hash again.

The same exclusions as E000M1 apply. `PASS`, `MATERIAL_BLOCKED` and `NO_GO`
retain their exact meanings. The direct CDN transfer is acquisition evidence,
not loadability or performance evidence.

