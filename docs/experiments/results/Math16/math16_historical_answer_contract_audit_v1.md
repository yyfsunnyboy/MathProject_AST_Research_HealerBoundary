# Math16 Historical Answer Contract Audit v1

**Date:** 2026-08-02  
**HEAD:** `62172cac3642def11e4c0fdc4fd28eedd3fe4871` (`main`)  
**Mode:** Read-only; no LLM calls; no re-runs; no prompt/artifact edits; no commit/push.  
**Working tree at start:** only prior forensic file untracked (`math16_ab2d_qualification_8cell_forensic_v1.md`) — allowed.

**Question:** Did formal Ab1 / Ab2g / old Ab2d actually inject per-task answer contracts into rendered prompts, and were historical FAILs contaminated by contract absence?

**Authority rule:** Only runner-consumed rendered prompts (cell `prompt.txt`), manifests/freezes, and existing evaluation/raw artifacts. Design docs alone are insufficient.

---

## 1. FORMAL_SOURCE_CHAIN

### 1.1 Shared builder path (Ab1 / Ab2g / old Ab2d)

| Layer | Path / evidence |
|-------|-----------------|
| Runners (Gemini Pilot-02) | `scripts/run_math16_pilot02_integer_generation.py`, `scripts/run_math16_pilot02_full_generation.py` |
| Runners (Qwen) | `scripts/run_math16_pilot02_qwen4b_generation.py`, `scripts/run_math16_pilot02_qwen9b_generation.py` |
| Condition builder | `agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py` → `build_condition_prompt` |
| Ab1 base (injects contracts) | `agent_tools/finals_rebuild/math_boundary_pilot.py` → `build_ab1_prompt` (oracle_type → `correct_answer must …`) |
| Ab2g | Ab1 base + `## Clean-incremental GENERIC` |
| Old formal Ab2d (`ab2d` / Ab2d+api) | Ab2g + `## Clean-incremental DOMAIN` (task-local Domain API) |
| Pool freeze | `frozen_for_prompt` / `math16_pool.py` |
| Manifest prompt_sources | `docs/experiments/manifests/math16_pilot02_integer_runtime_manifest.json` |

Manifest quote:

```json
"prompt_sources": {
  "ab1": "runtime-built via build_condition_prompt() from ce115_clean_incremental_ablation.py",
  "ab2g": "runtime-built via build_condition_prompt() from ce115_clean_incremental_ablation.py",
  "ab2d": "runtime-built via build_condition_prompt() from ce115_clean_incremental_ablation.py",
  "ab2d_spec": "static txt files under docs/experiments/prompts/ab2d_spec/prompts/"
}
```

**Standalone `docs/experiments/prompts/ab1|ab2g|ab2d/*.txt`:** absent. Formal rendered authority = **per-cell `prompt.txt`** under Pilot-02 result trees (plus compiled `docs/experiments/prompts/math16/math16_ab{1,2g,2d}_prompts.md` as secondary ledger).

### 1.2 Ab2d+spec (control)

| Variant | Formal use | Rendered source |
|---------|------------|-----------------|
| `ab2d_spec` (v1) | Gemini Pilot-02 80 cells | `docs/experiments/prompts/ab2d_spec/prompts/*.txt` + `manifest.json` |
| `ab2d_spec_v2` | Qwen4B/9B fourth condition | `docs/experiments/prompts/ab2d_spec_v2/prompts/*.txt` |

Gemini runners read static v1 `.txt` when `cond == "ab2d_spec"`. Spot-check: freeze file SHA == cell `prompt.txt` SHA for `ce112_q09` seed `2026071301`.

### 1.3 Formal artifact roots used

| Model | Generation cells | Evaluation baseline |
|-------|------------------|---------------------|
| Gemini 3.5 Flash | `math16_pilot02_integer_gemini` (80) + `math16_pilot02_full_gemini` (240) = 320 | `math16_pilot02_full_evaluation_v4_r001/cell_level_baseline.jsonl` (320) |
| Qwen3.5 4B | `math16_pilot02_qwen4b` | `math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl` |
| Qwen3.5 9B | `math16_pilot02_qwen9b` | `math16_pilot02_qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl` |

Cell naming: `{model}__{task_id}__{condition}__seed_{seed}` with files `prompt.txt`, `raw_response.txt`, `artifact.json`.

**Out of scope (not old formal Ab2d):** `ab2d_full`, `ab2d_domain_menu` (recent fairness line; contracts missing there — separate forensic).

---

## 2. CONDITION_SUMMARY

Audit unit: primary formal seed `2026071301` cell `prompt.txt` for each of 16 tasks × 4 conditions (Gemini trees). Classification against checklist: bare/object, required keys, value-type hints, nested shape, serialization, optional/forbidden when applicable.

| Condition | COMPLETE_CONTRACT | PARTIAL_OR_AMBIGUOUS | CONTRACT_MISSING | FORMAL_SOURCE_UNRESOLVED |
|-----------|-------------------:|---------------------:|-----------------:|-------------------------:|
| Ab1 | **16** | 0 | 0 | 0 |
| Ab2g | **16** | 0 | 0 | 0 |
| Old Ab2d (`ab2d`) | **16** | 0 | 0 | 0 |
| Ab2d+spec (`ab2d_spec`) | **16** | 0 | 0 | 0 |

**Additional checks:**
- Ab1 vs Ab2d+spec **answer-contract sentence**: **16/16 identical** on seed `2026071301` (same `correct_answer must …` clause; conditions differ only by GENERIC/DOMAIN/spec scaffolding).
- Qwen Ab1 cell prompts (sample + all `OUTPUT_SCHEMA_MISMATCH` fails): still contain `correct_answer must …`.
- Contracts are injected in **Ab1 base** (`math_boundary_pilot.build_ab1_prompt`); Ab2g/Ab2d inherit them automatically.

**Residual prose limits (not downgraded to PARTIAL):** some tasks state types in prose (“irreducible fraction”, “single exact integer”) rather than full JSON Schema; optional/forbidden fields appear mainly where needed (remainder-only, compound ±1, factor-order). Shape + keys + bare/object are explicit for all 16.

---

## 3. TASK_BY_TASK_CONTRACT_AUDIT

Legend: **C** = COMPLETE_CONTRACT. Evidence = Gemini seed `2026071301` `prompt.txt`.

| task_id | oracle_type (pool) | Contract shape in rendered prompt | Ab1 | Ab2g | Ab2d | Ab2d+spec |
|---------|--------------------|-----------------------------------|-----|------|------|-----------|
| `ce115_calc_polynomial_division_l1` | `math16_polynomial_division_general` | object: quotient_coefficients, remainder_coefficients, quotient_latex, remainder_latex; Exact arithmetic; no floats | C | C | C | C |
| `ce115_calc_polynomial_factor_roots_l1` | `math16_polynomial_factor_roots` | object: roots (ascending), factorization_latex, roots_latex | C | C | C | C |
| `ce115_calc_exact_rational_expression_l1` | `math16_exact_rational_expression` | object: value (irreducible p/q string), canonical_latex | C | C | C | C |
| `ce115_calc_radical_simplification_l1` | `math16_radical_simplification` | object: coefficient, radicand, canonical_latex; Exact integers | C | C | C | C |
| `ce111_q02_polynomial_division_remainder` | `polynomial_division_remainder_only` | object: **only** remainder + canonical_latex (quotient not scored) | C | C | C | C |
| `ce111_q08_polynomial_factor_parameter_recovery` | `polynomial_factor_parameter_recovery` | **bare int** `a+2c`; forbidden redefine-after-swap | C | C | C | C |
| `ce111_q03_prime_factor_selection` | `integer_exact` | **bare** single exact integer | C | C | C | C |
| `ce112_q01_negative_integer_power` | `integer_exact` | **bare** single exact integer | C | C | C | C |
| `ce112_q09_divisor_multiple_intersection` | `integer_count` | object: exactly `count` (int) | C | C | C | C |
| `ce111_nonchoice_q01_part1_exponential_growth` | `integer_exact_k` | object: exactly `k` (int) | C | C | C | C |
| `ce111_q05_exact_fraction_expression` | `exact_fraction_canonical` | object: numerator, denominator, canonical_latex | C | C | C | C |
| `ce113_q01_negative_fraction_subtraction` | `exact_fraction_canonical` | same | C | C | C | C |
| `ce112_q12_independent_probability_fraction` | `exact_fraction_canonical` | same | C | C | C | C |
| `ce112_q04_radical_simplification` | `radical_simplification_canonical` | object: coefficient, radicand, canonical_latex | C | C | C | C |
| `ce111_q10_ordered_quadratic_roots_radical` | `compound_radical_result` | nested **result** with rational, radical_coefficient (±1), radicand, canonical_latex; structured comparison | C | C | C | C |
| `ce113_q11_rationalize_denominator` | `integer_exact` | **bare** single exact integer | C | C | C | C |

**Example rendered Ab1 opening (poly div):**

> `correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex. Exact arithmetic; no floats.`

**Example rendered Ab1 count task:**

> `correct_answer must be a JSON-compatible dict with exactly count (int).`

---

## 4. FAIL_CELL_RECLASSIFICATION

### 4.1 Gemini Pilot-02 — Ab1 / Ab2g / Ab2d (14 FAILED)

Source: `math16_pilot02_full_evaluation_v4_r001/cell_level_baseline.jsonl`.

| Reclass | Count | Meaning |
|---------|------:|---------|
| Math value wrong; schema OK; contract present | **11** | `g3s_output_schema=PASS`, `g4_correctness=FAIL`, tag `algorithmic_error` |
| Parse/format contamination | **3** | `PARSE_ERROR` / L1; schema not assessed |
| Schema fail with missing contract | **0** | — |
| Prompt contract absence → false FAIL | **0** | — |

**Per-condition:**

| Condition | FAILED | Math+schemaOK | Parse | g3s FAIL |
|-----------|-------:|--------------:|------:|---------:|
| Ab1 | 8 | 5 | 3 | 0 |
| Ab2g | 4 | 4 | 0 | 0 |
| Ab2d | 2 | 2 | 0 | 0 |

**Fail cell list (Gemini Ab1/Ab2g/Ab2d):**

| cell_id | Reclass |
|---------|---------|
| `…ce111_q08…__ab1__seed_2026071301` | Math wrong / schema OK / contract present (`correct_answer must be the integer a+2c`) |
| `…ce111_q08…__ab1__seed_2026072002` | same |
| `…ce111_q08…__ab1__seed_2026072004` | same |
| `…ce113_q11…__ab1__seed_2026071301` | Math wrong / schema OK / contract present (replay `correct_answer=11` int; wrong value) |
| `…ce113_q11…__ab1__seed_2026072001` | Parse/format (SyntaxError in raw) |
| `…ce113_q11…__ab1__seed_2026072002` | Math wrong / schema OK |
| `…ce113_q11…__ab1__seed_2026072003` | Parse/format |
| `…ce113_q11…__ab1__seed_2026072004` | Parse/format |
| `…ce111_q08…__ab2g__seed_2026071301` | Math wrong / schema OK |
| `…ce113_q11…__ab2g__seed_2026071301` | Math wrong / schema OK |
| `…ce113_q11…__ab2g__seed_2026072003` | Math wrong / schema OK |
| `…ce113_q11…__ab2g__seed_2026072004` | Math wrong / schema OK |
| `…ce113_q11…__ab2d__seed_2026072001` | Math wrong / schema OK (contract present; Domain API used) |
| `…ce113_q11…__ab2d__seed_2026072003` | Math wrong / schema OK |

Spot-check: Ab1 `ce113_q11` seed `2026071301` raw replays to bare `int` 11 — packaging matches contract; evaluator marks correctness fail → **not** a contract-gap false FAIL.

### 4.2 Gemini Ab2d+spec (17 FAILED) — control context

All 17: `DOMAIN_API_CALL_ERROR` (L3); `g3s` PASS; prompts still contain full contracts. **Not** contract-absence failures.

### 4.3 Qwen — Ab1 / Ab2g / Ab2d schema mismatches

| Model | `OUTPUT_SCHEMA_MISMATCH` on ab1/ab2g/ab2d | Prompts with `correct_answer must` |
|-------|------------------------------------------:|-----------------------------------:|
| Qwen4B | 15 | **15/15** |
| Qwen9B | 4 | **4/4** |

**Reclass:** model received complete contract but did not assemble required shape → **not** “Prompt contract 缺失可能造成假 FAIL”.

Large Qwen L5 `CORRECTNESS_FAIL` / L1 `PARSE_ERROR` / L4 runtime counts are likewise **not** attributable to missing answer contracts on these conditions.

---

## 5. POTENTIALLY_AFFECTED_RESULTS

| Claim | Result |
|-------|--------|
| Historical Ab1/Ab2g/Ab2d FAILs caused by missing answer contract | **None identified** |
| Cells where contract absence could create false FAIL | **Empty set** for formal Pilot-02 Ab1/Ab2g/Ab2d |
| Contrast (out of scope, prior forensic) | Recent `ab2d_domain_menu` / fairness `ab2d_full` **lack** per-task contracts → those qualification schema fails are a **different** lineage defect |

---

## 6. AB2D_SPEC_CONTROL_CHECK

| Check | Result |
|-------|--------|
| 16/16 freeze prompts contain `correct_answer must …` | **Yes** (reconfirmed on Gemini cell prompts + freeze dir) |
| Gemini cell `prompt.txt` matches freeze SHA (spot `ce112_q09`) | **Yes** |
| Contract sentences vs Ab1 base | **Identical** for all 16 tasks (seed `2026071301`) |
| Prior conclusion “Ab2d+spec has complete contracts” | **Unchanged; not re-litigated** |

Ab2d+spec adds scaffolds/guardrails/API cards; the **answer-contract clause itself is shared with Ab1**.

---

## 7. EVIDENCE_GAPS

| Gap | Impact |
|-----|--------|
| No standalone frozen `.txt` dirs for Ab1/Ab2g/Ab2d | Mitigated: formal cell `prompt.txt` + runtime builder path are authoritative |
| Generation cells omit durable `extracted_source.py` | Mitigated for Gemini fails via `raw_response.txt` + selective local replay; Qwen schema-mismatch reclass uses evaluation subtype + prompt presence, not full CA replay for all cells |
| Qwen eval rows often have `g3s_output_schema=null` | Relied on `failure_subtype` / layers; does not overturn prompt-side contract presence |
| Not every Qwen FAIL raw replayed for math-vs-packaging | Unnecessary for contract-absence claim once prompts show COMPLETE_CONTRACT |
| LaTeX-v1 48-cell earlier freeze hashes may differ from Pilot-02 | This audit’s formal scope = Pilot-02 80×conditions; older latex freeze not used as prompt authority |

---

## 8. Statistics rollup

| Metric | Value |
|--------|------:|
| Conditions audited | 4 (Ab1, Ab2g, Ab2d, Ab2d+spec) |
| Tasks × conditions with COMPLETE_CONTRACT | **64 / 64** |
| Gemini Ab1/Ab2g/Ab2d FAILs potentially from missing contract | **0 / 14** |
| Qwen schema-mismatch cells with contract still in prompt | **19 / 19** |

---

## 9. FINAL_VERDICT

**`HISTORICAL_CONTRACTS_COMPLETE`**

Formal Ab1, Ab2g, and old Ab2d **did** inject per-task answer contracts into runner-rendered prompts (via Ab1 base `build_ab1_prompt`), matching Ab2d+spec’s contract clauses. Existing Pilot-02 FAILs on these conditions are parse/API/math failures (or Qwen non-compliance despite a present contract), **not** false FAILs from contract omission.

---

## REVIEW_DOCUMENT_PATH

`docs/experiments/results/Math16/math16_historical_answer_contract_audit_v1.md`
