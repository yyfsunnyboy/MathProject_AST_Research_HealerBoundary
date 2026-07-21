# Math16 Pilot-02 Full Evaluation Revision v4_r001 Report (post schema-normalize re-score)

Offline blinded baseline + Taxonomy v3 + frozen deterministic Healer for the complete Math16 320-cell inventory.

## 1. Metadata
- **Evaluation ID**: `math16_pilot02_full_evaluation_v4_r001`
- **Revision**: `v4_r001`
- **Taxonomy SHA-256**: `7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304`
- **Evaluator SHA-256**: `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc`
- **Source Commit**: `6fadc0a54548c7006de865079d312d8c0be2f9d5`
- **LLM calls**: `0`
- **API cost**: `$0.00`
- **Integer reproducibility**: `80/80 matched`

## 2. Overall
- Baseline pass: `289/320` (90.31%)
- Post-Healer pass: `289/320` (90.31%)
- Baseline fail: `31/320`
- Eligible: `0`
- Transformed: `0`
- Rescued: `0`
- Regressed: `0`
- Abstained: `31`
- Preserved pass: `289`

## 3. By condition (display names; machine id `ab2d` = Ab2d+api)
| Condition | Baseline pass | Post-Healer pass | Eligible | Rescued | Regressed |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **Ab1** | 72/80 | 72/80 | 0 | 0 | 0 |
| **Ab2g** | 76/80 | 76/80 | 0 | 0 | 0 |
| **Ab2d+api** | 78/80 | 78/80 | 0 | 0 | 0 |
| **Ab2d+spec** | 63/80 | 63/80 | 0 | 0 | 0 |

> Ab2d+api 與 Ab2d+spec 為完整介入策略比較，不是單純 API 有無的因果估計。

## 4. By family
| Family | Baseline pass | Post-Healer pass | L2 | L3 | L4 | L5 | Ceiling | Discriminative | L2–L4 exposure | Frozen Healer window |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: | :---: | :---: |
| **Integer** | 80/80 | 80/80 | 0 | 0 | 0 | 0 | Y | N | N | N |
| **Polynomial** | 74/80 | 74/80 | 0 | 2 | 0 | 4 | N | Y | Y | N |
| **Radical** | 70/80 | 70/80 | 0 | 0 | 0 | 7 | N | Y | N | N |
| **Fraction** | 65/80 | 65/80 | 0 | 15 | 0 | 0 | N | Y | Y | N |

## 5. By task (20 cells = 4 conditions × 5 seeds)
| Task | Family | Baseline | Post-Healer | Ab1 | Ab2g | Ab2d+api | Ab2d+spec | Eligible | Rescued |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ce111_q03_prime_factor_selection` | Integer | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce112_q01_negative_integer_power` | Integer | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce112_q09_divisor_multiple_intersection` | Integer | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce111_nonchoice_q01_part1_exponential_growth` | Integer | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce111_q02_polynomial_division_remainder` | Polynomial | 18/20 | 18/20 | 5/5 | 5/5 | 5/5 | 3/5 | 0 | 0 |
| `ce111_q08_polynomial_factor_parameter_recovery` | Polynomial | 16/20 | 16/20 | 2/5 | 4/5 | 5/5 | 5/5 | 0 | 0 |
| `ce115_calc_polynomial_division_l1` | Polynomial | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce115_calc_polynomial_factor_roots_l1` | Polynomial | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce111_q10_ordered_quadratic_roots_radical` | Radical | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce112_q04_radical_simplification` | Radical | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce113_q11_rationalize_denominator` | Radical | 10/20 | 10/20 | 0/5 | 2/5 | 3/5 | 5/5 | 0 | 0 |
| `ce115_calc_radical_simplification_l1` | Radical | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce111_q05_exact_fraction_expression` | Fraction | 15/20 | 15/20 | 5/5 | 5/5 | 5/5 | 0/5 | 0 | 0 |
| `ce112_q12_independent_probability_fraction` | Fraction | 15/20 | 15/20 | 5/5 | 5/5 | 5/5 | 0/5 | 0 | 0 |
| `ce113_q01_negative_fraction_subtraction` | Fraction | 15/20 | 15/20 | 5/5 | 5/5 | 5/5 | 0/5 | 0 | 0 |
| `ce115_calc_exact_rational_expression_l1` | Fraction | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |

## 6. By seed
| Seed | Baseline pass | Post-Healer pass | Eligible | Rescued |
| :--- | ---: | ---: | ---: | ---: |
| `2026071301` | 56/64 | 56/64 | 0 | 0 |
| `2026072001` | 59/64 | 59/64 | 0 | 0 |
| `2026072002` | 59/64 | 59/64 | 0 | 0 |
| `2026072003` | 57/64 | 57/64 | 0 | 0 |
| `2026072004` | 58/64 | 58/64 | 0 | 0 |

## 7. G1–G4
- G1 FAIL: `3` / PASS: `317`
- G2 FAIL: `17` / PASS: `300`
- G3 FAIL: `0` / PASS: `300`
- G4 FAIL: `11` / PASS: `289`

## 8. L0–L5 (baseline failures only)
- L0: `0`
- L1: `3`
- L2: `0`
- L3: `17`
- L4: `0`
- L5: `11`

## 9. Formal condition differences (paired by task×seed)
- **Ab2g - Ab1**: `4` (76/80 − 72/80; 5.0 pp)
- **Ab2d+api - Ab2g**: `2` (78/80 − 76/80; 2.5 pp)
- **Ab2d+spec - Ab2g**: `-13` (63/80 − 76/80; -16.25 pp)
- **Ab2d+spec - Ab2d+api**: `-15` (63/80 − 78/80; -18.75 pp)
- **post-Healer − baseline**: `0` (289/320 − 289/320; 0.0 pp)

## 10. Ceiling / discrimination / Healer window
- **Integer**: ceiling=True, discriminative=False (spread 0.0 pp), L2–L4 exposure=False, frozen_healer_window=False, pure_L5=False
- **Polynomial**: ceiling=False, discriminative=True (spread 15.0 pp), L2–L4 exposure=True, frozen_healer_window=False, pure_L5=False
- **Radical**: ceiling=False, discriminative=True (spread 25.0 pp), L2–L4 exposure=False, frozen_healer_window=False, pure_L5=False
- **Fraction**: ceiling=False, discriminative=True (spread 75.0 pp), L2–L4 exposure=True, frozen_healer_window=False, pure_L5=False

## 11. v3 → v4 comparison (evaluator schema normalize)
- v3 baseline pass: `265/320`
- v4 baseline pass: `289/320`
- delta: `24` (fail→pass `24`, pass→fail `0`)
- cells with `changed_by_evaluator_fix=true`: `24`
- oracle SHA-256: `8b8e2a2086c302576eeb69a1ae28dd9220e5c1d5c9e97f5b384a3c285e7b4a44`
- audit reference: `docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md` (**immutable V1; not modified**)

### GAP task effects (pass /20)
| Task | Gap | v3 | v4 | flips | V1 corrected estimate |
| :--- | :--- | ---: | ---: | ---: | :--- |
| `ce111_q02_polynomial_division_remainder` | `GAP_CONFIRMED:evaluate_polynomial_division_remainder_only` | 0/20 | 18/20 | 18 | 18/20 |
| `ce111_q08_polynomial_factor_parameter_recovery` | `GAP_CONFIRMED:evaluate_polynomial_factor_parameter_recovery` | 14/20 | 16/20 | 2 | 16/20 |
| `ce115_calc_polynomial_factor_roots_l1` | `GAP_CONFIRMED:evaluate_math16_polynomial_factor_roots` | 18/20 | 20/20 | 2 | 20/20 |
| `ce111_q10_ordered_quadratic_roots_radical` | `GAP_CONFIRMED:evaluate_compound_radical_result` | 18/20 | 20/20 | 2 | 20/20 |
| `ce112_q04_radical_simplification` | `GAP_SUSPECTED:evaluate_radical_simplification_canonical` | 20/20 | 20/20 | 0 | 20/20 (no L5 hit) |
| `ce115_calc_radical_simplification_l1` | `GAP_SUSPECTED:evaluate_math16_radical_simplification` | 20/20 | 20/20 | 0 | 20/20 (no L5 hit) |
| `ce111_q05_exact_fraction_expression` | `GAP_SUSPECTED:evaluate_exact_fraction_canonical` | 15/20 | 15/20 | 0 | n/a (L3 dominant) |
| `ce112_q12_independent_probability_fraction` | `GAP_SUSPECTED:evaluate_exact_fraction_canonical` | 15/20 | 15/20 | 0 | n/a (L3 dominant) |
| `ce113_q01_negative_fraction_subtraction` | `GAP_SUSPECTED:evaluate_exact_fraction_canonical` | 15/20 | 15/20 | 0 | n/a (L3 dominant) |
| `ce115_calc_exact_rational_expression_l1` | `GAP_SUSPECTED:evaluate_math16_exact_rational_expression` | 20/20 | 20/20 | 0 | 20/20 (no L5 hit) |

### Confound status
- GAP_CONFIRMED packaging/type false negatives are addressed in this revision.
- GAP_SUSPECTED latex coupling was relaxed to structural judge (latex kept as presentation / `latex_ok`); this completes the incomplete `math16_latex_semantic_v2` rollout recorded in V1.
- Condition-level deltas in §9 should no longer be confounded by the four confirmed schema gaps.
- Residual risks: Ab2d+spec L3 Domain-API misuse remains a separate confound; true mathematical L5 errors remain.

## 12. Integrity
- Inventory unique cells: `320`
- Raw/prompt/fingerprint verified in preflight
- Integer prior revision match: `80/80`
- Healer allowlist frozen: `L1_CLOSE_UNBALANCED_PARENTHESIS, L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED, L1_PROSE_RESIDUE_NARROW, L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP, L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM, L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`
- v3 artifacts left intact under `math16_pilot02_full_evaluation_v3_r001/`

## 13. Method notes
- No Gemini or other LLM calls during evaluation (`LLM calls=0`, `$0.00`).
- Display label `Ab2d+api` maps from machine condition `ab2d` without rewriting raw identity.
- Unknown classifier outcomes are `PENDING_REVIEW`, never auto-mapped to L5.
- Frozen Healer runs only on `healer_eligible=true` cells; ambiguous entry-points abstain.
- Re-score uses existing raw_response only; frozen prompts/contracts/answers unchanged.

ORACLE_SCHEMA_FIX_APPLIED
EVALUATION_V4_RESCORED_ZERO_MODEL_CALLS
MATH16_320_BLINDED_V4_RESCORE_COMPLETE
FROZEN_HEALER_EVALUATION_COMPLETE
V3_V4_COMPARISON_READY
