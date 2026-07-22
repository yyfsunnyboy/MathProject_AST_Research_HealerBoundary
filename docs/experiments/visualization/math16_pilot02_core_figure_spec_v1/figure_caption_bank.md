# Math16 Pilot-02 Core Figure Caption Bank v1

```text
FIGURE_CAPTION_BANK_V1
DUAL_CAPTION_STRUCTURE_ENFORCED
EXPLICIT_PRIMARY_POSTHOC_ACCOUNTING
NO_VAGUE_RANGE_PHRASES
```

> **使用說明**：
> 本圖說庫提供 6 張核心圖表之雙版本圖說：
> 1. **正式報告圖說 (Formal Report Caption)**：適用於成果報告書與正式論文，敘事嚴謹、包含完整條件與限制說明。
> 2. **口試簡報圖說 (Oral Presentation Caption)**：適用於口試 Slide、展板 (Poster) 與 One-Pager，重點突出、口語簡潔。

---

## Figure 1: Baseline Overall Performance across Three Models (三模型 Baseline 總覽)

* **正式報告圖說**：
  > **圖 1：三模型在 320 個測試單元中之端到端 Baseline 通過率。**
  > Gemini 3.5 Flash 達到 289/320 (90.3%)，作為 Tier 2 描述性基準參照；Qwen 3.5 9B 達到 101/320 (31.6%)，顯著高於 Qwen 3.5 4B 之 78/320 (24.4%)，兩者構成 Tier 1 正式配對比較。通過率反映包含 Python 語法、JSON 包裝與 API 呼叫之端到端執行成功率，不等於純數學推理能力；Baseline 高低亦不直接代表 Healer 可修復視窗之大小。

* **口試簡報圖說**：
  > **圖 1：三模型基線通過率對比。**
  > 9B 基線 (101/320) 高於 4B (78/320)；Gemini (289/320) 作為強模型參照。基線高低不代表 Healer 修復視窗的大小。

---

## Figure 2: Four Prompt Conditions across Three Models (四 Prompt 條件 × 三模型)

* **正式報告圖說**：
  > **圖 2：四種 Prompt 提示條件在三模型中之通過數對比 ($n=80$ per cell)。**
  > 對 Qwen 4B 與 9B 小模型而言，提供完整家族規格之 `Ab2d+spec-v2` 觀察到最高通過數 (36/80 與 40/80)；對 Gemini 而言，簡潔之 `Ab2d+api` (78/80) 表現優於 `Ab2d+spec-v1` (63/80)。Gemini 未正式重新生成 `Ab2d+spec-v2`；其 Post-hoc 80/80 僅屬事後 API 簽名補齊機制驗證，不列入 Primary 正式 Bar。 Prompt 效果依模型、提示版本與部署條件而異。

* **口試簡報圖說**：
  > **圖 2：提示條件效果依模型與提示版本而異。**
  > 4B 與 9B 在家族規格 v2 下表現最好；Gemini 正式生成只跑到 v1，事後補齊才達 80/80，證明沒有普遍最佳 Prompt。

---

## Figure 3: Four Mathematical Families for Qwen 4B vs Qwen 9B (四 Family × Qwen 4B／9B)

* **正式報告圖說**：
  > **圖 3：Qwen 4B 與 9B 在四大數學家族之通過數比較 ($n=80$ per family)。**
  > 9B 在 Integer (42 vs 30)、Fraction (31 vs 17) 與 Radical (19 vs 15) 均高於 4B；惟在 Polynomial 呈現反向低下 (9 vs 16)。診斷顯示 9B 在 Polynomial 之偏低高度集中於 `ce115` 多項式除法單一題型與 LaTeX 組裝衝突，屬特定結構敏感性，尚未證實因果，不可外推為 9B 全域失控或純數學能力下降。

* **口試簡報圖說**：
  > **圖 3：四大數學家族表現對比。**
  > 9B 整體較高，但在 Polynomial 出現反向偏低，主要受單一題型 LaTeX 欄位組裝影響，非全域數學能力下降。

---

## Figure 4: Tier 1 Paired 2x2 Contingency and Discordant Analysis (Tier 1 配對不一致格分析)

* **正式報告圖說**：
  > **圖 4：Qwen 4B 與 9B 在 320 個匹配測試單元中之 2x2 四格聯表與配對檢定。**
  > 兩模型同對 `BOTH_PASS` 52 格、同錯 `BOTH_FAIL` 193 格；不一致配對中 `9B_ONLY_PASS` (49格) 顯著多於 `4B_ONLY_PASS` (26格)，細胞層級 Exact McNemar 檢定具顯著方向性 ($p = 0.010582$)。然考慮 16 個 Task 聚類效應之 Task-clustered Bootstrap 95% CI 跨 0 (`[-0.94%, +14.38%]`)，顯示外推至未知全新題型時仍具抽樣不確定性。

* **口試簡報圖說**：
  > **圖 4：4B vs 9B 配對四格表與不一致分析。**
  > 9B 獨勝 49 格多於 4B 獨勝 26 格，細胞層級 McNemar 顯著 ($p=0.0106$)；但 Task 聚類 CI 跨 0，提醒全域外推不確定性。

---

## Figure 5: Healer Eligibility and Rescue Boundary across Three Models (Healer Eligibility／Rescue 邊界)

* **正式報告圖說**：
  > **圖 5：三模型 Baseline FAIL 案例中 Healer 審查 (Eligibility) 與救回 (Rescue) 邊界。**
  > 在 Gemini (31 FAIL) 與 Qwen 9B (219 FAIL) 中，由於殘餘失敗未命中事前凍結規則，Healer 主動選擇 Abstain (Eligible=0)；在 Qwen 4B (242 FAIL) 中識別出 10 個 Eligible 案例，Primary 救回 5 格 (Primary final = 83/320)，Post-hoc 修正後救回 6 格 (Post-hoc final = 84/320)。實際執行修復之案例中均觀察到 Regression=0。FAIL 總數不等於可修復數。

* **口試簡報圖說**：
  > **圖 5：Healer 介入邊界與救援成果。**
  > 失敗多不等於修復多。4B 命中 10 格，Primary 救回 5 格 (83/320)，Post-hoc 救回 6 格 (84/320)；Gemini 與 9B 因未命中凍結規則主動 Abstain，觀察到 zero regression。

---

## Figure 6: Healer Boundary 3-Zone Conceptual Model (Healer 安全介入邊界概念圖)

* **正式報告圖說**：
  > **圖 6：Deterministic AST Healer 之三區域安全介入邊界概念架構。**
  > Healer 僅在 Zone 1 (Safe Repair Window) 介入：必須同時滿足明確語法/契約瑕疵、確定性 unique fix 且不反推答案；Zone 2 (Abstain Zone) 涵蓋入口點模糊或多可能修法歧義，系統主動放棄修改以防 Regression；Zone 3 (Out of Scope) 為演算法或數學邏輯錯誤，非確定性 Healer 之處理範疇。

* **口試簡報圖說**：
  > **圖 6：Healer 三區域安全介入邊界。**
  > Healer 只修 Zone 1 的表面臨門一腳瑕疵；對 Zone 2 歧義主動 Abstain 放棄盲猜，防止將可能的程式改壞。
