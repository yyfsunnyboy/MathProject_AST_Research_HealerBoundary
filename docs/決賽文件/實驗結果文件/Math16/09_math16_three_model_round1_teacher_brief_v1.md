# Math16 三模型 Round 1 — 老師展示摘要 v1

> **一句話（corrected overlay）：** 同一套凍結、FAIL-only、單輪 Deterministic Healer 下，4B／9B／Gemini 的 verified rescue 為 **8／1／0**；regression 皆為 **0**。（frozen archive 仍記 4B＝**9**。）
>
> **Round 角色：** Round 1 = **正式主分析**；**Round 2 尚未執行**（若未來執行，僅 post-hoc iterative replay，不得覆寫 Round 1 主表）。
>
> **⚠ 2026-07-30：** 詳見 [Correction Note](10_math16_aggressive_round1_source_label_promotion_mismatch_correction_note_v1.md) 與 `docs/experiments/reports/math16_aggressive_round1_source_label_promotion_mismatch_correction_note_v1.md`；479-cell formal evidence：`docs/experiments/results/math16_historical_round1_final_overlay_audit_v1/final_overlay_audit.jsonl`、`validation_summary.json`、`sha256_manifest.json`、`scripts/build_math16_historical_round1_final_overlay_audit_v1.py`、`docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md`／`math16_healer_rule_provenance_audit_v1_manifest.json`。Conservative 79→85／rescue 6 不受影響。

---

## 1. 安全邊界 vs 能力邊界

| 概念 | 含義 | 口試一句話 |
|---|---|---|
| **能力邊界（Capability）** | Baseline 生成能解多少題（PASS／320） | 「模型本來會不會寫對」 |
| **安全邊界（Safety／Healer）** | 殘餘 FAIL 是否落入 frozen rules 的唯一、局部、可驗證修法窗口 | 「失敗能不能安全修，還是該 Abstain」 |

**口號：** **先求不修壞，再求修得好**（Abstain／regression=0 優先於追求更多 rescue）。

- Baseline 高 ≠ Healer 修復率高。
- Gemini Baseline 289/320 高，但殘餘 31 FAIL **未命中**現有安全窗口 → rescue **0**（全層 Abstain）。
- 4B Baseline 較低，殘餘失敗較多落入規則窗口 → corrected rescue **8**（frozen 帳面曾記 9，含 1 格幽靈 C2）。
- 核心機制變項是 **residual failure type／rule fit**，不是「模型越大越好修」。

---

## 2. 核心數字（Round 1）

| 模型 | Baseline → Final | verified rescue | Baseline FAIL | 修復率 |
|---|---|---:|---:|---|
| Gemini 3.5 Flash | 289 → 289 | 0 | 31 | 0/31 = **0%** |
| Qwen 9B | 101 → 102 | 1 | 219 | 1/219 = **0.46%** |
| Qwen 4B（corrected） | 79 → **87** | **8** | 241 | 8/241 = **3.32%** |
| Qwen 4B（frozen） | 79 → 88 | 9 | 241 | 9/241 = 3.73% |

- 三模型 **regression = 0**。
- 本次觀察到修復率隨 Baseline 升高而遞減（**3.32%** → 0.46% → 0%；frozen 4B 曾記 3.73%）；**只描述本次範圍內的關聯，不宣稱模型規模與修復率的普遍因果**。
- 4B 真 rescue＝Tier A **6**＋D1 active-shadow **2**。

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

**Qwen 4B（cumulative `_v1`；overlay）**

| 層 | verified rescue | 備註 |
|---|---:|---|
| Tier A | 6 | 不變 |
| Tier B | **0**（frozen 帳面 1） | 幽靈帳：EMPTY_SUITE 開發 replay 成功但 sealed bytes 未晉升 |
| D3+D1 | 2 | active-shadow；seeds 1301／2002 |

---

## 4. 正式主結論（可直接引用）

在同一套凍結、FAIL-only、單輪 Deterministic Healer 下，分析層 corrected overlay 為 Qwen 4B、Qwen 9B 與 Gemini 分別獲得 **8**、1、0 格 verified rescue；以 Baseline FAIL 為分母，修復率分別為 **3.32%**、0.46% 與 0%（frozen archive 仍記 4B＝9／3.73%）。在本次三模型與 16 題實驗範圍內，Baseline 表現較高的模型，其殘餘失敗較少命中現有 frozen rules 的安全修復窗口。此結果顯示 Healer 效益與 residual failure type 及規則適配程度密切相關，但不宣稱模型規模與修復率存在普遍因果關係。三模型 regression 均為 0。

---

## 5. 三重安全性驗證（精簡總表）

### Fixpoint（residual FAIL）

| 模型 | residual | 第1輪 | 第2輪 | rescue | cycle | max-round |
|---|---:|---:|---:|---:|---:|---:|
| 4B | 232 | 232 | 0 | 0 | 0 | 0 |
| 9B | 218 | 215 | 3 | 0 | 0 | 0 |
| Gemini | 31 | 31 | 0 | 0 | 0 | 0 |
| **合計** | **481** | **478** | **3** | **0** | **0** | **0** |

### Safety（320×3＝960）

| 模型 | PASS | preserved | regression | modified |
|---|---:|---:|---:|---:|
| 4B（source-validated） | 87 | 87 | 0 | 2 |
| 9B | 102 | 102 | 0 | 13 |
| Gemini | 289 | 289 | 0 | 5 |
| **合計** | **478** | **478** | **0** | **20** |

> 4B＝sealed-source corrected（87／87）；9B／Gemini＝frozen label 且與 sealed-source 一致（102／102、289／289）。479-cell audit 僅 4B 一格 mismatch。

### 三句結論

1. Round 1 只修 FAIL；PASS 不進正式修復流程。
2. 三模型 residual 481 最多兩輪收斂、無新增 rescue；不得說「單輪＝真實 fixpoint」。
3. 960-cell safety：source-validated PASS 全 preserved、regression＝0（樣本觀察，非絕對保證）。
