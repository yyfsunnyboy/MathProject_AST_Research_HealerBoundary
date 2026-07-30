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
**正式回答：** 不能這樣解讀。9B 總體通過數 (101/320) 高於 4B (79/320；本管線原始紀錄為歷史 78/320，經 Method 1/Method 2 交叉稽核確認為候選 artifact 擷取誤選，校正詳見 Correction Note `./math16_baseline_correction_note_v1.md`)。Polynomial 的低下高度集中於 `ce115_calc_polynomial_division_l1` 單一題型，與多個 LaTeX 欄位組裝高度共現，屬特定提示結構敏感性，尚未證實因果，不可外推為 9B 全域失控或純數學能力落後。
**口試短答：** 不能。9B 總分 (101) 仍高於 4B (79，歷史紀錄 78 已校正)，Polynomial 偏低集中於單一多項式題型與 LaTeX 組裝衝突，屬於結構敏感性，未證明因果。

### Q5: 為什麼不修改 Evaluator 的 Parser 讓採分更寬鬆？
**正式回答：** Evaluator 的職責是維護嚴謹的評分契約。在 Qwen 4B Ab2d+api 27 格診斷樣本中，21/27 格 (77.8%) 屬候選 Python 本體內部的 SyntaxError (如括號不平衡或字串未閉合)，僅 5/27 格 (18.5%) 屬 parser 不友善，1/27 格 (3.7%) 屬真邏輯錯誤。結果不支持「Evaluator Parser 不公平是主要失敗來源」；隨意放寬 Parser 並無法修復破損的 Python 程式本體。
**口試短答：** 因為評分標準必須嚴謹，且診斷顯示 77.8% 的失敗是 Python 程式本體壞掉，放寬 Parser 並無法修復語法錯誤的程式。

### Q6: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**正式回答：** 因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合、語法結構混亂）並沒有唯一的修復解答。若強行修復將違反「修法唯一、不可反推答案」的核心原則，帶來極高修壞風險。
**口試短答：** 因為大多數語法錯誤沒有唯一的解答，強行盲猜修改會破壞可解釋性，違反 deterministic 修復的核心規範。

### Q7: 為什麼正式帳目是 Baseline 79/320 → Final 85/320（Verified rescue = 6），而不是 Primary 83 或 Post-hoc 84？
**正式回答：** 因為 79/320 是經過 Method 1/Method 2 交叉稽核與 Confirmatory re-evaluation 確認的校正後 Baseline（原始管線歷史紀錄為 78/320，凍結證據不變，詳見 Correction Note `./math16_baseline_correction_note_v1.md`）；85/320 是基線校正後的正式 Final 數據，Verified rescue 恆為 6 格（該格 healer_eligible=false，從未進入救援母體，故不受基線校正影響）。歷史上曾以事前預註冊 Primary 83/320 與事後修正 false-loop revalidation 邏輯後的 Post-hoc 84/320 嚴格分帳；隨基線校正，舊 Primary 83 在算術上移動為 84，現已降級為附錄/校正註記層級，不再列為主表結果，但歷史 Primary/Post-hoc 分帳邏輯仍可作研究歷程說明。
**口試短答：** 正式帳目是 Baseline 79 → Final 85，Rescue 恆為 6 格；歷史上的 Primary 83／Post-hoc 84 分帳邏輯仍成立，但數字已因基線校正而移動，且已降級為附錄說明，不作正式主表數字。

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

### Q17: 4B 的歷史 Primary (83) 與 Post-hoc (84) 差 1 格，這與目前正式的 79→85 帳目如何對應？是否代表流程不可靠？
**正式回答：** 10 格 eligible 案例中，有 8 格在 Primary 與 corrected-chain replay 間完全不變；1 格 Radical 由 `no_op` 改為 `rescued`，使歷史 Post-hoc 通過數由 83 增至 84；另 1 格 q09 由 `no_op` 改為 `repaired_still_fail`，但最終仍為 FAIL。因此共有 2 格處置狀態改變，只有 1 格改變最終 PASS/FAIL 結果，且本次觀察到 regression=0。此 eligible/rescue 帳目與另一件與 Baseline 78→79 相關但獨立的候選 artifact 校正無關（詳見 Q21）；目前正式主表採用校正後的 Baseline 79/320 → Final 85/320，Verified rescue 恆為 6 格，歷史 Primary 83/Post-hoc 84 已降級為附錄層級的研究歷程說明。
**口試短答：** 10 格裡 8 格完全不變，2 格處置狀態有改，其中只有 1 格從 FAIL 變 PASS；這件事和另一件獨立的 Baseline 78→79 校正無關。Rescue 一直是 6 格，正式數字現在是 79→85。

### Q18: Overall McNemar 與 Task-clustered Bootstrap 結論看似不同，該如何解讀？
**正式回答：** 兩者代表不同層級的統計檢視。McNemar 顯示本次 320 個 matched cells 中 discordant 方向偏向 9B ($p = 0.015440$，基於校正後 Baseline 79/320 重新計算；4B-only discordant 格數由歷史 26 更新為 27，BOTH_FAIL 由 193 更新為 192，詳見 Correction Note)；而 task-clustered bootstrap CI 跨 0 (95% CI `[-1.56%, +14.37%]`)，顯示外推到其他未知題目時仍具抽樣不確定性。
**口試短答：** McNemar 顯示本次 320 個 matched cells 中 discordant 方向偏向 9B（校正後 p=0.015440）；task-clustered bootstrap CI 跨 0，外推到其他題目仍有不確定性。

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
6. ❌ **「Post-hoc 數據 (84/320 或 306/320) 是主要的實驗結果」** $\rightarrow$ ⭕ 應說：「正式主表數據為校正後的 Baseline 79/320 → Final 85/320（Verified rescue = 6）；歷史 Primary 83/84 與 Post-hoc 306/320 僅作研究歷程與探索討論，不作正式主張。」



### Q20: Healer 規則的 Provenance（來源與凍結狀態）與雙層學術定位為何？
**正式回答：**
1. **規則凍結狀態 (`rule_freeze_status = PRE_FROZEN_UNCHANGED`)**：六條 Healer 規則及其適用條件均於正式 Math16 320-cell generation 前完成凍結 (d9aa264c)，且後續未修改 detector、eligibility、transform 或 activation scope。
2. **Primary 5 定位 (`validation_status = PROSPECTIVE_WITHIN_MATH16_COHORT`)**：Primary 帳目的 5 格救援屬於預先固定規則在 Math16 cohort 上的前瞻性評估結果；但因規則源自先期開發資料，且尚未在完全獨立資料集驗證 (independent_external_validation = false)，本研究不主張其為外部獨立確認性證據。
3. **Corrected 第 6 格定位 (POST_HOC_TECHNICAL_CORRECTION)**：第 6 格來自既有規則成功 transform 被 runner false-loop rollback 錯誤撤回後的技術修正。此修正未新增或修改 Healer 規則，不改變 PRE_FROZEN_UNCHANGED 狀態；但因屬正式結果揭露後的技術重算，只列入 Corrected technical account，不回寫 Primary。
4. **Payload Wrap 結構 (oracle_payload 內部包裝)**：single-key 指固定三欄回傳結構中 oracle_payload 欄位內部的唯一包裝鍵，不是最外層 return dict 只有一個鍵。Healer 不讀取 correct_answer，oracle_answer_used = false。此結果支持窄範圍、唯一、局部且離線可驗證的 deterministic repair candidate，不代表零副作用或一般語意安全保證。

- 權威 Provenance Audit 報告：docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md (SHA256: 05a1ef08836e7f957cd0d4e87be9090d863b0c290474ae8b80bfd9ed4347bb4a)
- 權威 Provenance Audit Manifest：docs/experiments/reports/math16_healer_rule_provenance_audit_v1_manifest.json (SHA256: b882b4d31a61dbca8ab60622c75ecf82290223cdab3a816de7116e4bb515ecd5)
- 規則凍結 Commit：d9aa264c | 分類修正 Commit：97c4e985

---

### Q21: 為什麼最終 Baseline 是 79/320，而早期紀錄是 78/320？

> 權威 Correction Note：`./math16_baseline_correction_note_v1.md`（人工核准之正式校正說明，僅作用於分析／報告層，不修改任何凍結證據）。

**正式回答：** 78 與 79 兩個數字源自**同一次原始模型生成（same raw response）**；唯一差異來自分析層對候選 artifact 的選取。Method 1 原始評分管線在單一格（`ce115_calc_polynomial_division_l1__ab1__seed_2026072003`）**選錯了候選 artifact**——擷取器誤將模型自身敘述文字中一段偶然出現的 code-fence 符號當作程式邊界，產生一個截斷、無法解析的候選碼並評為 FAIL；Method 2 獨立重新擷取的原始碼，與 Method 1 自己已計算但未採用的 `candidate_hash` 位元組完全相同，以同一凍結 Evaluator 重新評分則為 PASS。針對此發現，團隊執行了一次**零 LLM/Healer 呼叫的 Confirmatory re-evaluation**，對全部 320 格逐格離線重算：結果精確重現——對 Method 1 已評分的 artifact 得 78/320，對 Method 2 的原始碼得 79/320，全 320 格僅此一格不一致，其餘 319 格兩方法完全吻合。基於此稽核鏈，本手冊採用**校正後的正式主表數字：Baseline 79/320 → Final 85/320**；**Verified rescue 恆為 6 格不變**（該格 `healer_eligible=false`，從未進入救援母體，故完全不受基線校正影響）。凍結的原始評測證據（journals、manifests、pinned Evaluator/Protocol scripts、regression tests）依規範**永久保留歷史 78/83/84 數字**，本次校正僅發生於分析／報告層，未修改、也不會修改任何一份凍結證據。

**口試短答：** 78 和 79 其實來自同一次模型回答，只是早期分析管線不小心選到一個被截斷的候選檔案；獨立複核與逐格重算證實正確答案是 79，Rescue 仍然是 6 格沒變，凍結的原始資料完全沒有被更動，正式數字現在是 79 → 85。

---

### Q22: 你們如何確認 Ab2d+api／Ab2d+spec 真的照設計運作？

**正式回答：** 我們另外稽核了 32 個題目條件與 422 個既有正式輸出。系統契約有 29/32 正確，另外 2 處 prompt 內部矛盾與 1 處未明確指定 method，均已標記並排除於後續契約型 Healer 候選。模型端有 20/422（4.7%）雖然答對，但未完全依約使用指定工具，因此我們不把所有 PASS 都解釋成 API 使用成功。我們再抽樣 30 格，涵蓋兩處系統契約缺陷、一處未指定 method，以及 compliant、noncompliant 與其他失敗類別；兩種抽取路徑下的 compliance 標籤 30/30 完全一致。這些補充結果不改變既有 Baseline、Healer rescue 與 Tier 1 統計，但 Ab2d 條件應解讀為系統工具選擇與 prompt 暴露設計的比較，而非所有模型都百分之百依約。

**口試短答：** 32 個條件裡 29 個契約正確、2 個 prompt 矛盾與 1 個 method 未指定已排除；422 格中有 20 格答對但未完全依約。抽樣 30 格兩種抽取路徑標籤全一致；分數與 Healer 統計不變，Ab2d 要比的是工具與 prompt 設計。

---

## 三、 最終高風險追問速答

### R1: 六條規則是否看完正式 320 格才寫？
**直接回答：** 不是；規則在正式 generation 前凍結，freeze 後未改邏輯。**證據：** 6/6 `PRE_FROZEN_UNCHANGED`，freeze commit `d9aa264c`。**限制：** 尚無獨立外部驗證。**不可宣稱：** 已完成外部確認性驗證。

### R2: Primary 5 為何可算前瞻性？
**直接回答：** 它是預先凍結規則在 Math16 cohort 內的前瞻性評估。**證據：** 79/320 baseline（凍結歷史紀錄為 78/320，經 Correction Note 校正）、10 eligible、5 rescued（歷史 Primary 帳目），隨基線校正在算術上移動為 84/320，現已降級為附錄/校正註記層級、不作主表數字；目前正式主表為 Verified rescue=6、Final 85/320，分類為 `PROSPECTIVE_WITHIN_MATH16_COHORT`。**限制：** 不等於外部獨立驗證。**不可宣稱：** Primary 5 是外部確認證據。

### R3: Corrected 第 6 格是否事後灌水？
**直接回答：** 不是新增規則，而是 runner rollback 錯誤撤回既有成功 transform 的技術勘誤。**證據：** Corrected=6，隨基線校正（78→79）在算術上移動為 85/320（即目前正式 Final 85/320，Verified rescue=6 不變），規則仍為 `PRE_FROZEN_UNCHANGED`。**限制：** 屬 `POST_HOC_TECHNICAL_CORRECTION`。**不可宣稱：** Corrected 6 等同 Primary 6。

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
