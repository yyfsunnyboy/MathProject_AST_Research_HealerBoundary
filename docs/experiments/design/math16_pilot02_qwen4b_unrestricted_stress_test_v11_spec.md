# Math16 Qwen4B Unrestricted Healer Stress Test v1.1 Specification

```text
MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_PREREGISTERED
THREE_LAYER_ARCHITECTURE_REFLECTED
LAYER2_SAFETY_GATE_REMOVED_FOR_UNRESTRICTED
LAYER1_DETECTOR_AND_NO_CANDIDATE_NO_OP_PRESERVED
OUTCOME_BY_SAFETY_DUAL_CLASSIFICATION_MANDATED
OFFICIAL_RESULTS_PRESERVED
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**規格版本：** v1.1 (Refined Preregistration Specification)
**前版規格：** `docs/experiments/design/math16_pilot02_qwen4b_unrestricted_stress_test_v1_spec.md` (保留不蓋)
**標的數據庫：** Math16 Pilot-02 Qwen 3.5 4B（242 個 Baseline FAIL cells）

---

> **固定聲明 (Mandatory Disclaimer)：**
> 本實驗為 Evidence Complete 凍結後之 Post-hoc 補充 Stress Test v1.1，不修改、取代或重新解釋既有 Primary 與正式 Post-hoc 結果。

---

## 1. 三層架構與 v1.1 核心修訂 (Three-Layer Architecture & Revisions)

根據 **Eligibility Semantics Audit v1** 之發現，Healer 運算流程分為三層：
1. **Layer 1: Rule Candidate Detection** (規則候選偵測)
2. **Layer 2: Primary Safety Eligibility Gate** (安全與資格閘門)
3. **Layer 3: Transformation Execution** (實際修復執行)

在 **Unrestricted Stress Test v1.1** 中：
- **真正被取消的是 Layer 2 (Primary Safety Eligibility Gate)**。
- **Layer 1 (Rule Candidate Detection) 依然保留**：無規則候選 (231 個 `NO_RULE_CANDIDATE` cells) **強制實施 NO_OP / ABSTAIN**，不得對未命中規則之程式進行隨意修改。
- **歧義處置政策 (Ambiguous Handling Policy)**：`AMBIGUOUS_MULTIPLE_CANDIDATES` (1 cell: `qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`) 不得自動套用首條規則，於預設組實施 Abstain，於 Forced Exploratory Arm 中獨立對比。

---

## 2. 雙重分類維度與 Accidental Rescue 嚴格定義 (Dual Classification)

所有實際發動修改之案例，必須同時記錄 Outcome 與 Safety 雙重維度：

### 2.1 Outcome 維度
- `MODIFIED_RESCUED`: 修改後單元測試通過 (PASS)
- `MODIFIED_STILL_FAIL`: 修改後單元測試仍失敗 (FAIL)
- `MODIFIED_NEW_FAILURE`: 修改後引發新錯誤 / 語法毀損 (Regression)
- `MODIFIED_UNEVALUABLE`: 無法評估

### 2.2 Safety 維度 (Property-Based Rule-Level Metric)
```text
SAFE_REPAIR_CANDIDATE =
(oracle_answer_used == false)
AND (unique == true)
AND (local == true)
AND (offline_verifiable == true)
```
- `SAFE_REPAIR_CANDIDATE`: 四項屬性均有前置證據支持
- `UNSAFE_MODIFICATION`: 缺少任一屬性支持之修改
- `UNRESOLVED_SAFETY`: 證據不足

### 2.3 偶然救回 (Accidental Rescue) 嚴格判定
```text
ACCIDENTAL_RESCUE = (Outcome == MODIFIED_RESCUED) AND (Safety == UNSAFE_MODIFICATION)
```
> **強行規定**：Accidental Rescue 絕不可算作安全修復成功 (Safe Rescue)！

---

## 3. 242 格處置政策 (Cell Handling Policy)

- `NO_RULE_CANDIDATE` (231 cells): **NO_OP / ABSTAIN**
- `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE` (10 cells): **Transform (Forced Pass)**
- `UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE` (0 cells): N/A
- `AMBIGUOUS_MULTIPLE_CANDIDATES` (1 cell): **Abstain (Default) / Forced Exploratory Arm**
- `DETECTION_UNRESOLVED` (0 cells): N/A

---

## 4. 預註冊 Verdict

```text
MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V11_PREREGISTERED
THREE_LAYER_ARCHITECTURE_REFLECTED
LAYER2_SAFETY_GATE_REMOVED_FOR_UNRESTRICTED
LAYER1_DETECTOR_AND_NO_CANDIDATE_NO_OP_PRESERVED
OUTCOME_BY_SAFETY_DUAL_CLASSIFICATION_MANDATED
OFFICIAL_RESULTS_PRESERVED
```
