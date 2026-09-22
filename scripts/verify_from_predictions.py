#!/usr/bin/env python3
"""Recompute CISC TRACE tables from retained predictions. No training."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [42, 0, 1, 123, 7]
MODELS = [
    ('feat', 'TRACE', 'nothink_feat'),
    ('lstm', 'Bi-LSTM', 'nothink_lstm'),
    ('lgbm', 'Seq. LGBM', 'nothink_lgbm'),
    ('cnn', 'CNN', 'nothink_cnn'),
    ('bert', 'DistilBERT', 'nothink_bert'),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run_dir(runs: Path, token: str, seed: int) -> Path:
    named = runs / f'{token}_s{seed}'
    if named.is_dir():
        return named
    if seed == 42 and (runs / token).is_dir():
        return runs / token
    return named


def confusion(pred: Path):
    rows = list(csv.DictReader(pred.open()))
    cm = [[0] * 5 for _ in range(5)]
    for row in rows:
        cm[int(row['target'])][int(row['prediction'])] += 1
    n = len(rows)
    acc = sum(cm[i][i] for i in range(5)) / n
    f1s = []
    for i in range(5):
        denom = sum(cm[i]) + sum(c[i] for c in cm)
        f1s.append((2 * cm[i][i] / denom) if denom else 0.0)
    return acc, sum(f1s) / 5, cm, n


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--runs', type=Path,
        default=Path('/home/pc/whisperleak/whisper_leak/results/runs'),
    )
    args = parser.parse_args()
    expected = json.loads((ROOT / 'expected' / 'prediction_hashes.json').read_text())
    hash_by = {(r['trainer_token'], r['seed']): r for r in expected['predictions']}
    table1 = {
        (r['model'], int(r['seed'])): r
        for r in csv.DictReader((ROOT / 'expected' / 'table1_per_seed.csv').open())
    }
    errors = []
    pooled = [[0] * 5 for _ in range(5)]

    for token, name, prefix in MODELS:
        for seed in SEEDS:
            d = run_dir(args.runs, prefix, seed)
            pred = d / 'test_results.csv'
            if not pred.is_file():
                errors.append(f'missing {pred}')
                continue
            digest = sha256(pred)
            rec = hash_by[(token, seed)]
            if digest != rec['prediction_sha256']:
                errors.append(f'{d.name}: hash {digest} != {rec["prediction_sha256"]}')
            acc, mf1, cm, n = confusion(pred)
            if n != 121:
                errors.append(f'{d.name}: n={n} != 121')
            exp = table1[(token, seed)]
            if abs(acc - float(exp['accuracy'])) > 1e-12 or abs(mf1 - float(exp['macro_f1'])) > 1e-12:
                errors.append(f'{d.name}: metrics drifted acc={acc} f1={mf1}')
            if token == 'feat':
                for i in range(5):
                    for j in range(5):
                        pooled[i][j] += cm[i][j]
            print(f'{name:12} seed {seed:4}  acc {acc:.3f}  macro-F1 {mf1:.3f}  {d.name}')

    conf_rows = list(csv.reader((ROOT / 'expected' / 'table2_pooled_confusion.csv').open()))
    for i, row in enumerate(conf_rows[1:]):
        got = [int(x) for x in row[1:]]
        if got != pooled[i]:
            errors.append(f'pooled row {row[0]}: {pooled[i]} != {got}')
    if sum(sum(r) for r in pooled) not in (0, 605):
        errors.append(f'pooled total {sum(sum(r) for r in pooled)} != 605')

    if errors:
        print('VERIFY FAIL', file=sys.stderr)
        for e in errors:
            print(' -', e, file=sys.stderr)
        return 1
    print('verified Table 1 and Table 2 against hashed predictions')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
