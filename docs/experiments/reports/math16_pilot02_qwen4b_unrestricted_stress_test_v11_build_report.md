# Math16 Qwen4B Unrestricted Stress Test v1.1 Build & Verification Report

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告版本：** v1.0 (Formal Build Report)
**建置時間 UTC：** 2026-07-23

---

> **固定聲明 (Mandatory Disclaimer)：**
> 本建置報告紀錄 Math16 Qwen4B Unrestricted Stress Test v1.1 之 formal 構建過程與產出校驗，未對 Primary 與既有 Post-hoc 數據進行任何覆寫。

---

## 1. 構建與執行過程 (Build Process Summary)

1. **零模型執行 (Zero-Model Execution)**:
   - 僅呼叫已凍結之 Healer 轉換器與 Evaluator v4 評估器。
   - LLM / VLM API 呼叫次數：`0`。
2. **Default Arm (242 cells)**:
   - 231 格 `NO_RULE_CANDIDATE` 實施 `ABSTAIN_NO_RULE`
   - 1 格 `AMBIGUOUS_MULTIPLE_CANDIDATES` 實施 `ABSTAIN_AMBIGUOUS`
   - 10 格 `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE` 發動 Healer 修改並執行 Evaluator 評估
3. **Forced Exploratory Arm (1 cell)**:
   - 標的 Cell: `qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`
   - 依據 `DETERMINISTIC_FIRST_ENTRY_POINT_SOURCE_PREORDER` 選擇 target 發動修改與評估
   - 安全強制標註為 `UNSAFE_MODIFICATION`
4. **雙重配對證據保存**:
   - `transformed_sources/`: 保存 11 份完整的轉譯後 Python 原始碼。
   - `unified_diffs/`: 保存 11 份 before/after unified diff 文字檔。

---

## 2. 產出檔案盤點 (Artifact Checklist)

- `artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal/`:
  - `default_arm_results.jsonl`
  - `forced_exploratory_arm_result.json`
  - `transformed_sources/` (11 files)
  - `unified_diffs/` (11 files)
  - `disposition_summary.json`
  - `outcome_safety_crosstab.csv`
  - `eligibility_outcome_crosstab.csv`
  - `condition_disposition_crosstab.csv`
  - `family_disposition_crosstab.csv`
  - `rule_outcome_crosstab.csv`
  - `execution_manifest.json`
  - `evidence_index.json`

---

## 3. 驗證結論 (Verification Conclusion)

所有正式產出檔案完整創建，帳目完全相符（Default 242 格 + Forced 1 格），11/11 份轉譯源代碼與 Unified Diff 100% 完整存盤。
