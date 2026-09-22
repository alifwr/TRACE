# Artifact map

## Released in this repository

| Path | Role |
|---|---|
| `prompts/prompts.json` | 283 study prompts (160 topical + 123 Negative) |
| `data/nothink/*.pcap` | 603 TLS captures (`hash_rep_Vllm_t07.pcap`) |
| `data/nothink/Vllm_t07.json` | Session index: prompt text, ports, timestamps |
| `models/nothink_feat_s{42,0,1,123,7}/feat_multiclass_classifier_gbdt{0,1,2}.joblib` | TRACE LightGBM bags |
| `models/nothink_feat_s*/feat_multiclass_classifier_feat.json` | TRACE feature/ensemble metadata |
| `models/nothink_feat_s*/run_config.json` | Trainer settings for that seed |
| `expected/table1_per_seed.csv` | Per-seed accuracy and macro-F1 (five methods) |
| `expected/table2_pooled_confusion.csv` | TRACE confusion pooled over 605 test appearances |
| `expected/prediction_hashes.json` | SHA-256 of the original `test_results.csv` files |

TRACE boosters record 202 inputs (`max_feature_idx=201`). Duplicate `checkpoint_*` copies from the trainer were not shipped.

## Prediction files (not shipped)

Table verification still needs the original `test_results.csv` files. They live in the local experiment tree (override with `--runs`):

```
/home/pc/whisperleak/whisper_leak/results/runs
```

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

## Not stored here

Sequence-baseline checkpoints (Bi-LSTM, Sequence LightGBM, CNN, DistilBERT), DistilBERT tokenizer weights, vLLM serving flags, and `cisc-prism/main.tex`.
