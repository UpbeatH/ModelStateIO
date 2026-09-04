#!/usr/bin/env python3
import argparse, json
from pathlib import Path

FORBIDDEN = {'drop_caches', 'sysctl', 'remount', 'raw_device', 'undocumented'}

def classify(label, method, evidence):
    if label == 'natural_warm' and method == 'normal_process_start' and evidence:
        return {'decision': 'ACCEPT', 'state': 'natural_warm', 'reason': 'audited_warm_no_cache_control'}
    if label == 'explicit_cold' and method not in FORBIDDEN and evidence:
        return {'decision': 'ACCEPT', 'state': 'explicit_cold', 'reason': 'audited_non_global_cold_method'}
    if label == 'unknown':
        return {'decision': 'ABSTAIN', 'state': 'unknown', 'reason': 'insufficient_state_evidence'}
    return {'decision': 'NO_GO', 'state': label, 'reason': 'forbidden_or_missing_state_evidence'}

def main():
    p = argparse.ArgumentParser(); p.add_argument('--label', required=True); p.add_argument('--method', required=True); p.add_argument('--evidence', action='store_true'); p.add_argument('--output', required=True)
    a = p.parse_args(); result = classify(a.label, a.method, a.evidence); Path(a.output).write_text(json.dumps(result, sort_keys=True) + '\n', encoding='utf-8'); print(json.dumps(result, sort_keys=True)); return 0 if result['decision'] in {'ACCEPT', 'ABSTAIN'} else 2

if __name__ == '__main__': raise SystemExit(main())

