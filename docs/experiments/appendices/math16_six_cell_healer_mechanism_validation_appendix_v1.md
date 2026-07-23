# 《Math16 六格 Healer 救援機制驗證附錄 v1》

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**文件類型：** 正式審查附錄 A (Official Review Appendix A)
**建置時間 UTC：** 2026-07-23

---

> **摘要 (Abstract - 186字)：**
> 本附錄針對 Math16 實驗中 6 個 Post-hoc 救援案例進行機制驗證。既有 Primary 報告救援 5 格，事後更正鏈修正 false-loop bug 後確認技術救回 6 格；差集唯一 cell 為 `...seed_2026071301`。6 格 100% 命中同一條 L2 規則 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`，6/6 原始 before 代碼已完全回收並經 AST 靜態確認符合前置條件。本附錄提供規則層級證據，受限於既有檔案未留存逐字 after 代碼，不以示意碼冒充真實 diff。

---

## 1. 六格救援來源與分布 (Origin & Distribution)

### 1.1 數據對齊 (Primary 5 vs Corrected Technical 6)
- **Primary Rescued Count**: `5` 格 (既有 Primary 報告呈現)
- **Corrected Technical Rescued Count**: `6` 格 (修正 false-loop rollback bug 後呈現)
- **差集唯一案例**:
  - `cell_id`: `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301`
  - **Primary Disposition**: `NO_OP` (因舊版 runner 誤判迴圈退回)
  - **Corrected Disposition**: `MODIFIED_RESCUED` (評估為 PASSED)
  - **原則屬性**: 非新增規則、非新增 Prompt、非重新生成代碼、非 Oracle 輔助。

### 1.2 Prompt Condition 分布 (Condition Distribution)
- **Ab1 (Native 8B Baseline)**: `0` 格
- **Ab2g (Scaffold General)**: `2` 格 (`ab2g`)
- **Ab2d+api (Scaffold Domain API)**: `2` 格 (`ab2d`)
- **Ab2d+spec-v2 (Scaffold Spec-v2)**: `2` 格 (`ab2d_spec_v2`)
- **總計**: `6` 格

### 1.3 Task Family 分布 (Family Distribution)
- **Radical (根式運算)**: `4` 格
- **Fraction (分數四則)**: `2` 格
- **Integer (整數運算)**: `0` 格
- **Polynomial (多項式)**: `0` 格
- **總計**: `6` 格

---

## 2. 修復機制與安全判準 (Mechanism & Safety Criteria)

### 2.1 根機制與命中規則 (Root Mechanism & Rule)
- **Root Mechanism**: `L2_CONTRACT_SCHEMA_ENTRYPOINT` (契約 schema 介面修復)
- **Hit Rule**: `100%` (6/6) 命中 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
- **問題特徵**: 模型正確生成了題目與答案，但將 `oracle_payload` 誤包裝為單一 Key 字典，不符合執行器介面規範。

### 2.2 四大安全屬性 (Four Safety Properties)
6 格修復案例 100% 滿足以下屬性判準：
1. **`oracle_answer_used = false`**: 未讀取或依賴 Oracle 標準答案進行修改。
2. **`unique = true`**: 語意修復點在 AST 中具備唯一解，無歧義入口。
3. **`local = true`**: 修改僅限於局部介面解包，未動及全局推理邏輯。
4. **`offline_verifiable = true`**: 修改結果可於離線環境以 AST 語法樹靜態驗證。

---

## 3. 證據層級與限制聲明 (Evidence Boundary & Limitations)

1. **Before 代碼驗證**: 6/6 真實 before 原始碼已全數回收存盤，且經 Python AST 靜態掃描 100% 確認回傳字典中含有裸純量 `oracle_payload` 前置條件。
2. **After 代碼限制**: 既有硬碟歷史紀錄僅保存了修復後的 SHA256 雜湊值與評估結果 JSON，並未保存轉譯後的逐字 after 原始碼。
3. **原則誠信**: 本附錄嚴格歸類為 **Rule-Level 證據**，絕不使用模擬或示意程式碼冒充真實 paired diff。

---

## 4. 評審／老師關切問答 (Teacher / Jury Q&A)

### Q1: 到底修成功 5 格還是 6 格？
**答：** 兩者皆為真實現象。在最原始的 Primary Healer 執行中，因舊版迴圈偵測器過度敏感發動退回，故記錄為 5 格；在事後更正鏈（Corrected Chain）修復該評估器邏輯 bug 後，確認實際技術救援成功數為 6 格。

### Q2: 第 6 格是不是事後加規則？
**答：** 絕對不是。第 6 格所 Hit 的規則依然是凍結 allowlist 中的 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`，規則本身完全未變，Prompt 與生成代碼也完全未變，僅為修正了 runner 的 false-loop 退回邏輯。

### Q3: 6 格是不是 6 種不同修法？
**答：** 不是。這 6 格 100% 命中同一條確定性規則 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`，屬於同一種介面格式導正。

### Q4: Healer 有沒有偷看答案？
**答：** 完全沒有。Healer 僅檢查模型輸出的 AST 字典結構，對 Key 名稱進行拆包，整個過程 `oracle_answer_used = false`，未參照任何標準答案。

### Q5: 為什麼沒有完整 before／after diff？
**答：** 因當初實驗 pipeline 的儲存策略為 `sha_only_not_committed_py`（僅留存 SHA256 雜湊與得分紀錄以節省空間）。我們選擇如實說明證據限制，絕不造假。

### Q6: safe candidate 是否代表一定 PASS？
**答：** 不代表。`safe_repair_candidate` 僅代表該修改符合四項安全屬性且不會引入不安全副作用；修復後程式碼是否能順利通過 Evaluator 得分，仍取決於代碼本身的數學邏輯是否正確。

### Q7: 這 6 格能否代表所有題型？
**答：** 不能。這 6 格主要集中於 Radical（4格）與 Fraction（2格），代表特定模型在鷹架導引下常見的介面包裝小瑕疵，不能推廣至所有題型。

### Q8: 這個實驗對研究主題有何意義？
**答：** 證明了小型本地模型 (8B/4B) 產出的代碼常因語法或介面微小瑕疵而失敗，而工程化的語義 Healer 能在不偷看答案、不重跑 LLM 的前提下完成確定性修復。

---

## 5. 獨立證據索引 (Independent Evidence Index)

| 主張 (Claim) | 檔案路徑 (Artifact Path) | Manifest 路徑 | SHA256 | 支持內容 |
|---|---|---|---|---|
| Primary 5 / Corrected 6 | `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json` | `docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json` | `e199110fa67459de663a60f5ca03085b6a1f42cba2c6a0bdd470f36c1ff2266a` | 比較表呈現 5 格與 6 格之差異 cell |
| 6 格同一 L2 規則 | `artifacts/math16_posthoc_six_cell_rescue_audit_v1/formal/six_cell_audit_table.csv` | `docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json` | `97392be833786bab90bcd5f1cb9eb9b57edaffc681466bdda62650f29dda35de` | 6 格均標註為 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` |
| 6/6 Before AST 確認 | `artifacts/math16_posthoc_six_cell_before_signature_confirmation_v1/before_signature_table.csv` | `docs/experiments/manifests/math16_posthoc_six_cell_before_signature_confirmation_v1_manifest.json` | `1b52f0680a644f4637703dab2f7817b88e64e6fa87a667d22f237f4e0d2716ef` | 6/6 AST 靜態確認 100% 吻合前置條件 |
