# Math16 Pilot-02 評審追問與標準應答手冊 (Jury Defense Q&A Final v1)

```text
MATH16_PILOT02_JURY_QA_FINAL_PRECISION_CLEANUP_COMPLETED
Q9_GEMINI_V2_BOUNDARY_CLARIFIED
Q17_CORRECTED_CHAIN_DISPOSITION_RECONCILED
OVERCLAIMS_REMOVED
CATEGORY_B_QA_COMPLETED
CATEGORY_C_ROUND1_PARTIAL_REPAIR_2B_QA_ADDED
THREE_MODEL_ROUND1_ACCOUNTS_SEPARATED
```

> **使用說明**：
> 本手冊為「Ivan旺宏科學展」HealerBoundary 研究線之正式口試 defense 檔案。
> 每一題目均包含：
> 1. **正式回答**：適用於成果報告書、論文與評審正式書面審查（2~5句，嚴謹客觀）。
> 2. **口試短答**：適用於現場口頭報告與評審快速追問（1~2句，20~60字，高中生自然口語）。

---

## 一、 21 題評審追問與標準應答

### Q1: 為什麼要先做 Eligibility 審查，不直接全部程式都嘗試修復？
**正式回答：** 若不設 Eligibility 門檻，修復器將被迫對無明確修復依據的程式進行猜測性修改，破壞可解釋性並可能引入倒退 (Regression)。Eligibility 是維護「確定性安全介入」的必要防禦。
**口試短答：** 因為缺乏明確規則強行盲目修復會破壞可解釋性並把程式改壞。Eligibility 能確保修復只在修法唯一且安全時介入。

### Q2: Gemini 與 9B 的 `eligible=0` 是否代表 Healer 沒有用？
**正式回答：** 不是。就 **Conservative／Primary Method 1** 帳而言，Gemini 與 9B 的 `eligible=0` 代表在該帳與既有凍結規則下，失敗案例未同時滿足唯一、安全、可驗證的介入條件，系統 Abstain。就後續封存的 **Aggressive Healer Round 1** 正式主分析而言，9B 在 FAIL-only 單輪累積下獲得 verified rescue **1**（101→102），Gemini 仍為 **0**（289→289）；Gemini 的 0 rescue 代表殘餘失敗未命中安全修法窗口，不是系統失效。Healer 的價值同時包含：命中時可驗證救援、未命中時 Abstain、以及不計入 rescue 的 partial repair。
**口試短答：** 不是。Primary 帳的 eligible=0 是安全 Abstain；Round 1 正式比較下 9B 有 1 格 rescue、Gemini 仍 0，代表沒打中安全窗口，不是 Healer 沒用。

### Q3: 為什麼 4B 可以修復較多格，9B／Gemini 反而較少或為 0？
**正式回答：** 必須分帳。Conservative／Primary Method 1：4B verified rescue **6**（79→85），9B／Gemini 在該帳為 0。Aggressive Healer Round 1（正式三模型主分析）：4B **9**（79→88）、9B **1**（101→102）、Gemini **0**（289→289）；修復率 3.73%／0.46%／0%。差異來自殘餘失敗型態是否落入凍結規則窗口（residual failure type／rule fit），不是「模型越大越好修」。本次觀察到 Baseline 較高者修復率較低的遞減關聯，**不宣稱普遍因果**。
**口試短答：** 分兩帳：Primary 是 4B 救 6 格；Round 1 正式比較是 4B／9B／Gemini＝9／1／0。關鍵是失敗型態有沒有打中凍結規則，不是模型越大越好修。

### Q4: 9B Polynomial 只有 9/80，是否代表 9B 的數學能力比 4B 差？
**正式回答：** 不能這樣解讀。9B 總體通過數 (101/320) 高於 4B (79/320；本管線原始紀錄為歷史 78/320，經 Method 1/Method 2 交叉稽核確認為候選 artifact 擷取誤選，校正詳見 Correction Note `05_math16_baseline_correction_note_v1.md`)。Polynomial 的低下高度集中於 `ce115_calc_polynomial_division_l1` 單一題型，與多個 LaTeX 欄位組裝高度共現，屬特定提示結構敏感性，尚未證實因果，不可外推為 9B 全域失控或純數學能力落後。
**口試短答：** 不能。9B 總分 (101) 仍高於 4B (79，歷史紀錄 78 已校正)，Polynomial 偏低集中於單一多項式題型與 LaTeX 組裝衝突，屬於結構敏感性，未證明因果。

### Q5: 為什麼不修改 Evaluator 的 Parser 讓採分更寬鬆？
**正式回答：** Evaluator 的職責是維護嚴謹的評分契約。在 Qwen 4B Ab2d+api 27 格診斷樣本中，21/27 格 (77.8%) 屬候選 Python 本體內部的 SyntaxError (如括號不平衡或字串未閉合)，僅 5/27 格 (18.5%) 屬 parser 不友善，1/27 格 (3.7%) 屬真邏輯錯誤。結果不支持「Evaluator Parser 不公平是主要失敗來源」；隨意放寬 Parser 並無法修復破損的 Python 程式本體。
**口試短答：** 因為評分標準必須嚴謹，且診斷顯示 77.8% 的失敗是 Python 程式本體壞掉，放寬 Parser 並無法修復語法錯誤的程式。

### Q6: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**正式回答：** 因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合、語法結構混亂）並沒有唯一的修復解答。若強行修復將違反「修法唯一、不可反推答案」的核心原則，帶來極高修壞風險。
**口試短答：** 因為大多數語法錯誤沒有唯一的解答，強行盲猜修改會破壞可解釋性，違反 deterministic 修復的核心規範。

### Q7: 為什麼正式帳目是 Baseline 79/320 → Final 85/320（Verified rescue = 6），而不是 Primary 83 或 Post-hoc 84？
**正式回答：** 因為 79/320 是經過 Method 1/Method 2 交叉稽核與 Confirmatory re-evaluation 確認的校正後 Baseline（原始管線歷史紀錄為 78/320，凍結證據不變，詳見 Correction Note `05_math16_baseline_correction_note_v1.md`）；85/320 是基線校正後的正式 Final 數據，Verified rescue 恆為 6 格（該格 healer_eligible=false，從未進入救援母體，故不受基線校正影響）。歷史上曾以事前預註冊 Primary 83/320 與事後修正 false-loop revalidation 邏輯後的 Post-hoc 84/320 嚴格分帳；隨基線校正，舊 Primary 83 在算術上移動為 84，現已降級為附錄/校正註記層級，不再列為主表結果，但歷史 Primary/Post-hoc 分帳邏輯仍可作研究歷程說明。
**口試短答：** 正式帳目是 Baseline 79 → Final 85，Rescue 恆為 6 格；歷史上的 Primary 83／Post-hoc 84 分帳邏輯仍成立，但數字已因基線校正而移動，且已降級為附錄說明，不作正式主表數字。

### Q8: Gemini 基線已經 289/320 (90.3%)，為什麼還要研究 Healer？
**正式回答：** 本研究的核心目標是探索「修復邊界／安全邊界」。能力邊界（Baseline PASS）與安全邊界（殘餘 FAIL 是否可被凍結規則安全修復）不同。Aggressive Healer Round 1 顯示 Gemini 在 31 格殘餘 FAIL 上 eligible＝0、rescue＝0（Abstain），同時 4B／9B 分別獲得 9／1 格 verified rescue；這正好劃定規則適配窗口，而非否定 Healer。Post-hoc 提示修復實驗 (306/320) 則另帳揭示強模型在 API 簽名補齊後的探索天花板，不作 Primary／Round 1 主表。
**口試短答：** 因為我們要畫安全邊界，不是只看誰 Baseline 高。Gemini 殘餘失敗沒打中規則所以 Abstain；同一套規則在 4B／9B 仍有救援。

### Q9: Ab2d+spec-v2 是不是最好的 Prompt 條件？
**正式回答：** 對 4B 與 9B 而言，Ab2d+spec-v2 在本次正式四條件比較中通過數最高，分別為 36/80 與 40/80。Gemini 在 Ab2d+spec-v2 補齊 API 簽名卡後最終達 80/80；其正式 Primary 採用 Ab2d+spec-v1 為 63/80（屬研究歷程）。因此不能將 Gemini 的 80/80 與 Qwen 的 36/80/40/80 假裝為同條件 Primary 直接比較。Prompt 效果依模型、提示版本與部署條件而異。
**口試短答：** 4B 和 9B 正式跑過 v2；Gemini 在 v2 補齊簽名卡後達 80/80，但正式 Primary 只跑到 v1 的 63/80，不能直接比較。

### Q10: 為什麼 FAIL 有 242 個，可修復的 (Eligible) 卻只有 10 個？
**正式回答：** 因為 LLM 生成程式的失敗大多是演算法邏輯不通或結構大段缺失，真正屬於「程式本體正確、僅差語法臨門一腳且有唯一修法」的瑕疵案例本來就非常稀少。
**口試短答：** 因為多數 failure 是邏輯不通或整段 missing，真正只差臨門一腳語法瑕疵且有唯一修法的案例本來就很稀少。

### Q11: Abstain（不介入）是不是代表 Healer 的能力不足？
**正式回答：** 不是。知曉「何時不該介入」與「何時該介入」同等重要。本研究採 **先求不修壞，再求修得好**：Abstain 是控制 Regression 風險的防禦機制，代表系統在面臨不明確修復目標時主動放棄盲猜；verified rescue 與 partial repair 僅在唯一、局部、可驗證窗口內進行。
**口試短答：** 不是。我們先求不修壞再求修得好；Abstain 是為了不猜修、不把程式改壞。

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
6. ❌ **「Post-hoc 數據 (84/320 或 306/320) 是主要的實驗結果」** $\rightarrow$ ⭕ 應說：「Conservative／Primary 正式主表為校正後的 Baseline 79/320 → Final 85/320（Verified rescue = 6）；歷史 Primary 83/84 與 Post-hoc 306/320 僅作研究歷程與探索討論。三模型 Aggressive Healer Round 1 另帳為 4B 79→88（rescue 9）、9B 101→102（rescue 1）、Gemini 289→289（rescue 0），兩者不得混帳。」
7. ❌ **「模型越大／Baseline 越高，Healer 修復率一定越高」** $\rightarrow$ ⭕ 應說：「本次三模型 Round 1 觀察到修復率 3.73%／0.46%／0% 的遞減關聯；只描述本次範圍，不宣稱普遍因果。核心是 residual failure type／rule fit。」
8. ❌ **「Gemini rescue=0 代表 Healer 無效」** $\rightarrow$ ⭕ 應說：「代表殘餘失敗未命中安全修法窗口，系統 Abstain；這是安全邊界結果，不是系統失效。」
9. ❌ **「Partial repair 也算 verified rescue」** $\rightarrow$ ⭕ 應說：「Partial repair 不計入 verified rescue；它表示 blocker 已移除並進入可診斷狀態。」
10. ❌ **「Round 2 已完成／可覆寫 Round 1」** $\rightarrow$ ⭕ 應說：「Round 2 尚未執行；若執行，僅 post-hoc iterative replay，不得覆寫 Round 1 主表。」
11. ❌ **「2B 已完成 320 格與完整 Healer 正式帳」** $\rightarrow$ ⭕ 應說：「2B 僅有四條件 smoke 0/16 PASS；尚未做完整 frozen Healer replay，屬待補 exploratory lower-bound evidence。」



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

### Q21: 為什麼最終 Baseline 是 79/320，而早期紀錄是 78/320？

> 權威 Correction Note：`05_math16_baseline_correction_note_v1.md`（人工核准之正式校正說明，僅作用於分析／報告層，不修改任何凍結證據）。

**正式回答：** 78 與 79 兩個數字源自**同一次原始模型生成（same raw response）**；唯一差異來自分析層對候選 artifact 的選取。Method 1 原始評分管線在單一格（`ce115_calc_polynomial_division_l1__ab1__seed_2026072003`）**選錯了候選 artifact**——擷取器誤將模型自身敘述文字中一段偶然出現的 code-fence 符號當作程式邊界，產生一個截斷、無法解析的候選碼並評為 FAIL；Method 2 獨立重新擷取的原始碼，與 Method 1 自己已計算但未採用的 `candidate_hash` 位元組完全相同，以同一凍結 Evaluator 重新評分則為 PASS。針對此發現，團隊執行了一次**零 LLM/Healer 呼叫的 Confirmatory re-evaluation**，對全部 320 格逐格離線重算：結果精確重現——對 Method 1 已評分的 artifact 得 78/320，對 Method 2 的原始碼得 79/320，全 320 格僅此一格不一致，其餘 319 格兩方法完全吻合。基於此稽核鏈，本手冊採用**校正後的正式主表數字：Baseline 79/320 → Final 85/320**；**Verified rescue 恆為 6 格不變**（該格 `healer_eligible=false`，從未進入救援母體，故完全不受基線校正影響）。凍結的原始評測證據（journals、manifests、pinned Evaluator/Protocol scripts、regression tests）依規範**永久保留歷史 78/83/84 數字**，本次校正僅發生於分析／報告層，未修改、也不會修改任何一份凍結證據。

**口試短答：** 78 和 79 其實來自同一次模型回答，只是早期分析管線不小心選到一個被截斷的候選檔案；獨立複核與逐格重算證實正確答案是 79，Rescue 仍然是 6 格沒變，凍結的原始資料完全沒有被更動，正式數字現在是 79 → 85。

---

### Q22: 你們如何確認 Ab2d+api／Ab2d+spec 真的照設計運作？

**正式回答：** 我們另外稽核了 32 個題目條件與 422 個既有正式輸出。系統契約有 29/32 正確，另外 2 處 prompt 內部矛盾與 1 處未明確指定 method，均已標記並排除於後續契約型 Healer 候選。模型端有 20/422（4.7%）雖然答對，但未完全依約使用指定工具，因此我們不把所有 PASS 都解釋成 API 使用成功。我們再抽樣 30 格，涵蓋兩處系統契約缺陷、一處未指定 method，以及 compliant、noncompliant 與其他失敗類別；兩種抽取路徑下的 compliance 標籤 30/30 完全一致。這些補充結果不改變既有 Baseline、Healer rescue 與 Tier 1 統計，但 Ab2d 條件應解讀為系統工具選擇與 prompt 暴露設計的比較，而非所有模型都百分之百依約。

**口試短答：** 32 個條件裡 29 個契約正確、2 個 prompt 矛盾與 1 個 method 未指定已排除；422 格中有 20 格答對但未完全依約。抽樣 30 格兩種抽取路徑標籤全一致；分數與 Healer 統計不變，Ab2d 要比的是工具與 prompt 設計。

---

## 三、 Round 1／安全邊界／Partial repair／2B 補充題（Category C）

### Q23: 有沒有跑更小的模型（例如 2B）？
**正式回答：** 有。Qwen 3.5 2B 已完成四條件 smoke：`qwen35_2b_math16_four_condition_smoke_20260725_001`，結果為 **0/16 PASS**。此為 exploratory lower-bound／基礎設施驗證證據，**不是** 320 格正式主表，亦**尚未**完成完整 frozen Healer replay。
**口試短答：** 有跑 2B 的 16 格四條件 smoke，結果 0/16 PASS；還沒做完整 Healer，也不算 320 正式主表。

### Q24: 為什麼 2B 沒有擴到 320 格？
**正式回答：** 2B 屬於探索性下界探針，目的是確認更小模型在相同 Math16 契約下是否已具可用 Baseline。在 16 格四條件皆 0 PASS 的情況下，優先保留算力於 4B／9B／Gemini 正式 320 格與 Round 1 Healer 主分析；將 2B 擴至 320 並非本輪正式主表必要條件。
**口試短答：** 2B 先做 16 格探針就全掛，正式主表仍以 4B／9B／Gemini 的 320 格為準，沒有為了湊數硬擴。

### Q25: 2B 有沒有實際用 Healer 修？
**正式回答：** **尚未**對 2B 執行完整 frozen Healer replay。現況僅有 Baseline smoke（0/16 PASS）。此項已列為 Round 2 前優先補作之 exploratory lower-bound evidence；補作後仍屬探索帳，不得覆寫 Round 1 三模型主表。
**口試短答：** 還沒。現在只有 0/16 的 Baseline smoke；完整 Healer 列在 Round 2 前優先補作，而且仍是探索帳。

### Q26: 有沒有把後段修好的程式回頭重跑（多輪迭代）？
**正式回答：** **Round 1 為固定 single-pass 正式主分析**：每一層只承接上一層 final source，僅對仍 FAIL 的格子套用下一層規則，不做以 evaluator 結果回頭改寫流程的多輪搜尋。**Round 2 尚未執行**；若未來執行，僅定位為 post-hoc iterative replay，必須獨立分帳，**不得覆寫 Round 1 主表**。
**口試短答：** Round 1 是固定單輪正式主分析，沒有把修好的結果拿去反復試修；Round 2 還沒做，若做也只是事後重放，不能改 Round 1 主表。

### Q27: 為什麼 partial repair 仍有價值？它算不算 rescue？
**正式回答：** **不算 verified rescue。** 正式定義：Partial repair 不計入 verified rescue，但可表示 Healer 已移除語法、執行或結構 blocker，使程式由不可解析／不可執行前進至可診斷狀態。例如 9B Tier B 有 parse gain 4、execution gain 2、blocker-removal-only 3；D1 有 execution gain 3、blocker-removal-only 3。4B cumulative sealed 帳中缺獨立欄位者維持 **「—／不推估」**，不以敘事補數字。這些顯示安全規則已產生可審計進展，但最終 PASS 仍須另計。
**口試短答：** Partial repair 不是 rescue；它代表卡點被拿掉、程式變得可診斷，但還沒變成 PASS，所以要和 rescue 分帳。

### Q28: 為什麼 Gemini Round 1 rescue＝0 不代表 Healer 無效？
**正式回答：** Gemini Baseline 已達 289/320，殘餘僅 31 FAIL。Round 1 全層 eligible＝0、modified＝0，系統 Abstain，故 verified rescue＝0。這劃定的是**安全邊界未命中**，不是能力或系統失效：同一凍結規則在 4B／9B 上仍分別得到 9 與 1 格 verified rescue，並伴隨可審計的 partial repair。Healer 的正確行為包含「該修則修、不該修則 Abstain」。
**口試短答：** Gemini 剩下的失敗沒打中安全修法窗口，所以 Abstain；同一套規則在 4B／9B 仍有救援，這正好說明 Healer 在量安全邊界，不是壞掉。

### Q29: Development 40／Evaluation 120 與 Round 1 320 格如何分帳？
**正式回答：** Development 40／Evaluation 120 屬 Method 1 contract-aware 切分另帳（Evaluation 120 為該切分主要結果）。三模型 Aggressive Healer Round 1 以全量 **320** 格 FAIL-only cumulative 為正式比較 headline。兩套帳目並存，**不得互相覆寫或加總混報**。
**口試短答：** 40／120 是 Method 1 的切分另帳；Round 1 三模型比較用全量 320，兩套數字不能混在一起講。
