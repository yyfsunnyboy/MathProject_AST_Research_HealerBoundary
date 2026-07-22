# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Poster v1 Content & Layout Spec Generator.

Outputs:
  - docs/experiments/presentation/math16_pilot02_poster_v1_spec.md
  - docs/experiments/presentation/math16_pilot02_poster_v1_content_map.json
  - docs/experiments/presentation/math16_pilot02_poster_v1_build_report.md
  - tests/test_math16_pilot02_poster_v1_spec.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Formal Input Source Paths
FINAL_REPORT_V11 = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v11.md"
MILESTONE_DIR = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1"
FROZEN_CLAIMS = MILESTONE_DIR / "frozen_numeric_claims.json"
JURY_QA = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
CORE_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
ONE_PAGER_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23"

# Output Paths
OUT_SPEC = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_spec.md"
OUT_CONTENT_MAP = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_content_map.json"
OUT_BUILD_REPORT = ROOT / "docs/experiments/presentation/math16_pilot02_poster_v1_build_report.md"
OUT_TEST = ROOT / "tests/test_math16_pilot02_poster_v1_spec.py"


def sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# ── Poster Specification Markdown ──────────────────────────────────────────────

POSTER_SPEC_MARKDOWN = """# Math16 Pilot-02 展板內容藍圖與版面規格 (Poster v1 Spec)

```text
MATH16_PILOT02_POSTER_V1_SPEC_FROZEN
THREE_COLUMN_LANDSCAPE_LAYOUT_ARCHITECTURE
VISUAL_HIERARCHY_HERO_FIGURE4_DEFINED
PRIMARY_POSTHOC_ACCOUNTING_PRESERVED
```

> **展板核心問題**：
> AI生成程式失敗時，哪些錯誤可由Deterministic AST Healer安全修復？哪些必須Abstain？
>
> **展板核心主張**：
> Healer不是第二個解題模型，只在修法唯一、局部、可驗證的窄小窗口介入。

---

## 一、 版面架構與視覺階層 (Layout & Visual Hierarchy)

展板採用橫式三欄（Landscape 3-Column）經典學術展板架構設計，各區域與視覺焦距規範如下：

```text
+-----------------------------------------------------------------------------------------+
|                                    HEADER REGION                                       |
|  [主標題] Small but Precise: Outperforming Large Models through Engineered Self-Healing |
|  [研究問題] AI生成程式失敗時，哪些錯誤可由Deterministic AST Healer安全修復？哪些必須Abstain？   |
|  [實驗規模] 16題 x 3模型 x 4條件 x 5 seeds = 960 cells                                     |
|  [核心數字卡 1: Gemini 289/320]  [核心數字卡 2: 4B Primary 83/320]  [核心數字卡 3: 9B 101/320] |
+-----------------------------------+-----------------------------------+-----------------+
| LEFT COLUMN: 研究設計             | MIDDLE COLUMN: 主要證據 (主焦點)    | RIGHT COLUMN: 解讀與邊界 |
|                                   |                                   |                 |
| 1. 研究動機 (短句流程)            | 1. Figure 4 Tier 1配對分析 (Hero) | 1. Figure 3 Family差異 |
| 2. Healer定位 (窄小窗口)          |    - BOTH_PASS 52                 | 2. Figure 2 Prompt條件  |
| 3. 16題 / 四大家族                |    - 4B_ONLY 26                   |    (含 spec-v1/v2 警語) |
| 4. 三模型陣容                     |    - 9B_ONLY 49 (Hero焦點)        | 3. Figure 6 安全概念圖  |
| 5. 四Prompt條件                   |    - BOTH_FAIL 193                | 4. 五項主要發現        |
| 6. Baseline-Healer-Abstain 流程   |    - McNemar p / Cluster CI       | 5. 三項展板限制        |
| 7. Primary / Post-hoc 分帳說明     | 2. Figure 1 Baseline總覽          | 6. 一句結論             |
|                                   | 3. Figure 5 Eligibility/Rescue    |                 |
+-----------------------------------+-----------------------------------+-----------------+
```

### 視覺階層四級規範 (Four-Level Visual Hierarchy)

1. **Hero Level (最大主視覺)**：
   - **Figure 4 Tier 1 配對分析**：作為全展板視線焦距最大圖表，突出呈現 9B 獨過 49 格 vs 4B 獨過 26 格、McNemar $p = 0.010582$ 與 Task-clustered Bootstrap 95% CI `[-0.94%, +14.38%]`。
2. **Level 2 (次要焦點)**：
   - **Header 三大數字卡**：Gemini 289/320 (90.31%)、Qwen 4B Primary 83/320 (Baseline 78 + 救援 5)、Qwen 9B 101/320 (31.56%)。
3. **Level 3 (支撐數據)**：
   - **Figure 1 (Baseline 總覽)** 與 **Figure 5 (Eligibility / Rescue 邊界)**。
4. **Level 4 (輔助說明)**：
   - **Figure 3 (Family 差異)**、**Figure 2 (Prompt 條件)** 與 **Figure 6 (安全介入概念圖)**。

> **觀眾 3 秒即視感目標 (3-Second Glance Rule)**：
> 觀眾行經展板前 3 秒內，必須清晰捕捉四個核心視覺標記：
> (1) **全量 960 cells 實證** → (2) **4B 成功救回 5 格 (83/320)** → (3) **9B-only 49 vs 4B-only 26** → (4) **Healer 只修窄小窗口，無確定解即 Abstain**。

---

## 二、 欄位詳細內容配置 (Column Content Specifications)

### 1. Header (展板頁眉區)
- **主標題**：`Small but Precise: Outperforming Large Models through Engineered Self-Healing`
- **副標題／研究問題**：`AI生成程式失敗時，哪些錯誤可由Deterministic AST Healer安全修復？哪些必須Abstain？`
- **實驗規模標籤**：`16題型 × 3模型 × 4Prompt條件 × 5隨機種子 = 全量 960 cells`
- **三大核心數字卡**：
  - **Gemini 3.5 Flash**：`289 / 320` 格 PASS (通過率 90.31%，雲端強模型參照)
  - **Qwen 3.5 4B**：`83 / 320` 格 PASS (Primary Rescue = 5 格，Baseline 78 → 83，Observed Regression = 0)
  - **Qwen 3.5 9B**：`101 / 320` 格 PASS (Baseline / Final = 101/320，通過率 31.56%)

---

### 2. 左欄：研究設計 (Left Column: Study Design)

以極簡短句、流程方塊與點狀條列為主，禁止冗長內文段落：

1. **研究動機**：
   - 小模型 (4B/9B) 部署於邊緣算力常面臨語法與結構崩潰。
   - 對話式修復延遲高且易引入倒退；硬性 AST 修復提供確定性安全防線。
2. **Healer 定位**：
   - Healer 不是第二個解題模型，不重寫解題邏輯。
   - 僅在修法唯一、局部、可驗證之窄小窗口介入。
3. **16 題型／四大家族**：
   - **Integer (整數)**：`ce101`~`ce104` | **Polynomial (多項式)**：`ce113`~`ce116`
   - **Radical (根式)**：`ce121`~`ce124` | **Fraction (分數)**：`ce131`~`ce134`
4. **三模型陣容**：
   - Qwen 3.5 4B (Local) | Qwen 3.5 9B (Local) | Gemini 3.5 Flash (Cloud Tier 2 Reference)
5. **四 Prompt 引導條件**：
   - `Ab1` (Native) | `Ab2g` (Generic) | `Ab2d+api` (Domain API) | `Ab2d+spec` (Standard Spec)
6. **評估與干預流程**：
   - `LLM Code Generation` → `Evaluator Baseline Check` → `Eligibility Static Review` → `Active Healer / Abstain`
7. **Primary / Post-hoc 分帳宣告**：
   - 4B Baseline = 78/320
   - Primary Rescue = 5 格 → **Primary Final = 83/320** (唯一正式預註冊結論)
   - Post-hoc Rescue = 6 格 → **Post-hoc Final = 84/320** (相較 Primary 僅增加 1 個 PASS)

---

### 3. 中欄：主要證據 (Middle Column: Primary Evidence - Focal Area)

作為全展板尺寸最大、視覺最集中之地帶：

1. **Figure 4 Tier 1 配對分析 (Hero Figure - 最大圖)**：
   - 引用路徑：`../visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.png`
   - **核心數據高亮**：
     - **BOTH_PASS**：52 格 | **FOUR_B_ONLY**：26 格
     - **NINE_B_ONLY**：49 格 (重點高亮) | **BOTH_FAIL**：193 格
     - **Net Cell Gain**：+23 格 ($49 - 26$, RD = +7.1875%)
     - **Exact McNemar Test**：$p = 0.010582$ (單元層級顯著偏向 9B)
     - **Task-clustered Bootstrap 95% CI**：`[-0.94%, +14.38%]` (考量 16 題型聚類效應後信賴區間跨 0)

2. **Figure 1 Baseline 總覽**：
   - 引用路徑：`../visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.png`
   - **展示亮點**：Gemini 289/320 vs 9B 101/320 vs 4B 78/320 之出發基線比對。

3. **Figure 5 Eligibility / Rescue 邊界**：
   - 引用路徑：`../visualization/math16_pilot02_core_figures_v1/figure_05_healer_eligibility_boundary.png`
   - **展示亮點**：Qwen 4B Baseline FAIL 242 格中，僅 10 格符合 Eligible，Primary 成功救援 5 格 (83/320)；Gemini 與 9B 之 `Eligible = 0`。

---

### 4. 右欄：解讀與邊界 (Right Column: Interpretation & Boundary)

1. **Figure 3 Family 差異**：
   - 引用路徑：`../visualization/math16_pilot02_core_figures_v1/figure_03_family_breakdown.png`
   - **家族配對亮點**：
     - Integer: `29 / 1 / 13 / 37` ($p = 0.001831$)
     - Polynomial: `3 / 13 / 6 / 58` (4B 獨過較多)
     - Radical: `10 / 5 / 9 / 56`
     - Fraction: `10 / 7 / 21 / 42` ($p = 0.012541$, 9B 淨勝 14 格)

2. **Figure 2 Prompt 條件**：
   - 引用路徑：`../visualization/math16_pilot02_core_figures_v1/figure_02_prompt_conditions.png`
   - **圖側強制警語標籤**：
     > [!IMPORTANT]
     > Gemini 80/80 屬 Post-hoc 機制驗證；Primary spec-v1 為 63/80；Qwen 使用 spec-v2 正式生成；兩者提示版本不同，不作完全同條件 Primary 推論。

3. **Figure 6 安全概念圖**：
   - 引用路徑：`../visualization/math16_pilot02_core_figures_v1/figure_06_healer_concept_zones.png`
   - **概念三區塊**：Repair Window (窄小救援) | Abstain Zone (主動放棄) | Zero Regression (零倒退防線)

4. **五項主要發現 (Five Main Discoveries)**：
   1. **Baseline能力與Healer可修復窗口不同**：高 Baseline 通過率不代表剩餘失敗包含更多修復窗口。
   2. **4B存在窄小且可驗證的repair window**：Primary 救援 5 格 (83/320)，結果顯示小模型配接硬性干預具救援價值。
   3. **9B整體通過較高，但Family結果非單調**：Polynomial 家族出現局部格式敏感性逆轉。
   4. **Prompt效果依模型、版本與部署條件而異**：同一條件在 4B 與 Gemini 展現截然不同效果。
   5. **Abstain是Deterministic Healer的重要安全能力**：面臨不明確修法主動 Abstain，是控制 Regression 的核心防禦。

5. **三項展板限制 (Three Key Poster Limitations)**：
   1. **McNemar 單元層級顯著 ($p = 0.010582$)，但 Task-clustered CI 跨 0 (`[-0.94%, +14.38%]`)**：外推至未知題型具抽樣不確定性。
   2. **Fraction 差距包含 15 格 L1–L4 問題，屬探索性分析**：不可直接解讀為純數學能力差異。
   3. **`Observed Regression = 0` 與 `Eligible = 0` 僅限本次測試**：僅適用於凍結資料與特定規則，非全域萬能保證。

6. **展板總結 (Conclusion)**：
   - **Deterministic AST Healer 不扮演第二個解題模型，其核心價值在於精準劃定確定性修復之窄小安全邊界，面臨不明確修法時主動 Abstain 放棄盲猜，以維護整體系統之可解釋性與安全性。**

---

## 三、 排版與 BBox 測量方法學凍結 (BBox Measurement Methodology Freeze)

在後續展板實體渲染 (Poster Rendering) 階段，**必須嚴格遵守**以下量測與幾何規範，不得退回估算：

```text
POSTER_RENDERER_MEASURED_BBOX_METHODOLOGY_FROZEN
1. MATPLOTLIB_RENDERER_GET_WINDOW_EXTENT_BASED_MEASUREMENT (via get_window_extent() and get_position())
2. ABSOLUTE_FIGURE_COORDINATES_CONVERSION
3. NAMED_ELEMENT_PAIRWISE_COLLISION_DETECTION (ANY INTERSECTION AREA > 0 -> RAISE RUNTIME_ERROR)
4. PROHIBIT_HARDCODED_PERCENTAGE_STACKING
```

---

## 四、 嚴格禁用語氣與宣稱 (Banned Claims Guardrails)

展板文字 **嚴禁出現** 以下過度宣稱：
- ❌ 「證明 9B 較強」 / 「證明 9B 數學能力全面壓倒 4B」
- ❌ 「Healer 保證絕不倒退 (Zero Regression Guard)」
- ❌ 「額外救回 6 格」
- ❌ 「語法與格式標點缺失為主要原因」
- ❌ 「eligible=0 代表 Healer 無效」
- ❌ 「Post-hoc 84/320 為 Primary 正式結果」
"""

# Clean trailing whitespace from POSTER_SPEC_MARKDOWN
POSTER_SPEC_MARKDOWN = "\n".join(line.rstrip() for line in POSTER_SPEC_MARKDOWN.splitlines()) + "\n"

# ── JSON Content Map Generation ───────────────────────────────────────────────

def build_content_map_and_reports():
    v11_sha = sha256(FINAL_REPORT_V11)
    claims_sha = sha256(FROZEN_CLAIMS)
    qa_sha = sha256(JURY_QA)
    one_pager_sha = sha256(ONE_PAGER_DIR / "math16_pilot02_one_pager_v23.png")

    fig_shas = {
        "fig1": sha256(CORE_FIG_DIR / "figure_01_baseline_overall.png"),
        "fig2": sha256(CORE_FIG_DIR / "figure_02_prompt_conditions.png"),
        "fig3": sha256(CORE_FIG_DIR / "figure_03_family_breakdown.png"),
        "fig4": sha256(CORE_FIG_DIR / "figure_04_tier1_paired_analysis.png"),
        "fig5": sha256(CORE_FIG_DIR / "figure_05_healer_eligibility_boundary.png"),
        "fig6": sha256(CORE_FIG_DIR / "figure_06_healer_concept_zones.png"),
    }

    content_map_data = {
        "manifest_id": "math16_pilot02_poster_v1_content_map",
        "version": "1.0.0",
        "project": "Ivan旺宏科學展 HealerBoundary",
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "starting_head_commit": "d17a086d55e27e9b2d60783004dfd4511fdabc1b",
        "poster_title": "Small but Precise: Outperforming Large Models through Engineered Self-Healing",
        "research_question": "AI生成程式失敗時，哪些錯誤可由Deterministic AST Healer安全修復？哪些必須Abstain？",
        "core_claim": "Healer不是第二個解題模型，只在修法唯一、局部、可驗證的窄小窗口介入。",
        "column_structure": [
            "Left Column: Study Design (Motivation, Healer Role, 16 Tasks, 3 Models, 4 Prompts, Protocol Flow)",
            "Middle Column: Primary Evidence (Hero Figure 4, Figure 1 Baseline, Figure 5 Eligibility/Rescue)",
            "Right Column: Interpretation & Boundary (Figure 3 Family, Figure 2 Prompts, Figure 6 Concept, 5 Discoveries, 3 Limitations)"
        ],
        "visual_hierarchy": {
            "hero_figure": {
                "figure_id": "fig4_tier1_paired_analysis",
                "filename": "figure_04_tier1_paired_analysis.png",
                "scale_level": "Largest focal element on poster"
            },
            "level_2_elements": ["header_core_cards"],
            "level_3_elements": ["figure_01_baseline_overall.png", "figure_05_healer_eligibility_boundary.png"],
            "level_4_elements": ["figure_02_prompt_conditions.png", "figure_03_family_breakdown.png", "figure_06_healer_concept_zones.png"]
        },
        "source_paths": {
            "final_report_v11": "docs/experiments/reports/math16_pilot02_final_report_v11.md",
            "frozen_numeric_claims": "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json",
            "jury_qa_final": "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md",
            "core_figures_dir": "docs/experiments/visualization/math16_pilot02_core_figures_v1/",
            "one_pager_v23_dir": "docs/experiments/presentation/math16_pilot02_one_pager_v23/"
        },
        "figure_paths": {
            "fig1": "docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.png",
            "fig2": "docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_02_prompt_conditions.png",
            "fig3": "docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_03_family_breakdown.png",
            "fig4": "docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.png",
            "fig5": "docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_05_healer_eligibility_boundary.png",
            "fig6": "docs/experiments/visualization/math16_pilot02_core_figures_v1/figure_06_healer_concept_zones.png"
        },
        "source_shas": {
            "final_report_v11_sha256": v11_sha,
            "frozen_numeric_claims_sha256": claims_sha,
            "jury_qa_sha256": qa_sha,
            "one_pager_v23_sha256": one_pager_sha,
            "core_figures_sha256": fig_shas
        },
        "frozen_numbers": {
            "gemini_primary": "289/320",
            "gemini_posthoc": "306/320",
            "qwen_4b_baseline": "78/320",
            "qwen_4b_primary": "83/320 (rescue=5)",
            "qwen_4b_posthoc": "84/320 (rescue=6, +1 PASS vs Primary)",
            "qwen_9b_baseline_final": "101/320",
            "tier1_both_pass": 52,
            "tier1_four_b_only": 26,
            "tier1_nine_b_only": 49,
            "tier1_both_fail": 193,
            "exact_mcnemar_p": 0.010582,
            "task_clustered_bootstrap_95ci": "[-0.94%, +14.38%]"
        },
        "primary_posthoc_accounting": {
            "qwen4b_primary": "83/320 (Primary, 5 cells rescued)",
            "qwen4b_posthoc": "84/320 (Post-hoc, 6 cells rescued, +1 PASS vs Primary)",
            "gemini_primary": "289/320 (Primary, spec-v1=63/80)",
            "gemini_posthoc": "306/320 (Post-hoc, spec-v2=80/80 Mechanism Validation)"
        },
        "required_disclaimers": [
            "Gemini 80/80 is Post-hoc mechanism validation, NOT formal Primary re-run result.",
            "Gemini Primary spec-v1 = 63/80; Qwen 4B/9B used spec-v2.",
            "Do NOT infer direct Primary equivalence due to prompt version differences."
        ],
        "five_main_discoveries": [
            "1. Baseline能力與Healer可修復窗口不同。",
            "2. 4B存在窄小且可驗證的repair window。",
            "3. 9B整體通過較高，但Family結果非單調。",
            "4. Prompt效果依模型、版本與部署條件而異。",
            "5. Abstain是Deterministic Healer的重要安全能力。"
        ],
        "three_poster_limitations": [
            "1. McNemar顯著 (p=0.010582)，但 Task-clustered Bootstrap 95% CI 跨 0 ([-0.94%, +14.38%])，外推具不確定性。",
            "2. Fraction 差距包含 15 格 L1-L4 問題，屬探索性分析，不可解讀為純數學能力差距。",
            "3. Observed Regression = 0 與 Eligible = 0 僅限本次凍結測試單元與特定規則。"
        ],
        "bbox_methodology": "renderer_measured_pairwise_collision_free",
        "prohibited_claims": [
            "證明9B較強",
            "證明9B數學能力全面壓倒4B",
            "Healer保證絕不倒退",
            "額外救回6格",
            "語法與格式標點缺失為主要原因",
            "eligible=0代表Healer無效",
            "Post-hoc 84/320為Primary正式結果"
        ]
    }

    with open(OUT_CONTENT_MAP, "w", encoding="utf-8") as f:
        json.dump(content_map_data, f, ensure_ascii=False, indent=2)

    spec_sha = sha256(OUT_SPEC)

    build_report_text = f"""# Math16 Pilot-02 Poster v1 建置報告 (Spec Build Report)

```text
MATH16_PILOT02_POSTER_V1_SPEC_COMPLETED
THREE_COLUMN_CONTENT_ARCHITECTURE_FROZEN
VISUAL_HIERARCHY_AND_FIGURE_PLACEMENT_DEFINED
PRIMARY_POSTHOC_ACCOUNTING_PRESERVED
POSTER_READY_FOR_RENDERING
```

## 一、 版控與基線 (Version Control & Baseline)
- **Starting / Ending HEAD**: `d17a086d55e27e9b2d60783004dfd4511fdabc1b`
- **Final Report v1.1 SHA-256**: `{v11_sha}`
- **Output Spec File**: `docs/experiments/presentation/math16_pilot02_poster_v1_spec.md`
- **Poster Spec SHA-256**: `{spec_sha}`

## 二、 三欄內容藍圖與視覺階層 (Three-Column Content Architecture)
1. **Header**: 主標題、研究問題短句、960 cells 規模標籤、三大數字卡（Gemini 289/320, 4B 83/320, 9B 101/320）。
2. **Left Column (研究設計)**：極簡短句與流程圖（動機、Healer定位、16題/4家族、3模型、4Prompts、干預流程、Primary/Post-hoc分帳）。
3. **Middle Column (主要證據 - 最大主視覺焦點)**：
   - **Figure 4 Tier 1 配對分析 (Hero Figure - 最大圖)**
   - **Figure 1 Baseline 總覽**
   - **Figure 5 Eligibility / Rescue 邊界**
4. **Right Column (解讀與邊界)**：
   - **Figure 3 Family 差異**
   - **Figure 2 Prompt 條件 (含 spec-v1/v2 警語)**
   - **Figure 6 安全介入概念圖**
   - **五項主要發現**
   - **三項精選展板限制**
   - **一句總結**

## 三、 Renderer 實測 BBox 方法學凍結 (Methodology Freeze)
- 未來展板實體渲染階段，**強制使用** Matplotlib Renderer `get_window_extent()` / `get_position()` 實測 BBox 及具名 Pairwise 零碰撞檢測（繼承 v2.3 標準），嚴禁使用硬編碼百分比。

## 四、 產物約束檢查 (Output Constraint Check)
- 本輪僅輸出藍圖規格 (`.md`) 與內容映射檔 (`.json`)，未生成任何 PNG、PDF、PPT 或 Slides。
"""
    with open(OUT_BUILD_REPORT, "w", encoding="utf-8") as f:
        f.write(build_report_text)


def main():
    print("Writing Poster v1 Specification Markdown...")
    with open(OUT_SPEC, "w", encoding="utf-8") as f:
        f.write(POSTER_SPEC_MARKDOWN)

    print("Building Content Map JSON & Build Report...")
    build_content_map_and_reports()

    print("Poster v1 Spec generation completed successfully!")


if __name__ == "__main__":
    main()
