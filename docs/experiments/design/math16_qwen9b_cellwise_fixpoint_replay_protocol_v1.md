# Math16 Qwen 9B — Cell-wise Deterministic Fixpoint Replay Protocol v1

> **status:** `FROZEN_PROTOCOL_NOT_EXECUTED`
> **protocol_id:** `math16_qwen9b_cellwise_fixpoint_replay_protocol_v1`
> **machine_readable:** `docs/experiments/manifests/math16_qwen9b_cellwise_fixpoint_replay_protocol_v1.json`
> **focused_tests:**
> - `tests/finals_rebuild/test_math16_qwen9b_cellwise_fixpoint_replay_protocol_v1.py`
> - `tests/finals_rebuild/test_math16_qwen9b_cellwise_fixpoint_replay_runner_v1.py`
> **HEAD_at_authoring:** `b04d8a166e9a3bfb31e3e2b6af31b96829b5b799`
> **origin/main_at_authoring:** `b04d8a166e9a3bfb31e3e2b6af31b96829b5b799`
> **this_round:** 只凍結 protocol／runner／preflight／tests；**不**執行 fixpoint replay、**不**跑模型、**不**修改 frozen rules／Round 1 artifacts／4B 產物

---

## 1. Positioning

| Attribute | Binding |
|---|---|
| Model scope | **僅 Qwen 9B**（`qwen3.5:9b`／`model_group=qwen9b`） |
| Role | **post-hoc 9B-only mechanism pilot**（對稱於 4B fixpoint） |
| Relation to Round 1 | Round 1＝正式主分析（已封存）；本協議＝獨立 post-hoc iterative replay 規格 |
| Relation to 4B fixpoint | **平行協議**：複用同一套 stack／SHA／終止判定；**不得**覆寫 4B 產物 |
| Cross-model inference | **禁止**對 4B／Gemini／2B 作任何 fixpoint 推論或執行 |
| Rule mutation | **禁止**新增規則、改 guard、改 threshold、改 order |

本協議**不得覆寫** Round 1 主表、closures、journals、sources 或 headline。

---

## 2. Input population（closure）

### 2.1 Round 1 sealed headline（權威）

| Quantity | Value | Authority |
|---|---:|---|
| Total cells | 320 | Round 1 three-model summary |
| Round 1 final PASS | **102** | `math16_three_model_round1_summary_v1.json`／`math16_c5c_final_source_closure_qwen9b_fail_gated_authoritative_v1.json` |
| Round 1 final FAIL | **218** | same |
| Round 1 verified rescue | 1 | sealed; **not** re-attributed by this protocol |

### 2.2 Fixpoint input

- **掃描／修改集合：** Round 1 final 後仍 **FAIL** 的 **218** cells
- **永久排除：** Round 1 final 已 **PASS** 的 **102** cells — **永不掃描、不修改、不進 SHA history、不進 fixpoint journal active set**
- **恒等式：** `102 + 218 = 320`
- **禁止：** 4B 專用 D5／D2 development override population logic；9B 起點一律 C5c final source

### 2.3 Round 1 final source（每 cell 起點）

每個 residual FAIL cell 的 fixpoint 起點＝該 cell 的 **C5c final post-source**：

| Field | Authority |
|---|---|
| path | `c5c_final_source_path` |
| sha256 | `c5c_final_source_sha256` |
| outcome | `c5c_outcome` ∈ `{PASSED, FAILED}` → protocol `PASS`／`FAIL` |

**SHA history 初始值：** `full_sha_history = [round1_final_source_sha256]`。

---

## 3. Fixed rule order（凍結；與 4B 相同）

```text
A → B → C1 → C2 → D3 → D1 → D5 → D2
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

---

## 4. Observational evaluator（唯一釘死）

| Item | Binding |
|---|---|
| Binding id | `math16_observational_evaluator_v1` |
| Classifier | `scripts.run_math16_latex_v1_gemini_live.classify_math16_response` |
| Mapper | `scripts.evaluate_math16_pilot02_full_v4.classify_outcome_to_v3` |
| Wrapper reference | `scripts.run_math16_c5a_c5c_tier_d_d5_d2_qwen9b_fail_gated_authoritative_v1.score_source` |
| Injectable factory | `agent_tools.finals_rebuild.math16_observational_evaluator_v1.make_observational_pass_fail_evaluator` |
| Scoring statuses | `PASSED`／`FAILED` |
| Protocol statuses | `PASS`／`FAIL`（`PASSED→PASS`，`FAILED→FAIL`） |
| Mutates source／artifacts | **No** |
| Rule selection | evaluator-blind（僅完整一輪後觀測／終止分類） |

Default CLI／preflight **不得**呼叫 evaluator；僅在授權正式執行且明確注入／`inject_authoritative_evaluator` 時可觀測。

---

## 5. Termination judgment order（與 4B 相同）

完整一輪後，嚴格依序：

1. evaluator **PASS** → `ITERATIVE_RESCUE`
2. 仍 FAIL 且 source SHA 不變 → `ZERO_CHANGE_CONVERGENCE`
3. 仍 FAIL、source 有變、且 end SHA 已在 `full_sha_history` → `CYCLE_DETECTED`（不 append）
4. 否則 append（若有變）並在 `cycle_index == max_round(8)` 時 → `MAX_ROUND_NON_CONVERGENT`；否則僅該 cell 進下一輪

---

## 6. Required journal fields

與 4B fixpoint journal schema 相容，另應可記錄 `evaluator_result`（PASS｜FAIL）於 final journal。

至少含：`cell_id`、`cycle_index`、`round_start_sha`／`round_end_sha`、per-rule pre／post SHA、`rule_id`／eligible／modified／abstained、`full_sha_history`、`termination_reason`、`rescue_cycle`／`rescue_rule_id`、`cycle_detected`、`max_round_reached`。

---

## 7. Non-goals（本協議輪）

1. 不執行正式 218-cell fixpoint
2. 不呼叫模型
3. 不修改 Healer 規則／4B frozen artifacts／Round 1 closures
4. 不做 Gemini
5. 不覆寫 Final Report／Jury Q&A／總報告
