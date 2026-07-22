# Math16 Pilot-02 證據完整里程碑總結報告 (Evidence Complete Report v1)

```text
MATH16_PILOT02_EVIDENCE_COMPLETE_V1_FROZEN
FORMAL_NUMERIC_CLAIMS_FROZEN
PRIMARY_POSTHOC_ACCOUNTING_FROZEN
SOURCE_SHA_CLOSURE_COMPLETED
PRESENTATION_ONLY_PHASE_OPENED
```

> **報告簡介**：
> 本報告為「Ivan旺宏科學展」HealerBoundary 研究線在 Math16 Pilot-02 實驗階段之正式 Evidence Complete 里程碑總結報告。
> 匯總收攏 3 模型、960-cell 測試單元之凍結 Ground-Truth 數據、配對統計、Healer 救援實證、Primary/Post-hoc 分帳、圖表規格與 10 項方法學限制，作為後續展板、一頁摘要與簡報製作之單一權威錨點。

---

## 一、 研究範疇與實驗架構 (Research Scope & Design)

1. **核心研究問題**：
   > 不同模型規模、Prompt 條件與數學家族，如何影響 AI 生成 Python 數學程式之成功率與失敗型態；以及 Deterministic AST Healer 在何種失敗範圍內具有安全、確定性介入價值。

2. **實驗矩陣 (960-Cell Matrix)**：
   - **題型**: 16 道 K12 數學題型（涵蓋 Integer, Polynomial, Radical, Fraction 四大家族）。
   - **Prompt 條件**: 4 種條件 (Ab1, Ab2g, Ab2d+api, Ab2d+spec)。
   - **隨機種子**: 5 個獨立 Seed。
   - **模型配置**:
     - Gemini 3.5 Flash (Cloud API, Tier 2 描述性基準參照)
     - Qwen 3.5 4B (Local Q4_K_M, Tier 1 正式配對比較)
     - Qwen 3.5 9B (Local Q4_K_M, Tier 1 正式配對比較)

---

## 二、 凍結核心 Ground-Truth 數據 (Frozen Ground-Truth Metrics)

| 評估維度 | Gemini 3.5 Flash | Qwen 3.5 4B | Qwen 3.5 9B |
| :- | :--- | :--- | :--- |
| **Baseline Pass Rate** | **289 / 320 (90.31%)** | **78 / 320 (24.38%)** | **101 / 320 (31.56%)** |
| **Baseline Fail Count** | 31 | 242 | 219 |
| **Healer Eligible Cases** | 0 | 10 | 0 |
| **Primary Rescue Count** | 0 | **5 (83/320, 25.94%)** | 0 |
| **Post-hoc Rescue Count** | 0 | **6 (84/320, 26.25%)** | 0 |
| **Observed Regression** | 0 | 0 (本次觀察到) | 0 |

---

## 三、 Tier 1 配對統計與 4 大家族對決 (Tier 1 Paired Analysis & Family Breakdown)

### 1. Tier 1 (4B vs 9B) 320-Cell 匹配四格表
* `BOTH_PASS`: **52 格**
* `FOUR_B_ONLY_PASS`: **26 格**
* `NINE_B_ONLY_PASS`: **49 格**
* `BOTH_FAIL`: **193 格**
* **淨勝單元數 ($\Delta$)**: $+23$ 格 (+7.19%)
* **細胞層級 Exact McNemar 檢定**: $p = 0.010582$
* **Task-clustered Bootstrap 95% CI**: `[-0.94%, +14.38%]` (跨 0 提醒全域外推不確定性)

### 2. 四大數學家族四格聯表 ($n=80$ per family)
* **Integer**: `BOTH_PASS=29 / 4B_ONLY=1 / 9B_ONLY=13 / BOTH_FAIL=37` ($p=0.001831$)
* **Polynomial**: `BOTH_PASS=3 / 4B_ONLY=13 / 9B_ONLY=6 / BOTH_FAIL=58` ($p=0.167089$)
* **Radical**: `BOTH_PASS=10 / 4B_ONLY=5 / 9B_ONLY=9 / BOTH_FAIL=56` ($p=0.423950$)
* **Fraction**: `BOTH_PASS=10 / 4B_ONLY=7 / 9B_ONLY=21 / BOTH_FAIL=42` ($p=0.012541$)

---

## 四、 Primary / Post-hoc 嚴格分帳與治理 (Primary vs Post-hoc Governance)

1. **Gemini 分帳**:
   - Primary score = `289/320` (預註冊 Baseline)。
   - Post-hoc score = `306/320` (Hybrid 機制驗證)。Gemini 事後 `80/80` 不得繪入 Primary 4-condition 主比較柱。
2. **Qwen 4B 分帳**:
   - Primary score = `83/320` (Primary rescue = 5)。
   - Post-hoc score = `84/320` (Post-hoc rescue = 6)。Post-hoc 救回 6 格不得取代 Primary 5 格。
3. **預設引用規範**:
   - 所有正式報告、Executive One-Pager、Poster 與 Oral Slides **預設引用 Primary 數據**。

---

## 五、 產物清冊與 SHA-256 Closure (SHA Closure Summary)

所有源檔案之密碼學 Hash 均已記錄於 [source_sha_closure.json](file:///c:/Projects/MathProject_AST_Research_HealerBoundary/docs/experiments/milestones/math16_pilot02_evidence_complete_v1/source_sha_closure.json)，起點 commit 為 `5c15b0aee0ef0d4bfa0439c8d0759ed0e4e2af49`。

---

## 六、 後續 presentation-only 工作清單 (Presentation-Only Task Inventory)

1. **High-res Vector Chart Scripts** (繪製 6 張核心圖表之 SVG/PNG 視覺檔)。
2. **Executive One-Pager Document** (組裝 1,000 字精簡一頁摘要)。
3. **Exhibition Poster Document** (製作展板專用 Layout 與圖表排版)。
4. **Oral Defense Slides Deck** (製作口試 5 Slide + Back-up slide 簡報)。
