# Executive One-Pager Figure Selection & Layout Specification v1

```text
ONE_PAGER_FIGURE_SELECTION_V1
EXACTLY_FOUR_FIGURES_SELECTED
EMPIRICAL_AND_CONCEPTUAL_BALANCE
```

## 一、 One-Pager 選圖策略 (Selection Strategy)

Executive One-Pager 限制為單頁 1,000 字精簡摘要，版面空間極度珍貴。在 6 張核心圖表中，依據敘事主軸**精選 4 張圖表**：

| 選用順序 | 圖表 ID | 圖表名稱 | 敘事功能 | 選用理由 |
| :- | :--- | :--- | :--- | :--- |
| **1** | **Figure 1** | 三模型 Baseline 總覽 | 建立全域能力基線與參照背景 | 一眼展示 Gemini (90.3%)、9B (31.6%) 與 4B (24.4%) 的端到端基準。 |
| **2** | **Figure 3** | 四 Family × Qwen 4B／9B | 揭示家族層級非單調性與結構敏感性 | 呈現 9B 在 Integer/Fraction 大勝，但在 Polynomial 出現反向特徵。 |
| **3** | **Figure 4** | Tier 1 配對不一致分析 | 提供 4B vs 9B 嚴謹統計證據 | 呈現 2x2 配對四格表 ($52/26/49/193$) 與 McNemar/Bootstrap 雙重解讀。 |
| **4** | **Figure 5** | Healer Eligibility／Rescue 邊界 | 展示實證修復成果與安全防禦 | 實證呈現 4B 救回 5~6 格、Gemini/9B 全面 Abstain，證明 FAIL 不等於可修復。 |

---

## 二、 擇一決策說明 (Figure 5 vs Figure 6 Choice Rationale)

* **選用決策**: 主版面選用 **Figure 5 (實證修復與邊界漏斗圖)**。
* **選擇理由**:
  1. One-Pager 必須呈現硬實證數據 (4B 救回 5 格, Regression=0, Gemini/9B Eligible=0)。
  2. Figure 5 能直接回答評審「Healer 到底救了多少格程式」的實證問題。
  3. **Figure 6 (三區域概念圖)** 以小圖/側邊欄 (Sidebar Inset Box) 形式附屬於 Figure 5 旁，用一小圖說明「Safe Window / Abstain / Out of Scope」之理論防禦。

---

## 三、 版面佈局與視覺層級 (Layout & Visual Hierarchy)

```text
+-------------------------------------------------------------------------+
| [Header] Small but Precise: Outperforming Large Models through Healer  |
+-------------------------------------------------------------------------+
| [Top Left: Fig 1] Baseline Overall        | [Top Right: Fig 3] Family Breakdown |
|  - Gemini (90.3%) vs 9B (31.6%) vs 4B     |  - Integer (+12), Fraction (+14)    |
|  - Baseline != Repair Window              |  - Polynomial anomaly localized     |
+-------------------------------------------------------------------------+
| [Mid Left: Fig 4] Paired 2x2 Matrix       | [Mid Right: Fig 5 + Fig 6 Inset]    |
|  - BothPass: 52, 4BOnly: 26, 9BOnly: 49   |  - 4B Rescued: 5 (Primary) / 6      |
|  - McNemar p=0.0106, Boot CI [-0.94,14.4] |  - Gemini/9B Eligible=0 (Abstain)   |
+-------------------------------------------------------------------------+
| [Footer] Executive Key Takeaways & Methodology Boundary Summary          |
+-------------------------------------------------------------------------+
```
