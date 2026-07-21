# Qwen 4B Ab2d+api Anomaly Diagnosis v1

```text
QWEN4B_AB2D_API_ANOMALY_DIAGNOSED
PARSER_VS_LOGIC_ROOT_CAUSE_CLASSIFIED
QWEN4B_AB2D_API_ANOMALY_DIAGNOSIS_FROZEN
```

**Policy:** diagnosis only — no evaluator/prompt/raw changes, no rescoring, 0 model calls. Does **not** overwrite baseline scores, re-judge cells, or rescore.

## 0. Freeze metadata

| Field | Value |
| :--- | :--- |
| Diagnosis id | `math16_pilot02_qwen4b_ab2d_api_anomaly_diagnosis_v1` |
| Baseline evaluation | `math16_pilot02_qwen4b_evaluation_v4_r001` |
| Source scoring commit | `9bfbd30bdc965c5f26003043606ca02d8096314c` |
| Corpus SHA closure | `7dd3ba5f7e7a38e7ad20142e8c5c5b2e84c20df1b7f5abcf5701c23d24172a22` |
| Evaluator hash | `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc` |
| Taxonomy hash | `7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304` |
| MD path | `docs/experiments/audits/math16_pilot02_qwen4b_ab2d_api_anomaly_diagnosis_v1.md` |
| JSON path | `docs/experiments/audits/math16_pilot02_qwen4b_ab2d_api_anomaly_diagnosis_v1.json` |
| MD SHA-256 | `a308f73daebf72ee2574fc474fdf22fe3e4305c25d37f6705ffd97e3ba348c6c` |
| JSON SHA-256 | `b82f4f99881a5cb220d1a1b248c07865fccd34fcb6ffc8d6afcbdd4739135393` |
| llm_calls | `0` |
| rescored | `false` |
| ab3 / healer | `false` / `false` |

Note: **MD SHA-256** is `freeze.md_body_sha256` (Markdown body with the MD/JSON SHA rows omitted). **JSON SHA-256** is the full companion JSON file digest. Stable content digest without hash fields: `freeze.json_content_sha256`.

## 0b. Scope

- Condition: `ab2d` (Ab2d+api)
- Filter: `primary_failure_layer ∈ {L1,L2,L3}` **or** `format_contamination` in tags
- Subset size: **27** / 72 Ab2d fails (remaining fails are mostly L4/L5, out of this filter)
- Ab2d overall: **8/80** pass

## 1. Per-cell table (full subset)

| task | seed | layer | tags | outcome | exc | parse step | root cause | structure notes |
| :--- | ---: | :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| `ce111_q05_exact_fraction_expression` | 2026072004 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `invalid syntax (<unknown>, line 7)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce111_q08_polynomial_factor_parameter_recovery` | 2026072002 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `expected an indented block after 'else' statement on line 15` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce111_q08_polynomial_factor_parameter_recovery` | 2026072004 | L2 | `ambiguous_entry_point` | `missing_entry_point` | — | G3_contract/schema_or_entry | **PARSER_UNFRIENDLY** | no fence; extract=extracted/plain_text |
| `ce111_q10_ordered_quadratic_roots_radical` | 2026072001 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `invalid syntax (<unknown>, line 33)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce112_q04_radical_simplification` | 2026072001 | L2 | `output_packaging,schema_mismatch` | `schema_failure` | — | G3_contract/schema_or_entry | **PARSER_UNFRIENDLY** | no fence; extract=extracted/plain_text |
| `ce112_q04_radical_simplification` | 2026072003 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `expected an indented block after 'if' statement on line 24 (` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce112_q04_radical_simplification` | 2026072004 | L3 | `invalid_api_call` | `runtime_failure` | NameError: `NameError: name 'MinimalRadicalOps' is not defined` | G2_exec_domain_api | **TRUE_LOGIC_ERROR** | no fence; extract=extracted/plain_text |
| `ce112_q09_divisor_multiple_intersection` | 2026072003 | L1 | `candidate_extraction_failure,truncation` | `catastrophic_truncation` | — | G1_parse/extract | **PARSER_UNFRIENDLY** | python_fence; trunc?; extract=extracted/plain_text |
| `ce112_q09_divisor_multiple_intersection` | 2026072004 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unterminated triple-quoted string literal (detected at line ` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce112_q12_independent_probability_fraction` | 2026072001 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unmatched '}' (<unknown>, line 45)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce112_q12_independent_probability_fraction` | 2026072002 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unmatched '}' (<unknown>, line 46)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce112_q12_independent_probability_fraction` | 2026072004 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `closing parenthesis '}' does not match opening parenthesis '` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce113_q11_rationalize_denominator` | 2026072001 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `invalid syntax (<unknown>, line 147)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce113_q11_rationalize_denominator` | 2026072002 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `invalid syntax (<unknown>, line 494)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce115_calc_exact_rational_expression_l1` | 2026071301 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unmatched '}' (<unknown>, line 26)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce115_calc_exact_rational_expression_l1` | 2026072001 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unmatched '}' (<unknown>, line 32)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce115_calc_exact_rational_expression_l1` | 2026072003 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unmatched '}' (<unknown>, line 33)` | G1_parse/extract | **OTHER** | python_fence; extract=extracted/fenced_python |
| `ce115_calc_exact_rational_expression_l1` | 2026072004 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unmatched '}' (<unknown>, line 23)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce115_calc_polynomial_division_l1` | 2026071301 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unterminated string literal (detected at line 24) (<unknown>` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce115_calc_polynomial_factor_roots_l1` | 2026071301 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `expected 'else' after 'if' expression (<unknown>, line 45)` | G1_parse/extract | **OTHER** | python_fence; extract=extracted/fenced_python |
| `ce115_calc_polynomial_factor_roots_l1` | 2026072001 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unexpected character after line continuation character (<unk` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce115_calc_polynomial_factor_roots_l1` | 2026072002 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `expected an indented block after 'else' statement on line 28` | G1_parse/extract | **OTHER** | python_fence; extract=extracted/fenced_python |
| `ce115_calc_polynomial_factor_roots_l1` | 2026072003 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `unmatched '}' (<unknown>, line 176)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce115_calc_polynomial_factor_roots_l1` | 2026072004 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `'{' was never closed (<unknown>, line 102)` | G1_parse/extract | **OTHER** | python_fence; extract=extracted/fenced_python |
| `ce115_calc_radical_simplification_l1` | 2026071301 | L2 | `output_packaging,schema_mismatch` | `schema_failure` | — | G3_contract/schema_or_entry | **PARSER_UNFRIENDLY** | no fence; extract=extracted/plain_text |
| `ce115_calc_radical_simplification_l1` | 2026072001 | L1 | `format_contamination` | `parse_minor` | SyntaxError: `f-string: single '}' is not allowed (<unknown>, line 14)` | G1_parse/extract | **OTHER** | no fence; extract=extracted/plain_text |
| `ce115_calc_radical_simplification_l1` | 2026072002 | L2 | `output_packaging,schema_mismatch` | `schema_failure` | — | G3_contract/schema_or_entry | **PARSER_UNFRIENDLY** | no fence; extract=extracted/plain_text |

## 2. Root-cause summary

| Label | N | Share |
| :--- | ---: | ---: |
| PARSER_UNFRIENDLY | 5 | 18.5% |
| TRUE_LOGIC_ERROR | 1 | 3.7% |
| OTHER | 21 | 77.8% |

**Interpretation:** Most taxonomy `format_contamination` tags in this subset are **SyntaxError inside an already-extracted candidate** (OTHER), not outer prose/markdown wrapping. PARSER_UNFRIENDLY packaging is **5/27** — **not the primary cause**. Widening a prose-tolerant parser is **not recommended** from this evidence alone.

### Pollution / format patterns (counts overlap)

| Pattern | Count |
| :--- | ---: |
| `parse_minor_syntax_in_extracted` | 21 |
| `schema_packaging` | 3 |
| `catastrophic_truncation` | 1 |
| `odd_fence_or_ellipsis_truncation` | 1 |

**PARSER_UNFRIENDLY share = 18.5%** (<20%)

## 3. Gemini Ab2d+api contrast (v4_r001)

Gemini Ab2d+api: **78/80**. The only 2 failures:

| task | seed | layer | tags | outcome |
| :--- | ---: | :---: | :--- | :--- |
| `ce113_q11_rationalize_denominator` | 2026072001 | L5 | `['algorithmic_error']` | `answer_incorrect` |
| `ce113_q11_rationalize_denominator` | 2026072003 | L5 | `['algorithmic_error']` | `answer_incorrect` |

**Conclusion:** Gemini’s 2 Ab2d misses are both **L5 algorithmic_error** (true answer errors after successful parse/exec). Qwen’s filtered 27-cell cluster is **not** the same failure layer: dominated by **G1 SyntaxError-in-candidate** (OTHER), plus a smaller packaging cluster (PARSER_UNFRIENDLY). This supports a **generation-quality / malformed-Python** hypothesis for most of the L1 mass — **not** the same L5 capability-gap pattern as Gemini, and **not** primarily a Gemini-tuned parser intolerance story.

Note: Qwen Ab2d still has many **L4/L5** fails outside this filter (45 cells); those are separate capability/execution issues and are **not** counted as PARSER_UNFRIENDLY here.

## 4. Governance implication (diagnosis only)

1. PARSER_UNFRIENDLY share is modest (<20%); widening prose-tolerant extraction is **unlikely** to recover most of this Ab2d L1 mass. Prefer tracking **emitted-Python SyntaxError** as a model-side generation defect. Packaging (schema/entry/truncation) may still deserve a separate audit.
2. This diagnosis **must not** modify evaluator, prompts, or raw; **must not** overwrite baseline; **must not** re-judge or rescore.
3. Model calls: **0**. Ab3 / Healer: **not run**.

## 5. Verdict

```text
QWEN4B_AB2D_API_ANOMALY_DIAGNOSED
PARSER_VS_LOGIC_ROOT_CAUSE_CLASSIFIED
QWEN4B_AB2D_API_ANOMALY_DIAGNOSIS_FROZEN
QWEN4B_PARSER_VS_LOGIC_EVIDENCE_VERIFIED
```
