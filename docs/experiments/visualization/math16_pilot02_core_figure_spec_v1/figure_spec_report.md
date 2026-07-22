# Math16 Pilot-02 核心圖表設計規格報告書 (Figure Spec Report v1)

```text
MATH16_PILOT02_CORE_FIGURE_SPEC_V1_FROZEN
SIX_CORE_FIGURES_DEFINED
PRIMARY_POSTHOC_VISUAL_GOVERNANCE_PRESERVED
SOURCE_TRACEABILITY_COMPLETED
CATEGORY_B_FIGURE_SPEC_COMPLETED
```

> **文件簡介**：
> 本報告書為「Ivan旺宏科學展」HealerBoundary 研究線之核心視覺產物規格書。
> 凍結成果報告書 (Integrated Report)、Executive One-Pager、競賽展板 (Poster) 與口頭簡報 (Oral Defense Slides) 共用之 6 張核心圖表數據、視覺規範、圖說與溯源資訊。

---

## 一、 6 張核心圖表總覽 (Six Core Figures Overview)

| 圖表 ID | 中文名稱 | 英文名稱 | 單一核心訊息 (One-Sentence Message) |
| :- | :--- | :--- | :--- |
| **Figure 1** | 三模型 Baseline 總覽 | Baseline Overall Performance across Three Models | 三模型端到端通過率不同，但 Baseline 高低不等於 Healer 可修復窗口大小。 |
| **Figure 2** | 四 Prompt 條件 × 三模型 | Four Prompt Conditions across Three Models | Prompt 條件效果依模型與提示版本而異，沒有普遍最佳條件。 |
| **Figure 3** | 四 Family × Qwen 4B／9B | Four Mathematical Families for Qwen 4B vs 9B | 9B 整體較高，但 Family 差異非單調，Polynomial 出現反向結果。 |
| **Figure 4** | Tier 1 配對不一致格分析 | Tier 1 Paired 2x2 Contingency and Discordant Analysis | 9B-only PASS 多於 4B-only PASS，但 task-level 外推仍有不確定性。 |
| **Figure 5** | Healer Eligibility／Rescue 邊界 | Healer Eligibility and Rescue Boundary | FAIL 數量不等於可安全修復數量；Healer 只在窄小唯一修法窗口介入。 |
| **Figure 6** | Healer 安全介入邊界概念圖 | Healer Boundary 3-Zone Conceptual Model | Deterministic Healer 只修復明確、局部、唯一、可驗證的表面錯誤；其他錯誤必須 Abstain。 |

---

## 二、 視覺數據與格式治理規範 (Data & Visual Governance)

1. ** Primary 與 Post-hoc 嚴格分帳**：
   - 所有實體 Bar 僅能繪製事前預註冊 Primary 數據。
   - Post-hoc 事後探討數據（如 Gemini 80/80 或 4B Post-hoc rescue = 6）僅能以虛線框 (Dashed Box)、灰色旁註或半透明疊層標示，**嚴禁**繪成同級正式 Bar。

2. **雙重統計證據並列**：
   - Figure 4 必須同時標註 **細胞層級 Exact McNemar $p = 0.010582$** 與 **題目層級 Task-clustered Bootstrap 95% CI `[-0.94%, +14.38%]`**。
   - 禁止僅寫「統計顯著」而忽略 Bootstrap CI 跨 0 之全域外推不確定性。

3. **禁止圖型與視覺約束**：
   - 嚴禁 3D 圖、圓餅圖 (Pie Chart)、雷達圖 (Radar Chart)、雙 Y 軸圖 (Dual Y-axis Chart)。
   - 所有 Bar Chart Y 軸起點必須為 **0**。
   - 數值標籤必須保留分子與分母 (如 `289/320`, `78/320`, `101/320`)。

---

## 三、 圖表跨媒體配置與選用 (Cross-Medium Allocation)

### 1. Executive One-Pager (選用 4 張)
- **選用圖表**: Figure 1, Figure 3, Figure 4, Figure 5 (附帶 Figure 6 小圖概念側邊欄)。
- **理由**: 兼顧全域基線 (Fig 1)、家族非單調性 (Fig 3)、嚴謹配對檢定 (Fig 4) 與實證修復救援成果 (Fig 5)。

### 2. 競賽展板 (Poster Layout - 5 張)
- **選用圖表**: Figure 1, Figure 2, Figure 4, Figure 5, Figure 6 (Hero Conceptual Center)。
- **排列**: Column 1 (Fig 1, Fig 2) $\rightarrow$ Column 2 (Fig 6 Hero) $\rightarrow$ Column 3 (Fig 4, Fig 5)。

### 3. 口頭簡報 (Oral Defense Slides - 5 張)
- **選用圖表**: Figure 1 (Slide 4) $\rightarrow$ Figure 2 (Slide 6) $\rightarrow$ Figure 4 (Slide 8) $\rightarrow$ Figure 5 (Slide 10) $\rightarrow$ Figure 6 (Slide 11)。
- **排列理由**: 順應「全域基線 $\rightarrow$ 提示條件 $\rightarrow$ 配對對決 $\rightarrow$ 實證救援 $\rightarrow$ 邊界防禦」之邏輯故事線。
