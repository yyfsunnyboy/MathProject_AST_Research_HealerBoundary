# Math16 Method 2 All-Cell 正式結果報告 v1

報告日期：2026-07-28

適用模型：Qwen 3.5 4B

母體：320 cells（16 題 × 4 條件 × 5 seeds）

更正說明：Method 2 本身之 Raw／Final 數字（79/320、85/320、rescue 6、regression 0）為既有正式凍結證據，不受任何更正影響。Method 1 之 Baseline 78/320 經 audit 確認獨立擷取錯誤後，分析/報告層更正為 79/320，與 Method 2 Raw PASS 79/320 一致；詳見 [`math16_baseline_correction_note_v1.md`](math16_baseline_correction_note_v1.md) 及 [`math16_method1_method2_78_79_discrepancy_audit_v1.md`](math16_method1_method2_78_79_discrepancy_audit_v1.md)。

## 1. 方法與範圍

Method 2 採 all-cell eligibility-first 流程：

1. 對 320 格既有 raw source 全部執行 Eligibility，不讀取 Baseline PASS／FAIL、答案值或 evaluator outcome。
2. Eligible cells 才套用既有 frozen Healer；Noneligible cells 的 Final source 與 Raw source 完全相同。
3. 320 格 source decision 全部完成並凍結後，使用同一 pinned Evaluator 分別獨立評分 Raw source 與 Final source。
4. Transition 僅由 `(raw_status, final_status)` 導出，不以評分結果接受、回退或重做修復。

本次未重跑模型，亦未修改 Healer、Eligibility、Guard、rule、allowlist、priority、max passes、Protocol、Manifest 或 Method 1 結果。

## 2. 正式主結果

| 項目 | 結果 |
|---|---:|
| Raw PASS | 79/320 |
| Final PASS | 85/320 |
| 淨變化 | +6 |
| Eligible | 11 |
| Rule triggered | 11 |
| Source changed | 11 |
| Noneligible | 309 |

Method 2 對 Raw 與 Final 的 320 格均完成實際評分；Raw PASS 79/320，Final PASS 85/320，淨增 6 格。

## 3. 四種 Transition

| Raw → Final | Transition | 數量 |
|---|---|---:|
| FAILED → PASSED | `verified_rescue` | 6 |
| PASSED → FAILED | `regression` | 0 |
| PASSED → PASSED | `preserved_pass` | 79 |
| FAILED → FAILED | `still_failed` | 235 |
| **合計** |  | **320** |

`regression = 0/320` 是 Method 2 對全部 320 格 Raw／Final source 分別評分後的實際量測結果。此數字只陳述本次凍結 corpus、規則與 Evaluator 下的觀察結果。

## 4. Eligible 11 格逐格分帳

| Cell ID | Rule ID | Raw | Final | Transition |
|---|---|---|---|---|
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | FAILED | PASSED | `verified_rescue` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301` | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | FAILED | PASSED | `verified_rescue` |
| `qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072001` | `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` | FAILED | FAILED | `still_failed` |
| `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d_spec_v2__seed_2026072002` | `L1_PROSE_RESIDUE_NARROW` | FAILED | FAILED | `still_failed` |
| `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072002` | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | FAILED | FAILED | `still_failed` |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002` | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | FAILED | PASSED | `verified_rescue` |
| `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002` | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | FAILED | PASSED | `verified_rescue` |
| `qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072003` | `L1_PROSE_RESIDUE_NARROW` | FAILED | FAILED | `still_failed` |
| `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003` | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | FAILED | PASSED | `verified_rescue` |
| `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004` | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | FAILED | PASSED | `verified_rescue` |
| `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026072004` | `L1_CLOSE_UNBALANCED_PARENTHESIS` | FAILED | FAILED | `still_failed` |

Eligible 11 格合計為 6 格 `verified_rescue`、5 格 `still_failed`、0 格 `regression`、0 格 `preserved_pass`。

## 5. Rule ID 分帳

| Rule ID | Cells | Source changed | Verified rescue | Regression | Preserved pass | Still failed |
|---|---:|---:|---:|---:|---:|---:|
| `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | 7 | 7 | 6 | 0 | 0 | 1 |
| `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` | 1 | 1 | 0 | 0 | 0 | 1 |
| `L1_PROSE_RESIDUE_NARROW` | 2 | 2 | 0 | 0 | 0 | 2 |
| `L1_CLOSE_UNBALANCED_PARENTHESIS` | 1 | 1 | 0 | 0 | 0 | 1 |
| **Eligible 合計** | **11** | **11** | **6** | **0** | **0** | **5** |
| Noneligible | 309 | 0 | 0 | 0 | 79 | 230 |
| **全體** | **320** | **11** | **6** | **0** | **79** | **235** |

`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 為 6 格 rescue、1 格 still failed；其餘三類規則合計 4 格，均為 still failed。

## 6. Method 1 與 Method 2 差異

| 比較面向 | Method 1 | Method 2 |
|---|---|---|
| Eligibility 母體 | Baseline FAIL cells | 全部 320 格 raw source |
| Baseline PASS cells 是否執行 Healer | 否 | 先執行 Eligibility；僅 Eligible 才執行 Healer |
| Raw／Final 評分 | 未形成全 320 格雙路評分 | Raw 320 與 Final 320 分別獨立評分 |
| Regression | **Not measured** | **Measured = 0/320** |
| 正式結果分帳（凍結管線歷史輸出，永久不變） | Baseline 78/320；Primary 83/320；corrected-chain 技術結果 84/320 | Raw 79/320；Final 85/320 |
| 正式結果分帳（分析/報告層更正後，見 Correction Note） | Baseline 79/320；Primary 84/320（歷史中繼值，demoted）；corrected-chain Final 85/320 | Raw 79/320；Final 85/320（不變） |

兩種方法的程序與正式分帳不同；Method 2 數字不得回寫或取代 Method 1 結果。Method 1 未對 Baseline PASS cells 執行 Healer，因此 `Regression not measured`；Method 2 完成全 320 格 Raw／Final 雙路評分，因此 `Regression measured = 0/320`。Method 1 之凍結管線歷史輸出（Baseline 78/320）本身不予修改；經 audit 確認獨立於 Eligibility 之外的單一 Baseline 擷取錯誤後，分析/報告層更正為 79/320，與 Method 2 Raw PASS 79/320 一致，詳見 [`math16_baseline_correction_note_v1.md`](math16_baseline_correction_note_v1.md)。

## 7. 正式證據

- Frozen Protocol：[`math16_method2_all_cell_frozen_protocol_v1.md`](../protocols/math16_method2_all_cell_frozen_protocol_v1.md)
- Frozen Manifest：[`math16_method2_all_cell_protocol_v1.json`](../manifests/math16_method2_all_cell_protocol_v1.json)
- Phase A／B Results：[`math16_method2_all_cell_replay_v1`](../results/math16_method2_all_cell_replay_v1/)
- Phase B 320-cell journal：[`transition_journal.jsonl`](../results/math16_method2_all_cell_replay_v1/transition_journal.jsonl)
- Phase B journal SHA-256：`5d11fb404930c5387f0f91b7dcc69c621ef477f4a22d0419a8afe2493068ae52`
- Correction Note（Method 1 Baseline 78→79 分析/報告層更正）：[`math16_baseline_correction_note_v1.md`](math16_baseline_correction_note_v1.md)
- Method 1／Method 2 差異 Audit：[`math16_method1_method2_78_79_discrepancy_audit_v1.md`](math16_method1_method2_78_79_discrepancy_audit_v1.md)
