# Math16 三模型 Aggressive Healer Round 1 正式比較 v1

> **Round 角色：** Round 1 = **正式主分析（Primary formal analysis）**
> **Round 2：** **尚未執行**；若未來執行，僅作 post-hoc iterative replay，**不得覆寫 Round 1 主表**
> **Archive HEAD：** `e6ceffbd5601605d116a3a28ff38aa4b7542fc20`
> **Protocol：** 凍結規則 × FAIL-only × 單輪 Deterministic Healer（不呼叫模型）
> **⚠ 2026-07-30 overlay：** 4B 主表採 corrected overlay（Final **87**／rescue **8**／**3.32%**）；frozen archive 仍為 88／9／3.73%。見 [Correction Note](10_math16_aggressive_round1_source_label_promotion_mismatch_correction_note_v1.md)。

---

## 1. 核心統計

| 模型 | Baseline PASS | Final PASS | verified rescue | Baseline FAIL | 修復率 | regression |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.5 Flash | 289/320 | 289/320 | 0 | 31 | 0.00% | 0 |
| Qwen 9B | 101/320 | 102/320 | 1 | 219 | 0.46% | 0 |
| Qwen 4B（corrected overlay） | 79/320 | **87/320** | **8** | 241 | **3.32%** | 0 |
| Qwen 4B（frozen archive） | 79/320 | 88/320 | 9 | 241 | 3.73% | 0 |

修復率分母 = Baseline FAIL：

- Qwen 4B（corrected）：`8/241 = 3.32%`（分析主敘事）
- Qwen 4B（frozen）：`9/241 = 3.73%`（永久封存）
- Qwen 9B：`1/219 = 0.46%`
- Gemini：`0/31 = 0%`

## 2. Cumulative PASS 曲線

| 模型 | C0 | C1 | C2 | C3 | C4 | C5a | C5b | C5c |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Gemini 3.5 Flash | 289 | 289 | 289 | 289 | 289 | 289 | 289 | 289 |
| Qwen 9B | 101 | 101 | 102 | 102 | 102 | 102 | 102 | 102 |
| Qwen 4B（corrected） | 79 | 85 | **85** | **85** | **85** | **87** | **87** | **87** |
| Qwen 4B（frozen） | 79 | 85 | 86 | 86 | 86 | 88 | 88 | 88 |

## 3. 正式主結論

在同一套凍結、FAIL-only、單輪 Deterministic Healer 下，分析層 corrected overlay 為 Qwen 4B／9B／Gemini verified rescue **8／1／0**（frozen archive 仍記 4B＝9）；以 Baseline FAIL 為分母，修復率分別為 **3.32%**／0.46%／0%。4B 真 rescue＝Tier A 6＋D1 active-shadow 2；C2 +1 為幽靈帳（source–label promotion mismatch）。在本次三模型與 16 題實驗範圍內，Baseline 表現較高的模型，其殘餘失敗較少命中現有 frozen rules 的安全修復窗口。此結果顯示 Healer 效益與 residual failure type 及規則適配程度密切相關，但不宣稱模型規模與修復率存在普遍因果關係。三模型 regression 均為 0。

## 4. Round 邊界

| 項目 | 狀態 |
|---|---|
| Round 1 | **正式主分析**（本文件；4B 以 corrected overlay 為分析主敘事） |
| Round 2 | **尚未執行** |
| 未來 Round 2（若執行） | 僅 post-hoc iterative replay |
| Round 2 可否覆寫 Round 1 主表 | **否** |
| Frozen C5a／summary／journals | **永久保留 88／9** |

## 5. 圖表

| 圖 | 路徑 |
|---|---|
| Baseline vs Final | `docs/決賽文件/實驗結果文件/Math16/figures/figure_07_round1_baseline_vs_final.svg` |
| Verified rescue | `docs/決賽文件/實驗結果文件/Math16/figures/figure_08_round1_verified_rescue.svg` |
| Pass curves | `docs/決賽文件/實驗結果文件/Math16/figures/figure_09_round1_pass_curves.svg` |
| Rescue rate | `docs/決賽文件/實驗結果文件/Math16/figures/figure_10_round1_rescue_rate.svg` |
| Frozen chart data | `docs/決賽文件/實驗結果文件/Math16/figures/round1_chart_data_v1.json` |
| Corrected overlay | `docs/experiments/manifests/math16_aggressive_round1_corrected_overlay_v1.json` |

> Figure 07–10 仍顯示 **frozen** 88／9／3.73%；口試／主表以 overlay 為準並加 footnote。
