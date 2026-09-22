# CISC-W 2026 TRACE — private reproducibility support

Support package for verifying the numerical claims in:

**Beyond the Sequence: Evaluating Traffic Features for Encrypted LLM Topic Inference**

(CISC-W 2026 draft. TRACE = Traffic-descriptor Classification Ensemble.)

This repository is **not** a public artifact release. The manuscript states that no public release is committed for prompts, feature matrices, evaluation code, or serving configurations. This package therefore contains only:

- the evaluation protocol as written in the draft
- published table values
- SHA-256 hashes of the retained prediction files
- a verifier that recomputes accuracy, macro-F1, and the pooled TRACE confusion matrix from those files

It does **not** contain prompts, packet captures, feature matrices, trained models, tokenizer weights, serving flags, or the paper source. The CISC draft was not edited when this repository was created.

## Name mapping

| Paper | Local trainer token | Run directories |
|---|---|---|
| TRACE | `FEAT` | `nothink_feat_s{42,0,1,123,7}` |
| Bi-LSTM | `LSTM` | `nothink_lstm` (seed 42) and `nothink_lstm_s{0,1,123,7}` |
| Sequence LightGBM | `LGBM` | `nothink_lgbm` / `nothink_lgbm_s*` |
| CNN | `CNN` | `nothink_cnn` / `nothink_cnn_s*` |
| DistilBERT | `BERT` | `nothink_bert` / `nothink_bert_s*` |

LSTM–BERT exists among historical runs and is omitted from the current draft.

## Verify published tables

Point `--runs` at the retained `results/runs` directory (default: this machine’s Whisper Leak tree):

```bash
python3 scripts/verify_from_predictions.py
python3 scripts/verify_from_predictions.py --runs /path/to/whisper_leak/results/runs
```

The script exits nonzero if a prediction file is missing, its SHA-256 differs from `expected/prediction_hashes.json`, or recomputed metrics differ from `expected/table1_per_seed.csv` / `expected/table2_pooled_confusion.csv`.

This is a **saved-prediction audit**. It does not retrain models or recapture traffic.

## What this does not establish

- Feature-only attribution (pipelines still differ)
- Generalization beyond the 603-trace closed-world corpus
- Exact Qwen checkpoint revision, vLLM release, or run-pinned tokenizer source
- A formula-level inventory of every 202-d coordinate
- Public availability of the underlying data

See `PROTOCOL.md` and `ARTIFACT_MAP.md`.
