# Math16 Qwen 4B — Cell-wise Deterministic Fixpoint Replay Protocol v1

> **status:** `FROZEN_PROTOCOL_NOT_EXECUTED`
> **protocol_id:** `math16_qwen4b_cellwise_fixpoint_replay_protocol_v1`
> **machine_readable:** `docs/experiments/manifests/math16_qwen4b_cellwise_fixpoint_replay_protocol_v1.json`
> **focused_test:** `tests/finals_rebuild/test_math16_qwen4b_cellwise_fixpoint_replay_protocol_v1.py`
> **HEAD_at_authoring:** `328001b2f7aa0a1474d126de9686852257326e75`
> **origin/main_at_authoring:** `328001b2f7aa0a1474d126de9686852257326e75`
> **this_round:** 只凍結規格；**不**執行 fixpoint replay、**不**跑模型、**不**修改 frozen rules／Round 1 artifacts

---

## 1. Positioning

| Attribute | Binding |
|---|---|
| Model scope | **僅 Qwen 4B**（`qwen3.5:4b`／`model_group=qwen4b`） |
| Role | **post-hoc 4B-only mechanism pilot** |
| Relation to Round 1 | Round 1＝正式主分析（已封存）；本協議＝獨立 post-hoc iterative replay 規格 |
| Cross-model inference | **禁止**對 9B／Gemini／2B 作任何 fixpoint 推論或執行 |
| Rule mutation | **禁止**新增規則、改 guard、改 threshold、改 order |

本協議**不得覆寫** Round 1 主表、closures、journals、sources 或 headline。

---

## 2. Input population（closure）

### 2.1 Round 1 sealed headline（權威）

| Quantity | Value | Authority |
|---|---:|---|
| Total cells | 320 | Round 1 three-model summary |
| Round 1 final PASS | **88** | `math16_three_model_round1_summary_v1.json`／`math16_c5a_final_source_closure_v1.json` |
| Round 1 final FAIL | **232** | same |
| Round 1 verified rescue | 9 | sealed; **not** re-attributed by this protocol |

### 2.2 Fixpoint input

- **掃描／修改集合：** Round 1 final 後仍 **FAIL** 的 **232** cells
- **永久排除：** Round 1 final 已 **PASS** 的 **88** cells — **永不掃描、不修改、不進 SHA history、不進 fixpoint journal active set**
- **恒等式：** `88 + 232 = 320`

### 2.3 Round 1 final source（每 cell 起點）

每個 residual FAIL cell 的 fixpoint 起點＝該 cell 的 **Round 1 cumulative final post-source**（單輪 A→B→C1→C2→D3→D1→D5→D2 完成後的最終 source）：

| Case | Round 1 final source |
|---|---|
| 多數 C5a FAIL 且未被 D5／D2 修改 | `math16_c5a_final_source_closure_v1.json` 之 `c5a_final_source_*` |
| D5 development 修改且仍 FAIL（1 cell） | `math16_c5a_tier_d_d5_development_replay_v1` post-source |
| D2 development 修改且仍 FAIL（1 cell） | `math16_c5a_tier_d_d2_development_replay_v1` post-source |

**SHA history 初始值：** 每個 active cell 在 cycle 開始前，`full_sha_history = [round1_final_source_sha256]`。

---

## 3. Fixed rule order（凍結）

每一 **cycle**（對單一仍 active 的 cell）完整套用一輪固定順序：

```text
A → B → C1 → C2 → D3 → D1 → D5 → D2
```

機器可讀層標籤：

```text
tier_a → tier_b → tier_c1 → tier_c2 → tier_d3 → tier_d1 → tier_d5 → tier_d2
```

| Layer | Frozen rule set（不得改） |
|---|---|
| A | Pilot-02 Tier A 六條 |
| B | Tier B 四條（legacy IDs 保留） |
| C1 | `TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1` |
| C2 | `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1` |
| D3 | `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` |
| D1 | `TIER_D_OPS_SHADOW_REMOVAL_V1` |
| D5 | `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1`（min_score=8, min_margin=2） |
| D2 | `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1` |

**禁止：** 修改 rule 語意、guard、threshold、order；不得新增規則；不得因 PASS／FAIL 調整規則。

---

## 4. Cell-wise execution model

### 4.1 Unit of work

- **逐 cell** 獨立推進；**禁止**整批 232 cells 同步一起重跑下一輪。
- 僅 **仍 active** 的 residual FAIL cell 進入下一 cycle。
- 已 PASS（本協議內 rescue）或已終止的 cell 不再掃描。

### 4.2 One cycle（對單一 active cell）

```text
1. cycle_index += 1（1-based；上限 max_round=8）
2. round_start_source / round_start_sha ← 當前 source
3. 依固定順序 A→B→C1→C2→D3→D1→D5→D2 套用規則：
   - 每條記錄 pre_sha／post_sha、eligible／modified／abstained
   - 記錄 newly_eligible／enabling_prior_rule（若適用）
4. round_end_source / round_end_sha ← 本輪結束 source
5. source_changed ← (round_end_sha != round_start_sha)
6. 對 round_end_source 做 final evaluation（觀測用）
7. 依 §5 終止判斷（固定順序）
```

### 4.3 Blindness／acceptance

| Signal | Allowed? |
|---|---|
| Evaluator PASS／FAIL 用於**觀測／記帳／終止分類** | 允許（僅在完整一輪後的固定判斷） |
| Evaluator 結果決定是否**接受／回退** source | **禁止** |
| Evaluator 結果決定是否**跳過／重排**規則 | **禁止** |
| Outcome-guided acceptance／rollback | **禁止** |
| 依 PASS／FAIL 調整規則 | **禁止** |

規則 eligibility／mutation **僅**依 frozen rule＋當前 source＋凍結 contract；不得讀答案或用修後結果回饋選元。

---

## 5. Termination judgment order（固定）

每個仍 active 的 cell，**完整跑完一輪後**，嚴格依下列順序判斷（先命中先停）：

### 5.1 `ITERATIVE_RESCUE`

若 final evaluation = **PASS**：

1. 停止
2. `termination_reason = ITERATIVE_RESCUE`
3. 記錄 `rescue_cycle = cycle_index`
4. 記錄 `rescue_rule_id`（見 §7）
5. 保留完整 rule trace
6. `cycle_detected = false`；`max_round_reached = false`

### 5.2 `ZERO_CHANGE_CONVERGENCE`

若仍 **FAIL**，且 `round_end_source == round_start_source`（`source_changed = false`）：

1. 停止
2. `termination_reason = ZERO_CHANGE_CONVERGENCE`
3. `convergence_cycle_count = cycle_index`

### 5.3 `CYCLE_DETECTED`

若仍 **FAIL**，且 source 有變：

1. 計算 `round_end_sha`
2. 與該 cell 自 Round 1 final source 起累積的完整 `full_sha_history` 比對
3. 若 `round_end_sha` **已出現**於 history：
   - `termination_reason = CYCLE_DETECTED`
   - `cycle_detected = true`
   - 停止（**不**把重複 SHA 再 append；或 append 並標記 detected — 機器可讀採：**detected 後停止且不 append**）
4. 若**未出現**：將 `round_end_sha` **加入** `full_sha_history`，繼續 §5.4

### 5.4 `MAX_ROUND_NON_CONVERGENT`

若已達 `max_round = 8`：

1. `termination_reason = MAX_ROUND_NON_CONVERGENT`
2. `max_round_reached = true`
3. 停止

### 5.5 Continue

否則：

- **只有該 cell** 進入下一輪（`cycle_index` 再＋1）
- 不得整批一起重跑

---

## 6. SHA history／cycle detection

| Rule | Binding |
|---|---|
| Origin | `full_sha_history[0] = round1_final_source_sha256` |
| Per successful non-cycling change | append `round_end_sha` after §5.3「未出現」分支 |
| Detection predicate | `round_end_sha ∈ full_sha_history`（在 append 之前） |
| Zero-change | **不**因 SHA 重複觸發 CYCLE；走 `ZERO_CHANGE_CONVERGENCE`（因未變，end==start，而 start 必已在 history） |
| PASS cells | 不維護／不掃描 |

`round_start_sha` 在 cycle 開始時等於當前 source SHA；其必須已在 `full_sha_history` 中（初始或前一輪 append）。

---

## 7. Rescue attribution

| Field | Definition |
|---|---|
| `rescue_cycle` | 達 PASS 的 `cycle_index` |
| `rescue_rule_id` | **本輪（該 rescue cycle）最後一次修改 source、且其後 final evaluation 為 PASS 的規則** |
| Full rule trace | 該 cycle 內 A→…→D2 每條的 eligible／modified／abstained／pre_sha／post_sha 必保留 |

若一輪內多條規則修改 source，且最終 PASS：`rescue_rule_id`＝時間序上**最後一個** `modified=true` 且 `post_sha != pre_sha` 的 `rule_id`。

若理論上 PASS 但本輪無任何 modified（不應發生於本協議輸入）：`rescue_rule_id = null` 並記 anomaly（正式 runner 必須 fail-closed 報告；本凍結輪不執行）。

---

## 8. Required journal fields

每個 active cell 每個 cycle／終止列至少記錄：

| Field | Notes |
|---|---|
| `cell_id` | |
| `cycle_index` | 1..8 |
| `round_start_sha` | |
| per-rule `pre_sha`／`post_sha` | 依固定順序 |
| `rule_id` | 每條 |
| `eligible`／`modified`／`abstained` | 每條 |
| `round_end_sha` | |
| `source_changed` | bool |
| `full_sha_history` | 自 Round 1 final 起 |
| `newly_eligible` | 本輪因**先前規則**修改後才變 eligible 的規則集合／事件 |
| `enabling_prior_rule` | 使某規則 newly eligible 的先前 `rule_id` |
| `iterative_partial_repair` | 本輪或跨輪曾 source_changed 且仍非 PASS |
| `rescue_cycle` | 僅 `ITERATIVE_RESCUE`；否則 null |
| `rescue_rule_id` | 僅 `ITERATIVE_RESCUE`；否則 null |
| `convergence_cycle_count` | 終止時已完成 cycles |
| `termination_reason` | 四種之一或 `null`（仍 active） |
| `regression` | Round 1 PASS 不在本協議；本欄記本協議內觀測之 PASS→FAIL（預期不發生於已排除 88）；殘餘 FAIL 路徑通常 false |
| `cycle_detected` | bool |
| `max_round_reached` | bool |

### Termination enum

```text
ITERATIVE_RESCUE
ZERO_CHANGE_CONVERGENCE
CYCLE_DETECTED
MAX_ROUND_NON_CONVERGENT
```

---

## 9. Hard bans

1. 不依 evaluator 結果決定是否繼續、接受或回退 source（終止分類除外，見 §4.3／§5）
2. 不因某格 PASS／FAIL 調整規則
3. 不新增規則
4. 不做 outcome-guided acceptance
5. 不覆寫 Round 1
6. 不執行 9B／Gemini／2B fixpoint
7. 不整批同步重跑下一輪
8. 本凍結輪不建立正式 replay 結果目錄、不跑模型

---

## 10. Outputs（未來執行時；本輪不建立）

預留路徑（**本輪不得寫入正式結果**）：

```text
docs/experiments/results/math16_qwen4b_cellwise_fixpoint_replay_v1/
docs/experiments/manifests/math16_qwen4b_cellwise_fixpoint_replay_v1.json   # future run manifest
```

本輪僅存在 protocol design／protocol manifest／focused tests。

---

## 11. Validation checklist（protocol freeze）

- [x] 232 residual FAIL closure（對齊 Round 1 sealed）
- [x] 88 PASS exclusion closure
- [x] `max_round = 8`
- [x] SHA history 從 Round 1 final source 起算
- [x] 終止判斷順序固定（§5）
- [x] cycle detection focused test
- [x] zero-change／rescue／cycle／max-round 四種 termination focused tests
- [x] protocol JSON 可解析
- [ ] 正式 fixpoint replay（**本輪不做**）

---

## Document control

| Field | Value |
|---|---|
| Document | `docs/experiments/design/math16_qwen4b_cellwise_fixpoint_replay_protocol_v1.md` |
| Kind | Cell-wise deterministic fixpoint replay protocol（4B-only，post-hoc） |
| Execution this round | **none** |
| Commit／push this round | **none** |
