# Math16 C4→C5 Tier D D3+D1 Development Replay v1

> **verdict:** `TIER_D_DEVELOPMENT_RESCUE_OBSERVED`
> **verdicts:** `TIER_D_DEVELOPMENT_RESCUE_OBSERVED`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`

## Scope

- Input: **C4 final post-source** for census D3/D1 eligible cells only
- Rules: `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` → `TIER_D_OPS_SHADOW_REMOVAL_V1`
- No model calls; evaluator observation-only; no Confirmatory; no v2; D2/D4/D5/D6 not executed

## Aggregate

- Cells: **8** (D3 eligible 5, D1 eligible 4, overlap 1)
- Triggered / modified / abstained: **8** / **7** / **1**
- Parse gain / regression: **1** / **0**
- Executable gain / regression: **4** / **0**
- Verified rescue: **2**
- Still failed / degraded: **6** / **0**

### D1 verified-rescue mechanism（措辭鎖定；不改上表數字）

兩格 verified rescue 均為 D1、task `ce112_q04_radical_simplification`（seed `2026071301`／`2026072002`）。

- Binding class（權威）：**`ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`**（見 supplemental closure）
- AST：`generate` 內 `RadicalOps.simplify_term`／`format_term` 移除前綁定本地 `ClassDef RadicalOps`；移除後改綁 frozen scaffold 注入 Ops
- **正式統一措辭：** 以 frozen scaffold 注入的正式 Ops implementation，取代模型自訂的 active shadow implementation。
- **禁止：** 稱這兩格為死代碼清除／清除未使用 class／刪除無關定義（該等用語僅適用已證明之 `DEAD_SHADOW_REMOVAL`）

### Per-rule

| Rule | eligible | triggered | modified | abstained |
|---|---:|---:|---:|---:|
| `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` | 5 | 5 | 4 | 4 |
| `TIER_D_OPS_SHADOW_REMOVAL_V1` | 4 | 5 | 4 | 4 |

## Overlap

- Policy: D3→D1; each ≤1; one formal post-source
- Overlap cells: 1
- `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d__seed_2026072002`: fired=['TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1', 'TIER_D_OPS_SHADOW_REMOVAL_V1'] selected=`TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1+TIER_D_OPS_SHADOW_REMOVAL_V1` modified=True transition=still_failed

## Per-cell one-sentence results

- `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d__seed_2026072002`: triggered=True selected=TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1+TIER_D_OPS_SHADOW_REMOVAL_V1; modified[TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1,TIER_D_OPS_SHADOW_REMOVAL_V1]; still_failed; FAILED->FAILED (runtime_failure->runtime_failure)
- `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d__seed_2026072004`: triggered=True selected=TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1; modified[TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1]; still_failed; FAILED->FAILED (runtime_failure->runtime_failure)
- `qwen3_5_4b__ce111_q05_exact_fraction_expression__ab2d__seed_2026072003`: triggered=True selected=TIER_D_OPS_SHADOW_REMOVAL_V1; modified[TIER_D_OPS_SHADOW_REMOVAL_V1]; still_failed; FAILED->FAILED (answer_incorrect->answer_incorrect)
- `qwen3_5_4b__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026072002`: triggered=True selected=TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1; modified[TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1]; parse_gain; executable_gain; still_failed; FAILED->FAILED (runtime_failure->structural_mismatch)
- `qwen3_5_4b__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026072003`: triggered=True selected=TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1; modified[TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1]; executable_gain; still_failed; FAILED->FAILED (runtime_failure->answer_incorrect)
- `qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026071301`: triggered=True selected=TIER_D_OPS_SHADOW_REMOVAL_V1; modified[TIER_D_OPS_SHADOW_REMOVAL_V1]; executable_gain; verified_rescue; FAILED->PASSED (runtime_failure->passed)
- `qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026072002`: triggered=True selected=TIER_D_OPS_SHADOW_REMOVAL_V1; modified[TIER_D_OPS_SHADOW_REMOVAL_V1]; executable_gain; verified_rescue; FAILED->PASSED (runtime_failure->passed)
- `qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab1__seed_2026071301`: triggered=True selected=-; abstained(no_ops_shadow); FAILED->FAILED (schema_failure->schema_failure)

## Worth D2 / D5?

- recommend_d2: **False**
- recommend_d5: **False**
- D3/D1 showed Development signal on C4 residual; D2 (1 eligible) and D5 (4 ranked) remain secondary candidates but were not implemented this round.

## Supplemental closure（交叉引用；不改本頁統計）

唯讀補充閉合見：

`docs/experiments/reports/math16_c4_c5_tier_d_d3_d1_supplemental_closure_v1.md`

涵蓋：D1 triggered=5 vs eligible=4（`LOGGING_ONLY_DIFFERENCE`）；兩格 rescue 為 `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`（非 dead-code removal）；重疊格固定 D3→D1 序列累積。本報告 aggregate／per-cell 數字不變。

## Declarations

- No model calls
- No D2/D4/D5/D6
- No Confirmatory
- No Aggressive Healer v2
- No commit / push
