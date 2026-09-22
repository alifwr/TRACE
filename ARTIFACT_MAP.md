# Artifact map

Prediction files live in the local experiment tree, not in this repository.

Default root:

```
/home/pc/whisperleak/whisper_leak/results/runs
```

Override with `--runs`.

## Manuscript methods

| Paper name | Seed | Directory | `test_results.csv` SHA-256 (prefix) |
|---|---:|---|---|
| TRACE | 42 | `nothink_feat_s42` | `efffcfaa45d885d1…` |
| TRACE | 0 | `nothink_feat_s0` | `4965276ba26955c7…` |
| TRACE | 1 | `nothink_feat_s1` | `96e95445b20ecf0d…` |
| TRACE | 123 | `nothink_feat_s123` | `f964d0ad6b8c90a5…` |
| TRACE | 7 | `nothink_feat_s7` | `50265ff5f7f044c0…` |
| Bi-LSTM | 42 | `nothink_lstm` | `20ff0f80e71ed663…` |
| Bi-LSTM | 0–7 | `nothink_lstm_s{0,1,123,7}` | see `expected/prediction_hashes.json` |
| Seq. LGBM | 42 | `nothink_lgbm` | `3277ad97e90486d2…` |
| Seq. LGBM | 0–7 | `nothink_lgbm_s*` | see JSON |
| CNN | 42 | `nothink_cnn` | `d2d618e6f85a6049…` |
| CNN | 0–7 | `nothink_cnn_s*` | see JSON |
| DistilBERT | 42 | `nothink_bert` | `bc819af0495c8cde…` |
| DistilBERT | 0–7 | `nothink_bert_s*` | see JSON |

Full hashes are in `expected/prediction_hashes.json`. TRACE boosters record 202 inputs (`max_feature_idx=201`).

## Published tables in this repo

| File | Role |
|---|---|
| `expected/table1_per_seed.csv` | Per-seed accuracy and macro-F1 (five methods) |
| `expected/table2_pooled_confusion.csv` | TRACE confusion pooled over 605 test appearances |

## Not stored here

Prompts (`prompts/topics/prompts.json`), captures (`data/nothink`), selected checkpoints, DistilBERT weights, vLLM flags, and `cisc-prism/main.tex`.
