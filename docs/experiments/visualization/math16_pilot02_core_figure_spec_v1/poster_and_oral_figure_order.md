# Exhibition Poster & Oral Defense Slide Figure Order Specification v1

```text
POSTER_AND_ORAL_FIGURE_ORDER_V1
MAX_FIVE_FIGURES_PER_MEDIUM
OPTIMIZED_NARRATIVE_FLOW
```

## 一、 展板版面配置與層級 (Exhibition Poster Layout - 5 Figures Max)

科學展覽展板 (Poster) 採用 **3 欄垂直視覺流 (3-Column Layout)**，最多納入 **5 張核心圖表**：

### 1. 展板圖表清單與配置

| 展板欄位 (Column) | 圖表 ID | 圖表名稱 | 展板尺寸 / 層級 | 視覺亮點 |
| :- | :--- | :--- | :--- | :--- |
| **Column 1 (Left)** | **Figure 1** | 三模型 Baseline 總覽 | 中型圖表 (Main Benchmark) | 突顯 Gemini 90.3% 與 9B 31.6% vs 4B 24.4% 的全域差異。 |
| **Column 1 (Left)** | **Figure 2** | 四 Prompt 條件 × 三模型 | 中型圖表 (Prompt Delta) | 展示 Ab2d+spec-v2 於小模型之提昇，及 Gemini 於 Ab2d+api 之高分。 |
| **Column 2 (Center)**| **Figure 6** | Healer 安全介入邊界概念圖 | 大型主視覺 (Central Hero) | 放在展板正中央，清楚展示 Safe Window / Abstain / Out of Scope 邊界。 |
| **Column 3 (Right)**| **Figure 4** | Tier 1 配對不一致分析 | 中型圖表 (Paired Matrix) | 呈現 2x2 四格表、McNemar $p=0.0106$ 與 Cluster Bootstrap CI。 |
| **Column 3 (Right)**| **Figure 5** | Healer Eligibility／Rescue 邊界 | 中型圖表 (Rescue Results) | 展示 4B 救回 5~6 格、Gemini/9B 0 格與 Regression=0 實證。 |

*注：Figure 3 (Family Breakdown) 轉為展板表格內嵌於 Column 2 底部。*

---

## 二、 口頭簡報簡燈片順序 (Oral Defense Slides - 5 Figures Max)

口頭簡報簡燈片 (Oral Slides) 遵循 **提問 $\rightarrow$ 實證基線 $\rightarrow$ 配對對決 $\rightarrow$ 修復邊界 $\rightarrow$ 安全結論** 的故事線，最多選用 **5 張圖表**：

### 1. 口頭簡報投影片順序與時間分配

| Slide # | 主題 | 引用圖表 | 口頭報告重點 | 預估時間 |
| :- | :--- | :--- | :--- | :- |
| **Slide 4** | 全域基線與問題意識 | **Figure 1** | 說明三模型基線通過率，強調「基線高低 $\neq$ 可修復視窗」。 | 60 秒 |
| **Slide 6** | 提示工程與條件探索 | **Figure 2** | 說明家族規格對 4B/9B 之提昇，澄清 Gemini 事後補齊之界線。 | 60 秒 |
| **Slide 8** | 4B vs 9B 配對精確對決 | **Figure 4** | 展示 2x2 配對陣列 ($52/26/49/193$)，雙重解讀 McNemar 與 CI。 | 90 秒 |
| **Slide 10** | Healer 介入視窗與救援實證 | **Figure 5** | 說明 4B 救回 5~6 格、Gemini/9B 全面 Abstain，證明修復率不等於涵蓋率。 | 90 秒 |
| **Slide 11** | Healer 安全邊界與結論 | **Figure 6** | 用球場小柵欄比喻 Safe Window、Abstain Zone 與 Out of Scope，總結工程價值。 | 90 秒 |

*注：Figure 3 作為 Back-up Slide 備答。*
