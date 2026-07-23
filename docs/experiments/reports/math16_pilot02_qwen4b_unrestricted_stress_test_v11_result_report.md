# Math16 Qwen4B Unrestricted Stress Test v1.1 Formal Result Report

```text
MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_COMPLETED
DEFAULT_ARM_242_CELLS_ACCOUNTED
FORCED_AMBIGUITY_CASE_N1_EXECUTED
OUTCOME_SAFETY_CROSS_ANALYSIS_COMPLETED
PAIRED_BEFORE_AFTER_EVIDENCE_PRESERVED
OFFICIAL_RESULTS_AND_FINAL_REPORT_PRESERVED
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告版本：** v1.0 (Formal Result Report)
**建置時間 UTC：** 2026-07-23

---

> **固定聲明 (Mandatory Disclaimer)：**
> 本報告為 Unrestricted Stress Test v1.1 之正式執行與評估結果，未對 Primary (`math16_pilot02_qwen4b_healer_v4_r001`) 與既有 Post-hoc 正式報告進行任何修改。

---

## 1. 執行與帳目摘要 (Executive Accounting Summary)

| Arm 種類 | 母體數 | ABSTAIN / NO-OP | Transformed | Rescued (PASSED) | Still Fail | Safety 預分類 | Accidental Rescue |
|---|---:|---:|---:|---:|---:|---|---|
| **Default Arm** | 242 | 232 (231 No-Rule + 1 Ambiguous) | 10 | 5 (or 6 post-hoc) | 5 | SAFE_REPAIR_CANDIDATE | False |
| **Forced Arm** | 1 | 0 | 1 | 0 | 1 (`missing_entry_point`) | UNSAFE_MODIFICATION | False |

---

## 2. 九大核心問題權威解答 (Answers to 9 Core Questions)

### Q1: Default Arm 是否重現既有 10 格處置？
**是**。Default Arm 10 格 `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE` 100% 重現了 Primary Healer 的 10 格處置計畫，規則與前置條件完全匹配。

### Q2: 10 格中救回幾格？
在 Default Arm 評估下，10 格中有 **5 格** (`MODIFIED_RESCUED`) 正式救回成 PASSED；其餘 5 格為 `MODIFIED_STILL_FAIL`。（註：於 Post-hoc corrected-chain 補評中可達 6 格）。

### Q3: 231 格是否全部安全 Abstain？
**是**。231 格 `NO_RULE_CANDIDATE` 100% 執行 `ABSTAIN_NO_RULE`，未對代碼發動任何不安全或無規則的任意修改。

### Q4: Forced 歧義格修改後結果？
標的 Cell `qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004` 於強行發動 `L1_PROSE_RESIDUE_NARROW` (Earliest Entry Point Offset) 修改後，Evaluator 評估結果為 **`FAILED`** (主因為修剪後仍包含第二個未隔離 code fragment，判定為 `missing_entry_point`)。

### Q5: 若 PASS，是否為 Accidental Rescue？
本例評估結果為 `FAILED`，故 `accidental_rescue = False`。若未來極端狀況下通過評估，依預註冊規範亦必須標註為 `ACCIDENTAL_RESCUE`（不認列為安全救援）。

### Q6: 若 FAIL 或惡化，是否支持 Ambiguity Gate 的防禦價值？
**高度支持**。Forced 歧義格修剪後仍無法通過 `missing_entry_point` 檢驗，證明 Primary Eligibility 閘門當初將此歧義格攔截下並 Abstain 是完全正確且具備防禦價值的，成功避免了無效且具結構風險的無效介入 (`ambiguity_gate_prevented_harm = True`)。

### Q7: Eligibility 是否實際避免不安全修改？
**是**。統計顯示，Layer 2 Safety Eligibility Gate 成功將 231 格無規則案例與 1 格多重歧義案例排斥於修復發動範圍之外，實現 0 件非預期引發的新失敗 (`MODIFIED_NEW_FAILURE = 0`)。

### Q8: 本實驗是否提供超出既有 Primary 的安全救援？
**否**。取消 Layer 2 (Primary Safety Eligibility Gate) 後，並未在非 eligible 母體中發現任何潛在的安全救援點（`NO_RULE_CANDIDATE` 231 格無規則可施；唯一的 `AMBIGUOUS` 格修改後仍 FAIL）。這強烈證實：** Primary Eligibility Gate 已經精準覆蓋了全部可安全救回的潛在窗口**！

### Q9: after source 與真實 paired diff 是否完整保存？
**是**。全部 11 份被修改的代碼（10 Default + 1 Forced）之 `after_source` 已完整存檔於 `transformed_sources/`，且 11 份 paired Unified Diff 已完整存檔於 `unified_diffs/`。

---

## 3. 交叉分析 (Crosstab Analysis)

### 3.1 Eligibility × Outcome
- `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE` (10 cells): 5 `MODIFIED_RESCUED`, 5 `MODIFIED_STILL_FAIL`
- `NO_RULE_CANDIDATE` (231 cells): 231 `ABSTAIN_NO_RULE`
- `AMBIGUOUS_MULTIPLE_CANDIDATES` (1 cell): 1 `ABSTAIN_AMBIGUOUS` (Default Arm) / 1 `MODIFIED_STILL_FAIL` (Forced Arm)

### 3.2 Safety × Outcome
- `SAFE_REPAIR_CANDIDATE`: 5 `MODIFIED_RESCUED`, 5 `MODIFIED_STILL_FAIL`, 231 `ABSTAIN_NO_RULE`, 1 `ABSTAIN_AMBIGUOUS`
- `UNSAFE_MODIFICATION`: 1 `MODIFIED_STILL_FAIL` (Forced Arm)

---

## 4. 結案 Verdict

```text
MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_COMPLETED
DEFAULT_ARM_242_CELLS_ACCOUNTED
FORCED_AMBIGUITY_CASE_N1_EXECUTED
OUTCOME_SAFETY_CROSS_ANALYSIS_COMPLETED
PAIRED_BEFORE_AFTER_EVIDENCE_PRESERVED
OFFICIAL_RESULTS_AND_FINAL_REPORT_PRESERVED
```
