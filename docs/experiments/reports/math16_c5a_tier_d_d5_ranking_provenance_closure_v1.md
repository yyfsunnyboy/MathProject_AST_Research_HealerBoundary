# Math16 D5 Ranking Provenance Closure v1

> **verdict:** `SPEC_DRIVEN_ELIGIBILITY_CHANGE`
> **census_implementation_inconsistency:** `false`
> **authority:** C5a census = frozen-spec authoritative；舊 C4 Tier D supply D5 = pre-freeze exploratory
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **parent_c5a_supply:** `docs/experiments/manifests/math16_c5a_tier_d_d5_d2_residual_supply_v1.json`
> **parent_old_supply:** `docs/experiments/manifests/math16_c4_c5_tier_d_supply_v1.json`

---

## 1. Scope

舊 C4 Tier D supply 將 D5 標為 `RANKED_ELIGIBLE` **4** 格；C5a residual supply 在凍結 §5 ranking 下僅 **1** 格 `D5_RANKED_ELIGIBLE`。本文件逐格閉合差異根因。

候選集合（舊 4 格）：

1. `…ce111_q05_exact_fraction_expression__ab2d_spec_v2__seed_2026072001`
2. `…ce111_q05_exact_fraction_expression__ab2d_spec_v2__seed_2026072002`
3. `…ce111_q05_exact_fraction_expression__ab2d_spec_v2__seed_2026072004`
4. `…ce113_q11_rationalize_denominator__ab2d__seed_2026072003`

---

## 2. Per-cell provenance

| Cell | C4 SHA == C5a SHA? | Old status | C5a status | Cause |
|---|---|---|---|---|
| q05…2001 | **Yes** (`59606ce4…`) | RANKED_ELIGIBLE (site-only) | D5_AMBIGUOUS_ABSTAIN (`similarity_sole_decision_or_tie_without_similarity`) | Spec gates |
| q05…2002 | **Yes** (`8e924c24…`) | RANKED_ELIGIBLE (site-only) | D5_AMBIGUOUS_ABSTAIN (same) | Spec gates |
| q05…2004 | **Yes** (`f838ff92…`) | RANKED_ELIGIBLE (site-only) | D5_AMBIGUOUS_ABSTAIN (same) | Spec gates |
| q11…2003 | **Yes** (`add4133b…`) | RANKED_ELIGIBLE (site-only) | D5_RANKED_ELIGIBLE (winner=`create`, score=18.4, runner-up=15.0, margin≈3.4) | Spec gates pass |

### Ranking contract applied on C5a (frozen)

| Parameter | Value |
|---|---|
| Weights | §5 provisional (`F_prompt_contract_token`=5 … `F_method_name_similarity`=1) |
| minimum_score | 8 |
| minimum_margin | 2 |
| Tie | abstain |
| Similarity sole-decision ban | ON |

### Old C4 census behavior (pre-freeze exploratory)

- Eligibility =「唯一 wrong method site 且 exposed candidates ≥2」
- **未**計算 feature scores、**未**套 minimum_score／margin／tie／similarity ban
- 故 4 格皆標 `RANKED_ELIGIBLE`

### q05 三格 abstain 細節（SHA 不變 → 非 source-driven）

- Candidates 分數例：`create≈22.22`、`from_parts=22.0`、`add=19`、`sub=19`
- 去掉 similarity 後 `create` 與 `from_parts` **並列 22.0** → similarity sole-decision／tie-without-similarity → **abstain**
- 符合凍結規格，**不是** C5a source 變更

---

## 3. Cause codes

| Code | Result |
|---|---|
| `SOURCE_DRIVEN_ELIGIBILITY_CHANGE` | **駁回**（四格 C4／C5a SHA 全等；皆 `C4_PRESERVED`） |
| `SPEC_DRIVEN_ELIGIBILITY_CHANGE` | **成立** |
| `CENSUS_IMPLEMENTATION_INCONSISTENCY` | **否**（舊 census 明確為 site-only exploratory；C5a 為 §5 authoritative） |
| `MIXED_CAUSE` | **否** |

---

## 4. Authority statement

> 舊 `math16_c4_c5_tier_d_supply_v1` 之 D5=4 為 **pre-freeze exploratory**（未套 §5 數值門檻）。  
> `math16_c5a_tier_d_d5_d2_residual_supply_v1` 之 D5=1 為 **frozen-spec authoritative**。  
> D5 Development replay **只**以 C5a 的 1 格 eligible 為準。

---

## 5. Gate to implementation

- Provenance verdict = `SPEC_DRIVEN_ELIGIBILITY_CHANGE`
- No census implementation inconsistency → **允許**繼續 D5／D2 最小實作與各 1 格 Development replay

## Declarations

- Read-only provenance；未改 C0–C5a frozen 結果
- 未呼叫模型；未執行 evaluator 作 ranking
