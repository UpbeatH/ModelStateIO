#!/usr/bin/env python3
import argparse
import json
import math
import random
import statistics
from pathlib import Path

REQUESTS = 160
BLOCKS = 6
BOOTSTRAPS = 20000
SEED = 20260905

def nearest_rank(values, q):
    values = sorted(values)
    return values[max(0, math.ceil(q * len(values)) - 1)]

def percentile_type7(values, q):
    values = sorted(values)
    h = (len(values) - 1) * q
    lo = math.floor(h); hi = math.ceil(h)
    if lo == hi:
        return values[lo]
    return values[lo] + (h - lo) * (values[hi] - values[lo])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('receipt')
    ap.add_argument('--output')
    args = ap.parse_args()
    data = json.loads(Path(args.receipt).read_text())
    if not data.get('completed') or data.get('cleanup', {}).get('model_process_present'):
        raise SystemExit('experiment or cleanup incomplete')
    rows = data.get('rows', [])
    if len(rows) != BLOCKS * 3:
        raise SystemExit(f'expected 18 rows, got {len(rows)}')
    compact = []
    for row in rows:
        req = row['requests']
        if len(req) != REQUESTS:
            raise SystemExit(f"{row['label']}: request count")
        if any(x['http_status'] != 200 or not x['content_present'] for x in req):
            raise SystemExit(f"{row['label']}: correctness")
        compact.append({
            'label': row['label'], 'block': row['block'],
            'position': row['position'], 'arm': row['arm'],
            'foreground_p95_s': nearest_rank([x['latency_s'] for x in req], .95),
            'foreground_p50_s': statistics.median(x['latency_s'] for x in req),
            'max_schedule_lag_s': max(x['schedule_lag_s'] for x in req),
            'preparation_bytes': row['preparation']['actual_bytes'],
            'preparation_s': row['preparation']['duration_s'],
            'preparation_bps': row['preparation']['achieved_bps'],
            'cold_residency_fraction': row['cold']['resident_fraction'],
            'prepared_residency_fraction': row['after_preparation']['resident_fraction'],
            'background_ready_s': row['background_probe']['wall_s'],
            'background_probe_returncode': row['background_probe']['returncode'],
        })
    by_block = {}
    for row in compact:
        by_block.setdefault(row['block'], {})[row['arm']] = row
    paired = []
    for block in range(1, BLOCKS + 1):
        arms = by_block[block]
        if set(arms) != {'none', 'eager75', 'paced75'}:
            raise SystemExit(f'block {block}: missing arm')
        n, e, p = arms['none'], arms['eager75'], arms['paced75']
        harm = (e['foreground_p95_s'] - n['foreground_p95_s']) / n['foreground_p95_s']
        excess = e['foreground_p95_s'] - n['foreground_p95_s']
        recovery = ((e['foreground_p95_s'] - p['foreground_p95_s']) / excess
                    if excess > 0 else None)
        paired.append({
            'block': block, 'eager_relative_p95_harm': harm,
            'pacing_recovery_fraction': recovery,
            'eager_readiness_benefit_s': n['background_ready_s'] - e['background_ready_s'],
            'paced_readiness_benefit_s': n['background_ready_s'] - p['background_ready_s']})
    harms = [x['eager_relative_p95_harm'] for x in paired]
    rng = random.Random(SEED); boot = []
    for _ in range(BOOTSTRAPS):
        sample = [harms[rng.randrange(BLOCKS)] for _ in range(BLOCKS)]
        boot.append(statistics.median(sample))
    median_harm = statistics.median(harms)
    recoveries = [x['pacing_recovery_fraction'] for x in paired
                  if x['pacing_recovery_fraction'] is not None]
    eager_benefit = statistics.median(x['eager_readiness_benefit_s'] for x in paired)
    paced_benefit = statistics.median(x['paced_readiness_benefit_s'] for x in paired)
    preserved = paced_benefit / eager_benefit if eager_benefit > 0 else None
    interval = [percentile_type7(boot, .025), percentile_type7(boot, .975)]
    all_checks = (all(x['background_probe_returncode'] == 0 for x in compact)
                  and data['cleanup']['gpu']['rows'][0]['memory_used_mib'] == 0)
    decision = bool(all_checks and median_harm >= .10 and interval[0] > 0
                    and recoveries and statistics.median(recoveries) >= .50
                    and preserved is not None and preserved >= .50)
    out = {
        'experiment_id': 'MSIO-CA-E001',
        'status': 'GO' if decision else 'NO_GO',
        'analysis_unit': 'paired_block',
        'foreground_quantile': 'nearest_rank_p95_of_160',
        'bootstrap': {'seed': SEED, 'resamples': BOOTSTRAPS,
                      'interval': 'type7_percentile_95'},
        'all_correctness_action_cleanup_checks_passed': all_checks,
        'median_eager_relative_p95_harm': median_harm,
        'eager_relative_p95_harm_ci95': interval,
        'positive_eager_excess_blocks': len(recoveries),
        'median_pacing_recovery_fraction_on_positive_excess_blocks':
            statistics.median(recoveries) if recoveries else None,
        'median_eager_readiness_benefit_s': eager_benefit,
        'median_paced_readiness_benefit_s': paced_benefit,
        'paced_preserved_readiness_fraction': preserved,
        'thresholds': {'eager_harm_min': .10, 'harm_interval_lower_gt': 0,
                       'pacing_recovery_min': .50,
                       'preserved_readiness_min': .50},
        'paired_blocks': paired,
        'trials': compact,
    }
    text = json.dumps(out, indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(text)
    else:
        print(text, end='')

if __name__ == '__main__':
    main()
