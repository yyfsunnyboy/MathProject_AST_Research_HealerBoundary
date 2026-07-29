# Math16 C0→C1 Tier A Reproducibility v1

> **Verdict:** `C0_C1_REPRODUCIBILITY_MATCH`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **Frozen Method2 root:** `docs/experiments/results/math16_method2_all_cell_replay_v1/`
> **Repro root:** `docs/experiments/results/math16_c0_c1_tier_a_reproducibility_v1/`

## 1. Scope

Zero-model offline re-execution of Method 2 Phase A（Tier A six-rule allowlist）
+ Phase B（independent Raw/Final evaluation）on frozen Qwen 4B Pilot-02 320 cells.
New artifacts written only under the reproducibility directory; frozen journals/sources untouched.

## 2. Core counts

| Metric | Expected (frozen) | Reproduced |
|---|---:|---:|
| C0 Baseline (raw PASS) | 79 | 79 |
| C1 Tier A (final PASS) | 85 | 85 |
| verified_rescue | 6 | 6 |
| regression | 0 | 0 |
| preserved_pass | 79 | 79 |
| still_failed | 235 | 235 |

## 3. Per-cell agreement vs frozen journal

- Cell identity set match: **True**
- Raw SHA mismatches: **0**
- Final SHA mismatches: **0**
- Eligibility / source_changed mismatches: **0**
- Rule ID mismatches: **0**
- PASS/FAIL status mismatches: **0**
- Transition mismatches: **0**
- Verified rescue identity match: **True**

### Verified rescue cell_ids (repro)

- `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004`
- `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002`
- `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003`
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301`
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002`
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301`

### Verified rescue cell_ids (frozen)

- `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004`
- `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002`
- `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003`
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301`
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002`
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301`

## 4. Journal SHA-256

- Frozen eligibility: `1fd8aab4a7dadfeaca58af51b65bfb4c1f860037b218468dec844bc7ce9198f6`
- Repro eligibility: `1fd8aab4a7dadfeaca58af51b65bfb4c1f860037b218468dec844bc7ce9198f6`（**byte-identical**）
- Frozen transition: `5d11fb404930c5387f0f91b7dcc69c621ef477f4a22d0419a8afe2493068ae52`
- Repro transition: `f5fdfeb4e00834a22644f7f9a7a8c4ae3999b4dab1a71cb4296e7541bfdca1e5`

Transition journal **byte SHA differs** only because the repro writer omits frozen diagnostic fields
（`*_classifier_outcome` / `*_primary_failure_layer` / `*_failure_subtype`）and includes
`healer_provenance`. Core per-cell fields（identity、raw/final SHA、eligibility、rule_id、
raw/final PASSED|FAILED、transition）are **0-mismatch** vs frozen.

## 5. Sample mismatches (cap 40)

```json
[]
```

## 6. Declarations

- Model calls: **0**
- Frozen Method2 artifacts modified: **No**
- Tier C processed: **No**
- Aggressive Healer v2 created: **No**
- Commit / push: **No**
