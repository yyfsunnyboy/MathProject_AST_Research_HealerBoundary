# Math16 三模型 Round 1 — 老師展示摘要 v1

> **一句話：** 同一套凍結 FAIL-only 單輪 Healer 下，4B／9B／Gemini 的 verified rescue 為 **9／1／0**；regression 皆為 **0**。

## 核心數字

| 模型 | Baseline → Final | rescue | 修復率（／Baseline FAIL） |
|---|---|---:|---|
| Gemini 3.5 Flash | 289 → 289 | 0 | 0/31 = 0.00% |
| Qwen 9B | 101 → 102 | 1 | 1/219 = 0.46% |
| Qwen 4B | 79 → 88 | 9 | 9/241 = 3.73% |

## 正式主結論（可直接引用）

在同一套凍結、FAIL-only、單輪 Deterministic Healer 下，Qwen 4B、Qwen 9B 與 Gemini 分別獲得 9、1、0 格 verified rescue；以 Baseline FAIL 為分母，修復率分別為 3.73%、0.46% 與 0%。在本次三模型與 16 題實驗範圍內，Baseline 表現較高的模型，其殘餘失敗較少命中現有 frozen rules 的安全修復窗口。此結果顯示 Healer 效益與 residual failure type 及規則適配程度密切相關，但不宣稱模型規模與修復率存在普遍因果關係。三模型 regression 均為 0。

## 展示提醒

- Round 1 是正式主分析；**Round 2 尚未執行**。
- 不把「模型越大／Baseline 越高 → 修復率越高」講成普遍因果。
- 重點講：**Healer 效益取決於 residual failure 是否落入 frozen safe-repair window**。

## 建議展示圖

1. `figures/figure_07_round1_baseline_vs_final.svg`
2. `figures/figure_08_round1_verified_rescue.svg`
3. `figures/figure_10_round1_rescue_rate.svg`

