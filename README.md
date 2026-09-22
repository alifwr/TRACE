# CISC-W 2026 TRACE — reproducibility support

Support package for:

**Beyond the Sequence: Evaluating Traffic Features for Encrypted LLM Topic Inference**

(CISC-W 2026 draft. TRACE = Traffic-descriptor Classification Ensemble.)

This repository contains the study prompts, the captured traffic used in the draft, the trained TRACE models, the evaluation protocol, published table values, prediction-file hashes, and a verifier that recomputes Tables 1–2 from retained `test_results.csv` files.

## Released artifacts

| Path | Contents |
|---|---|
| `prompts/prompts.json` | 283 study prompts: 40 × travel / cooking / climate / sports (`repeat: 3`) and 123 Negative (`repeat: 1`). Labels follow list membership. |
| `data/nothink/*.pcap` | 603 packet captures (`<prompt-hash>_<rep>_Vllm_t07.pcap`). |
| `data/nothink/Vllm_t07.json` | Per-session metadata (prompt text, ports, timestamps) aligned with those pcaps. |
| `models/nothink_feat_s{42,0,1,123,7}/` | Trained TRACE ensemble for each reported seed: three LightGBM bags (`feat_multiclass_classifier_gbdt{0,1,2}.joblib`), `feat_multiclass_classifier_feat.json`, and `run_config.json`. |
| `expected/` | Published-table CSVs and SHA-256 hashes of the original prediction files. |
| `scripts/verify_from_predictions.py` | Recomputes accuracy, macro-F1, and the pooled TRACE confusion matrix. |
| `PROTOCOL.md` | Evaluation protocol as written in the draft. |

Sequence-baseline checkpoints (Bi-LSTM, Sequence LightGBM, CNN, DistilBERT) are not included: DistilBERT and Bi-LSTM weights are hundreds of megabytes to over a gigabyte per method.

## Name mapping

| Paper | Local trainer token | Run directories |
|---|---|---|
| TRACE | `FEAT` | `nothink_feat_s{42,0,1,123,7}` |
| Bi-LSTM | `LSTM` | `nothink_lstm` (seed 42) and `nothink_lstm_s{0,1,123,7}` |
| Sequence LightGBM | `LGBM` | `nothink_lgbm` / `nothink_lgbm_s*` |
| CNN | `CNN` | `nothink_cnn` / `nothink_cnn_s*` |
| DistilBERT | `BERT` | `nothink_bert` / `nothink_bert_s*` |

## Verify published tables

The verifier reads saved prediction CSVs (not the models or pcaps). Point `--runs` at a `results/runs` tree that still has those files:

```bash
python3 scripts/verify_from_predictions.py --runs /path/to/whisper_leak/results/runs
```

The script exits nonzero if a prediction file is missing, its SHA-256 differs from `expected/prediction_hashes.json`, or recomputed metrics differ from `expected/table1_per_seed.csv` / `expected/table2_pooled_confusion.csv`.

This is a **saved-prediction audit**. Loading the released TRACE models or recapturing traffic is a separate step.

## What this does not establish

- Feature-only attribution (pipelines still differ)
- Generalization beyond the 603-trace closed-world corpus
- Exact Qwen checkpoint revision, vLLM release, or run-pinned tokenizer source
- A formula-level inventory of every 202-d coordinate

See `PROTOCOL.md` and `ARTIFACT_MAP.md`.
