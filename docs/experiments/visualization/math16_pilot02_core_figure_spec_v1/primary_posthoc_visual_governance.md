# Math16 Pilot-02 Primary / Post-hoc Visual Governance Specification v1

```text
PRIMARY_POSTHOC_VISUAL_GOVERNANCE_SPEC_V1
PRESERVED_ACCOUNTING_INTEGRITY
EXPLICIT_ANNOTATION_RULES_ENFORCED
```

## 一、 基本原則 (Core Principles)

為維護「Ivan旺宏科學展」HealerBoundary 研究之科學嚴謹性，本圖表視覺治理規範針對全書及簡報中所有核心圖表制定強制規範：

1. **Primary 與 Post-hoc 嚴格視覺區隔**：
   - **Primary 數據**（預註冊事前凍結 Protocol 數據）使用實線、飽和色、主要直條柱狀 (Solid Main Bars)。
   - **Post-hoc 數據**（事後除錯探討或機制驗證數據）僅能以虛線框 (Dashed Outline)、灰階/半透明柱、旁註 (Footnotes) 或獨立標記呈現，**嚴禁**與 Primary 畫成同級正式 Bar。

2. **禁止因果與能力過度解讀 (Forbidden Interpretations)**：
   - Gemini (289/320) 與 Qwen 4B (78/320)、9B (101/320) 之比較屬 **Tier 2 描述性參照**，不得宣稱「證明大模型數學能力全面碾壓」或「純參數規模效果」。
   - Pass rate 係「端到端生成與執行成功率」，包含 Python 語法、JSON 包裝與 API 呼叫，不等於「純數學能力」。
   - `Regression = 0` 必須明確註記為「**在本次 320 個測試單元與凍結規則中觀察到**」，不得宣稱「保證絕不倒退」或「100% 安全」。

3. **雙層統計同時呈現規範**：
   - 包含統計檢定之圖表（如 Tier 1 配對分析 Figure 4），必須**同時呈現**：
     - 細胞層級獨立性證據：Exact McNemar $p = 0.010582$
     - 題目群集外推不確定性：Task-clustered Bootstrap 95% CI `[-0.94%, +14.38%]`
   - 不得單獨寫「統計顯著」而忽略 Bootstrap CI 跨 0 之全域外推不確定性。

4. **圖表類型限制 (Chart Type Restrictions)**：
   - 嚴禁使用 3D 圖、圓餅圖 (Pie Chart)、雷達圖 (Radar Chart) 及雙 Y 軸圖 (Dual Y-axis Chart)。
   - 所有直條圖 (Bar Charts) 之 Y 軸起點必須為 **0**（不可裁切 Y 軸底端）。
   - 所有數值標籤必須包含 **分子 / 分分母**，百分比標籤至多保留 1 位小數。

---

## 二、 6 張核心圖表具體治理規範 (Per-Figure Visual Rules)

### 1. Figure 1: Baseline Overall Performance across Three Models
* **圖型**: 單組垂直直條圖 (Vertical Bar Chart)。
* **視覺分層**:
  - Qwen 3.5 4B (78/320, 24.4%) 與 Qwen 3.5 9B (101/320, 31.6%) 為 **Tier 1 Matched Comparison**（相同顏色系，如 4B 深藍、9B 淺藍）。
  - Gemini 3.5 Flash (289/320, 90.3%) 標示為 **Tier 2 Descriptive Reference**（灰色或特殊色帶，搭配「雲端參照」文字標記）。
* ** mandatory 註記**: "Pass rate represents end-to-end Python/JSON execution success, not pure mathematical reasoning."

### 2. Figure 2: Four Prompt Conditions across Three Models
* **圖型**: 分組直條圖 (Grouped Bar Chart)，X 軸為 4 個條件 (Ab1, Ab2g, Ab2d+api, Ab2d+spec)。
* **視覺分層**:
  - Gemini 的 `Ab2d+spec` 標示為 **`spec-v1` (63/80)**；Qwen 4B 與 9B 的 `Ab2d+spec` 標示為 **`spec-v2` (36/80 與 40/80)**。
  - Gemini Post-hoc 提示修復數據 (80/80) **不得** 畫在 `Ab2d+spec` 主柱上；僅能以虛線框 (Dashed Box) 疊加或在旁註說明。
* ** mandatory 註記**: "Gemini primary tested spec-v1; Qwen models tested spec-v2. Gemini Post-hoc 80/80 is mechanism verification only."

### 3. Figure 3: Four Mathematical Families for Qwen 4B vs Qwen 9B
* **圖型**: 分組直條圖 (Grouped Bar Chart)，X 軸為 4 個家族 (Integer, Polynomial, Radical, Fraction)。
* **視覺分層**: 4B (藍色) vs 9B (黃色/橘色)，每柱標示分子/80 (如 4B Polynomial: 16/80, 9B Polynomial: 9/80)。
* ** mandatory 註記**: "Polynomial localized drop in 9B is tied to template formatting (ce115) and cannot be extrapolated to overall math capability."

### 4. Figure 4: Tier 1 Paired 2x2 Contingency and Discordant Analysis
* **圖型**: 2x2 熱力矩陣圖 (Contingency Matrix) 或 兩柱不一致配對條形圖 (Discordant Bar Chart: 4B-only 26 vs 9B-only 49)。
* **視覺呈現**: 矩陣四格填入 `BOTH_PASS=52`, `4B_ONLY=26`, `9B_ONLY=49`, `BOTH_FAIL=193`。
* ** mandatory 註記**: 並列標示 `Exact McNemar p = 0.010582` (Cell-level direction) 與 `Cluster Bootstrap 95% CI = [-0.94%, +14.38%]` (Task-level uncertainty).

### 5. Figure 5: Healer Eligibility and Rescue Boundary across Three Models
* **圖型**: 階梯漏斗圖 (Stepped Funnel) 或 分層直條圖 (Layered Bar Chart)。
* **柱體分層**:
  - 第一層: Baseline FAIL (Gemini 31, 4B 242, 9B 219)
  - 第二層: Eligible Window (Gemini 0, 4B 10, 9B 0)
  - 第三層: Primary Rescue (Gemini 0, 4B 5, 9B 0)
* **Post-hoc 標記**: 4B Post-hoc Rescue = 6 僅能以半透明點線 (Dotted Overlay) 標示於 4B Primary 柱上方。
* ** mandatory 註記**: "Primary final = 83/320; Post-hoc final = 84/320. Regression=0 observed in tested cells."

### 6. Figure 6: Healer Boundary 3-Zone Conceptual Model
* **圖型**: 三區域示意概念圖 (3-Zone Structural Concept Diagram)。
* **區劃內容**:
  - Zone 1: Safe Repair Window (綠色，確定性唯一規則修復)
  - Zone 2: Abstain Zone (黃色，入口模糊/多可能修法主動放棄)
  - Zone 3: Out of Scope (灰色，演算法邏輯/數學語義錯誤)
* ** mandatory 規範**: 示意圖中嚴禁放置任何虛構或假造之數據數字。
