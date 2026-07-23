# Math16 Pilot-02 評審追問與標準應答手冊 (Jury Defense Q&A Final v1)

```text
MATH16_PILOT02_JURY_QA_FINAL_PRECISION_CLEANUP_COMPLETED
Q9_GEMINI_V2_BOUNDARY_CLARIFIED
Q17_CORRECTED_CHAIN_DISPOSITION_RECONCILED
OVERCLAIMS_REMOVED
CATEGORY_B_QA_COMPLETED
```

> **使用說明**：
> 本手冊為「Ivan旺宏科學展」HealerBoundary 研究線之正式口試 defense 檔案。
> 每一題目均包含：
> 1. **正式回答**：適用於成果報告書、論文與評審正式書面審查（2~5句，嚴謹客觀）。
> 2. **口試短答**：適用於現場口頭報告與評審快速追問（1~2句，20~60字，高中生自然口語）。

---

## 一、 19 題評審追問與標準應答

### Q1: 為什麼要先做 Eligibility 審查，不直接全部程式都嘗試修復？
**正式回答：** 若不設 Eligibility 門檻，修復器將被迫對無明確修復依據的程式進行猜測性修改，破壞可解釋性並可能引入倒退 (Regression)。Eligibility 是維護「確定性安全介入」的必要防禦。
**口試短答：** 因為缺乏明確規則強行盲目修復會破壞可解釋性並把程式改壞。Eligibility 能確保修復只在修法唯一且安全時介入。

### Q2: Gemini 與 9B 的 `eligible=0` 是否代表 Healer 沒有用？
**正式回答：** 不是。`eligible=0` 代表在本次 320 個單元與現有凍結規則下，失敗案例未同時滿足唯一、安全、可驗證的介入條件。Healer 在無適用規則時選擇 Abstain（不介入），屬符合規範的安全行為。
**口試短答：** 不是。`eligible=0` 代表現有規則未命中失敗案例，Healer 選擇 Abstain 主動放棄猜測，這展現了強烈的安全邊界防禦。

### Q3: 為什麼 4B 可以修復 5~6 格，9B 反而 0 格？
**正式回答：** 因為 4B 模型的失敗案例中恰好有 10 格命中事前凍結的特定語法與 JSON 瑕疵規則（如 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 等）；而 9B 雖然也有語法、執行與語義失敗，但沒有案例同時符合唯一且安全的現有修法條件。修復視窗取決於失敗型態是否落在凍結規則內。
**口試短答：** 4B 有 10 格命中凍結規則；9B 雖有語法與執行失敗，但沒有案例符合唯一且安全的現有修法。

### Q4: 9B Polynomial 只有 9/80，是否代表 9B 的數學能力比 4B 差？
**正式回答：** 不能這樣解讀。9B 總體通過數 (101/320) 高於 4B (78/320)。Polynomial 的低下高度集中於 `ce115_calc_polynomial_division_l1` 單一題型，與多個 LaTeX 欄位組裝高度共現，屬特定提示結構敏感性，尚未證實因果，不可外推為 9B 全域失控或純數學能力落後。
**口試短答：** 不能。9B 總分高於 4B，Polynomial 偏低集中於單一多項式題型與 LaTeX 組裝衝突，屬於結構敏感性，未證明因果。

### Q5: 為什麼不修改 Evaluator 的 Parser 讓採分更寬鬆？
**正式回答：** Evaluator 的職責是維護嚴謹的評分契約。在 Qwen 4B Ab2d+api 27 格診斷樣本中，21/27 格 (77.8%) 屬候選 Python 本體內部的 SyntaxError (如括號不平衡或字串未閉合)，僅 5/27 格 (18.5%) 屬 parser 不友善，1/27 格 (3.7%) 屬真邏輯錯誤。結果不支持「Evaluator Parser 不公平是主要失敗來源」；隨意放寬 Parser 並無法修復破損的 Python 程式本體。
**口試短答：** 因為評分標準必須嚴謹，且診斷顯示 77.8% 的失敗是 Python 程式本體壞掉，放寬 Parser 並無法修復語法錯誤的程式。

### Q6: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**正式回答：** 因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合、語法結構混亂）並沒有唯一的修復解答。若強行修復將違反「修法唯一、不可反推答案」的核心原則，帶來極高修壞風險。
**口試短答：** 因為大多數語法錯誤沒有唯一的解答，強行盲猜修改會破壞可解釋性，違反 deterministic 修復的核心規範。

### Q7: 為什麼 Primary (83/320) 與 Post-hoc (84/320) 要嚴格分帳？
**正式回答：** 因為 83/320 是事前預註冊 Protocol 產生的唯一正式數據；84/320 是事後修正 false-loop revalidation 邏輯後的探討結果。科學規範要求嚴格區分預註冊結論與事後探討，不可將事後探討冒充為事前結論。
**口試短答：** 因為 83/320 是事前凍結實驗的預註冊數據，84/320 是事後除錯的探討結果。嚴謹研究不能拿事後結果冒充事前結論。

### Q8: Gemini 基線已經 289/320 (90.3%)，為什麼還要研究 Healer？
**正式回答：** 本研究的核心目標是探索「修復邊界」。在本次 Gemini、題目與凍結規則下，剩餘失敗沒有形成安全的 Healer 介入視窗；而 Post-hoc 提示修復實驗 (306/320) 則揭示了強模型在 API 簽名補齊後的真實天花板。
**口試短答：** 本研究旨在劃定 Healer 的修復邊界。在本次 Gemini 測試與凍結規則下，剩餘失敗沒有形成安全的 Healer 介入視窗。

### Q9: Ab2d+spec-v2 是不是最好的 Prompt 條件？
**正式回答：** 對 4B 與 9B 而言，Ab2d+spec-v2 在本次正式四條件比較中通過數最高，分別為 36/80 與 40/80。Gemini 的正式生成只比較到 Ab2d+spec-v1，其中 Ab2d+api 為 78/80、spec-v1 為 63/80；Gemini 沒有正式重新生成 Ab2d+spec-v2。後續 80/80 僅是 Post-hoc API 文件補齊機制驗證，因此不能當作正式四條件比較結果。Prompt 效果依模型、提示版本與部署條件而異。
**口試短答：** 4B 和 9B 正式跑過 v2，規格較有幫助；Gemini 正式只跑到 v1，後來的 80/80 是事後機制驗證，不能當正式比較。

### Q10: 為什麼 FAIL 有 242 個，可修復的 (Eligible) 卻只有 10 個？
**正式回答：** 因為 LLM 生成程式的失敗大多是演算法邏輯不通或結構大段缺失，真正屬於「程式本體正確、僅差語法臨門一腳且有唯一修法」的瑕疵案例本來就非常稀少。
**口試短答：** 因為多數 failure 是邏輯不通或整段 missing，真正只差臨門一腳語法瑕疵且有唯一修法的案例本來就很稀少。

### Q11: Abstain（不介入）是不是代表 Healer 的能力不足？
**正式回答：** 不是。知曉「何時不該介入」與「何時該介入」同等重要。Abstain 是控制 Regression 風險的防禦機制，代表系統在面臨不明確修復目標時主動放棄盲猜。
**口試短答：** 不是。知道何時不該猜是安全的表現，Abstain 能防止系統盲目修改而把原本可能的程式改壞。

### Q12: 這個研究真正的新發現是什麼？
**正式回答：** 我們劃定了 Deterministic AST Healer 的精確價值邊界：Healer 並非第二個解題模型，而在特定表面語法瑕疵區域提供可解釋防禦，且在本次命中凍結規則的修復案例中，觀察到 regression=0。
**口試短答：** 我們劃定了 Healer 的價值邊界：證明在本次命中凍結規則的修復案例中，觀察到 regression=0。

### Q13: 是否有挑選容易修復的案例來美化數據？
**正式回答：** 所有 320 格測試單元均依凍結流程納入全量評估，無人工選擇。Eligibility 審查規則均在實驗啟動前預先凍結，Baseline FAIL 自動進行審查。
**口試短答：** 所有 320 格單元均依凍結流程納入，沒有依結果人工挑選修復案例。

### Q14: Healer 在修復過程中是否有偷看測試集答案？
**正式回答：** Eligibility 審查與修法不依賴正確答案反推，也不以測試 PASS/FAIL 反覆試修。修復後的評估僅用於記錄結果與安全檢查，不反向決定修改內容。
**口試短答：** Eligibility 與修法不依賴正確答案反推，也不依 PASS/FAIL 反覆試修；修復後評估只用於記錄結果。

### Q15: 你們如何確保 Healer 不會把原本寫對的程式改壞 (Regression)？
**正式回答：** 通過兩道防線：(1) Eligibility 審查僅允許失敗模式明確且修法唯一的案例；(2) Revalidation 機制在修復後重新執行靜態檢核。在本次 320 個測試單元中，實際執行修復的案例均觀察到 Regression=0。
**口試短答：** 我們嚴格限制只修復有唯一答案的語法瑕疵，並在修改後再次自動檢核。本次實驗中觀察到 zero regression。

### Q16: 為什麼不新增更多修復規則來救援 9B 的 219 個失敗？
**正式回答：** 因為事前凍結可降低事後配合資料造成的 rule overfitting；新規則應在 development 證據建立，再用未參與建置的資料驗證，以維持實證研究的科學可重複性。
**口試短答：** 事前凍結可降低事後配合資料造成的 rule overfitting；新規則應在開發階段建立，再用獨立資料驗證。

### Q17: 4B 的 Primary (83) 與 Post-hoc (84) 差 1 格，是否代表流程不可靠？
**正式回答：** 10 格 eligible 案例中，有 8 格在 Primary 與 corrected-chain replay 間完全不變；1 格 Radical 由 `no_op` 改為 `rescued`，使 Post-hoc 通過數由 83 增至 84；另 1 格 q09 由 `no_op` 改為 `repaired_still_fail`，但最終仍為 FAIL。因此共有 2 格處置狀態改變，只有 1 格改變最終 PASS/FAIL 結果，且本次觀察到 regression=0。
**口試短答：** 10 格裡 8 格完全不變，2 格處置狀態有改；其中只有 1 格從 FAIL 變 PASS，另一格仍 FAIL，所以 83 與 84 只差 1 格。

### Q18: Overall McNemar 與 Task-clustered Bootstrap 結論看似不同，該如何解讀？
**正式回答：** 兩者代表不同層級的統計檢視。McNemar 顯示本次 320 個 matched cells 中 discordant 方向偏向 9B ($p = 0.010582$)；而 task-clustered bootstrap CI 跨 0 (95% CI `[-0.94%, +14.38%]`)，顯示外推到其他未知題目時仍具抽樣不確定性。
**口試短答：** McNemar 顯示本次 320 個 matched cells 中 discordant 方向偏向 9B；task-clustered bootstrap CI 跨 0，外推到其他題目仍有不確定性。

### Q19: 為什麼 Fraction family 的 9B 優勢最明顯 (淨增加 14 格)？
**正式回答：** 在配對分析中，Fraction 家族 9B 獨勝 $c = 21$ 格，4B 獨勝 $b = 7$ 格，淨增加 14 格 (Exact two-sided McNemar $p = 0.012541$). 在 21 格 9B-only 中，4B 有 15 格 (71.43%) 落在 L1~L4，包括語法 (L1)、契約 (L2)、API (L3) 與執行 (L4) 問題；差距較多反映端到端生成穩定性，不可只解讀為純數學能力差異。
**口試短答：** 21 格 9B-only 中，4B 有 15 格落在 L1~L4，包括語法、契約、API 與執行問題；差距較多反映端到端生成穩定性，不可只解讀為數學能力差異。

---

## 二、 評審口試不可宣稱之事項 (Forbidden Overclaims)

在簡報、論文與口試回答中，**嚴禁使用**以下過度外推或缺乏因果證據的非中性措辭：

1. ❌ **「證明 9B 數學能力全面優於 4B」** $\rightarrow$ ⭕ 應說：「在 320 個測試 cells 中觀察到 9B 通過率較高，但特定家族出現非單調狀況。」
2. ❌ **「Healer 100% 安全、保證絕不倒退 (Zero Regression Guard)」** $\rightarrow$ ⭕ 應說：「在本次 320 個單元及既有凍結規則下，觀察到 Regression = 0。」
3. ❌ **「Polynomial 異常完全是 Prompt 造成的」** $\rightarrow$ ⭕ 應說：「Polynomial 偏低集中於單一題型與 LaTeX 欄位組裝共現，未確認因果責任。」
4. ❌ **「Evaluator Parser 100% 沒有任何限制或偏見」** $\rightarrow$ ⭕ 應說：「診斷數據不偏向以 Evaluator 偏差為主要失敗原因，77.8% 屬候選碼本體 SyntaxError。」
5. ❌ **「Gemini 代表所有雲端大模型的極限」** $\rightarrow$ ⭕ 應說：「Gemini 3.5 Flash 作為強模型參照組，展現了高基線下的 Ceiling Effect。」
6. ❌ **「Post-hoc 數據 (84/320 或 306/320) 是主要的實驗結果」** $\rightarrow$ ⭕ 應說：「Primary 預註冊數據 (83/320) 為唯一正式結果，Post-hoc 僅作探索討論。」



### Q20: Healer 規則的 Provenance（來源與凍結狀態）與雙層學術定位為何？
**正式回答：**
1. **規則凍結狀態 (`rule_freeze_status = PRE_FROZEN_UNCHANGED`)**：六條 Healer 規則及其適用條件均於正式 Math16 320-cell generation 前完成凍結 (d9aa264c)，且後續未修改 detector、eligibility、transform 或 activation scope。
2. **Primary 5 定位 (`validation_status = PROSPECTIVE_WITHIN_MATH16_COHORT`)**：Primary 帳目的 5 格救援屬於預先固定規則在 Math16 cohort 上的前瞻性評估結果；但因規則源自先期開發資料，且尚未在完全獨立資料集驗證 (independent_external_validation = false)，本研究不主張其為外部獨立確認性證據。
3. **Corrected 第 6 格定位 (POST_HOC_TECHNICAL_CORRECTION)**：第 6 格來自既有規則成功 transform 被 runner false-loop rollback 錯誤撤回後的技術修正。此修正未新增或修改 Healer 規則，不改變 PRE_FROZEN_UNCHANGED 狀態；但因屬正式結果揭露後的技術重算，只列入 Corrected technical account，不回寫 Primary。
4. **Payload Wrap 結構 (oracle_payload 內部包裝)**：single-key 指固定三欄回傳結構中 oracle_payload 欄位內部的唯一包裝鍵，不是最外層 return dict 只有一個鍵。Healer 不讀取 correct_answer，oracle_answer_used = false。此結果支持窄範圍、唯一、局部且離線可驗證的 deterministic repair candidate，不代表零副作用或一般語意安全保證。

- 權威 Provenance Audit 報告：docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md (SHA256: 872fb71d602c11c3600fbbf0d762b8dc046a167d00205c460341809f45e70965)
- 權威 Provenance Audit Manifest：docs/experiments/reports/math16_healer_rule_provenance_audit_v1_manifest.json (SHA256: 3e45b5e67d32e6d43a1aea5928af0879e78ac1fdf7244a86c3f5b8f269f99bbf)
- 規則凍結 Commit：d9aa264c | 分類修正 Commit：97c4e985

---

## 三、 最終高風險追問速答

### R1: 六條規則是否看完正式 320 格才寫？
**直接回答：** 不是；規則在正式 generation 前凍結，freeze 後未改邏輯。**證據：** 6/6 `PRE_FROZEN_UNCHANGED`，freeze commit `d9aa264c`。**限制：** 尚無獨立外部驗證。**不可宣稱：** 已完成外部確認性驗證。

### R2: Primary 5 為何可算前瞻性？
**直接回答：** 它是預先凍結規則在 Math16 cohort 內的前瞻性評估。**證據：** 78/320 baseline、10 eligible、5 rescued、83/320 final，分類為 `PROSPECTIVE_WITHIN_MATH16_COHORT`。**限制：** 不等於外部獨立驗證。**不可宣稱：** Primary 5 是外部確認證據。

### R3: Corrected 第 6 格是否事後灌水？
**直接回答：** 不是新增規則，而是 runner rollback 錯誤撤回既有成功 transform 的技術勘誤。**證據：** Corrected=6、84/320，規則仍為 `PRE_FROZEN_UNCHANGED`。**限制：** 屬 `POST_HOC_TECHNICAL_CORRECTION`。**不可宣稱：** Corrected 6 等同 Primary 6。

### R4: 為何不只強化 Prompt？
**直接回答：** Prompt 降低生成錯誤；Healer 處理生成後可唯一、局部、離線判定的窄型契約錯誤。**證據：** 4B 有 242 個 baseline FAIL，僅 10 格符合唯一候選。**限制：** Healer 不是 Prompt 替代品。**不可宣稱：** Healer 優於 Prompt。

### R5: 231/242 無候選是否代表 Healer 失敗？
**直接回答：** 不是；這是介入窗口很窄的負面邊界結果。**證據：** `NO_RULE_CANDIDATE=231`、unique=10、ambiguous=1。**限制：** 僅描述此規則庫與 Math16 cohort。**不可宣稱：** 231 格代表 Healer 無效。

### R6: PASS 案例誤觸會不會造成 regression？
**直接回答：** 不應任意改寫 PASS；detector、eligibility 與 abstain gate 必須分離。**證據：** 本次 Observed Regression=0，候選須唯一、局部、離線可驗證。**限制：** 觀察到零倒退不代表零副作用。**不可宣稱：** Healer 保證安全。

### R7: 9B eligible=0 是模型太強還是規則沒用？
**直接回答：** 只能說 9B 在此 cohort 沒有六條規則可捕捉的失敗型態。**證據：** 9B=101/320、eligible=0，仍有 219 FAIL。**限制：** 不能外推至其他模型或錯誤。**不可宣稱：** 9B 完全不需要 Healer。

### R8: 只有 6 格成功能否泛化？
**直接回答：** 不能；Six-Cell 是機制驗證與自然窗口描述。**證據：** Primary=5、Corrected=6、231/242 無安全候選。**限制：** 仍需未參與規則開發的獨立資料。**不可宣稱：** 六格證明可泛化。
