#!/usr/bin/env python3
import argparse, json, statistics, sys
from pathlib import Path

def analyze(receipt_dir, expected_experiment):
    receipts = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(Path(receipt_dir).glob('*.receipt.json'))]
    if len(receipts) != 18:
        raise ValueError(f'incomplete_count:{len(receipts)}:expected:18')
    for r in receipts:
        if not str(r.get('trial', '')).startswith(('b1-', 'b2-', 'b3-', 'b4-', 'b5-', 'b6-')):
            raise ValueError('invalid_trial_id')
    modes = {}
    for mode in ('mmap', 'none', 'dio'):
        values = [float(r['time_to_ok_s']) for r in receipts if r.get('mode') == mode]
        if len(values) != 6:
            raise ValueError(f'incomplete_mode:{mode}:{len(values)}')
        median = statistics.median(values)
        mad = statistics.median(abs(v - median) for v in values)
        modes[mode] = {'n': 6, 'median_time_to_ok_s': median, 'mad_time_to_ok_s': mad, 'robust_cv': 1.4826 * mad / median}
    return {'experiment': expected_experiment, 'expected_trials': 18, 'valid_trials': 18, 'modes': modes, 'decision': 'PASS' if all(v['robust_cv'] <= 0.15 for v in modes.values()) else 'NO_GO'}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--receipt-dir', required=True)
    p.add_argument('--experiment', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    try:
        result = analyze(a.receipt_dir, a.experiment)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f'REJECTED:{exc}', file=sys.stderr)
        return 2
    Path(a.output).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

