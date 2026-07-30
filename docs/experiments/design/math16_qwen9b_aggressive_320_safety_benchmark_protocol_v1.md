# Math16 Qwen 9B — Aggressive Healer Full 320-cell Safety Benchmark Protocol v1

> **status:** `FROZEN_PROTOCOL_NOT_EXECUTED`
> **protocol_id:** `math16_qwen9b_aggressive_320_safety_benchmark_protocol_v1`
> **machine_readable:** `docs/experiments/manifests/math16_qwen9b_aggressive_320_safety_benchmark_protocol_v1.json`
> **focused_tests:**
> - `tests/finals_rebuild/test_math16_qwen9b_aggressive_320_safety_benchmark_protocol_v1.py`
> - `tests/finals_rebuild/test_math16_qwen9b_aggressive_320_safety_benchmark_runner_v1.py`
> **HEAD_at_authoring:** `b04d8a166e9a3bfb31e3e2b6af31b96829b5b799`
> **origin/main_at_authoring:** `b04d8a166e9a3bfb31e3e2b6af31b96829b5b799`
> **this_round:** 只凍結 protocol／runner／preflight／tests；**不**正式執行 320 cells、**不**跑模型、**不**修改 frozen rules／Round 1／fixpoint／4B 產物／文件主表

---

## 1. Positioning

| Attribute | Binding |
|---|---|
| Model scope | **僅 Qwen 9B**（`qwen3.5:9b`／`model_group=qwen9b`） |
| Role | **`Aggressive Healer full 320-cell safety benchmark`**（post-hoc safety probe） |
| Relation to Round 1 | Round 1＝正式主分析（已封存）；本協議＝獨立全量 PASS／FAIL 安全基準規格 |
| Relation to 9B fixpoint | **不同協議**：fixpoint 僅掃 218 FAIL、排除 102 PASS；本協議 **320 全進** |
| Relation to 4B safety | **平行協議**：複用同一 transition／stack 判定；**不得**覆寫 4B 產物 |
| Relation to Method 2／Round 2 | **不同協議**；不是三模型 Round 2 正式覆寫 |
| Rule mutation | **禁止**新增規則、改 guard、改 threshold、改 order |

---

## 2. Input population（lock）

| Quantity | Value | Authority |
|---|---:|---|
| Total cells | **320** | C5c closure／three-model summary |
| Round 1 final PASS | **102** | frozen labels |
| Round 1 final FAIL | **218** | frozen labels |
| Identity | `102 + 218 = 320` | mandatory |
| Source stage | **C5c** | `c5c_final_source_*` only；**禁止** 4B D5／D2 overrides |

- **掃描／修改集合：** 全部 320 cells
- **禁止：** 依原始 PASS／FAIL 決定 eligibility／接受／回退／改規則

---

## 3. Fixed rule order（與 4B／9B fixpoint 相同）

```text
A → B → C1 → C2 → D3 → D1 → D5 → D2
```

每 cell **恰好一輪**（非 iterative fixpoint）。

---

## 4. Observational evaluator（唯一釘死）

與 9B fixpoint 相同：`math16_observational_evaluator_v1`
（`classify_math16_response` → `classify_outcome_to_v3` → `PASSED|FAILED` → `PASS|FAIL`）。

Preflight **不得**呼叫 evaluator。

---

## 5. Transitions（與 4B 相同）

| Transition | Definition |
|---|---|
| `preserved_pass` | PASS→PASS |
| `regression` | PASS→FAIL |
| `verified_rescue` | FAIL→PASS |
| `unchanged_fail` | FAIL→FAIL 且 source 未改 |
| `modified_still_failed` | FAIL→FAIL 且 source 已改 |

Rates：rescue／218；regression／102；preservation／102；modification／320；net＝rescue−regression。

---

## 6. Dual accounting（label／source mismatch）

若 frozen Round-1 label 與 sealed-source evaluator 重評不一致：

| Account | Rule |
|---|---|
| **Primary** | 使用 frozen labels（102／218）；寫入 `cell_journal.jsonl` |
| **Sealed-source sensitivity** | 分析 overlay only（`summary.sealed_source_sensitivity`）；**不得**覆寫 journal 原標籤 |

---

## 7. Non-goals（本協議輪）

1. 不正式執行 320-cell benchmark
2. 不呼叫模型
3. 不修改 Healer 規則／4B／Round 1 frozen artifacts
4. 不做 Gemini
5. 不覆寫 Final Report／Jury Q&A／總報告
