# Evaluation protocol (from the CISC-W 2026 draft)

Copied here as documentation. If this file and the draft ever disagree, the draft wins.

## Task and corpus

- Model served: Qwen3.5-9B (`Qwen/Qwen3.5-9B`) via vLLM, through a CDN, HTTP/2, TLS 1.3.
- Streaming on, reasoning off, temperature 0.7.
- Capture dates: 1–2 September 2026 (KST). New TLS connection per session.
- Capture window: ClientHello until response consumption. Filtering keeps server-to-client TLS application-data only.
- Each trace is one isolated, pre-segmented response.
- 40 English prompts × 4 topics (travel, cooking, climate, sports), each replayed three times.
- 123 general-knowledge Negative prompts, recorded once.
- 283 prompts, 603 traces. Labels follow source-prompt list membership.
- Everyday-topic separability test, not sensitive-category detection.

Checkpoint revision and vLLM release were not recorded.

## Splits

- Stratified, prompt-grouped: all replays of one prompt stay in one partition.
- 20% of prompts for test; 10% of the remainder for validation.
- Seeds `{42, 0, 1, 123, 7}`.
- Per seed: 203 / 23 / 57 train / val / test prompts; 433 / 49 / 121 traces.
- Test: 8 prompts (24 traces) per topic and 25 Negative prompts.
- Five test sets give 5 × 121 = 605 trace *appearances* drawn from the 603-trace corpus (reuse across seeds).
- Methods share partitions **within each seed**.

## TRACE

- 202 features from complete traces (k-fingerprinting / CUMUL families).
- Families: 33 summary + 96 cumulative curves + 16 size histogram + 17 groups/first differences + 40 first/last sizes.
- Cumulative curves: 48 points, scaled by byte and time totals.
- Histogram: 0–1024 bytes.
- A new record group starts when an arrival gap exceeds the trace’s 80th-percentile inter-arrival time.
- No z-score on TRACE features.
- Three LightGBM models, different seeds; feature fractions 60/70/80%; row fractions 70/80/90% without replacement.
- Max 2,000 boosting iterations, learning rate 0.03, at most 15 leaves.
- Stop after 60 iterations without validation multiclass log-loss improvement.
- Saved models retain the best 73–397 iterations across the five seeds.
- Prediction: highest mean class probability.

Local trainer name: `FEAT` (`FeatureGBDTClassifier`).

## Baselines (local implementations, not exact reproductions)

- Sequence LightGBM, attention Bi-LSTM, DistilBERT (Whisper Leak families); CNN (website-fingerprinting motivation).
- Sequence length: train-split 95th percentile (1,223–1,303 records).
- Neural inputs: train-split mean/SD standardization.
- Sequence LightGBM: unstandardized flattened sizes and timings.
- DistilBERT: 50 equal-count training bins; size tokens then timing tokens; 512-token cap (510 measurements). For 487 of 605 test appearances the trace has ≥510 records, so timing tokens are dropped. Tokenizer correspondence to the original run source is unverified.
- Neural: Adam 10⁻⁴, max 80 epochs, patience 12 on validation accuracy, restore best checkpoint.
- Sequence LightGBM: max 1,000 iterations, patience 12 on validation multiclass log-loss.
- CNN batch size 32 on seed 42 and 16 otherwise.

## Metrics

- Accuracy and macro-F1 from saved `target` / `prediction`.
- Macro-F1: unweighted mean of the five class F1 scores **within each seed**, then mean across seeds.
- Majority baseline: always Negative → 25/121 = 0.207 accuracy; macro-F1 0.068.
- Uniform expected accuracy 0.200 (analytical, not a sampled run).
- Comparisons are descriptive: reused splits and replays are dependent.
