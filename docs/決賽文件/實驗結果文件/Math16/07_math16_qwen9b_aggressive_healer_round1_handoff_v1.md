# Math16 Qwen9B Aggressive Healer — Round 1 Handoff v1

> **性質：** 今日封存事實整理；**Round 2 尚未執行**
>
> **起始 HEAD（封存前）：** `72117d3facd48b8e78af534290dc7dcd2001149a`
>
> **9B authoritative namespace：** `qwen9b_fail_gated_authoritative_v1`
>
> **權威 gate：** 上一層 FAIL 才進下一層 Healer；PASS source 原樣保留（`PRIOR_PASS_PRESERVED`）

---

## 1. 4B Tier E（已完成）

- Residual census：C5a still-FAIL／prompt-contract families **E1–E4**
- **eligible 全為 0** → 各 family `NO_GO`
- 裁決：`DO_NOT_ESTABLISH_TIER_E`
- 4B cumulative／Tier D Development 探索已關閉（`TIER_D_4B_EXPLORATION_CLOSED`）
- Artifacts：
  - `docs/experiments/manifests/math16_c5_tier_e_prompt_contract_residual_supply_v1.json`
  - `docs/experiments/reports/math16_c5_tier_e_prompt_contract_residual_supply_v1.md`

---

## 2. 9B authoritative Round 1（FAIL-only C0→C5c）

### Gate／權威

| 項目 | 內容 |
|---|---|
| Cell gate | 僅上一層 **FAIL** 進下一層 Healer |
| PASS 政策 | 不得掃描、不得修改；post SHA＝pre SHA |
| Namespace | `qwen9b_fail_gated_authoritative_v1` |
| Authority 標記 | `AUTHORITATIVE_FAIL_GATED_CUMULATIVE_V1` |

### PASS 曲線（320 格）

**101 → 101 → 102 → 102 → 102 → 102 → 102 → 102**

| 層 | PASS |
|---|---:|
| C0 | 101 |
| C1（Tier A） | 101 |
| C2（Tier B） | 102 |
| C3（Tier C1） | 102 |
| C4（Tier C2） | 102 |
| C5a（D3→D1） | 102 |
| C5b（D5） | 102 |
| C5c（D2） | **102** |

### 分層統計（authoritative）

| 層 | eligible | modified | verified rescue | 其他 |
|---|---:|---:|---:|---|
| Tier A | 0 | 0 | 0 | — |
| Tier B | 4 | 4 | **1** | parse gain 4；execution gain 2；blocker removal 3 |
| Tier C1 | 1 | 1 | 0 | modified-still-failed 1 |
| Tier C2 | **6** | **6** | 0 | modified-still-failed 6；**PASS→PASS＝0** |
| D3 | 0 | 0 | 0 | — |
| D1 | 12 | 12 | 0 | execution gain 3；blocker removal 3；modified-still-failed 12 |
| D5 | 0 | 0 | 0 | — |
| D2 | 0 | 0 | 0 | ambiguous 6（trigger-after-abstain only） |

### D1 shadow 分類

- `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`：**11**
- `DEAD_SHADOW_REMOVAL`：**1**
- 正式措辭（active）：以 frozen scaffold 注入的正式 Ops implementation，取代模型自訂的 active shadow implementation。

### Round 1 總結

- **Final：** **102／320**
- **Verified rescue 總計：** **1**（僅 Tier B）
- **Regression：** **0**
- **PASS→PASS modification：** **0**

---

## 3. 舊 9B all-cell exploratory

- **保留、不刪除**
- 標記：`NONAUTHORITATIVE_ALL_CELL_EXPLORATORY`
- **不可**用於三模型正式比較
- 與 authoritative FAIL-only 產物命名空間分離（無 `fail_gated_authoritative` 後綴者為 exploratory）
- Cell-gating provenance：`docs/experiments/reports/math16_qwen9b_c3_c4_tier_c2_cell_gating_provenance_v1.md`

---

## 4. 明日唯一主線 — Round 2（尚未執行）

固定順序：

**Tier A → Tier B → Tier C1 → Tier C2 → D3 → D1 → D5 → D2**

約束：

1. 從 **9B Round 1 C5c final source**（`math16_c5c_final_source_closure_qwen9b_fail_gated_authoritative_v1`）起跑
2. 只處理仍 **FAIL 218** 格；PASS 102 原樣保留
3. **不因結果增加第三輪**
4. 之後 **4B** 補相同 Round 2
5. **Gemini** 使用完全相同兩輪流程
6. 三模型欄位統一：
   `gated FAIL`、`eligible`、`modified`、`verified rescue`、`parse gain`、`execution gain`、`blocker removal only`、`modified-still-failed`、`regression`

> **Round 2 狀態：尚未執行。**

---

## 5. 關鍵路徑速查

| 用途 | 路徑 |
|---|---|
| Round 1 C5c closure | `docs/experiments/manifests/math16_c5c_final_source_closure_qwen9b_fail_gated_authoritative_v1.json` |
| Round 1 chain summary | `docs/experiments/manifests/math16_c5a_c5c_tier_d_d5_d2_chain_qwen9b_fail_gated_authoritative_v1.json` |
| C0→C4 chain | `docs/experiments/manifests/math16_c0_c4_fail_gated_authoritative_chain_qwen9b_fail_gated_authoritative_v1.json` |
| Tier E census | `docs/experiments/manifests/math16_c5_tier_e_prompt_contract_residual_supply_v1.json` |
| 本 handoff | `docs/決賽文件/實驗結果文件/Math16/07_math16_qwen9b_aggressive_healer_round1_handoff_v1.md` |

---

## 6. 聲明（封存時）

- 未呼叫模型
- 未開始 Round 2
- 未修改 frozen 規則／threshold／order
- 未修改 4B frozen 統計
- 舊 all-cell 僅標記、未刪除
