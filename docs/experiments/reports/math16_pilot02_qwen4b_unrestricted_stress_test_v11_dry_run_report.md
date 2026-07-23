# Math16 Qwen4B Unrestricted Stress Test v1.1 Zero-Model Dry Run Report

```text
MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_ZERO_MODEL_DRY_RUN_COMPLETED
DEFAULT_ARM_242_CELL_PLAN_VALIDATED
AMBIGUITY_CASE_N1_FULLY_SPECIFIED
FORCED_EXPLORATORY_SELECTION_POLICY_FROZEN
RUNTIME_AND_OUTPUT_ISOLATION_VALIDATED
OFFICIAL_RESULTS_PRESERVED
READY_FOR_EXPLICITLY_AUTHORIZED_STRESS_TEST_EXECUTION
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告版本：** v1.0 (Runtime Dry-Run Report)
**建置時間 UTC：** 2026-07-23

---

> **固定聲明 (Mandatory Disclaimer)：**
> 本 Dry Run 為 Zero-Model / Zero-Transform / Zero-Evaluator 之預執行驗證，未對任何程式碼發動修改，不變更、取代或重新解釋既有 Primary 與正式 Post-hoc 結果。

---

## 1. 執行摘要 (Executive Summary)

本報告對 **Unrestricted Stress Test v1.1** 進行 Zero-Model Dry Run 驗證，確立 242 個 Baseline FAIL cells 之執行計畫、輸出隔離機制與唯一 1 格歧義案例之 Forced Exploratory Arm 選擇政策。

### 核心結論：
1. **242 格帳目完全凍結與驗證**：
   - Total Baseline FAIL = `242`
   - `NO_RULE_CANDIDATE` = `231`
   - `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE` = `10`
   - `UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE` = `0`
   - `AMBIGUOUS_MULTIPLE_CANDIDATES` = `1`
   - `DETECTION_UNRESOLVED` = `0`
2. **Default Arm 計畫 (242 格)**：
   - 231 格 `NO_RULE_CANDIDATE` 實施 `ABSTAIN_NO_RULE`
   - 10 格 `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE` 建立 `PLANNED_TRANSFORM` (Dry Run 中未執行)
   - 1 格 `AMBIGUOUS_MULTIPLE_CANDIDATES` 實施 `ABSTAIN_AMBIGUOUS`
3. **Forced Exploratory Arm 確定性政策 (N=1 歧義格)**：
   - 標的 Cell: `qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`
   - 凍結選擇政策：固定 Rule Priority 序 + AST Preorder 原始碼最前段 Start Offset (`first_def_generate_offset`)。
   - 安全預分類：**`UNSAFE_MODIFICATION`** (絕對禁止標註為 `SAFE_REPAIR_CANDIDATE`)。
4. **輸出隔離與 Governance 驗證**：
   - 產出嚴格隔離於 `artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/dry_run/`。
   - `formal/` 目錄在 Dry Run 中**完全不存在**，驗證隔離無染。

---

## 2. 唯一歧義案例完整分析 (N=1 Ambiguity Specification)

- **Canonical Cell ID**: `qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`
- **Ambiguity Type**: `AMBIGUOUS_MULTIPLE_ENTRY_POINTS_OR_PROSE`
- **Primary Abstain Reason**: `"Ambiguous entry point; frozen healer abstains."`
- **語意結構**: 模型生成大量無 Code Fence 的 Prose 思考推理段落，並內含 Python 代碼與註解，導致多個候選 Entry-Point 切割邊界。
- **Forced Selection Policy (DETERMINISTIC_FIRST_ENTRY_POINT_SOURCE_PREORDER)**:
  1. 依據凍結 Priority: `L1_PROSE_RESIDUE_NARROW`
  2. 依據 AST Preorder / Source Span: 選擇最前開頭之 `def generate` offset (`first_def_generate_offset`)
- **Safety 預判**: **`UNSAFE_MODIFICATION`**

---

## 3. 兩個 Arm 執行計畫 (Two-Arm Execution Plans)

### 3.1 Default Arm
- **總格數**: 242
- **Planned Transforms**: 10 格 (`UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE`)
- **Abstains**: 232 格 (231 `NO_RULE_CANDIDATE` + 1 `AMBIGUOUS_MULTIPLE_CANDIDATES`)

### 3.2 Forced Exploratory Arm
- **總格數**: 1 格 (`qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`)
- **Planned Action**: `PLANNED_FORCED_TRANSFORM` (依 deterministic 政策選擇)
- **Safety Pre-classification**: `UNSAFE_MODIFICATION`

---

## 4. SHA 保護與檔案指紋

以下既有成果與基準檔案 SHA256 經比對 100% 保持未變：
- Final Report v1.3: `dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b` (未修改 ✅)
- Evidence Complete: `de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225` (未修改 ✅)
- Eligibility Semantics Audit Manifest: `7384bca4790a5362fe200819591e358b087374d42ea7eafbb715782a7e99468c` (未修改 ✅)

---

## 5. 結案 Verdict

```text
MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_ZERO_MODEL_DRY_RUN_COMPLETED
DEFAULT_ARM_242_CELL_PLAN_VALIDATED
AMBIGUITY_CASE_N1_FULLY_SPECIFIED
FORCED_EXPLORATORY_SELECTION_POLICY_FROZEN
RUNTIME_AND_OUTPUT_ISOLATION_VALIDATED
OFFICIAL_RESULTS_PRESERVED
READY_FOR_EXPLICITLY_AUTHORIZED_STRESS_TEST_EXECUTION
```
