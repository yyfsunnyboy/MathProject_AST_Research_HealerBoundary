# Math16 Pilot-02 核心圖表完整建置報告 (All 6 Core Figures Complete v1)

```text
MATH16_PILOT02_CORE_FIGURES_COMPLETE
FIGURES_2_AND_6_COMPLETED
ALL_SIX_CORE_FIGURES_RENDERED
EVIDENCE_COMPLETE_VALUES_PRESERVED
PRESENTATION_ASSET_LAYER_READY
```

## 一、 摘要 (Summary)
本建置報告記錄「Ivan旺宏科學展」HealerBoundary 研究線全套 6 張核心圖表 (Figure 1 ~ Figure 6) 之實體渲染產出結果。
第二批 2 張核心圖表 (Figure 2, Figure 6) 已完成渲染，同時 Figures 1, 3, 4, 5 之密碼學 Hash 保持 100% 不變。

## 二、 環境與字體 (Environment & Fonts)
* **Python Version**: `3.14.6`
* **Matplotlib Version**: `3.11.1`
* **Font Family**: `Microsoft JhengHei` (微軟正黑體, Native System Font)
* **Resolution**: 300 DPI (PNG) + SVG Vector Format

## 三、 全套 6 張核心圖表密碼學 SHA-256 清單

| 圖表 ID | 中文名稱 | PNG 檔名 | PNG SHA-256 | SVG SHA-256 |
| :- | :--- | :--- | :--- | :--- |
| **Figure 1** | 三模型 Baseline 總覽 | `figure_01_baseline_overall.png` | `5bc0c714769c9877...` | `8a3cc1c8c9bbc407...` |
| **Figure 2** | 四 Prompt 條件 × 三模型 | `figure_02_prompt_conditions.png` | `7df829db88a30c34...` | `76211c220a8eb304...` |
| **Figure 3** | 四 Family × Qwen 4B/9B | `figure_03_family_breakdown.png` | `f164edc807659c45...` | `8daf1901ca83b8f9...` |
| **Figure 4** | Tier 1 配對分析 | `figure_04_tier1_paired_analysis.png` | `f18bbb774e9a75c5...` | `b1d19764e6f16079...` |
| **Figure 5** | Healer Eligibility/Rescue | `figure_05_healer_eligibility_boundary.png` | `5887f0b829797ab6...` | `45126972a0373fca...` |
| **Figure 6** | Healer 安全介入邊界概念圖 | `figure_06_healer_concept_zones.png` | `3b358862434ea81b...` | `855f348a23fd78ee...` |

## 四、 驗證規範 (Verification Checkpoints)
1. **Figure 2 提示版本差異**: Gemini `spec-v1` (63/80) 與 Qwen `spec-v2` (36/80與40/80) 標記清晰，Post-hoc 80/80 旁註呈現。
2. **Figure 6 三區域概念**: 清楚標示 Safe Repair Window, Abstain Zone 與 Out of Scope，無虛構數字，強調 Healer 邊界與 `eligible=0` 意義。
3. **無過度宣稱**: 包含全部要求之警示註解與方法學限制 (Footnotes)。
