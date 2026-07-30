# Math16 三模型 Round 1 — 老師展示摘要 v1

> **一句話：** 同一套凍結、FAIL-only、單輪 Deterministic Healer 下，4B／9B／Gemini 的 verified rescue 為 **9／1／0**；regression 皆為 **0**。
>
> **Round 角色：** Round 1 = **正式主分析**；**Round 2 尚未執行**（若未來執行，僅 post-hoc iterative replay，不得覆寫 Round 1 主表）。

---

## 1. 安全邊界 vs 能力邊界

| 概念 | 含義 | 口試一句話 |
|---|---|---|
| **能力邊界（Capability）** | Baseline 生成能解多少題（PASS／320） | 「模型本來會不會寫對」 |
| **安全邊界（Safety／Healer）** | 殘餘 FAIL 是否落入 frozen rules 的唯一、局部、可驗證修法窗口 | 「失敗能不能安全修，還是該 Abstain」 |

**口號：** **先求不修壞，再求修得好**（Abstain／regression=0 優先於追求更多 rescue）。

- Baseline 高 ≠ Healer 修復率高。
- Gemini Baseline 289/320 高，但殘餘 31 FAIL **未命中**現有安全窗口 → rescue **0**（全層 Abstain）。
- 4B Baseline 較低，殘餘失敗較多落入規則窗口 → rescue **9**。
- 核心機制變項是 **residual failure type／rule fit**，不是「模型越大越好修」。

---

## 2. 核心數字（Round 1）

| 模型 | Baseline → Final | verified rescue | Baseline FAIL | 修復率 |
|---|---|---:|---:|---|
| Gemini 3.5 Flash | 289 → 289 | 0 | 31 | 0/31 = **0%** |
| Qwen 9B | 101 → 102 | 1 | 219 | 1/219 = **0.46%** |
| Qwen 4B | 79 → 88 | 9 | 241 | 9/241 = **3.73%** |

- 三模型 **regression = 0**。
- 本次三模型觀察到修復率隨 Baseline 升高而遞減（3.73% → 0.46% → 0%）；**只描述本次範圍內的關聯，不宣稱模型規模與修復率的普遍因果**。

---

## 3. Partial repair 分帳（不得只講 verified rescue）

**正式定義：** Partial repair 不計入 verified rescue，但可表示 Healer 已移除語法、執行或結構 blocker，使程式由不可解析／不可執行前進至可診斷狀態。

| 帳目 | 含義 |
|---|---|
| verified rescue | FAIL→PASS（唯一計入主表 rescue） |
| parse gain | 不可解析 → 可解析 |
| execution gain | 不可執行 → 可執行／可診斷 |
| blocker-removal-only | 已移除 blocker，但仍未 PASS |
| modified-still-failed | 有修改但最終仍 FAIL |
| abstain | 不滿足唯一安全修法 → 不介入 |
| regression | PASS→FAIL（本次三模型皆 0） |

### Round 1 已知分層（已封存）

**Qwen 9B（authoritative FAIL-gated）**

| 層 | verified rescue | parse | exec | blocker-only | modified-still-failed |
|---|---:|---:|---:|---:|---:|
| Tier B | 1 | 4 | 2 | 3 | 3 |
| Tier C1 | 0 | 0 | 0 | 0 | 1 |
| Tier C2 | 0 | 0 | 0 | 0 | 6 |
| D1（C4→C5a 管線） | 0 | 0 | 3 | 3 | 12 |

**Gemini：** 全層 eligible＝0、modified＝0 → **Abstain**；verified rescue／partial repair 增益皆 **0**。

**Qwen 4B（cumulative `_v1` sealed；僅列有欄位者）**

| 層 | verified rescue | parse | exec | blocker-only | modified-still-failed |
|---|---:|---:|---:|---:|---:|
| Tier A（Method2 C0→C1） | 6 | （sealed 無獨立欄） | （sealed 無獨立欄） | （sealed 無獨立欄） | 5 |
| Tier B | 1 | 5 | 1 | （無獨立欄） | 4 |
| Tier C2 | 0 | 0 | 0 | （無獨立欄） | 5 |
| D3+D1（合併） | 2 | 1 | 4 | （無獨立欄） | 5 |
| D5 | 0 | 0 | 0 | — | 1 |
| D2 | 0 | 0 | 1 | **BLOCKER_REMOVAL_ONLY** | 1 |

> 缺欄位處標「無獨立欄／—」，**不推估**。

---

## 4. 正式主結論（可直接引用）

在同一套凍結、FAIL-only、單輪 Deterministic Healer 下，Qwen 4B、Qwen 9B 與 Gemini 分別獲得 9、1、0 格 verified rescue；以 Baseline FAIL 為分母，修復率分別為 3.73%、0.46% 與 0%。在本次三模型與 16 題實驗範圍內，Baseline 表現較高的模型，其殘餘失敗較少命中現有 frozen rules 的安全修復窗口。此結果顯示 Healer 效益與 residual failure type 及規則適配程度密切相關，但不宣稱模型規模與修復率存在普遍因果關係。三模型 regression 均為 0。

---

## 5. 分帳與 2B exploratory lower-bound（已完成）

| 項目 | 狀態 |
|---|---|
| FAIL-only、single-pass Round 1 | **正式主分析**（三模型主表不變） |
| Round 2 | **尚未執行**；若做，僅 post-hoc iterative replay |
| Development 40／Evaluation 120 | Method 1 contract-aware 切分另帳（Evaluation 120 為該切分主要結果）；與 Round 1 全量 320 headline **分帳** |
| Qwen 3.5 2B | smoke **0/16 PASS**；**已完成** 16-cell exploratory lower-bound frozen Healer replay：**0/16 → 0/16**（rescue 0、regression 0）；**不納入**三模型正式主表，**不估計**一般修復率 |
| Abstain 的意義 | 安全邊界：不猜修 → 保護 regression=0 |
| Regression=0 的意義 | 本次三模型 Round 1 觀察到無 PASS→FAIL；不宣稱任意情境保證 |

### 2B 密封摘要（exploratory only）

| 指標 | 數值 |
|---|---|
| Baseline → Final | **0/16 → 0/16** |
| verified rescue／regression | **0／0** |
| Tier A | eligible 2、modified 2、parse gain 1、blocker-removal-only 1 |
| D3 | eligible 1、modified 1、modified-still-failed 1 |
| D1 | eligible 1、modified 1、modified-still-failed 1 |
| 主要失敗 | runtime 7、catastrophic truncation 5、parse minor 2、schema 1、answer incorrect 1 |

---

## 6. 四模型探索性「可修復窗口」（非正式同等比較）

> **老師版一句話：** 「太弱，錯得太深；太強，現有安全規則無處可修；Healer 最有價值的，是模型已接近成功、只差一道小柵欄的中間地帶。」

四模型結果呈現一個探索性的可修復窗口圖像：2B 的失敗雖可被局部修正，但多數仍距完整 PASS 較遠；Gemini 的 residual FAIL 未命中現有 frozen rules；介於兩者之間的 4B 與 9B 出現較多 deterministic rules 可介入案例，其中 4B 的 verified rescue 最明顯。這支持一項機制性假說：Healer 的施力空間可能集中在模型已具備主要解題骨架、但仍殘留局部、唯一、可驗證結構瑕疵的中間區間。

**限制（口試必講）：**
- 2B 僅 16 cells；4B／9B／Gemini 各 320 cells。
- 僅屬 exploratory mechanism hypothesis。
- 不作正式相關、因果或普遍化主張。
- 不寫「Gemini 幾乎無結構性失敗」。
- 不寫「9B 多數已是語意層」。
- **不得**把本段畫成與第 2 節三模型正式主表同等的統計比較。

---

## 7. 展示提醒

1. 先講 **安全邊界 ≠ 能力邊界**，並用口號 **「先求不修壞，再求修得好」**。
2. 再秀 **Baseline→Final** 與 **rescue／Baseline FAIL**（僅三模型正式主表）。
3. 補一句 **partial repair 有價值但不等於 rescue**。
4. 被問 Gemini 0 rescue：答「安全邊界命中為 0，不是系統壞掉」。
5. 被問 2B：答「已做完 16 格 Healer exploratory：0→0；有局部修正，但沒 rescue，不算正式主表」。
6. 若提四模型窗口：先講老師版一句話，立刻補樣本異質與「探索假說、非因果」限制。

## 建議展示圖

1. `figures/figure_07_round1_baseline_vs_final.svg`
2. `figures/figure_08_round1_verified_rescue.svg`
3. `figures/figure_10_round1_rescue_rate.svg`
4. （進階）`figures/figure_09_round1_pass_curves.svg`
