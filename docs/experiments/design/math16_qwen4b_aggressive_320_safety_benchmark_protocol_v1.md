# Math16 Qwen 4B — Aggressive Healer Full 320-cell Safety Benchmark Protocol v1

> **status:** `FROZEN_PROTOCOL_NOT_EXECUTED`
> **protocol_id:** `math16_qwen4b_aggressive_320_safety_benchmark_protocol_v1`
> **machine_readable:** `docs/experiments/manifests/math16_qwen4b_aggressive_320_safety_benchmark_protocol_v1.json`
> **focused_tests:**
> - `tests/finals_rebuild/test_math16_qwen4b_aggressive_320_safety_benchmark_protocol_v1.py`
> - `tests/finals_rebuild/test_math16_qwen4b_aggressive_320_safety_benchmark_runner_v1.py`
> **HEAD_at_authoring:** `d5286226e658810b7ab32ff43a16c534ca6d7b27`
> **origin/main_at_authoring:** `d5286226e658810b7ab32ff43a16c534ca6d7b27`
> **this_round:** 只凍結 protocol／runner／preflight／tests；**不**正式執行 320 cells、**不**跑模型、**不**修改 frozen rules／Round 1／fixpoint／文件主表

---

## 1. Positioning

| Attribute | Binding |
|---|---|
| Model scope | **僅 Qwen 4B**（`qwen3.5:4b`／`model_group=qwen4b`） |
| Role | **`Aggressive Healer full 320-cell safety benchmark`**（post-hoc safety probe） |
| Relation to Round 1 | Round 1＝正式主分析（已封存）；本協議＝獨立全量 PASS／FAIL 安全基準規格 |
| Relation to fixpoint | **不同協議**：fixpoint 僅掃 232 FAIL、排除 88 PASS；本協議 **320 全進** |
| Relation to Method 2 | **不同協議**：Method 2＝Conservative eligibility-first Raw／Final 雙路；本協議＝同一套 Aggressive frozen stack |
| Relation to Round 2 | **不是**三模型 Round 2 正式覆寫 |
| Rule mutation | **禁止**新增規則、改 guard、改 threshold、改 order |

本協議**不得覆寫** Round 1 主表、closures、journals、sources、fixpoint 結果或 headline。

---

## 2. Input population（lock）

### 2.1 Round 1 sealed headline（權威）

| Quantity | Value | Authority |
|---|---:|---|
| Total cells | **320** | Round 1 three-model summary／C5a closure |
| Round 1 final PASS | **88** | same |
| Round 1 final FAIL | **232** | same |
| Identity | `88 + 232 = 320` | mandatory |

### 2.2 Safety-benchmark active set

- **掃描／修改集合：** Round 1 final 之 **全部 320 cells**（PASS 88 ＋ FAIL 232）
- **起點 source：** 每 cell 的 **Round 1 cumulative final post-source**（含 D5／D2 仍 FAIL 覆寫，與 fixpoint 起點同源）
- **禁止：** 依原始 PASS／FAIL 決定是否進入 stack、eligibility、接受、回退或改寫規則

### 2.3 Round 1 final source policy

與 fixpoint 相同之 Round 1 final source 解析：

| Case | Round 1 final source |
|---|---|
| 多數 C5a 格 | `math16_c5a_final_source_closure_v1.json` 之 `c5a_final_source_*` |
| D5 development 修改且仍 FAIL（1 cell） | `math16_c5a_tier_d_d5_development_replay_v1` post-source |
| D2 development 修改且仍 FAIL（1 cell） | `math16_c5a_tier_d_d2_development_replay_v1` post-source |

---

## 3. Fixed rule order（凍結，不得改）

每一 cell **單輪**完整套用：

```text
A → B → C1 → C2 → D3 → D1 → D5 → D2
```

| Layer | Frozen rule set |
|---|---|
| A | Pilot-02 Tier A 六條 |
| B | Tier B 四條（legacy IDs 保留） |
| C1 | `TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1` |
| C2 | `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1` |
| D3 | `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` |
| D1 | `TIER_D_OPS_SHADOW_REMOVAL_V1` |
| D5 | `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1`（min_score=8, min_margin=2） |
| D2 | `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1` |

**禁止：** 修改 rule 語意、guard、threshold、order；不得新增規則。

---

## 4. Execution model

### 4.1 Unit of work

- **逐 cell** 各執行 **恰好一輪** frozen stack（非 iterative fixpoint；`max_round` 不適用）
- **全部 320** cells 皆 active（含原始 PASS）
- 禁止 batch-resync 改規則；禁止依 PASS／FAIL 跳過細胞

### 4.2 One cell（single stack pass）

```text
1. input_status ← Round1 final PASS|FAIL（僅作分帳標籤）
2. start_source / start_sha ← Round1 final source
3. 依固定順序 A→B→C1→C2→D3→D1→D5→D2 套用規則
4. end_source / end_sha ← stack 結束 source
5. source_changed ← (end_sha != start_sha)
6. 對 end_source 做 observational evaluation → output_status PASS|FAIL
7. 依 §5 分類 transition（觀測用；不得回退 source）
```

### 4.3 Blindness／acceptance

| Signal | Allowed? |
|---|---|
| Round1／evaluator PASS／FAIL 用於**觀測／記帳** | 允許 |
| Round1／evaluator 結果決定 eligibility／接受／回退 source | **禁止** |
| Evaluator 結果決定跳過／重排規則 | **禁止** |
| Outcome-guided acceptance／rollback | **禁止** |
| 依 PASS／FAIL 調整規則 | **禁止** |

---

## 5. Transition accounting（必須統計）

令 `input_status`＝Round1 final，`output_status`＝本協議觀測結果：

| Transition | Definition |
|---|---|
| `preserved_pass` | PASS→PASS |
| `regression` | PASS→FAIL |
| `verified_rescue` | FAIL→PASS |
| `unchanged_fail` | FAIL→FAIL 且 `source_changed=false` |
| `modified_still_failed` | FAIL→FAIL 且 `source_changed=true` |

**Rates（分母鎖定）：**

| Metric | Formula |
|---|---|
| rescue rate | `verified_rescue / 232` |
| regression rate | `regression / 88` |
| preservation rate | `preserved_pass / 88` |
| modification rate | `modified_cells / 320`（`source_changed=true`） |
| net PASS change | `verified_rescue − regression` |

---

## 6. Journal／summary schema

### 6.1 Cell journal（每 cell 一列）

Required fields：

```text
cell_id, input_status, output_status, transition,
start_sha, end_sha, source_changed, modified,
per_rule_pre_sha, per_rule_post_sha, rule_id,
eligible, modified_flags, abstained,
rescue, regression, preserved_pass,
unchanged_fail, modified_still_failed
```

### 6.2 Aggregate summary

Required fields：

```text
protocol_id, model_group, n_cells, n_input_pass, n_input_fail,
fixed_sequence, transition_counts,
verified_rescue_n, regression_n, preserved_pass_n,
unchanged_fail_n, modified_still_failed_n, modified_n,
rescue_rate, regression_rate, preservation_rate, modification_rate,
net_pass_change, model_calls, formal_benchmark_executed
```

---

## 7. Guards

| Guard | Rule |
|---|---|
| Population lock | `n_cells=320`、`n_input_pass=88`、`n_input_fail=232` |
| Duplicate／overwrite | 既有 results journal／summary／lock 存在時，禁止重複正式執行（除非顯式 resume triage） |
| Formal execution | 預設 **blocked**；需 `allow_formal_execution=True` 才可跑 320 |
| Zero-execution preflight | 可驗證 population／freeze／sources；**不**套用 healer、**不**呼叫模型 |
| Namespace | 結果僅寫入本協議 reserved results root；不得覆寫 Round1／Method2／fixpoint |

---

## 8. Outputs（本輪不建立 results）

| Path | Role |
|---|---|
| `docs/experiments/results/math16_qwen4b_aggressive_320_safety_benchmark_v1/` | reserved results root |
| `cell_journal.jsonl` | per-cell journal（未來正式執行） |
| `summary.json` | aggregate summary（未來正式執行） |

---

## 9. This round declarations

- `protocol_freeze_only`
- `no_formal_320_execution`
- `no_model_calls`
- `no_frozen_rule_changes`
- `no_round1_overwrite`
- `no_fixpoint_overwrite`
- `no_docs_headline_edit`
- `all_320_active_including_pass_88`
- `single_stack_pass_not_fixpoint`
- `observational_eval_only`
