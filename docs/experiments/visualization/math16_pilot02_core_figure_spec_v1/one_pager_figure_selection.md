# Executive One-Pager Figure Selection & Layout Specification v1

```text
ONE_PAGER_FIGURE_SELECTION_V1
EXACTLY_FOUR_FIGURES_SELECTED
EXACTLY_4_CORE_FIGURES = TRUE
NO_FIFTH_VISUAL_ELEMENT
```

## 一、 One-Pager 選圖策略 (Selection Strategy: Exactly 4 Figures)

Executive One-Pager 限制為單頁 1,000 字精簡摘要，版面空間極度珍貴。核心圖表硬性規定 **`exactly_4_core_figures = true`**，嚴格固定選用以下 4 張圖表：

| 選用順序 | 圖表 ID | 圖表名稱 | 敘事功能 | 選用理由 |
| :- | :--- | :--- | :--- | :--- |
| **1** | **Figure 1** | 三模型 Baseline 總覽 | 建立全域能力基線與參照背景 | 一眼展示 Gemini (90.3%)、9B (31.6%) 與 4B (24.7%) 的端到端基準。 |
| **2** | **Figure 3** | 四 Family × Qwen 4B／9B | 揭示家族層級非單調性與結構敏感性 | 呈現 9B 在 Integer/Fraction 大勝，但在 Polynomial 出現反向特徵。 |
| **3** | **Figure 4** | Tier 1 配對不一致分析 | 提供 4B vs 9B 嚴謹統計證據 | 呈現 2x2 配對四格表 ($52/27/49/192$) 與 McNemar/Bootstrap 雙重解讀。 |
| **4** | **Figure 5** | Healer Eligibility／Rescue 邊界 | 展示實證修復成果與安全防禦 | 實證呈現 Verified rescue = 6（79/320 → 85/320）、Gemini/9B 全面 Abstain。 |

---

## 二、 Figure 6 的單頁定位 (Figure 6 Treatment in One-Pager)

* **完全排除作為獨立圖**: One-Pager **不得包含 Figure 6 作為獨立圖、子圖、側邊小圖或任何第 5 個獨立視覺區塊**。
* **僅留純文字註解**: Figure 6 的「三區域概念 (Safe Repair Window / Abstain Zone / Out of Scope)」僅作為 Figure 5 下方的 **3 行文字註解 (3-line text annotation)**，說明確定性 Healer 的工程防禦邊界。

---

## 三、 版面佈局 (Layout - 4 Quadrants)

```text
+-------------------------------------------------------------------------+
| [Header] Small but Precise: Outperforming Large Models through Healer  |
+-------------------------------------------------------------------------+
| [Top Left: Fig 1] Baseline Overall        | [Top Right: Fig 3] Family Breakdown |
|  - Gemini (90.3%) vs 9B (31.6%) vs 4B     |  - Integer (+12), Fraction (+14)    |
|  - Baseline != Repair Window              |  - Polynomial anomaly localized     |
+-------------------------------------------------------------------------+
| [Bottom Left: Fig 4] Paired 2x2 Matrix    | [Bottom Right: Fig 5] Rescue Funnel |
|  - BothPass: 52, 4BOnly: 27, 9BOnly: 49   |  - Verified rescue = 6 (79/320→85/320) |
|  - McNemar p=0.0154, Boot CI [-1.56,14.37]|  * (Note: Safe/Abstain/Scope)       |
+-------------------------------------------------------------------------+
| [Footer] Executive Key Takeaways & Methodology Boundary Summary          |
+-------------------------------------------------------------------------+
```
