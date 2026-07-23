# 《Math16 Eligibility 與 Unrestricted Stress Test 驗證附錄 v1》

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**文件類型：** 正式審查附錄 B (Official Review Appendix B)
**建置時間 UTC：** 2026-07-23

---

> **摘要 (Abstract - 188字)：**
> 本附錄針對 Math16 Healer 之 Eligibility 資格閘門與 Unrestricted Stress Test v1.1 進行驗證。242 格 Baseline FAIL 母體中，231 格因無凍結規則可用而 Abstain，10 格為 Safe Candidate（救援 5 格 / post-hoc 6 格），僅 1 格為 Ambiguous Candidate。在強行取消閘門發動 Forced 探索後，該歧義格修剪後仍因 `missing_entry_point` 評估為 FAILED。這證實 Eligibility 範圍雖窄，但具備實質安全防禦價值。

---

## 1. Healer 三層運作架構 (Three-Layer Architecture)

Math16 Healer 具備嚴謹的三層分工架構：
1. **Layer 1: Rule Candidate Detection (規則候選偵測)**
   純語法特徵掃描，檢查輸入代碼是否命中凍結 allowlist 中的 6 條規則模式。
2. **Layer 2: Primary Safety Eligibility Gate (安全與資格閘門)**
   獨立安全判準過濾器，檢查 4 大安全屬性 (`oracle_answer_used == false`, `unique == true`, `local == true`, `offline_verifiable == true`) 並拒絕多重歧義入口。
3. **Layer 3: Transformation Execution (實際修復執行)**
   當 Layer 1 偵測與 Layer 2 安全閘門同時通過時，正式發動程式碼轉換。

---

## 2. 242 格 Baseline FAIL 互斥分層與處置 (Strata Breakdown & Dispositions)

### 2.1 固定帳目表 (242 Baseline FAIL Strata Table)

| 分層名稱 (Strata Name) | 數量 (Cells) | 佔比 (%) | Default Arm 處置說明 |
|---|---:|---:|---|
| **NO_RULE_CANDIDATE** | 231 | 95.45% | `ABSTAIN_NO_RULE` (無凍結規則 pattern 命中) |
| **UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE** | 10 | 4.13% | `PLANNED_TRANSFORM` (發動確定性修復與評估) |
| **UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE** | 0 | 0.00% | (無此類案例) |
| **AMBIGUOUS_MULTIPLE_CANDIDATES** | 1 | 0.41% | `ABSTAIN_AMBIGUOUS` (多重歧義入口點，依規 Abstain) |
| **DETECTION_UNRESOLVED** | 0 | 0.00% | (無未能解析案例) |
| **總和 (Total Baseline FAIL)** | **242** | **100.00%** | **五類互斥且總和恰為 242** |

### 2.2 關鍵發現
1. **無規則可施為主要主因**：231/242 (95.45%) 的失敗 cell 根本沒有對應的凍結修復規則，並非 Eligibility 閘門過度嚴格。
2. **非資格候選格為 0**：`UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE = 0`，代表沒有任何「單一規則命中但被 Eligibility 誤擋」的遺珠。
3. **閘門實際處置處**：Eligibility 閘門實際處置的僅為 1 格多重歧義案例 (`AMBIGUOUS_MULTIPLE_CANDIDATES = 1`)。

---

## 3. 兩個 Arm 執行結果分帳 (Two-Arm Results Accounting)

### 3.1 Default Arm (242 cells)
- **`ABSTAIN_NO_RULE`**: 231 格
- **`ABSTAIN_AMBIGUOUS`**: 1 格
- **10 格 Transformed 評估分帳**:
  - **Primary**: Rescued `5`, Still Fail `5`, New Failure `0`, Regression `0`
  - **Corrected Technical**: Rescued `6`, Still Fail `4`, New Failure `0`, Regression `0`

### 3.2 Forced Exploratory Arm (1 cell)
- **標的 Cell**: `qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`
- **命中規則與選擇政策**: `L1_PROSE_RESIDUE_NARROW` + `DETERMINISTIC_FIRST_ENTRY_POINT_SOURCE_PREORDER` (`first_def_generate_offset`)
- **Safety 預分類**: `UNSAFE_MODIFICATION` (絕對禁止標註為 `SAFE_REPAIR_CANDIDATE`)
- **Evaluator 評估結果**: **`FAILED`** (原因 `missing_entry_point`)
- **Outcome 分類**: `MODIFIED_STILL_FAIL`
- **Accidental Rescue**: `false`
- **New Failure / Regression**: `0` / `0`
- **證據鏈**: Transformed 原始碼與 Unified Diff 100% 配對存盤於 `artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal/`。

---

## 4. 防禦價值與精確語意解讀 (Defense Value & Accurate Interpretation)

> **正確嚴謹結論 (Mandatory Precision Statement)：**
> 歧義閘門避免了一次無法預先證明安全、且實際未能救回程式的介入 (`ambiguity_gate_prevented_harm = True`)。

### 嚴格禁止的誇大表述：
- ❌ **不得寫**：「已證明避免了實際毀損/破壞」（評估結果僅為 `missing_entry_point` 仍 FAIL，未產生新語法崩潰）。
- ❌ **不得寫**：「所有歧義修復都一定會失敗」。
- ❌ **不得寫**：「Eligibility 具備廣義的因果效果」。

---

## 5. 評審／老師關切問答 (Teacher / Jury Q&A)

### Q1: 為什麼 242 格只修 10 格？
**答：** 因為在 242 格 Baseline FAIL 案例中，有 231 格 (95.45%) 根本沒有命中任何凍結的修復規則 Pattern。Healer 修得少是因為模型錯誤型態多樣且缺乏對應規則，而非 Eligibility 閘門過度嚴格。

### Q2: 231 格為什麼不強迫修改？
**答：** 在沒有明確語法規則命中前發動任意代碼修改，屬於無根據的偽修復，會嚴重破壞科學實驗的控制變因與確定性原則。

### Q3: Eligibility 是什麼？
**答：** Eligibility 是 Healer 內部的第二層安全閘門。它在規則命中後，額外檢查 4 大安全屬性並過濾多重歧義入口，確保修復動作可離線驗證且不偷看答案。

### Q4: 取消 Eligibility 後新增了多少可修改案例？
**答：** 取消 Layer 2 Eligibility 閘門後，在全部 242 格 FAIL 母體中，真正釋放出來能進行對比修改的案例**僅有 1 格**（即唯一的歧義案例）。

### Q5: 為什麼真正新增對比只有 1 格？
**答：** 因為在 242 格中，231 格無規則可用、10 格本就屬於 Primary Eligible，而單一規則非資格案例 (`NONELIGIBLE`) 為 0。因此唯一受 Eligibility 攔截的僅有這 1 格歧義案例。

### Q6: Forced 案例為什麼不算安全修復？
**答：** 因為該案例包含多個未隔離的 Entry Point 切割邊界，修剪 Prose 有截斷關鍵變數的結構風險，無法滿足離線可驗證性，故強制預分類為 `UNSAFE_MODIFICATION`。

### Q7: Forced 案例失敗代表什麼？
**答：** 代表強行修剪 Prose 後，代碼中仍包含第二個未隔離片段，Evaluator 仍判定為 `missing_entry_point` 失敗。這證實當初 Eligibility 閘門將其擋下是正確的。

### Q8: 沒有 Regression 是否代表永遠安全？
**答：** 不代表。沒有 Regression 僅代表在本實驗的特定測試案例中未引發得分倒退，不能保證在所有未知場景下皆絕對安全。

### Q9: Eligibility 能保證修成功嗎？
**答：** 不能。Eligibility 僅能保證修復動作符合安全屬性且不破壞架構；修復後的代碼能否得滿分，仍取決於邏輯本身是否正確。

### Q10: 這個 Stress Test 最重要的結論是什麼？
**答：** 最重大的結論是：Primary Eligibility 閘門非常精準地覆蓋了全部可安全救回的潛在窗口，且成功攔截了無效的歧義介入，兼具精準度與防禦價值。

---

## 6. 獨立證據索引 (Independent Evidence Index)

| 主張 (Claim) | 檔案路徑 (Artifact Path) | Manifest 路徑 | SHA256 | 支持內容 |
|---|---|---|---|---|
| 242 FAIL 互斥分層 (231/10/0/1/0) | `artifacts/math16_qwen4b_eligibility_semantics_audit_v1/candidate_strata_table.csv` | `docs/experiments/manifests/math16_qwen4b_eligibility_semantics_audit_v1_manifest.json` | `7384bca4790a5362fe200819591e358b087374d42ea7eafbb715782a7e99468c` | 語意稽核呈現完整 242 格分層帳目 |
| Default 10 格與 Forced 1 格處置結果 | `artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal/disposition_summary.json` | `docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json` | `7cfc9f8f4de8b1fbf56ef19afdedba5dc43fd3ee70fe35d72c46cfeff33cdcf0` | 處置摘要紀錄 10 格救援與 Forced 1 格 FAILED |
| Forced 歧義格 Unified Diff 完整存盤 | `artifacts/math16_pilot02_qwen4b_unrestricted_stress_test_v11/formal/unified_diffs/qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004_forced.diff` | `docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json` | `7cfc9f8f4de8b1fbf56ef19afdedba5dc43fd3ee70fe35d72c46cfeff33cdcf0` | Unified diff 存檔紀錄前置與修剪後代碼 |
