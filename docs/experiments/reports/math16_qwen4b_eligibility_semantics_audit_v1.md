# Math16 Qwen4B Eligibility Semantics Audit Report v1

```text
MATH16_QWEN4B_ELIGIBILITY_SEMANTICS_AUDIT_V1_COMPLETED
RULE_DETECTION_AND_SAFETY_GATE_DISTINGUISHED
STRESS_TEST_INTERVENTION_CONTRAST_CONFIRMED
UNRESTRICTED_STRESS_TEST_V11_PREREGISTERED
OFFICIAL_RESULTS_PRESERVED
READY_FOR_ZERO_MODEL_V11_DRY_RUN
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告版本：** v1.0 (Eligibility Semantics Audit Report)
**標的數據庫：** Math16 Pilot-02 Qwen 3.5 4B（242 個 Baseline FAIL cells）

---

> **固定聲明 (Mandatory Disclaimer)：**
> 本分析為 Evidence Complete 凍結後之 Post-hoc 補充 Eligibility 語意稽核，不修改、取代或重新解釋既有 Primary 與正式 Post-hoc 結果。

---

## 1. 執行摘要 (Executive Summary)

本報告對 **Qwen 3.5 4B** 320 個實驗 cells 中之 242 個 Baseline FAIL cells 進行完整、唯讀的 Healer 語意三層架構盤點與 242 格互斥分層，旨在精準回答「取消 Eligibility」究竟取消了哪一層，並釐清與修訂 **Unrestricted Stress Test v1.1** 預註冊。

### 核心發現：
1. **Healer 運轉之三層架構明確釐清**：
   - **Layer 1: Rule Candidate Detection** (規則候選偵測)：純語法／模式匹配，判斷是否命中 6 條凍結 allowlist 規則之特徵前置條件。
   - **Layer 2: Primary Eligibility Gate** (安全與資格閘門)：獨立檢驗候選規則是否滿足四項安全屬性（`oracle_answer_used == false`, `unique == true`, `local == true`, `offline_verifiable == true`）及非歧義／代碼抽取完整性。
   - **Layer 3: Transformation Execution** (實際修復執行)：僅當 Layer 1 與 Layer 2 同時通過時發動程式碼轉換。
2. **Primary Eligible 與 Rule Match 之語意解耦**：
   - 在 242 個 FAIL 案例中，共有 10 個 cells 命中單一規則且通過 Layer 2 安全閘門（`UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE`）；另有 1 個 cell 涉及歧義入口點（`qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`，劃歸 `AMBIGUOUS_MULTIPLE_CANDIDATES`）；其餘 231 個 cells 均未命中任何凍結 allowlist 規則（`NO_RULE_CANDIDATE`）。
3. **Stress Test 可行性與情況 B 確認**：
   - 因 `UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE (0) + AMBIGUOUS_MULTIPLE_CANDIDATES (1) = 1 > 0`，符合**情況 B**，正式確定具備處置對比空間。據此正式修訂並提出 **Unrestricted Stress Test v1.1** 預註冊。

---

## 2. 三層架構與核心四問解答 (Three-Layer Architecture & Answers)

### Q1: Primary Eligible 是否等同 Rule Match？
**否（語意解耦，雖在 242 格中數值高度接近）**。Layer 1 (Rule Match) 為語法偵測，Layer 2 (Primary Eligibility Gate) 為獨立安全校驗與歧義過濾。

### Q2: Eligibility 是否包含獨立安全閘門？
**是**。Primary Eligibility Gate 包含獨立的安全校驗屬性（`oracle_answer_used == false`, `unique == true`, `local == true`, `offline_verifiable == true`）以及歧義與原始碼抽取檢查。

### Q3: 10 格 Eligible 是如何逐格產生？
- `7 格`: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` (模型生成 bare scalar `oracle_payload`)
- `1 格`: `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` (`json.dumps` 圍繞 `correct_answer`)
- `1 格`: `L1_PROSE_RESIDUE_NARROW` (去除 markdown 說明殘留)
- `1 格`: `L1_CLOSE_UNBALANCED_PARENTHESIS` (補全未閉合括號)

### Q4: Noneligible 232 格中，是否存在「Rule Candidate 已命中但被安全閘門擋下」？
**存在 1 格歧義案例** (`qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`，因 Ambiguous Entry Point 被 Healer 依規定 Abstain)，其餘 231 格均為 `NO_RULE_CANDIDATE` (227 格無規則 Pattern 命中 + 4 格無可抽取原始碼)。

---

## 3. 242 格 Baseline FAIL 候選分層矩陣 (Candidate Strata Matrix)

| 分層類別 (Strata) | Cell 數量 | 佔比 (%) | Stress Test 處置原則 (v1.1 Policy) |
|---|---:|---:|---|
| `NO_RULE_CANDIDATE` | 231 | 95.45% | **強行 NO_OP / ABSTAIN**（不得無規則任意修改） |
| `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE` | 10 | 4.13% | **強制進入 Transform 組** |
| `UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE` | 0 | 0.00% | N/A |
| `AMBIGUOUS_MULTIPLE_CANDIDATES` | 1 | 0.41% | **獨立形成 Abstain Arm / 預註冊 Forced Exploratory Arm** |
| `DETECTION_UNRESOLVED` | 0 | 0.00% | N/A |
| **總和 (Total Baseline FAIL)** | **242** | **100.00%** | **五類互斥且總和為 242** |

---

## 4. Unrestricted Stress Test v1.1 處置政策與雙重分類 (v1.1 Policy)

在修訂之 v1.1 預註冊中，正式取消的是 **Layer 2 Primary Safety Eligibility Gate**，但保留 **Layer 1 Rule Candidate Detection**：

### 4.1 雙重分類架構 (Outcome × Safety Dual Classification)
所有實際發動修改之案例，必須同時記錄 Outcome 與 Safety 兩個獨立維度：

- **Outcome 維度**: `MODIFIED_RESCUED`, `MODIFIED_STILL_FAIL`, `MODIFIED_NEW_FAILURE`, `MODIFIED_UNEVALUABLE`
- **Safety 維度**: `SAFE_REPAIR_CANDIDATE`, `UNSAFE_MODIFICATION`, `UNRESOLVED_SAFETY`

### 4.2 偶然救回 (Accidental Rescue) 嚴格定義
```text
ACCIDENTAL_RESCUE =
(Outcome == MODIFIED_RESCUED) AND (Safety == UNSAFE_MODIFICATION)
```
> **強行規定**：偶然救回 (Accidental Rescue) **嚴禁算作安全修復成功 (Safe Rescue)**！其數值將獨立記錄於警示分類中，用以證明若無 Primary Eligibility 防禦，不安全修改將導致破壞性救回。

---

## 5. 文件血緣與 SHA 保護 (File Provenance & SHA Integrity)

以下歷次正式報告與 Manifest SHA256 經比對 100% 保持未變：
- Final Report v1.3: `dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b` (未修改 ✅)
- Evidence Complete: `de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225` (未修改 ✅)
- Stress Test v1 Spec: `cbfdbcaacfa3f237bf32aa11e2f75a7c2fa8e734bc1fc4cf6dbfa48a4d4681fb` (保留完整，未覆寫 ✅)

---

## 6. 結案 Verdict

```text
MATH16_QWEN4B_ELIGIBILITY_SEMANTICS_AUDIT_V1_COMPLETED
RULE_DETECTION_AND_SAFETY_GATE_DISTINGUISHED
STRESS_TEST_INTERVENTION_CONTRAST_CONFIRMED
UNRESTRICTED_STRESS_TEST_V11_PREREGISTERED
OFFICIAL_RESULTS_PRESERVED
READY_FOR_ZERO_MODEL_V11_DRY_RUN
```
