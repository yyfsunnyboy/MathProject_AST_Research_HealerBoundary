# Qwen Phase 1 interim report

This document is a **Qwen Phase 1 interim report**. Gemini Phase 2 is not completed. No full three-model conclusions are drawn. New seeds are not used for rule development.

All tables below are generated programmatically.

## Model `qwen3.5:4b` (`qwen35_4b`)

### A. Per seed

| seed | PASS/48 | FAIL/48 | failure-layer counts |
|---|---:|---:|---|
| 2026071301 | 6/48 | 42/48 | L1:20, L3:4, L4:10, L5:8 |
| 2026072001 | 4/48 | 44/48 | L1:17, L3:6, L4:8, L5:13 |
| 2026072002 | 5/48 | 43/48 | L1:19, L2:5, L3:5, L4:6, L5:8 |
| 2026072003 | 6/48 | 42/48 | L1:16, L2:3, L3:4, L4:9, L5:10 |
| 2026072004 | 8/48 | 40/48 | L1:18, L2:5, L3:3, L4:7, L5:7 |

### B. Five-seed pooled

- pooled PASS: **29/240** (0.1208)
- seed-level mean ± SD: **0.1208 ± 0.0276**

### C. Task–condition stability (48 groups × 5 seeds)

- stable_pass (5/5): 1; stable_fail (0/5): 34; unstable (1–4/5): 13

### D. Prompt condition comparison

| condition | pooled PASS | seed mean | seed SD |
|---|---:|---:|---:|
| ab1 | 11/80 | 0.1375 | 0.0468 |
| ab2g | 7/80 | 0.0875 | 0.0306 |
| ab2d | 11/80 | 0.1375 | 0.0729 |

## Model `qwen3.5:9b` (`qwen35_9b`)

### A. Per seed

| seed | PASS/48 | FAIL/48 | failure-layer counts |
|---|---:|---:|---|
| 2026071301 | 7/48 | 41/48 | L1:15, L2:2, L3:4, L4:5, L5:15 |
| 2026072001 | 9/48 | 39/48 | L1:15, L2:2, L3:6, L4:4, L5:12 |
| 2026072002 | 6/48 | 42/48 | L1:19, L2:1, L3:3, L4:4, L5:15 |
| 2026072003 | 6/48 | 42/48 | L1:26, L3:3, L4:2, L5:11 |
| 2026072004 | 7/48 | 41/48 | L1:13, L2:1, L3:7, L4:7, L5:13 |

### B. Five-seed pooled

- pooled PASS: **35/240** (0.1458)
- seed-level mean ± SD: **0.1458 ± 0.0228**

### C. Task–condition stability (48 groups × 5 seeds)

- stable_pass (5/5): 2; stable_fail (0/5): 32; unstable (1–4/5): 14

### D. Prompt condition comparison

| condition | pooled PASS | seed mean | seed SD |
|---|---:|---:|---:|
| ab1 | 12/80 | 0.1500 | 0.0500 |
| ab2g | 17/80 | 0.2125 | 0.0306 |
| ab2d | 6/80 | 0.0750 | 0.0250 |

## E. Frozen Healer seed-generalization (4 new seeds only)

Label: `frozen-rule generalization across unseen generation seeds on the same fixed task set`

- H0 FAIL: 333
- evaluable FAIL: 333
- trigger: 8
- guarded abstention: 0
- layer exposure: 8
- rescue_to_pass: 0
- regression: 0
- trigger / 384: 0.020833333333333332
- trigger / H0 FAIL: 0.024024024024024024
- rescue / 384: 0.0
- rescue / triggered: 0.0
- regression / H0 PASS: 0.0

This is **not** cross-task held-out generalization.

## F. Prediction vs actual (192 new cells / model)

### `qwen35_4b`
- H0 PASS rate: actual 11.9792% (23/192); band [2.5, 22.5] → **within band**
- FAIL-share L0: 0.0000% band [0.0, 15.0] → **within band**
- FAIL-share L1: 41.4201% band [32.61904761904761, 62.61904761904761] → **within band**
- FAIL-share L2: 7.6923% band [0.0, 15.0] → **within band**
- FAIL-share L3: 10.6509% band [0.0, 24.523809523809526] → **within band**
- FAIL-share L4: 17.7515% band [8.809523809523807, 38.80952380952381] → **within band**
- FAIL-share L5: 22.4852% band [4.0476190476190474, 34.04761904761905] → **within band**
- trigger_count: 6 band [0, 8] → **within band**
- layer_exposure: 6 band [0, 8] → **within band**
- rescue_to_pass: 0 band [0, 2] → **within band**
- regression: 0 expected 0 → **within band**

### `qwen35_9b`
- H0 PASS rate: actual 14.5833% (28/192); band [4.583333333333334, 24.583333333333336] → **within band**
- FAIL-share L0: 0.0000% band [0.0, 15.0] → **within band**
- FAIL-share L1: 44.5122% band [21.585365853658537, 51.58536585365854] → **within band**
- FAIL-share L2: 2.4390% band [0.0, 19.878048780487806] → **within band**
- FAIL-share L3: 11.5854% band [0.0, 24.75609756097561] → **within band**
- FAIL-share L4: 10.3659% band [0.0, 27.195121951219512] → **within band**
- FAIL-share L5: 31.0976% band [21.585365853658537, 51.58536585365854] → **within band**
- trigger_count: 2 band [0, 8] → **within band**
- layer_exposure: 2 band [0, 8] → **within band**
- rescue_to_pass: 0 band [0, 2] → **within band**
- regression: 0 expected 0 → **within band**

## G. Limits

- Qwen Phase 1 interim report only
- Gemini Phase 2 not completed
- No full three-model conclusions
- New seeds not used for rule development

## Assertions

- `cells_per_model_seed_48`: True
- `cells_per_model_240`: True
- `qwen_total_480`: True
- `run_002_byte_level_unchanged`: True
- `ab3_outcome_sum_384`: True

## run_002 immutability

```json
{
  "qwen35_4b_math16_ab123_run_002": {
    "artifact_unchanged": true,
    "raw_unchanged": true
  },
  "qwen35_9b_math16_ab123_run_002": {
    "artifact_unchanged": true,
    "raw_unchanged": true
  }
}
```
