# Math16 Pilot-02 Oracle Schema Audit v1 (Pre-Fix Baseline)

```text
ORACLE_SCHEMA_AUDIT_V1_PRE_FIX
```

**Status:** frozen pre-fix diagnostic snapshot  
**Purpose:** Evidence baseline for subsequent evaluator / normalize fixes.  
**Immutability rule:** This V1 document MUST NOT be edited or overwritten after freeze. Later work must add a new version (e.g. `V2_POST_FIX`) for comparison.

---

## 0. Freeze metadata

| Field | Value |
|---|---|
| Audit id | `math16_pilot02_oracle_schema_audit_v1` |
| Freeze label | `ORACLE_SCHEMA_AUDIT_V1_PRE_FIX` |
| Document path | `docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md` |
| Companion manifest | `docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1_manifest.json` |
| Baseline evaluation revision | `math16_pilot02_full_evaluation_v3_r001` |
| Baseline evaluation commit (source HEAD at freeze) | `5961ef52c2b1d51a7cfb97fb7095f48d38d66acc` |
| Baseline report verdict | `MATH16_320_BLINDED_V3_EVALUATION_COMPLETE` |
| Published baseline overall | **265/320** (82.8125%) |
| Corrected estimate (informal) | **289/320** (90.3%) — **estimate only; not a formal re-score** |
| Taxonomy SSOT SHA-256 | `7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304` |
| Oracle implementation reviewed | `agent_tools/finals_rebuild/math16_oracles.py` (+ dispatch via `math_task_oracles.evaluate_math_task_oracle`) |
| G3 gate behavior reviewed | `scripts/run_math16_latex_v1_gemini_live.classify_math16_response` (top-level keys only) |

Document SHA-256 is recorded in the companion manifest after this file is written (hash of this Markdown file bytes).

---

## 1. Audit objective

Detect tasks where the model produces a **mathematically correct** answer that the oracle / schema path **false-negatives** because:

1. G3 only checks top-level `{question_text, correct_answer, oracle_payload}` and does not validate `correct_answer` internal shape; and/or  
2. The oracle uses strict `==` / narrow hardcoded forms without normalizing semantically equivalent representations (e.g. remainder `[4, 0]` vs `"4x"`, integer `-12` vs `"-12"`).

Index case already confirmed earlier: `ce111_q02_polynomial_division_remainder`.

---

## 2. Scope (16 tasks)

### Integer (4)
- `ce111_q03_prime_factor_selection`
- `ce112_q01_negative_integer_power`
- `ce112_q09_divisor_multiple_intersection`
- `ce111_nonchoice_q01_part1_exponential_growth`

### Polynomial (4)
- `ce111_q02_polynomial_division_remainder` ← previously confirmed; re-verified
- `ce111_q08_polynomial_factor_parameter_recovery`
- `ce115_calc_polynomial_division_l1`
- `ce115_calc_polynomial_factor_roots_l1`

### Radical (4)
- `ce111_q10_ordered_quadratic_roots_radical`
- `ce112_q04_radical_simplification`
- `ce113_q11_rationalize_denominator`
- `ce115_calc_radical_simplification_l1`

### Fraction (4)
- `ce111_q05_exact_fraction_expression`
- `ce112_q12_independent_probability_fraction`
- `ce113_q01_negative_fraction_subtraction`
- `ce115_calc_exact_rational_expression_l1`

---

## 3. Review dimensions (a–d)

For each task:

- **(a)** Does the evaluator check only top-level key presence, or also value types / formats / substructure?  
- **(b)** For nested `correct_answer`, is checking recursive to leaves or shallow?  
- **(c)** Are semantically equivalent types normalized before compare, or strict `==`?  
- **(d)** Are multiple legitimate representations possible while the oracle hardcodes one?

Labels:

- `SCHEMA_VALIDATION_STRICT_BUT_CORRECT`
- `SCHEMA_VALIDATION_GAP_SUSPECTED`
- `SCHEMA_VALIDATION_GAP_CONFIRMED`
- `INSUFFICIENT_INFO` (unused in this audit)

---

## 4. Sixteen-task marking table (with a/b/c/d)

| task_id | evaluator | (a) depth | (b) nesting | (c) normalize | (d) multi-form | label |
|---|---|---|---|---|---|---|
| `ce111_q03_prime_factor_selection` | `evaluate_integer_exact` | top-level `submitted == expected` | none | none (note: `13.0 == 13` happens to pass) | rejects str / wrapping dict | STRICT_BUT_CORRECT |
| `ce112_q01_negative_integer_power` | `evaluate_integer_exact` | same | none | none | rejects str / dict | STRICT_BUT_CORRECT |
| `ce112_q09_divisor_multiple_intersection` | `evaluate_integer_count` | requires dict; `count` exact int | one level | none | rejects bare int / str count | STRICT_BUT_CORRECT |
| `ce111_nonchoice_q01_part1_exponential_growth` | `evaluate_integer_exact_k` | requires dict; `k` exact int | one level | none | rejects bare int / str | STRICT_BUT_CORRECT |
| `ce111_q02_polynomial_division_remainder` | `evaluate_polynomial_division_remainder_only` | requires dict; `remainder` & `canonical_latex` only accept `"4x"` | one level; list not accepted | **none** | list / bare string / alternate latex rejected | **GAP_CONFIRMED** |
| `ce111_q08_polynomial_factor_parameter_recovery` | `evaluate_polynomial_factor_parameter_recovery` | bare int **or** dict `answer`/`value` | one level | none | **rejects string `"-12"`** | **GAP_CONFIRMED** (light) |
| `ce115_calc_polynomial_division_l1` | `evaluate_math16_polynomial_division_general` | coefficient structure is semantic judge | coefficient level | latex presentation-only | API-native coeff lists pass | STRICT_BUT_CORRECT |
| `ce115_calc_polynomial_factor_roots_l1` | `evaluate_math16_polynomial_factor_roots` | `roots` list is semantic judge | one level | latex presentation-only | bare prose string / non-list roots fail | **GAP_CONFIRMED** (packaging) |
| `ce111_q10_ordered_quadratic_roots_radical` | `evaluate_compound_radical_result` | structural normalize present | nested / flat | Fraction→int coerce | **if `result` is a str, it shadows correct flat fields** | **GAP_CONFIRMED** |
| `ce112_q04_radical_simplification` | `evaluate_radical_simplification_canonical` | coeff+radicand+**latex all required** | one level | no latex normalize | structural-correct but missing/variant latex → fail | GAP_SUSPECTED |
| `ce113_q11_rationalize_denominator` | `evaluate_integer_exact` | bare int | none | none | rejects str / dict | STRICT_BUT_CORRECT† |
| `ce115_calc_radical_simplification_l1` | `evaluate_math16_radical_simplification` | structural+**latex** | one level | none | same latex coupling risk | GAP_SUSPECTED |
| `ce111_q05_exact_fraction_expression` | `evaluate_exact_fraction_canonical` | num/den (Fraction-equal) + **latex required** | one level | fraction value reduces | latex variants / missing latex → fail | GAP_SUSPECTED |
| `ce112_q12_independent_probability_fraction` | `evaluate_exact_fraction_canonical` | same | one level | fraction value reduces | same | GAP_SUSPECTED |
| `ce113_q01_negative_fraction_subtraction` | `evaluate_exact_fraction_canonical` | same | one level | fraction value reduces | same | GAP_SUSPECTED |
| `ce115_calc_exact_rational_expression_l1` | `evaluate_math16_exact_rational_expression` | `value` string + latex | one level | none | rejects Fraction object / num-den shape | GAP_SUSPECTED |

† `ce113_q11` L5 failures in baseline were **mathematically wrong** (`11` vs expected `5`), not schema false negatives.

**Shared pipeline note:** G3 in `classify_math16_response` only validates top-level keys / frozen payload equality. Internal `correct_answer` schema errors therefore often surface as **L5**.

---

## 5. Manual Domain API calls (offline; not LLM)

| Call | Args | Return |
|---|---|---|
| `PolynomialOps.div_qr` | `[6, 4, 0], [2, 0, 0]` | quotient=`[3]`, remainder=`[4, 0]`; `format_latex(remainder)='4x'` |
| `PolynomialOps.div_qr` | `[6, 0, 6], [1, -4]` | quotient=`[6, 24]`, remainder=`[102]`; latex `6x + 24` / `102` |
| `RadicalOps.simplify_term` | `(1, 135)` | `(3, 15)` |
| `RadicalOps.simplify_term` | `(1, 27)` | `(3, 3)` |
| `FractionOps.create` | `"9/22"` | `Fraction(9, 22)` |

No exceptions on these frozen-parameter calls.

---

## 6. Manual oracle feed matrix (PASS/FAIL)

### 6.1 `ce111_q02_polynomial_division_remainder`

| Case | submitted `correct_answer` | is_correct |
|---|---|---|
| canonical_dict | `{"remainder":"4x","canonical_latex":"4x"}` | PASS |
| bare_string | `"4x"` | **FAIL** |
| api_native_list | `{"remainder":[4,0],"canonical_latex":"4x"}` | **FAIL** |
| remainder_only_string | `{"remainder":"4x"}` | **FAIL** |

### 6.2 Integer / count / k (control)

| task | case | result |
|---|---|---|
| q03 | bare `13` | PASS |
| q03 | `"13"` / `{"value":13}` | FAIL |
| q01 | bare `-27` | PASS |
| q01 | `"-27"` | FAIL |
| q09 | `{"count":6}` | PASS |
| q09 | bare `6` / `{"count":"6"}` | FAIL |
| nonchoice | `{"k":18}` | PASS |
| nonchoice | bare `18` / `{"k":"18"}` | FAIL |

### 6.3 `ce111_q08_polynomial_factor_parameter_recovery`

| case | result |
|---|---|
| bare `-12` | PASS |
| `{"answer":-12}` / `{"value":-12}` | PASS |
| string `"-12"` | **FAIL** |
| `28` / `"28"` | FAIL (true wrong) |

### 6.4 `ce115_calc_polynomial_division_l1`

| case | result |
|---|---|
| full canonical dict | PASS |
| structural coeffs only | PASS (`is_correct` ignores latex) |
| API-native coeffs from `div_qr` | PASS |
| wrong key shape `{quotient, remainder}` | FAIL |

### 6.5 `ce115_calc_polynomial_factor_roots_l1`

| case | result |
|---|---|
| `{"roots":[-6,2], ...}` | PASS |
| roots-only dict | PASS (latex presentation-only) |
| bare list `[-6,2]` | FAIL |
| roots as strings | FAIL |

### 6.6 `ce111_q10_ordered_quadratic_roots_radical`

| case | result |
|---|---|
| nested canonical `result` dict | PASS |
| flat `{rational, radical_coefficient, radicand}` | PASS |
| flat correct fields **plus** `result: "<latex string>"` | **FAIL** (`compound radical payload must be a dict`) — shadowing bug/gap |

### 6.7 Radical / fraction latex coupling (suspected)

| family | structural math OK, latex missing/variant | result |
|---|---|---|
| q04 / calc radical | structural only / spaced latex | FAIL (`is_correct` requires latex) |
| fraction ×3 | structural only / `\dfrac` / plain `n/d` latex | FAIL |
| fraction ×3 | unreduced nums with correct latex | PASS (Fraction equality) |
| calc exact rational | `value` Fraction object / num-den shape | FAIL |

---

## 7. GAP_CONFIRMED detail (4 tasks, 24 false negatives)

Source baseline: `docs/experiments/results/math16_pilot02_full_evaluation_v3_r001/cell_level_baseline.jsonl` at commit `5961ef52…`.

| task_id | original pass/fail | L5 sampled | schema FN count | other failures | corrected pass estimate |
|---|---|---|---|---|---|
| `ce111_q02_polynomial_division_remainder` | **0/20** | 18/18 L5 | **18** (14 bare `"4x"` + 4 API-native `[4,0]`+latex) | 2× L3 `to_latex` AttributeError (not schema) | **18/20** |
| `ce111_q08_polynomial_factor_parameter_recovery` | **14/20** | 6/6 L5 | **2** (`correct_answer="-12"` string) | 4× true wrong (`28`) | **16/20** |
| `ce115_calc_polynomial_factor_roots_l1` | **18/20** | 2/2 L5 | **2** (correct roots embedded in prose string, not dict) | 0 | **20/20** |
| `ce111_q10_ordered_quadratic_roots_radical` | **18/20** | 2/2 L5 | **2** (`result` string shadows correct flat structure) | 0 | **20/20** |

**Confirmed schema-gap false negatives total: 18 + 2 + 2 + 2 = 24 cells.**

### 7.1 q02 L5 packaging tags (all 18)

- `FN_BARE_STRING_MATH_OK` ×14 — `correct_answer == "4x"`  
- `FN_API_NATIVE_OR_ALT_SHAPE` ×4 — `remainder=[4,0]`, `canonical_latex="4x"`  
  (conditions: ab2d seed 1301; ab2d_spec seeds 2001, 2002, 2004)

### 7.2 Informal overall correction

```text
Published baseline:     265 / 320
Known schema FN:         24
Corrected estimate:     289 / 320  (90.3%)
```

**This 289/320 figure is an estimate only — not a formal re-evaluation.** Formal rescored numbers require a post-fix evaluator revision and offline re-score of existing raw responses.

---

## 8. GAP_SUSPECTED (6 tasks) — baseline not hit, risk remains

Per section 4 marking table (radical×2 + fraction×3 + calc exact rational):

| task_id | why suspected | baseline L5 from this gap? |
|---|---|---|
| `ce112_q04_radical_simplification` | `is_correct` requires exact latex in addition to structural coeff/radicand; no display normalize | No (20/20 pass) |
| `ce115_calc_radical_simplification_l1` | same latex coupling | No (20/20 pass) |
| `ce111_q05_exact_fraction_expression` | structural Fraction OK still needs exact latex | No L5; fails were L3 API misuse |
| `ce112_q12_independent_probability_fraction` | same | No L5; L3 API misuse |
| `ce113_q01_negative_fraction_subtraction` | same | No L5; L3 API misuse |
| `ce115_calc_exact_rational_expression_l1` | requires exact `value` string + latex; rejects alternate shapes | No (20/20 pass) |

**Explicit note (freeze language):**  
本輪 baseline 未命中，不代表沒有風險，可能因上游 L3 API misuse 尚未讓模型走到這一步。

After Ab2d+spec / Domain-API misuse is fixed upstream, these latex-coupled oracles may begin producing schema false negatives.

---

## 9. Research-design implications (recorded, not executed)

1. Prefer **infrastructure-level answer normalization** before compare, not one-off task patches.  
2. Recommended sequence: (a) fix evaluator normalize, (b) **re-score existing raw responses offline** (0 LLM), (c) only then decide whether any cells need regeneration.  
3. Prior Math16 ab123 / multiseed runs sharing `math16_oracles.py` should be back-labeled for the same gaps (especially q02). Named Pilot-00/01 CE115 runs are mostly different item sets but any shared evaluate helpers warrant spot checks.

---

## 10. Governance record for this audit

| Item | Status |
|---|---|
| LLM / Gemini calls | **0** |
| API cost | **$0.00** |
| Modified frozen prompts | No |
| Modified frozen answer contracts | No |
| Modified evaluator source | No |
| Modified raw responses | No |
| Modified baseline jsonl / summaries | No |
| Actions taken | Read-only static review + offline Domain API / oracle probes + baseline L5 sampling |

---

## 11. Verdict

```text
ORACLE_SCHEMA_AUDIT_COMPLETE
ORACLE_SCHEMA_AUDIT_V1_PRE_FIX
```

**Summary line:**  
16 題中 **4** 題確認有 schema gap（GAP_CONFIRMED），共影響 **24** 格 baseline 判定；另 **6** 題為 GAP_SUSPECTED（本輪無對應 L5 命中，風險仍在）。校正後估計 **289/320（90.3%）** —— **非正式重評**。

---

## 12. Appendix — evaluator source anchors

Primary file: `agent_tools/finals_rebuild/math16_oracles.py`

| Symbol | Approx. role |
|---|---|
| `evaluate_integer_exact` | Integer exact `==` |
| `evaluate_integer_count` | `{count}` |
| `evaluate_integer_exact_k` | `{k}` |
| `evaluate_polynomial_division_remainder_only` | q02 remainder string-only |
| `evaluate_polynomial_factor_parameter_recovery` | q08 int / dict answer |
| `evaluate_math16_polynomial_division_general` | calc division structural coeffs |
| `evaluate_math16_polynomial_factor_roots` | roots list semantic |
| `evaluate_compound_radical_result` | q10 normalize + structural |
| `evaluate_radical_simplification_canonical` | q04 structural+latex |
| `evaluate_math16_radical_simplification` | calc radical structural+latex |
| `evaluate_exact_fraction_canonical` | fraction structural+latex |
| `evaluate_math16_exact_rational_expression` | value string+latex |

Dispatch: `MATH16_ORACLE_DISPATCH` → `evaluate_math_task_oracle`.

Baseline cells root (non-integer): `docs/experiments/results/math16_pilot02_full_gemini/cells/`  
Integer reused root: `docs/experiments/results/math16_pilot02_integer_gemini/cells/`
