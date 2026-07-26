# Math16 Healer 7格 × Tier 1（4B vs 9B）配對交叉對照 v1

- **性質**：唯讀事後交叉標註（cross-reference）。未呼叫模型、未重跑Healer、未重評正式結果、未修改任何程式／規則／manifest／artifact／正式報告、未重新計算McNemar或改動Tier 1統計。Healer後結果（post-healer status）**僅列為附加欄位**，不寫回、不混入Baseline Tier 1 quadrant判定——Tier 1 quadrant欄位一律由Healer介入前的4B baseline outcome × 9B baseline outcome直接判定。
- **範圍**：僅Qwen 4B與Qwen 9B之math16_pilot02正式v4 cohort；不分析7B或任何其他模型；不補guard測試。
- **唯一鍵**：`task_id` / `condition` / `seed`。

---

## 〇、7格清單核對（先行核對，不得自行調整名單）

依 `docs/experiments/reports/math16_posthoc_six_cell_l2_payload_wrap_deep_audit_v1.md` 第三節逐格因果鏈與第六節 Regression 統計重建，`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 規則實際涉及7格：

- Primary rescue：5格
- Post-hoc technical-correction rescue：1格
- Repaired-still-fail：1格
- 合計：7格

**核對結果：一致，無SCOPE_MISMATCH。** 下列7格與 deep audit 第二節「Set C 六格」（含posthoc標註）及第三節附記「Set A獨有第7格」完全對應，數量、家族分布、rescue/repaired類型均與 deep audit 逐格結論一致。

---

## 一、7格逐格主表

| # | task_id | family | condition | seed | 4B baseline | 9B baseline | Tier1 quadrant | Healer action | post-healer status | evidence paths |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ce115_calc_radical_simplification_l1 | Radical | ab2d_spec_v2 | 2026071301 | FAILED (L2/OUTPUT_SCHEMA_MISMATCH) | FAILED | BOTH_FAIL | PRIMARY_VERIFIED_RESCUE | PASSED (rescue_to_pass) | `.../qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl`；`.../qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl`；`.../qwen4b_healer_v4_r001/{eligible_execution_records.jsonl,post_healer_scoring.jsonl}`；`.../tier1_paired_analysis_v1/paired_cell_ledger.jsonl`（pair_id見下方注1） |
| 2 | ce115_calc_radical_simplification_l1 | Radical | ab2d | 2026072002 | FAILED (L2/OUTPUT_SCHEMA_MISMATCH) | FAILED | BOTH_FAIL | PRIMARY_VERIFIED_RESCUE | PASSED (rescue_to_pass) | 同上（cell_id: `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002`） |
| 3 | ce113_q01_negative_fraction_subtraction | Fraction | ab2d_spec_v2 | 2026072002 | FAILED (L2/OUTPUT_SCHEMA_MISMATCH) | PASSED | NINE_B_ONLY_PASS | PRIMARY_VERIFIED_RESCUE | PASSED (rescue_to_pass) | 同上（cell_id: `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002`；pair_id: `pair_213`） |
| 4 | ce113_q01_negative_fraction_subtraction | Fraction | ab2g | 2026072003 | FAILED (L2/OUTPUT_SCHEMA_MISMATCH) | FAILED | BOTH_FAIL | PRIMARY_VERIFIED_RESCUE | PASSED (rescue_to_pass) | 同上（cell_id: `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003`） |
| 5 | ce112_q04_radical_simplification | Radical | ab2g | 2026072004 | FAILED (L2/OUTPUT_SCHEMA_MISMATCH) | FAILED | BOTH_FAIL | PRIMARY_VERIFIED_RESCUE | PASSED (rescue_to_pass) | 同上（cell_id: `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004`） |
| 6 | ce115_calc_radical_simplification_l1 | Radical | ab2d | 2026071301 | FAILED (L2/OUTPUT_SCHEMA_MISMATCH) | FAILED | BOTH_FAIL | POSTHOC_TECHNICAL_CORRECTION_RESCUE | Primary: FAILED (no_op) → Post-hoc corrected chain: PASSED (rescue_to_pass) | `.../qwen4b_healer_v4_r001/post_healer_scoring.jsonl`（primary=FAILED/no_op）；`.../qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json`（new_post_healer_status=PASSED，noop_to_rescue=true）；`.../math16_posthoc_six_cell_rescue_audit_v1_manifest.json` |
| 7 | ce112_q04_radical_simplification | Radical | ab2g | 2026072002 | FAILED (L2/OUTPUT_SCHEMA_MISMATCH) | FAILED | BOTH_FAIL | REPAIRED_STILL_FAIL | FAILED (changed_partial_progress) | `.../qwen4b_healer_v4_r001/{eligible_execution_records.jsonl,post_healer_scoring.jsonl}` |

注1：完整路徑前綴均為 `docs/experiments/results/`；Tier 1配對來源為 `math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/paired_cell_ledger.jsonl`（該分析之 `analysis_manifest.json` 標註 `source_qwen4b_baseline`／`source_qwen9b_baseline` 分別對應 `math16_pilot02_qwen4b_evaluation_v4_r001` 與 `math16_pilot02_qwen9b_evaluation_v4_r001` 之 `cell_level_baseline.jsonl`，`healer_execution: false`，`rescored: false`）。

**UNRESOLVED：無**——全部7格皆可在Tier 1配對帳中找到對應9B baseline結果，無任何一格缺少9B對應資料。

---

## 二、摘要表（依family）

| family | Primary rescue | Post-hoc rescue | Repaired-still-fail | total interventions |
|---|---|---|---|---|
| Integer | 0 | 0 | 0 | 0 |
| Polynomial | 0 | 0 | 0 | 0 |
| Radical | 3 | 1 | 1 | 5 |
| Fraction | 2 | 0 | 0 | 2 |
| **合計** | **5** | **1** | **1** | **7** |

**核對結果：與任務預期值完全一致**（Integer 0、Polynomial 0、Radical 3/1/1、Fraction 2/0/0、合計5/1/1）。

---

## 三、Tier 1 quadrant摘要

| Tier1 quadrant | Primary rescue | Post-hoc rescue | Repaired-still-fail | total |
|---|---|---|---|---|
| BOTH_FAIL | 4 | 1 | 1 | 6 |
| NINE_B_ONLY_PASS | 1 | 0 | 0 | 1 |
| **合計** | **5** | **1** | **1** | **7** |

（本表quadrant標籤採Tier 1配對帳原始標籤 `NINE_B_ONLY_PASS`／`BOTH_FAIL`；7格中無一格落在 `BOTH_PASS` 或 `FOUR_B_ONLY_PASS`，此為預期結果，因Healer eligibility前提為4B baseline FAILED。）

---

## 四、精簡結論

1. **7格實際分布**：`ce115_calc_radical_simplification_l1`（ab2d_spec_v2/seed 2026071301、ab2d/seed 2026072002、ab2d/seed 2026071301，共3格，Radical）、`ce113_q01_negative_fraction_subtraction`（ab2d_spec_v2/seed 2026072002、ab2g/seed 2026072003，共2格，Fraction）、`ce112_q04_radical_simplification`（ab2g/seed 2026072004、ab2g/seed 2026072002，共2格，Radical）。

2. **6格verified rescue在Tier 1表中落在哪些quadrant**：6格中5格（cell 1、2、4、5、6）落在 `BOTH_FAIL`，1格（cell 3：`ce113_q01_negative_fraction_subtraction/ab2d_spec_v2/seed_2026072002`）落在 `NINE_B_ONLY_PASS`。

3. **repaired-still-fail那格落在哪個quadrant**：cell 7（`ce112_q04_radical_simplification/ab2g/seed_2026072002`）落在 `BOTH_FAIL`。

4. **Healer是否改變原Baseline Tier 1統計**：**否**。本表之Tier 1 quadrant欄位完全由Healer介入前的4B baseline × 9B baseline判定（來源`healer_execution: false`之凍結配對帳），Healer後之post-healer status僅作為附加欄位並列呈現，不回寫、不改變、不重新計算原Baseline Tier 1配對統計或McNemar檢定；本報告僅為事後交叉標註。

---

## 五、Git與交付

**起始**：
- branch: `main`
- HEAD: `e61971733e9f6873c216be7b87e068824b93c8b9`
- origin/main: `e61971733e9f6873c216be7b87e068824b93c8b9`（同步）
- git status --short：2個既存modified正式檔案（`04_math16_pilot02_jury_qa_final_v1.md`、`05_math16_pilot02_appendices_v1.md`）+ 前幾輪session累積之untracked manifests/reports/results/scripts（詳見任務起始快照）

**結束**：
- branch: `main`（未變動）
- HEAD: `e61971733e9f6873c216be7b87e068824b93c8b9`（未變動，未commit）
- origin/main: `e61971733e9f6873c216be7b87e068824b93c8b9`（未變動）
- git status --short：與起始**完全相同**，僅新增本報告一個untracked檔案：`docs/experiments/reports/math16_healer_seven_cell_tier1_crosswalk_v1.md`
- 既存modified／untracked檔案內容與狀態**未變動**（全程僅讀取，未stage、未commit、未push、未stash、未restore）
