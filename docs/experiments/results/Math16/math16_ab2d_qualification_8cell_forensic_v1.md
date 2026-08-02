# Math16 Ab2d 8-cell qualification forensic v1

**Date:** 2026-08-02  
**HEAD:** `62172cac3642def11e4c0fdc4fd28eedd3fe4871` (`origin/main`)  
**Scope:** Read-only forensic of fairness-aligned dual qualification; **no LLM calls**, no prompt/API/evaluator/task edits, no re-run, no formal cells.  
**Namespaces:**
- `artifacts/math16_ab2d_full_plan_qualification_fairness_v1/`
- `artifacts/math16_ab2d_domain_menu_qualification_v1/`

**Note on failure count:** Qualification ledgers show **4** `answer_incorrect` cells (not 5). Analysis below covers all incorrect cells plus the 4 passes for contrast.

**Returned-value evidence method:** Fail `evaluation_result.json` / `execution_result.json` store `returned_value: null` (QFIX-001 assembly omits full payload on fail). Forensic recovered `correct_answer` by **local `generate()` replay** of frozen `extracted_source.py` (no model calls). Pass cells also replayed for ledger completeness.

---

## 1. EIGHT_CELL_LEDGER

| # | condition | domain | task_id | outcome | parse | exec runtime_error | returned `correct_answer` (replay) | evaluator expected schema (contract) | primary class |
|---|-----------|--------|---------|---------|-------|--------------------|--------------------------------------|--------------------------------------|---------------|
| 1 | ab2d_full | Polynomial | `ce115_calc_polynomial_division_l1` | **passed** | ok | null | `{quotient_coefficients:[6,24], remainder_coefficients:[102], quotient_latex, remainder_latex}` | object 4 keys (`math16_polynomial_division_general`) | OK |
| 2 | ab2d_full | Fraction | `ce113_q01_negative_fraction_subtraction` | **passed** | ok | null | `{numerator:19, denominator:28, canonical_latex:"\\frac{19}{28}"}` | object 3 keys (`exact_fraction_canonical`) | OK |
| 3 | ab2d_full | Radical | `ce112_q04_radical_simplification` | **answer_incorrect** | ok | null | `"3\\sqrt{15}"` (**str**) | `{coefficient, radicand, canonical_latex}` | **schema/field** |
| 4 | ab2d_full | Integer | `ce112_q09_divisor_multiple_intersection` | **passed** | ok | null | `{count: 6}` | `{count: int}` (`integer_count`) | OK |
| 5 | ab2d_domain_menu | Polynomial | `ce115_calc_polynomial_division_l1` | **passed** | ok | null | same 4-key object as #1 | same | OK |
| 6 | ab2d_domain_menu | Fraction | `ce113_q01_negative_fraction_subtraction` | **answer_incorrect** | ok | null | `"19/28"` (**str** via `to_exact`) | `{numerator, denominator, canonical_latex}` | **schema/field** (+ prompt ambiguity) |
| 7 | ab2d_domain_menu | Radical | `ce112_q04_radical_simplification` | **answer_incorrect** | ok | null | `"3\\sqrt{15}"` (**str**) | `{coefficient, radicand, canonical_latex}` | **schema/field** (+ prompt gap) |
| 8 | ab2d_domain_menu | Integer | `ce112_q09_divisor_multiple_intersection` | **answer_incorrect** | ok | null | `6` (**int**) | `{count: int}` | **schema/field** (+ prompt gap / misleading example) |

**Pipeline common facts (all 8):**
- `python_parse_ok: true`
- Domain Ops importable; referenced Ops match domain
- `runtime_error: null`
- Three top-level keys present on replay (`question_text`, `correct_answer`, `oracle_payload`); `oracle_payload` equals frozen params
- Fail artifact flags `three_key_output: false` are **assembly artifacts**, not true structural absence (replay contradicts them)

**Math equivalence (incorrect cells):** In all 4 fails, the **numeric / radical mathematical content matches** the expected semantics; only packaging differs.

---

## 2. FIVE_FAILURE_ROOT_CAUSES

*(Actual incorrect cells = **4**; labeled F1–F4.)*

### F1 — full / `ce112_q04_radical_simplification`

| Dimension | Finding |
|-----------|---------|
| Math value | Correct: `simplify_term(1,135) → (3,15)`; latex `3\sqrt{15}` |
| API choice / order / binding / unpacking | OK (`simplify_term` → `exact_integer` → `format_term`) |
| Schema / fields | **PRIMARY FAIL** — returned bare latex **str**, not dict |
| Exact serialization / type | type `str` ≠ required `dict` |
| LaTeX-only | Latex string itself is fine; failure is missing structural fields |
| Prompt insufficiency | **PARTIAL** — full has example dict + `Pack coefficient/radicand`, yet shared contract still only says “matching the task answer shape” |

**Source (excerpt):**
```python
canonical_latex = RadicalOps.format_term(coeff, rest)
"correct_answer": canonical_latex  # should pack coefficient/radicand + latex
```

**Classification:** `MODEL_CODE_ASSEMBLY_FAILURE` under ambient `PROMPT_CONTRACT_DEFECT` (vague shared contract; domain example is correct for this task but not elevated to normative per-task contract).

---

### F2 — menu / `ce113_q01_negative_fraction_subtraction`

| Dimension | Finding |
|-----------|---------|
| Math value | Correct: `19/28` |
| API | `create` + `sub` + `to_exact` — math OK; `create` vs `from_parts` not decisive |
| Schema | **PRIMARY** — `"19/28"` str vs `{numerator, denominator, canonical_latex}` |
| Prompt | **STRONG SECONDARY** — menu has **no** Processing steps; API cards repeatedly say `boundary: to_exact before correct_answer`, easily read as “answer = to_exact string”. Full steps say `Return numerator/denominator (+ optional to_latex)` and full **passed**. |

**Classification:** `PROMPT_CONTRACT_DEFECT` (missing task schema + misleading boundary language) → induced `MODEL_CODE_ASSEMBLY_FAILURE`.

---

### F3 — menu / `ce112_q04_radical_simplification`

Same packaging failure as F1 (`"3\\sqrt{15}"` str). Menu lacks Processing steps; relies on generic radical example (which *does* show the dict) + vague shared contract.

**Classification:** `PROMPT_CONTRACT_DEFECT` (no normative per-task contract) + `MODEL_CODE_ASSEMBLY_FAILURE`. Not math / API-order failure.

---

### F4 — menu / `ce112_q09_divisor_multiple_intersection`

| Dimension | Finding |
|-----------|---------|
| Math | Correct count `6` (valid set size) |
| API order | Same pattern as passing full cell: `positive_divisors` → `is_divisible` filter → length |
| Schema | **PRIMARY** — bare `int` `6` vs `{"count": 6}` |
| Prompt | **STRONG** — Integer domain example returns **bare** `chosen`; shared contract vague; full alone adds `Return {"count": len(valid)}.` and **passed** |

**Classification:** `PROMPT_CONTRACT_DEFECT` (missing `{count}` contract + misleading bare-int example) → `MODEL_CODE_ASSEMBLY_FAILURE`.

---

### Failure-category matrix

| Cell | math | API choice | API order | param bind | unpack | **schema/field** | exact type/ser | LaTeX-only | prompt insuff./ambiguity |
|------|------|------------|-----------|------------|--------|------------------|----------------|------------|--------------------------|
| F1 full radical | | | | | | **P** | type | | weak |
| F2 menu fraction | | | | | | **P** | type | | **strong** |
| F3 menu radical | | | | | | **P** | type | | medium |
| F4 menu count | | | | | | **P** | type | | **strong** |

No cell is explained by pure mathematical reasoning error on this seed.

---

## 3. ANSWER_SCHEMA_AUDIT (16 tasks × both conditions)

### 3.1 Prompt presence check

| Check | domain-menu | full-plan | old ab2d_spec |
|-------|-------------|-----------|---------------|
| Files | 16 | 16 | 16 |
| Byte-identical base (full = menu + `## Processing steps` only) | — | **16/16 True** | — |
| Per-task `correct_answer must …` schema sentence | **0/16** | **0/16** | **16/16** |
| Shared vague line `matching the task answer shape` | **16/16** | **16/16** | absent (replaced by explicit schema) |
| `math_answer_contracts.CONTRACTS` / `render_answer_contract` injected into prompt | **No** | **No** | Yes (inline opening paragraph + guardrails) |

**Verdict:** Neither menu nor full **explicitly** provides a per-task `correct_answer` contract covering bare vs object, required keys, value types, nested shape, exact serialization, optional/forbidden fields. Both only say:

> `correct_answer: JSON-compatible value matching the task answer shape.`

Evaluator SSOT remains off-prompt in `agent_tools/finals_rebuild/math_answer_contracts.py` + `math16_pool.py` `oracle_type` mapping.

### 3.2 Evaluator expected shapes (SSOT)

| task_id | oracle_type | expected `correct_answer` |
|---------|-------------|---------------------------|
| `ce115_calc_polynomial_division_l1` | `math16_polynomial_division_general` | object `{quotient_coefficients, remainder_coefficients, quotient_latex, remainder_latex}` |
| `ce115_calc_polynomial_factor_roots_l1` | `math16_polynomial_factor_roots` | object `{roots, factorization_latex, roots_latex}` |
| `ce115_calc_exact_rational_expression_l1` | `math16_exact_rational_expression` | object `{value: str, canonical_latex}` |
| `ce115_calc_radical_simplification_l1` | `math16_radical_simplification` | `{coefficient, radicand, canonical_latex}` |
| `ce111_q02_polynomial_division_remainder` | `polynomial_division_remainder_only` | `{remainder, canonical_latex}` (quotient not scored) |
| `ce111_q08_polynomial_factor_parameter_recovery` | `polynomial_factor_parameter_recovery` | **bare int** |
| `ce111_q03_prime_factor_selection` | `integer_exact` | **bare int** |
| `ce112_q01_negative_integer_power` | `integer_exact` | **bare int** |
| `ce112_q09_divisor_multiple_intersection` | `integer_count` | `{count: int}` |
| `ce111_nonchoice_q01_part1_exponential_growth` | `integer_exact_k` | `{k: int}` |
| `ce111_q05_exact_fraction_expression` | `exact_fraction_canonical` | `{numerator, denominator, canonical_latex}` |
| `ce113_q01_negative_fraction_subtraction` | `exact_fraction_canonical` | same |
| `ce112_q12_independent_probability_fraction` | `exact_fraction_canonical` | same |
| `ce112_q04_radical_simplification` | `radical_simplification_canonical` | `{coefficient, radicand, canonical_latex}` |
| `ce111_q10_ordered_quadratic_roots_radical` | `compound_radical_result` | nested `{result:{rational, radical_coefficient, radicand, canonical_latex}}` |
| `ce113_q11_rationalize_denominator` | `integer_exact` | **bare int** |

### 3.3 Domain generic examples vs evaluator (menu = full base)

| Domain example shape | Aligns with which tasks? | Misleads which tasks? |
|----------------------|--------------------------|------------------------|
| Poly: full div 4-key object | `ce115_calc_polynomial_division_l1` | remainder-only, factor-roots, parameter-recovery |
| Fraction: `{numerator, denominator, canonical_latex}` | three exact_fraction tasks | `ce115_calc_exact_rational_expression_l1` (`value` string contract) |
| Radical: `{coefficient, radicand, canonical_latex}` | two simplify tasks | `ce111_q10` nested result; `ce113_q11` bare int |
| Integer: bare `chosen` | bare-int integer tasks | **`ce112_q09` count**, **`ce111_nonchoice` k** |

### 3.4 Qualification cells vs contract

| Cell | Prompt task-schema explicit? | Domain example helpful? | Full steps schema leak? | Result |
|------|------------------------------|-------------------------|-------------------------|--------|
| full poly | no | yes | weak assemble | pass |
| full fraction | no | yes | **Return num/den** | pass |
| full radical | no | yes | Pack coeff/radicand | **fail** (assembly) |
| full count | no | **no** (bare) | **`{"count":…}`** | pass |
| menu poly | no | yes | — | pass |
| menu fraction | no | yes, but `to_exact` boundary competes | — | **fail** |
| menu radical | no | yes | — | **fail** |
| menu count | no | **actively wrong** | — | **fail** |

---

## 4. FULL_PLAN_SCHEMA_LEAKAGE_AUDIT

Builder claim (`math16_ab2d_full.py`): sole addition is `## Processing steps`. Empirically true at file-diff level (`full = menu + steps`).

**But steps embed answer-assembly schema**, not only API order:

| Severity | task_id | Leakage in `_steps_for_task` |
|----------|---------|------------------------------|
| **High** | `ce112_q09_divisor_multiple_intersection` | literal `Return {"count": len(valid)}.` |
| **High** | `ce111_nonchoice_q01_part1_exponential_growth` | `return {"k": k}` |
| **High** | `ce112_q01_negative_integer_power` | `Return bare int.` |
| **High** | `ce113_q11_rationalize_denominator` | `final bare answer` |
| Medium | fraction trio | `Return numerator/denominator (+ optional …to_latex)` |
| Medium | radical simplify ×2 | `Pack coefficient/radicand` |
| Medium | `ce111_q10` | `nested or flat result dict` |
| Medium | `ce115_calc_exact_rational_expression_l1` | `to_exact for value` |
| Weak | poly div / remainder / q08 | assemble / keep remainder / compute a+2c |

**Fairness implication:** Compared with domain-menu, full-plan is **not** “same prompt + solution steps only.” Steps restore fragments of the answer contract that menu lacks. Qualification pattern matches this asymmetry (menu fails 3/4; full fails 1/4; the three menu fails are exactly shapes steps would have clarified).

**Leakage ≠ complete fix:** Full radical still failed despite Pack instruction → schema leak helps but is incomplete / non-normative relative to old ab2d_spec opening contracts.

---

## 5. OLD_AB2D_SPEC_COMPARISON

Paths:
- `docs/experiments/prompts/ab2d_spec/prompts/` (and `_v2`)
- Guardrails under `docs/experiments/prompts/ab2d_spec/task_guardrails/`

Old Gemini Ab2d+spec 80/80 prompts included **task-specific output schema in the opening paragraph**, e.g.:

| task | ab2d_spec excerpt |
|------|-------------------|
| `ce112_q09` | `correct_answer must be a JSON-compatible dict with exactly count (int)` + guardrail `Use exactly the required count answer schema.` |
| `ce113_q01` | `correct_answer must include numerator, denominator, and canonical_latex` |
| `ce112_q04` | `correct_answer must include coefficient, radicand, and canonical_latex` |
| `ce115` poly div | `correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex` |
| `ce111_nonchoice` | `dict with exactly k (int)` |
| `ce113_q11` / bare ints | `correct_answer must be a single exact integer` |

**Currently missing from menu/full relative to ab2d_spec:**
1. Per-task output schema sentences (16/16)
2. Explicit answer assembly shape (object vs bare)
3. Guardrail “use exactly required X schema” lines
4. Unpacking / serialization directives that lived in guardrails (remainder-only, count schema, etc.)

Fairness fix aligned API menus and removed scaffolds, but **answer-contract text was not restored** into the shared base.

---

## 6. PROMPT_DEFECT_LIST

1. **Missing per-task `correct_answer` contract in both conditions** (shared vague “task answer shape”).  
   - Minimal fix: symmetrically inject `math_answer_contracts.CONTRACTS[oracle_type]` (or `render_answer_contract`) into **menu and full** base prompts.

2. **Misleading domain generic examples** for heterogeneous shapes within a domain (especially Integer bare `chosen` vs `{count}`/`{k}`; Poly full-div example vs remainder-only / factor-roots / bare int recovery; Radical flat vs nested / bare int).  
   - Minimal fix: mark examples non-normative **and** point to the injected contract; or split examples by answer shape.

3. **Fraction API boundary language** `to_exact before correct_answer` reads as final serialization.  
   - Minimal fix: reword to “JSON-safe adapter for Fraction values; final `correct_answer` must still match the task contract (often numerator/denominator/canonical_latex, not the raw to_exact string).”

4. **Full-plan Processing steps embed schema literals**, creating residual unfairness beyond “steps only.”  
   - Minimal fix after (1): strip literal `{"count"}` / `{"k"}` / “bare int” / “Pack …” assembly from steps; replace with “assemble `correct_answer` per Answer contract”; keep API call order only.

5. **Not defects (for this forensic):** evaluator contracts themselves; oracle math for these four tasks; transport/parse/exec pipeline completeness for qualification gate.

**Do not fix in this round** (per instructions).

---

## 7. Per-cell defect taxonomy (required distinction)

| Cell | Label |
|------|-------|
| F1 full radical | `MODEL_CODE_ASSEMBLY_FAILURE` (primary for this sample) under ambient `PROMPT_CONTRACT_DEFECT` |
| F2 menu fraction | `PROMPT_CONTRACT_DEFECT` → induced assembly failure |
| F3 menu radical | `PROMPT_CONTRACT_DEFECT` → induced assembly failure |
| F4 menu count | `PROMPT_CONTRACT_DEFECT` → induced assembly failure |
| All 4 passes | N/A |
| Single-seed caveat | Do **not** treat these fails as model capability boundary; none is pure `MODEL_REASONING_FAILURE` on this evidence |
| Evaluator/pipeline | Outcomes are real schema mismatches. Null `returned_value` on fail is an **evidence packaging** issue (`EVALUATOR_OR_PIPELINE_DEFECT` for forensics only), **not** the cause of `answer_incorrect` |

---

## 8. FORMAL_READINESS

**NOT READY for formal 80-cell runs** under either condition until:

1. Symmetric per-task answer contracts restored into menu+full freezes  
2. Processing-steps schema leakage neutralized (or accepted as intentional and fairness review rewritten — currently conflicts with “steps-only delta” claim)  
3. Prompt freeze rebuilt; **both** 4-cell qualifications re-run with new freezes  
4. No formal generation before that re-qualification gate

Qualification pipelines themselves completed (gate passed previously); readiness blocker is **prompt contract fairness / completeness**, not transport bugs.

---

## 9. Evidence index

| Item | Path |
|------|------|
| Full qual summary | `artifacts/math16_ab2d_full_plan_qualification_fairness_v1/qualification_summary.json` |
| Menu qual summary | `artifacts/math16_ab2d_domain_menu_qualification_v1/qualification_summary.json` |
| Rendered prompts | `docs/experiments/prompts/ab2d_{full,domain_menu}/prompts/*.txt` |
| Full steps source | `agent_tools/finals_rebuild/math16_ab2d_full.py` (`_steps_for_task`) |
| Menu shared contract | `agent_tools/finals_rebuild/math16_ab2d_domain_menu.py` (`SHARED_OUTPUT_CONTRACT`) |
| Evaluator contracts | `agent_tools/finals_rebuild/math_answer_contracts.py` |
| Old spec prompts | `docs/experiments/prompts/ab2d_spec/prompts/*.txt` |

---

## 10. FINAL_VERDICT

**`PROMPT_CONTRACT_DEFECT_FOUND`**

Rationale: All incorrect qualification cells fail on `correct_answer` packaging while mathematical content is correct. Both current conditions omit the per-task answer schemas that Ab2d+spec carried; domain examples and Fraction `to_exact` boundaries actively mislead; full-plan Processing steps partially reintroduce schema only for one side. Formal readiness is blocked pending a symmetric contract fix and re-qualification — **no code/prompt changes in this round**.
