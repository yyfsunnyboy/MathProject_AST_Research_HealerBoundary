# Math16 Pilot-02 Full Evaluation Revision v3_r001 Report

Offline blinded baseline + Taxonomy v3 + frozen deterministic Healer for the complete Math16 320-cell inventory.

## 1. Metadata
- **Evaluation ID**: `math16_pilot02_full_evaluation_v3_r001`
- **Revision**: `v3_r001`
- **Taxonomy SHA-256**: `7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304`
- **Evaluator SHA-256**: `a6e06c4de738fd61f5701094343de36afc1780057a3fb385dbf8caa84f37f6a6`
- **Source Commit**: `d28261da8dc781f5053964dbaa6659948dc38927`
- **LLM calls**: `0`
- **API cost**: `$0.00`
- **Integer reproducibility**: `80/80 matched`

## 2. Overall
- Baseline pass: `265/320` (82.81%)
- Post-Healer pass: `265/320` (82.81%)
- Baseline fail: `55/320`
- Eligible: `0`
- Transformed: `0`
- Rescued: `0`
- Regressed: `0`
- Abstained: `55`
- Preserved pass: `265`

## 3. By condition (display names; machine id `ab2d` = Ab2d+api)
| Condition | Baseline pass | Post-Healer pass | Eligible | Rescued | Regressed |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **Ab1** | 63/80 | 63/80 | 0 | 0 | 0 |
| **Ab2g** | 71/80 | 71/80 | 0 | 0 | 0 |
| **Ab2d+api** | 73/80 | 73/80 | 0 | 0 | 0 |
| **Ab2d+spec** | 58/80 | 58/80 | 0 | 0 | 0 |

> Ab2d+api 與 Ab2d+spec 為完整介入策略比較，不是單純 API 有無的因果估計。

## 4. By family
| Family | Baseline pass | Post-Healer pass | L2 | L3 | L4 | L5 | Ceiling | Discriminative | L2–L4 exposure | Frozen Healer window |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: | :---: | :---: |
| **Integer** | 80/80 | 80/80 | 0 | 0 | 0 | 0 | Y | N | N | N |
| **Polynomial** | 52/80 | 52/80 | 0 | 2 | 0 | 26 | N | Y | Y | N |
| **Radical** | 68/80 | 68/80 | 0 | 0 | 0 | 9 | N | Y | N | N |
| **Fraction** | 65/80 | 65/80 | 0 | 15 | 0 | 0 | N | Y | Y | N |

## 5. By task (20 cells = 4 conditions × 5 seeds)
| Task | Family | Baseline | Post-Healer | Ab1 | Ab2g | Ab2d+api | Ab2d+spec | Eligible | Rescued |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ce111_q03_prime_factor_selection` | Integer | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce112_q01_negative_integer_power` | Integer | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce112_q09_divisor_multiple_intersection` | Integer | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce111_nonchoice_q01_part1_exponential_growth` | Integer | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce111_q02_polynomial_division_remainder` | Polynomial | 0/20 | 0/20 | 0/5 | 0/5 | 0/5 | 0/5 | 0 | 0 |
| `ce111_q08_polynomial_factor_parameter_recovery` | Polynomial | 14/20 | 14/20 | 0/5 | 4/5 | 5/5 | 5/5 | 0 | 0 |
| `ce115_calc_polynomial_division_l1` | Polynomial | 20/20 | 20/20 | 5/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce115_calc_polynomial_factor_roots_l1` | Polynomial | 18/20 | 18/20 | 3/5 | 5/5 | 5/5 | 5/5 | 0 | 0 |
| `ce111_q10_ordered_quadratic_roots_radical` | Radical | 18/20 | 18/20 | 5/5 | 5/5 | 5/5 | 3/5 | 0 | 0 |
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
| `2026071301` | 53/64 | 53/64 | 0 | 0 |
| `2026072001` | 53/64 | 53/64 | 0 | 0 |
| `2026072002` | 53/64 | 53/64 | 0 | 0 |
| `2026072003` | 53/64 | 53/64 | 0 | 0 |
| `2026072004` | 53/64 | 53/64 | 0 | 0 |

## 7. G1–G4
- G1 FAIL: `3` / PASS: `317`
- G2 FAIL: `17` / PASS: `300`
- G3 FAIL: `0` / PASS: `300`
- G4 FAIL: `35` / PASS: `265`

## 8. L0–L5 (baseline failures only)
- L0: `0`
- L1: `3`
- L2: `0`
- L3: `17`
- L4: `0`
- L5: `35`

## 9. Formal condition differences (paired by task×seed)
- **Ab2g - Ab1**: `8` (71/80 − 63/80; 10.0 pp)
- **Ab2d+api - Ab2g**: `2` (73/80 − 71/80; 2.5 pp)
- **Ab2d+spec - Ab2g**: `-13` (58/80 − 71/80; -16.25 pp)
- **Ab2d+spec - Ab2d+api**: `-15` (58/80 − 73/80; -18.75 pp)
- **post-Healer − baseline**: `0` (265/320 − 265/320; 0.0 pp)

## 10. Ceiling / discrimination / Healer window
- **Integer**: ceiling=True, discriminative=False (spread 0.0 pp), L2–L4 exposure=False, frozen_healer_window=False, pure_L5=False
- **Polynomial**: ceiling=False, discriminative=True (spread 35.0 pp), L2–L4 exposure=True, frozen_healer_window=False, pure_L5=False
- **Radical**: ceiling=False, discriminative=True (spread 15.0 pp), L2–L4 exposure=False, frozen_healer_window=False, pure_L5=False
- **Fraction**: ceiling=False, discriminative=True (spread 75.0 pp), L2–L4 exposure=True, frozen_healer_window=False, pure_L5=False

## 11. Integrity
- Inventory unique cells: `320`
- Raw/prompt/fingerprint verified in preflight
- Integer prior revision match: `80/80`
- Healer allowlist frozen: `L1_CLOSE_UNBALANCED_PARENTHESIS, L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED, L1_PROSE_RESIDUE_NARROW, L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP, L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM, L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`

## 12. Method notes
- No Gemini or other LLM calls during evaluation.
- Display label `Ab2d+api` maps from machine condition `ab2d` without rewriting raw identity.
- Unknown classifier outcomes are `PENDING_REVIEW`, never auto-mapped to L5.
- Frozen Healer runs only on `healer_eligible=true` cells; ambiguous entry-points abstain.

MATH16_320_BLINDED_V3_EVALUATION_COMPLETE
FROZEN_HEALER_EVALUATION_COMPLETE
FULL_CONDITION_FAMILY_COMPARISON_READY
