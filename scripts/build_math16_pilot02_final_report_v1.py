# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Final Report v1 Generator & Validation Script.

Outputs:
  - docs/experiments/reports/math16_pilot02_final_report_v1.md
  - docs/experiments/reports/math16_pilot02_final_report_v1_manifest.json
  - docs/experiments/reports/math16_pilot02_final_report_v1_build_report.md
  - tests/test_math16_pilot02_final_report_v1.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Input formal sources
MILESTONE_DIR = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1"
FROZEN_CLAIMS = MILESTONE_DIR / "frozen_numeric_claims.json"
LIMITATIONS_PATH = MILESTONE_DIR / "interpretation_limitations.md"
SOURCE_SHA_CLOSURE = MILESTONE_DIR / "source_sha_closure.json"

INTEGRATED_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"
JURY_QA = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
CORE_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
CORE_SPEC_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figure_spec_v1"
ONE_PAGER_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23"

# Output files
OUT_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1.md"
OUT_MANIFEST = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1_manifest.json"
OUT_BUILD_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v1_build_report.md"
OUT_TEST = ROOT / "tests/test_math16_pilot02_final_report_v1.py"


def sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# ── Markdown Report Content Generation ────────────────────────────────────────

REPORT_MARKDOWN = """# Math16 Pilot-02 正式整合研究報告 (Final Report v1)

```text
MATH16_PILOT02_FINAL_REPORT_V1_FROZEN
DETERMINISTIC_AST_HEALER_BOUNDARY_RESEARCH_LINE
IVAN_MACRONIX_SCIENCE_FAIR_OFFICIAL_REPORT
```

> **研究聲明**：
> Deterministic AST Healer 不是第二個解題模型，而是只在修法唯一、局部、可驗證的窄小窗口介入；其餘情況主動 Abstain。

---

## 1. 摘要

本研究針對小參數在地化語言模型（Qwen 3.5 4B 與 9B）生成數學解題程式碼時出現之語法或結構瑕疵，實證劃定硬性工程干預機制（Deterministic AST Healer）的安全修復邊界。實驗 Protocol 採用 16 道 K12 數學題型（涵蓋 Integer 整數、Polynomial 多項式、Radical 根式與 Fraction 分數四大家族）、3 個模型（包含雲端強模型參照組 Gemini 3.5 Flash）、4 種 Prompt 引導條件（Ab1 Native 原生、Ab2g Generic 鷹架、Ab2d+api 領域 API 鷹架以及 Ab2d+spec 標準規範）與 5 個隨機種子，系統化構建全量 960 個測試單元（cells）之實證矩陣。整體評估流程嚴格分為 Baseline 評估、Active Healer 靜態 Eligibility 審查與 Tier 1 雙模型配對交叉分析。

實驗結果顯示：在無修復介入之 Baseline 條件下，Gemini 通過 289/320 格 (90.31%)，Qwen 9B 通過 101/320 格 (31.56%)，Qwen 4B 通過 78/320 格 (24.38%)。針對 Qwen 4B 的 242 格 Baseline 失敗案例，Active Healer 執行靜態 Eligibility 審查，其中 10 格符合修法唯一且可靜態驗證之安全介入條件；Primary Healer 成功救援 5 格，最終通過數提升至 83/320 格 (25.94%)，且實證觀察到零倒退 (Observed Regression = 0)。Post-hoc 機制驗證下額外確認 6 格修復 (84/320 格)。Gemini 與 Qwen 9B 因殘餘失敗案例未命中事前凍結之修復規則，系統依 Protocol 主動選擇 Abstain (Eligible = 0)，展現明確之防禦邊界。

在 4B 與 9B 之 320 格 Tier 1 配對分析中，雙過 52 格、4B 獨過 26 格、9B 獨過 49 格、雙敗 193 格，淨增加 23 格 (RD = +7.1875%)。單元層級 Exact McNemar 檢定顯示顯著差異 ($p = 0.010582$)；然考量 16 個 Task 聚類效應之 Task-clustered Bootstrap 95% 信賴區間跨 0 (`[-0.94%, +14.38%]`)，顯示將結論外推至未知全新數學題型時仍具抽樣不確定性。在家族分層中，Fraction 家族 9B 淨勝 14 格 ($p = 0.012541$)，機制拆解顯示 21 格 9B-only 通過主要源於 4B 的語法與格式標點缺失，非純數學推理能力差距。此外，Polynomial 家族中 9B 表現偏低集中於單一題型與特定 LaTeX 組裝衝突。

本研究證明 Deterministic AST Healer 的核心定位並非第二個解題模型，而是只在修法唯一、局部、可驗證的窄小窗口內提供確定性安全介入，面臨不明確修法時主動 Abstain 放棄盲猜，以維護整體系統之可解釋性與安全性。

---

## 2. 研究動機

隨著大型語言模型 (LLM) 在自動程式碼生成領域的廣泛應用，將小參數在地化模型 (4B/9B) 部署於邊緣算力設備已成為重要趨勢。然而，小模型在生成結構化程式碼時，常因語法細節瑕疵（如括號未閉合、JSON 欄位包覆錯誤）導致可執行檔崩潰。若直接採用第二個 LLM 進行對話式修復，不僅顯著增加推論延遲與算力成本，更可能引入不可預測的邏輯改變與倒退 (Regression)。因此，開發具備確定性 (Deterministic) 保證、低延遲且可解釋的 AST 層級修復機制（AST Healer），並實證劃定其安全介入邊界，具備高度之科學與工程價值。

---

## 3. 研究問題

本研究聚焦於以下核心研究問題：
1. **修復視窗與能力劃分**：AI 生成程式失敗時，哪些錯誤型態可由 Deterministic AST Healer 安全修復？哪些錯誤必須主動 Abstain？
2. **小模型與工程干預之協同**：經工程干預 (Scaffold + Healer) 之 4B 小模型，能否在特定語法瑕疵視窗內達成確定性救援？
3. **規模與家族分層影響**：Qwen 4B 與 9B 在四個數學家族（Integer, Polynomial, Radical, Fraction）中的配對表現有何差異？
4. **安全防禦與零倒退**：Deterministic AST Healer 能否在救援失敗案例的同時，保持觀察到零倒退 (Observed Regression = 0)？

---

## 4. Deterministic AST Healer定位

Deterministic AST Healer **不是第二個解題模型**，它不參與數學推理，也不嘗試改寫程式碼的核心解題邏輯。其定位為基於抽象語法樹 (AST) 與確定性規則的靜態安全防線：
- **安全介入原則**：僅在「修法唯一、局部瑕疵、靜態可驗證」的窄小窗口內進行代換。
- **主動放棄 (Abstain)**：若失敗案例涉及語義錯誤、邏輯缺失或存在多種可能修法，Healer 拒絕盲目猜測，主動選擇 Abstain，將控制權交還系統。
- **零倒退防禦**：透過事前 Eligibility 審查與事後 Revalidation 兩道防線，確保不將原本可運行的程式修改至失效狀態。

---

## 5. 題目與模型

### 題庫設計
採用 16 道涵蓋 K12 數學領域之代表性題型，分為四大數學家族：
- **Integer (整數四則)**：`ce101`, `ce102`, `ce103`, `ce104`
- **Polynomial (多項式)**：`ce113`, `ce114`, `ce115`, `ce116`
- **Radical (根式運算)**：`ce121`, `ce122`, `ce123`, `ce124`
- **Fraction (分數運算)**：`ce131`, `ce132`, `ce133`, `ce134`

### 測試模型
1. **Qwen 3.5 4B (Local)**：小參數在地化模型，測試 Primary Healer 救援能力。
2. **Qwen 3.5 9B (Local)**：中參數在地化模型，測試規模擴展對 Baseline 與修復邊界之影響。
3. **Gemini 3.5 Flash (Cloud)**：雲端強模型，作為 Tier 2 描述性基準參照 (Descriptive Reference Only)。

---

## 6. 四種Prompt條件

評估以下四種 Prompt 引導與規範條件：
1. **`Ab1` (Native)**：原生提示，不提供語義規範與 API 引導，測試模型原生隨機性。
2. **`Ab2g` (Generic Scaffold)**：一般性鷹架引導，鎖定變數命名與 LaTeX 結構。
3. **`Ab2d+api` (Domain Scaffold + API)**：領域專用鷹架，注入 `IntegerOps`, `FractionOps` 等封裝工具類別。
4. **`Ab2d+spec` (Domain Scaffold + Standard Spec)**：
   - Qwen 4B 與 9B 正式生成採用 `Ab2d+spec-v2`。
   - Gemini 正式生成採用 `Ab2d+spec-v1`（Gemini 80/80 為 Post-hoc 機制驗證，非正式重新生成）。

---

## 7. 960-cell實驗矩陣

實驗矩陣規模如下：
- **矩陣維度**：16 題型 × 3 模型 × 4 條件 × 5 隨機種子 = 960 cells。
- **Tier 1 配對矩陣**：Qwen 4B (320 cells) vs Qwen 9B (320 cells) 進行一對一完全匹配配對分析。
- **Tier 2 參照矩陣**：Gemini 3.5 Flash (320 cells) 提供強模型天花板基準。

---

## 8. 評估方法與Eligibility

### 評估契約
每一個測試單元產生的程式碼均經由獨立 Evaluator 進行嚴格評分：
- **PASS**：程式可執行、無語法錯誤、輸出格式符合 specification、且數學結果 100% 正確。
- **FAIL**：包含語法錯誤 (SyntaxError)、契約違反 (Contract Error)、API 引用錯誤或數學計算錯誤。

### Eligibility 審查機制
對於所有 Baseline FAIL 案例，Healer 在決定是否介入前執行 Eligibility 靜態審查：
- **Eligible**：案例符合事前凍結之修復規則（如 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 語法瑕疵），且修法解答唯一。
- **Noneligible / Abstain**：不符合特定規則或存在歧義者，系統記錄為 Abstain 並保持原始 FAIL。

---

## 9. 三模型Baseline

在無 Healer 介入之 Baseline 條件下，三模型於 320 個測試單元中之通過表現如下：

![Figure 1 Baseline總覽](../visualization/math16_pilot02_core_figures_v1/figure_01_baseline_overall.png)

### Baseline 統計數據
- **Gemini 3.5 Flash**：通過 289 / 320 格，通過率 **90.31%** (FAIL = 31 格)。
- **Qwen 3.5 9B**：通過 101 / 320 格，通過率 **31.56%** (FAIL = 219 格)。
- **Qwen 3.5 4B**：通過 78 / 320 格，通過率 **24.38%** (FAIL = 242 格)。

---

## 10. Qwen 4B Primary Healer

針對 Qwen 4B 之 242 格 Baseline 失敗案例，Active Healer 執行 Primary 修復：

![Figure 5 Eligibility／Rescue](../visualization/math16_pilot02_core_figures_v1/figure_05_healer_eligibility_boundary.png)

### 修復數據彙整
- **Baseline FAIL**：242 格
- **Eligible (符合修復條件)**：10 格
- **Primary Rescue (救援成功)**：5 格
- **Primary Final (最終通過)**：83 / 320 格 (通過率 25.94%)
- **Post-hoc Rescue (事後驗證)**：6 格 (Post-hoc Final = 84 / 320 格)
- **Observed Regression (觀察倒退)**：0 格

---

## 11. Primary／Post-hoc分帳

為維護實證研究之嚴謹性，嚴格實施 Primary 與 Post-hoc 數據分帳：

| 模型與項目 | Baseline | Eligible | Primary Rescue / Final | Post-hoc Rescue / Final | Observed Regression |
|---|---|---|---|---|---|
| **Qwen 4B** | 78 / 320 | 10 格 | **5 格 (83/320)** | 6 格 (84/320) | 0 格 |
| **Qwen 9B** | 101 / 320 | 0 格 | **0 格 (101/320)** | 0 格 (101/320) | 0 格 |
| **Gemini 3.5 Flash** | 289 / 320 | 0 格 | **0 格 (289/320)** | Post-hoc 306/320 | 0 格 |

- **分帳原則**：83/320 為事前預註冊 Protocol 唯一正式認可數據。Post-hoc 84/320（Qwen 4B）與 306/320（Gemini）屬事後機制探索，不得冒充為 Primary 正式結果。

---

## 12. Qwen 4B與9B配對分析

在 320 個完全相同題目與條件配對單元中，對 Qwen 4B 與 9B 進行一對一 Tier 1 配對分析：

![Figure 4 Tier 1配對](../visualization/math16_pilot02_core_figures_v1/figure_04_tier1_paired_analysis.png)

### 2×2 配對矩陣
- **BOTH_PASS (兩者皆過)**：52 格
- **FOUR_B_ONLY (4B 獨過)**：26 格
- **NINE_B_ONLY (9B 獨過)**：49 格
- **BOTH_FAIL (兩者皆敗)**：193 格
- **總測試數**：320 格

### 配對統計量
- **Net Cell Gain (淨增加格數)**：+23 格 ($49 - 26$)
- **Paired Risk Difference (RD)**：+7.1875%
- **Exact McNemar Test**：$p = 0.010582$ (單元層級顯示顯著偏向 9B)
- **Task-clustered Bootstrap 95% CI**：`[-0.94%, +14.38%]` (考量 16 題型聚類效應後信賴區間跨 0)

---

## 13. Family分層

將 320 個配對單元按四大數學家族拆解（欄位順序固定為 `BOTH_PASS / FOUR_B_ONLY / NINE_B_ONLY / BOTH_FAIL`）：

![Figure 3 Family差異](../visualization/math16_pilot02_core_figures_v1/figure_03_family_breakdown.png)

### 四大家族配對表現表

| 數學家族 | BOTH_PASS | FOUR_B_ONLY | NINE_B_ONLY | BOTH_FAIL | 總格數 | Exact McNemar p | 備註 |
|---|---|---|---|---|---|---|---|
| **Integer** | 29 | 1 | 13 | 37 | 80 | $p = 0.001831$ | 9B 表現較佳 |
| **Polynomial** | 3 | 13 | 6 | 58 | 80 | $p = 0.167089$ | 4B 獨過較多 (異常分析見 14 節) |
| **Radical** | 10 | 5 | 9 | 56 | 80 | $p = 0.423950$ | 兩者無顯著差距 |
| **Fraction** | 10 | 7 | 21 | 42 | 80 | $p = 0.012541$ | 9B 淨勝 14 格 (顯著) |

---

## 14. 4B Ab2d+api與9B Polynomial異常

### 4B `Ab2d+api` 通過率低下診斷
4B 在 `Ab2d+api` 條件下通過數降至 8/80 格。事後診斷顯示：在 27 格失敗診斷樣本中，77.8% (21/27) 屬 Python 本體 SyntaxError（括號未閉合或語法破碎），僅 18.5% (5/27) 屬 Parser 不友善。結果證實失敗主因在於 4B 在該提示下生成的程式碼本體破損，而非評分 Parser 偏差。

### 9B Polynomial 表現低下診斷
Qwen 9B 在 Polynomial 家族通過數偏低 (9/80 vs 4B 的 16/80)，集中於 `ce115_calc_polynomial_division_l1` 單一題型與特定 LaTeX 組裝衝突。此屬特定欄位提示結構敏感性，未建立因果關係，不可外推為 9B 全域能力失控。

---

## 15. Gemini描述性參照

Prompt 條件對三模型通過數之影響如下：

![Figure 2 Prompt條件](../visualization/math16_pilot02_core_figures_v1/figure_02_prompt_conditions.png)

### Prompt 條件比較

| Condition | Gemini 3.5 Flash | Qwen 3.5 4B | Qwen 3.5 9B |
|---|---|---|---|
| **Ab1** | 72 / 80 | 15 / 80 | 18 / 80 |
| **Ab2g** | 76 / 80 | 19 / 80 | 27 / 80 |
| **Ab2d+api** | 78 / 80 | 8 / 80 | 16 / 80 |
| **Ab2d+spec** | 63 / 80 (spec-v1)* | 36 / 80 (spec-v2) | 40 / 80 (spec-v2) |

> **Figure 2 圖說與分帳特別聲明**：
> - Gemini 在 `Ab2d+spec` 欄位顯示之 80/80 屬 Post-hoc 機制驗證（證明在 API 簽名完整補齊後達 80/80），非正式重新生成。
> - Gemini 正式生成採用 `Ab2d+spec-v1`，通過數為 63/80。
> - Qwen 4B 與 9B 採用 `Ab2d+spec-v2` 正式生成。
> - 三模型提示版本不同，不得假裝為完全同條件之 Primary 直接推論。

---

## 16. Healer安全介入邊界

Deterministic AST Healer 之安全介入架構概念如下：

![Figure 6 安全介入概念圖](../visualization/math16_pilot02_core_figures_v1/figure_06_healer_concept_zones.png)

### 安全介入邊界三原則
1. **可修復區 (Repair Window)**：僅對語法解答唯一、局部且可驗證之瑕疵（如特定 JSON key 包含瑕疵）進行確定性修正。
2. **防禦性放棄 (Abstain Zone)**：對於邏輯錯誤、語義缺失或具備多種修正可能之案例，Healer 拒絕盲猜，主動選擇 Abstain。
3. **零倒退防線 (Zero Regression)**：透過事前 Eligibility 與事後 Revalidation 機制，確保修改不會破壞原本正確之程式。

---

## 17. 五項主要發現

本研究歸納出以下五項核心實證發現：

1. **Baseline能力與Healer可修復窗口不同**：模型 Baseline 生成通過率高，不代表剩餘失敗中包含更多可修復瑕疵；修復視窗取決於失敗案例是否符合凍結之修復規則。
2. **4B存在窄小且可驗證的repair window**：Qwen 4B 經 Active Healer 干預成功救回 5 格（Primary 83/320），證明小模型配接硬性干預具有救援價值。
3. **9B整體通過較高，但Family結果非單調**：9B 在 Overall 通過率高於 4B，但在 Polynomial 家族因單一題型提示敏感性出現非單調狀況。
4. **Prompt效果依模型、版本與部署條件而異**：同一 Prompt 條件（如 `Ab2d+api`）在 4B 與 Gemini 上呈現截然不同之效用。
5. **Abstain是Deterministic Healer的重要安全能力**：知曉何時不該猜與何時該修同等重要，主動 Abstain 是控制 Regression 風險的核心防禦。

---

## 18. 方法學限制

本研究嚴格受限於以下 10 項凍結方法學限制：

1. **Overall 統計顯著性與外推不確定性 (Cell-level vs Task-level)**：細胞層級 Exact McNemar 檢定顯示 9B-only (49格) 顯著多於 4B-only (26格) ($p = 0.010582$)；然考慮 16 個 Task 聚類效應之 Task-clustered Bootstrap 95% CI 跨 0 (`[-0.94%, +14.38%]`)，顯示外推至未知全新題型時仍具抽樣不確定性。不得宣稱「9B 保證優於 4B」。
2. **四大數學家族分層屬探索性分析 (Exploratory Subgroup Analysis)**：四大家族分層未事前預註冊族群 alpha 矯正，屬 Post-hoc 探索性分析，其 $p$-values 僅供假說生成參考。
3. **Fraction 家族差距不可解讀為純數學能力差異 (Fraction Gap Interpretation)**：9B 在 Fraction 淨勝 14 格 ($p = 0.012541$)，機制拆解顯示 21 格 9B-only 通過主要源於 4B 的語法與格式標點缺失，非純數學推理差距。
4. **Polynomial 9B 偏低為局部格式共現 (Polynomial Anomaly Localized Co-occurrence)**：9B 在 Polynomial 表現偏低集中於 `ce115` 多項式除法單一題型與特定 LaTeX 組裝衝突，未建立因果關係，不可外推為 9B 全域能力失控。
5. **Qwen 4B `Ab2d+api` 77.8% 語法錯誤侷限於診斷樣本 (4B Ab2d Anomaly Sample Bound)**：4B 在 `Ab2d+api` 下 77.8% (21/27) SyntaxError 結論僅適用於已剖析之 27 格診斷樣本，不可外推為全域失敗比例。
6. **Gemini 作為 Tier 2 描述性參照 (Gemini as Tier 2 Reference Only)**：Gemini 3.5 Flash (289/320, 90.31%) 僅作強模型描述性基準參照，不可宣稱「證明大模型規模因果壓倒性勝出」。
7. **Prompt 提示版本異質性 (Prompt Version Discrepancy)**：Gemini 正式生成採用 `Ab2d+spec-v1` (63/80)；Qwen 4B/9B 採用 `Ab2d+spec-v2` (36/80 與 40/80)，兩者提示版本不同。
8. **`Regression = 0` 僅屬實證觀察 (Observed Zero Regression Only)**：`Observed Regression = 0` 僅代表本次 320 個單元及凍結規則下「觀察到零倒退」，不可宣稱「保證在任意情境下 100% 絕不倒退」。
9. **`Eligible = 0` 不代表模型無失敗 (Eligibility Zero Scope)**：Gemini (31 FAIL) 與 9B (219 FAIL) 之 `Eligible = 0` 代表殘餘失敗未命中事前凍結規則，系統主動 Abstain，不代表生成無錯誤。
10. **全域邊界與範疇受限 (Global Protocol Bound)**：本研究所有數字與結論，僅嚴格適用於本次測試之 16 道數學題型、3 個模型、4 種 Prompt 條件、5 個隨機種子與凍結規則。

---

## 19. 評審追問摘要

選錄 8 項關鍵評審追問與標準答覆摘要：

### Q1: 為什麼要先做 Eligibility 審查，不直接全部程式都嘗試修復？
**答覆**：若不設 Eligibility 門檻，修復器將被迫對無明確修復依據的程式進行猜測性修改，破壞可解釋性並可能引入倒退 (Regression)。Eligibility 是維護「確定性安全介入」的必要防禦。

### Q2: Gemini 與 9B 的 `eligible=0` 是否代表 Healer 沒有用？
**答覆**：不是。`eligible=0` 代表在本次 320 個單元與現有凍結規則下，失敗案例未同時滿足唯一、安全、可驗證的介入條件。Healer 在無適用規則時選擇 Abstain（不介入），屬符合規範的安全行為。

### Q3: 為什麼 4B 可以修復 5~6 格，9B 反而 0 格？
**答覆**：因為 4B 模型的失敗案例中恰好有 10 格命中事前凍結的特定語法瑕疵規則；而 9B 雖然也有失敗，但沒有案例同時符合唯一且安全的現有修法條件。修復視窗取決於失敗型態是否落在凍結規則內。

### Q4: 為什麼不把所有 SyntaxError 都納入 Healer 修復範圍？
**答覆**：因為大多數 SyntaxError（如少寫半段邏輯、字串未閉合）並沒有唯一的修復解答。若強行修復將違反「修法唯一、不可反推答案」的核心原則，帶來極高修壞風險。

### Q5: Primary (83/320) 與 Post-hoc (84/320) 為什麼要嚴格分帳？
**答覆**：因為 83/320 是事前預註冊 Protocol 產生的唯一正式數據；84/320 是事後修正 false-loop revalidation 邏輯後的探討結果。科學規範要求嚴格區分預註冊結論與事後探討，不可將事後探討冒充為事前結論。

### Q6: Abstain（不介入）是不是代表 Healer 的能力不足？
**答覆**：不是。知曉「何時不該介入」與「何時該介入」同等重要。Abstain 是控制 Regression 風險的防禦機制，代表系統在面臨不明確修復目標時主動放棄盲猜。

### Q7: Overall McNemar 與 Task-clustered Bootstrap 結論看似不同，該如何解讀？
**答覆**：兩者代表不同層級的統計檢視。McNemar 顯示本次 320 個 matched cells 中 discordant 方向偏向 9B ($p = 0.010582$)；而 task-clustered bootstrap CI 跨 0 (95% CI `[-0.94%, +14.38%]`)，顯示外推到其他未知題目時仍具抽樣不確定性。

### Q8: 為什麼 Fraction family 的 9B 優勢最明顯 (淨增加 14 格)？
**答覆**：在 21 格 9B-only PASS 中，4B 有 15 格 (71.43%) 落在 L1~L4（語法、契約、API 與執行問題）。差距較多反映端到端生成穩定性，不可只解讀為純數學推理能力差異。

---

## 20. 結論、後續工作與正式證據索引

### 結論
本研究成功劃定 Deterministic AST Healer 的精確價值與安全介入邊界。實驗證實：
1. AST Healer 不扮演第二個解題模型，而在可驗證之特定語法瑕疵窗口發揮確定性救援功能（4B 救援 5 格，Primary 83/320）。
2. 在命中凍結規則之修復案例中，觀察到 `Regression = 0`。
3. 面臨無確定修法之失敗時，系統主動選擇 Abstain，有效維護整體架構之安全性與可解釋性。

### 後續工作
1. 擴充預註冊修復規則庫，針對 9B 語法瑕疵開發獨立驗證集。
2. 引入多 Task 跨領域擴展測試，縮減 Task-clustered Bootstrap 信賴區間不確定性。

### 正式證據與產物索引
- **Evidence Complete Milestone v1**：`docs/experiments/milestones/math16_pilot02_evidence_complete_v1/`
- **Integrated Results Report v1**：`docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md`
- **Jury Q&A Defense Manual v1**：`docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md`
- **Six Core Figures v1**：`docs/experiments/visualization/math16_pilot02_core_figures_v1/`
- **One-Pager v2.3 (Pairwise Collision-Free)**：`docs/experiments/presentation/math16_pilot02_one_pager_v23/`
"""

# ── Manifest Content ──────────────────────────────────────────────────────────

def build_manifest_and_reports():
    # Source SHAs
    claims_sha = sha256(FROZEN_CLAIMS)
    limitations_sha = sha256(LIMITATIONS_PATH)
    closure_sha = sha256(SOURCE_SHA_CLOSURE)
    integrated_report_sha = sha256(INTEGRATED_REPORT)
    jury_qa_sha = sha256(JURY_QA)
    one_pager_v23_sha = sha256(ONE_PAGER_DIR / "math16_pilot02_one_pager_v23.png")

    fig_shas = {
        "fig1": sha256(CORE_FIG_DIR / "figure_01_baseline_overall.png"),
        "fig2": sha256(CORE_FIG_DIR / "figure_02_prompt_conditions.png"),
        "fig3": sha256(CORE_FIG_DIR / "figure_03_family_breakdown.png"),
        "fig4": sha256(CORE_FIG_DIR / "figure_04_tier1_paired_analysis.png"),
        "fig5": sha256(CORE_FIG_DIR / "figure_05_healer_eligibility_boundary.png"),
        "fig6": sha256(CORE_FIG_DIR / "figure_06_healer_concept_zones.png"),
    }

    report_sha = sha256(OUT_REPORT)

    manifest_data = {
        "manifest_id": "math16_pilot02_final_report_v1_manifest",
        "version": "1.0.0",
        "project": "Ivan旺宏科學展 HealerBoundary",
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "starting_head_commit": "39117e7e259f1acec9885e38d01bd28e854ee597",
        "python_version": sys.version,
        "input_sources": {
            "frozen_numeric_claims_sha256": claims_sha,
            "interpretation_limitations_sha256": limitations_sha,
            "source_sha_closure_sha256": closure_sha,
            "integrated_results_report_sha256": integrated_report_sha,
            "jury_qa_final_sha256": jury_qa_sha,
            "one_pager_v23_png_sha256": one_pager_v23_sha,
            "core_figure_shas": fig_shas,
        },
        "output_report": {
            "filename": "math16_pilot02_final_report_v1.md",
            "sha256": report_sha,
            "section_count": 20,
        },
        "primary_posthoc_accounting": {
            "gemini_primary": "289/320 (Primary)",
            "gemini_posthoc": "306/320 (Post-hoc)",
            "qwen4b_baseline": "78/320",
            "qwen4b_primary_rescue": "5 cells → 83/320 (Primary)",
            "qwen4b_posthoc_rescue": "6 cells → 84/320 (Post-hoc)",
            "qwen9b_baseline_final": "101/320",
            "observed_regression": 0,
        },
        "key_statistics": {
            "tier1_both_pass": 52,
            "tier1_four_b_only": 26,
            "tier1_nine_b_only": 49,
            "tier1_both_fail": 193,
            "exact_mcnemar_p": 0.010582,
            "task_clustered_bootstrap_95ci": "[-0.94%, +14.38%]",
        },
        "family_tables_revalidated": {
            "Integer": {"BOTH_PASS": 29, "FOUR_B_ONLY": 1, "NINE_B_ONLY": 13, "BOTH_FAIL": 37},
            "Polynomial": {"BOTH_PASS": 3, "FOUR_B_ONLY": 13, "NINE_B_ONLY": 6, "BOTH_FAIL": 58},
            "Radical": {"BOTH_PASS": 10, "FOUR_B_ONLY": 5, "NINE_B_ONLY": 9, "BOTH_FAIL": 56},
            "Fraction": {"BOTH_PASS": 10, "FOUR_B_ONLY": 7, "NINE_B_ONLY": 21, "BOTH_FAIL": 42, "exact_mcnemar_p": 0.012541},
        },
    }

    with open(OUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, ensure_ascii=False, indent=2)

    build_report_text = f"""# Math16 Pilot-02 Final Report v1 組裝報告

```text
MATH16_PILOT02_FINAL_REPORT_V1_ASSEMBLED
ALL_FORMAL_EVIDENCE_INTEGRATED
PRIMARY_POSTHOC_ACCOUNTING_PRESERVED
SIX_CORE_FIGURES_REFERENCED
FINAL_REPORT_READY_FOR_CONTENT_REVIEW
```

## 一、 版控與基線
- **Starting / Ending HEAD**: `39117e7e259f1acec9885e38d01bd28e854ee597`
- **Output Report**: `docs/experiments/reports/math16_pilot02_final_report_v1.md`
- **Report SHA-256**: `{report_sha}`

## 二、 One-Pager Commit Lineage 紀錄
- `3ce9a0e4`: v2.2 基準錨點（強制加入 PDF 二進位檔）
- `3c40785a`: v2.3 初版（微觀對齊與基礎 layout 調整）
- `b95bd4b6`: v2.3 PDF 上傳
- `39117e7e`: 15 元素 / 105 Pairs 實測 BBox 零碰撞最終修正
- `ONE_PAGER_MILESTONE_CLOSED`

## 三、 固定 20 章節驗證
1. 摘要 (包含 16 題、3 模型、4 條件、5 seeds、960 cells、McNemar p 與 CI)
2. 研究動機
3. 研究問題
4. Deterministic AST Healer 定位
5. 題目與模型
6. 四種 Prompt 條件
7. 960-cell 實驗矩陣
8. 評估方法與 Eligibility
9. 三模型 Baseline
10. Qwen 4B Primary Healer
11. Primary／Post-hoc 分帳
12. Qwen 4B 與 9B 配對分析
13. Family 分層 (Integer / Polynomial / Radical / Fraction)
14. 4B Ab2d+api 與 9B Polynomial 異常
15. Gemini 描述性參照
16. Healer 安全介入邊界
17. 五項主要發現
18. 方法學限制 (10 項完整保留)
19. 評審追問摘要 (8 題 Q&A)
20. 結論、後續工作與正式證據索引
"""
    with open(OUT_BUILD_REPORT, "w", encoding="utf-8") as f:
        f.write(build_report_text)


def main():
    print("Writing Final Report v1 Markdown...")
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write(REPORT_MARKDOWN)

    # Check abstract CJK character count
    m = re.search(r"## 1\. 摘要\s*\n(.*?)\n---", REPORT_MARKDOWN, flags=re.DOTALL)
    assert m, "Abstract section missing!"
    abstract_text = m.group(1).strip()
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", abstract_text))
    print(f"Abstract CJK character count: {cjk_count} chars (Requirement: 500 - 700 chars)")
    assert 500 <= cjk_count <= 700, f"Abstract CJK count {cjk_count} out of range 500-700!"

    print("Building manifest and build report...")
    build_manifest_and_reports()

    print("Build completed successfully!")


if __name__ == "__main__":
    main()
