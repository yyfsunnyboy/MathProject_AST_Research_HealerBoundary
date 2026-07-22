# Math16 Pilot-02 Final Report v1.3 人工全文驗收與最小修正建置報告

## 1. 第4／16節核對
- 修正前：兩處均以「確保...不會/不將...」描述 Regression 防線，屬保證語氣。
- 修正後：改為「降低...風險」之風險緩解語氣，不再宣稱保證或確保零倒退。
- `Regression = 0` 僅維持第18節第8項「僅屬實證觀察」之既有正確措辭，未變動。

## 2. 第14節核對
- 修正前：「結果證實失敗主因在於...而非評分 Parser 偏差」，屬過度宣稱（證實主因）且隱含完全排除 Parser。
- 修正後：改為「診斷結果不偏向以評分 Parser 偏差為主要失敗來源；此結論僅限定於已剖析之 27 格診斷樣本，未建立 Prompt 結構與生成錯誤之因果關係，亦不可外推為全域比例或完全排除 Parser 影響」。
- 21/27、18.5%／5/27 等凍結數字未變動，僅修正詮釋語氣與範疇聲明。

## 3. 第15節 Figure 2 核對
- 修正前：附註含「證明在 API 簽名完整補齊後達 80/80」，出現禁用詞「證明」。
- 修正後：改為「顯示在 API 簽名完整補齊後可達 80/80」。
- Gemini 80/80 Post-hoc 標示、Primary spec-v1=63/80、Qwen spec-v2、不作完全同條件因果推論之聲明均維持不變。

## 4. 第5節 16 題識別碼核對
- 逐一對照 `docs/experiments/manifests/math16_three_model_five_seed_manifest.json` 之 `task_ids`（16 題）。
- 修正前：使用不存在於正式 manifest 之簡化別名（`ce101`–`ce134` 風格）。
- 修正後：改列正式 16 題 ID，並依 Qwen 9B `family_summary.json` / `task_summary.json` 逐題通過數加總驗證家族歸屬完全一致（Integer=42、Polynomial=9、Radical=19、Fraction=31，均與 family_summary.json 吻合）。

## 5. 第20節核對
- 修正前：「...系統依凍結規則選擇 Abstain，有效維護整體架構之安全性與可解釋性」，隱含安全保證宣稱。
- 修正後：「...降低盲目修改帶來之風險並維持整體架構之可解釋性」，僅陳述風險降低與可解釋性維持，不宣稱保證安全。

## 6. 已通過帳目與第18節限制核對（未破壞）
- Primary／Post-hoc：`78/320 → 83/320`（rescue=5）；Post-hoc `84/320`（total rescue=6），相較 Primary 僅多 1 個 PASS —— 維持不變。
- Fraction：`NINE_B_ONLY=21`、`L1–L4=15`、`L5=6` —— 維持不變。
- Corrected-chain：`10／8／2／1` —— 維持不變。
- 第18節方法學限制：仍為 10 項，逐項標題與範圍未變動。

## 7. 實際修改位置
1. **title and report marker**：version label v1.2 -> v1.3; marker updated to V13_FINALIZED
2. **Section 4**：removed guarantee wording '確保不將...修改至失效狀態' -> reworded as risk reduction ('降低...風險')
3. **Section 5**：replaced fictional placeholder task ids (ce101-ce134 style) with the official 16 task_ids from math16_three_model_five_seed_manifest.json, grouped by family and verified against per-task qwen9b evaluation pass counts
4. **Section 14**：removed '結果證實失敗主因' overclaim; added explicit 27-cell sample bound, removed causal Prompt claim, avoided fully excluding Parser as a contributing factor
5. **Section 15 (Figure 2 note)**：removed '證明' overclaim wording -> reworded as descriptive '顯示'
6. **Section 16**：removed guarantee wording '確保修改不會破壞原本正確之程式' -> reworded as risk reduction
7. **Section 20 conclusion item 3**：removed '有效維護...安全性' safety-guarantee wording -> reworded as risk reduction + interpretability maintenance
8. **Section 18 item 4（同版號勘誤）**：舊值 `` `ce115` ``；新值 `` `ce115_calc_polynomial_division_l1` ``。此為單點正式 task_id 勘誤；無數字、結論、Primary／Post-hoc 分帳、Fraction 21／15／6、corrected-chain 10／8／2／1、限制內容或圖表變動。

## 8. v1.3 同版號勘誤凍結
- 本次不開 v1.4；v1.3 僅完成第18節第4項的非正式 task_id 勘誤。
- 全文裸露 `` `ce115` `` 引用為 0；`ce115_calc_polynomial_division_l1` 已出現在第5、14、18節。
- 第18節仍為 10 項限制；六張圖與凍結統計數字均未變更。

## 9. SHA 保護與來源未修改
- v1 SHA-256：`1a168805bfd8f2c076d2e8fd0556e90b049648e771d3481cc35abaeac250e730`
- v1.1 SHA-256：`a9df82efc2424b3c4f15b9f6daa725d2f40371d2c3be659a70fc5f494166cfe7`
- v1.2 SHA-256：`1e10eb3319272421f4866712a01c40eea12c4140d7264124c0fba4fb54c787b4`
- 正式 Task Roster SHA-256：`47a94f0e365d38e8c7bf107d1486de9432651723c261acd544023423ad85d298`
- Evidence Complete manifest SHA-256：`de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225`
- Integrated report SHA-256：`a13f0e0b71a1d1f0f0bc0ab0fdcecfc330c18238d0bd434218447939568992ca`
- Q&A SHA-256：`b2b0d2a750e5edf0a8b88cf31c2b238fa502d92787f220a9ca2d270e9e116741`
- v1.3 SHA-256：`dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b`
- v1、v1.1、v1.2、Evidence Complete、Integrated report、Q&A、六張核心圖均未修改。
