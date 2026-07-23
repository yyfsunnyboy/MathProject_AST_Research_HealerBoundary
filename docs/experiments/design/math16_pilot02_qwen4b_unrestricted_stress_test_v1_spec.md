# Math16 Qwen4B Unrestricted Healer Stress Test v1 Specification

```text
MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V1_PREREGISTERED
POPULATION_SIZE_242_BASELINE_FAIL_CELLS
FROZEN_ALLOWLIST_RULES_INHERITED
SAFETY_METRIC_PROPERTY_BASED
OFFICIAL_RESULTS_PRESERVED
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**規格版本：** v1.0 (Preregistration Specification)
**標的數據庫：** Math16 Pilot-02 Qwen 3.5 4B（320 個獨立實驗 cells 中之 242 個 Baseline FAIL cells）

---

> **固定聲明 (Mandatory Disclaimer)：**
> 本實驗為 Evidence Complete 凍結後之 Post-hoc 補充 Stress Test，不修改、取代或重新解釋既有 Primary 與正式 Post-hoc 結果。

---

## 1. 研究目的 (Research Motivation & Questions)

本實驗旨在對 **Qwen 3.5 4B** 正式 320-cell 全因子網格矩陣中之所有 Baseline FAIL 格 (共計 242 格)，**不考慮原 Primary 流程之 Eligibility 篩選機制**，完全無差別地送入既有凍結 Healer 規則集合，進而量測並回答以下 5 個核心科學問題：

1. **Healer 實際修改覆蓋率 (Modification Scope)**：當移除 Eligibility 門檻後，Healer 在 242 個失敗案例中實際發動修改了多少格？
2. **處置轉化分布 (Outcome Breakdown)**：修改後的案例中，分別有多少格達到救回 (`rescued`)、維持失敗 (`repaired_still_fail`)，或引入新失敗／倒退 (`introduced_new_fail / regressed`)？
3. **非 Eligibility 修改的安全性 (Unsafe Modification Risk)**：在原先被判定為不符合 Eligibility 的案例被強制修改時，是否會產生破壞程式語義、產生答案猜測或破壞構造之不安全修改？
4. **Primary Eligibility 門檻之防禦有效性 (Eligibility Defense Value)**：原 Primary Eligibility 規則是否成功精準地區分出了「安全介入窗口」與「高風險／無效介入區」？
5. **放棄與修改分布 (Abstain vs Transformation Distribution)**：在全體 242 個 FAIL 案例中，Healer 放棄介入 (Abstain) 與發動修改 (Transform) 的完整比例分布為何？

---

## 2. 實驗母體與進場規範 (Target Population & Intake Criteria)

### 2.1 固態母體網格
- **模型**: Qwen 3.5 4B (`qwen3.5:4b`)
- **任務數**: 16 題 K-12 數學題型（4 家族 × 4 題）
- **Prompt 條件**: 4 種（Ab1, Ab2g, Ab2d+api, Ab2d+spec-v2）
- **隨機種子**: 5 個（2026071301, 2026072001, 2026072002, 2026072003, 2026072004）
- **全矩陣總數**: 320 cells
- **Baseline PASS 數**: 78 cells（**禁止納入修復輸入母體**，可保留為唯讀參照）
- **Baseline FAIL 數 (Stress Test 輸入母體)**: **`ALL_BASELINE_FAIL_SET = 242 cells`**
- **Primary Eligible 數**: 10 cells

---

## 3. 凍結 Healer 規則與執行約束 (Frozen Healer Rules & Constraints)

Stress Test 必須 100% 使用 `math16_ab3_freeze_manifest.json` 所登錄之 6 條已凍結規則，按 Priority 升序執行，於首條觸發修復後停止 (Stop after first transformation pass)：

1. **`L1_CLOSE_UNBALANCED_PARENTHESIS`** (Priority: 90)
2. **`L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED`** (Priority: 95)
3. **`L1_PROSE_RESIDUE_NARROW`** (Priority: 98)
4. **`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`** (Priority: 100)
5. **`L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM`** (Priority: 110)
6. **`L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`** (Priority: 120)

### 嚴格禁令：
- **禁止** 新增任何未凍結規則。
- **禁止** 修改既有規則之前置條件 (Preconditions)。
- **禁止** 使用 Oracle 解答反推或篩選修改。
- **禁止** 根據最終 PASS/FAIL 結果選擇性接受修改。
- **禁止** 針對 Stress Test 結果進行事後規則調整。

---

## 4. 繼承安全標準與量尺 (Inherited Safety Metric)

正式繼承前續三次完整稽核之成果與 SHA256 指紋：
- [Six-Cell Rescue Audit Result Manifest](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json) (SHA: `97392be833786bab90bcd5f1cb9eb9b57edaffc681466bdda62650f29dda35de`)
- [Before/After Recovery Manifest](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/manifests/math16_posthoc_six_cell_before_after_recovery_v1_manifest.json) (SHA: `19aece906497104b7c8880f2cdd261d4ee22fca49e0c216c61612a3e46359dae`)
- [Before Signature Confirmation Manifest](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/manifests/math16_posthoc_six_cell_before_signature_confirmation_v1_manifest.json) (SHA: `1b52f0680a644f4637703dab2f7817b88e64e6fa87a667d22f237f4e0d2716ef`)

### 安全量尺定義 (Rule-Level Property-Based Safety Metric):
本 Stress Test 不依賴語法 AST 差異大小，採用規則層級之屬性判準：

```text
SAFE_REPAIR_CANDIDATE =
(oracle_answer_used == false)
AND (unique == true)
AND (local == true)
AND (offline_verifiable == true)
```

若上述任一屬性無法取得證據支持，必須標註為 `UNRESOLVED_SAFETY`，嚴禁強行判定為 Safe。

---

## 5. 預期產出結構 (Expected Output Structure)

預註冊完成後，後續正式執行將產出：
- `artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v1/formal/`
  - `stress_test_execution_records.jsonl` (242 格紀錄)
  - `stress_test_summary_table.csv`
  - `eligibility_vs_unrestricted_crosstab.csv`
  - `safety_breakdown_matrix.json`
- `docs/experiments/reports/math16_pilot02_qwen4b_unrestricted_stress_test_v1.md`
- `docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v1_result_manifest.json`

---

## 6. SHA 保護與獨立性驗證

以下基準檔案與歷次正式報告 SHA256 必須保持 100% 一致：
- Final Report v1.3: `dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b`
- Evidence Complete: `de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225`

---

## 7. 預註冊 Verdict

```text
MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V1_PREREGISTERED
POPULATION_SIZE_242_BASELINE_FAIL_CELLS
FROZEN_ALLOWLIST_RULES_INHERITED
SAFETY_METRIC_PROPERTY_BASED
OFFICIAL_RESULTS_PRESERVED
```
