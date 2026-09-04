# MSIO-CP-E027 non-repeated cost/overlap audit

## Audit rule

For E025 and E026R1 only, `trigger_to_ok_s` is the wall-clock interval from
preparation notice through foreground completion and background-worker join;
it therefore counts the artificial actual-lead wait and does not price
prefetch as free. `arrival_to_ok_s` is request-visible only. `none` is
comparable within the same frozen block because it shares that notice/arrival
schedule. This does not establish CPU, DRAM, energy, system-wide I/O or
opportunity cost.

## Established derived observations

E025 mean trigger-to-OK was 2.990 s for fixed75 versus 3.136 s for none;
E026R1 was 5.094 s versus 6.857 s, respectively. E026R1's 7B background
preparation completed in approximately 3.0--3.2 s while overlapping the
foreground path. These are host-local derived summaries of raw receipt fields,
not a new experiment or independent replication.

## Non-comparability and decision

E023 has no compatible `trigger_to_ok_s`, arrival timestamp, or background
completion field, so it cannot enter this total-cost comparison. E024 is not
comparable because its three-policy/lead schedule differs. The audit permits
the bounded statement that overlapping preparation did not increase the
recorded notice-to-completion wall time in E025/E026R1. It is **NO-GO for any
broader work-conservation or total-system-cost claim**: process CPU, cache
displacement, concurrent tenants and repeated decision workload remain
unmeasured.
