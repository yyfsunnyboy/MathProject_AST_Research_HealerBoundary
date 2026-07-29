# Math16 Domain API Inventory v1 (draft)

> **status:** `development_candidate_not_frozen`
> **contract_version:** `v1`
> **audit step:** Math16 Aggressive Healer Step -1 (read-only contract audit)
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **origin/main:** `f0eae63fe8c3760e9912589654657510119175ce`

## Scope

- Prompt conditions audited: **Ab2d+api** (`ab2d`) and **Ab2d+spec** (現行有效正式版 = `ab2d_spec_v2`).
- Early incomplete Ab2d+spec-v1 (`docs/experiments/prompts/ab2d_spec/`, condition `ab2d_spec`) is **excluded** from this inventory.
- Domains: Integer / Fraction / Radical / Polynomial.
- Evidence priority: formal prompt freeze → scaffold/templates → runner namespace → domain implementation → focused tests. `core/healers` is historical reference only and is not a contract source.

## Formal evidence paths

| Role | Path | SHA-256 |
|---|---|---|
| evidence | `core/prompts/domain_function_library.py` | `836de2f9229f1b2b52765d0a9c7b91af0e61eb58e092ffd8dd607d975ef80e3c` |
| evidence | `agent_tools/finals_rebuild/domain_api_ssot.py` | `5801f7ad3c7876fecbf672be034501e205d01dc0107694c886826537e148b443` |
| evidence | `agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py` | `7b7f373fc648048e0770a686ac823848ac077873a9ce6fce737d8cf3b3501c90` |
| evidence | `agent_tools/finals_rebuild/math16_pool.py` | `406965451600809fb0abb771073b90080eb2bc195fb4aabb8339413d42734a59` |
| evidence | `scripts/run_math16_latex_v1_gemini_live.py` | `fd757e612e9a82dcb0036796113f6e1ab368d65e8e4c30a9abfb9a9c5f2015d4` |
| evidence | `scripts/evaluate_math16_pilot02_full_v4.py` | `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/manifest.json` | `e204e07957b7b88ffb60e8d93e9f9a3ab7661c33c81877d1ad29f3d038f29ffd` |
| evidence | `tests/finals_rebuild/test_math16_domain_api_ssot.py` | `9657e0ae7a56f0cd0e5021f68cfa3c09d6f7d68bd677d74c1c46732a6d62db67` |
| evidence | `tests/finals_rebuild/test_domain_api_contract_hardening_v2.py` | `26efbf14e6ca8d897296d9739bd1e19e6b4c37493cd6bc7aaef506beca546638` |
| evidence | `tests/test_math16_ab2d_spec_v2.py` | `d7d882695ea1ee82f3449cd0a69156e13cb186aaf6686f49fb79c6e9a9d3b082` |
| evidence | `docs/experiments/templates/ab2d_spec_v2/integer_domain_scaffold_compact.py` | `657069bd70e3507be53c337716683e96f67b0321c3ac000b4a2177df903ff799` |
| evidence | `docs/experiments/templates/ab2d_spec_v2/fraction_domain_scaffold_compact.py` | `66a7e1dd30bac50608f685b78a798fada0a6dc54b7df9e2fe236753bfc9f6b4a` |
| evidence | `docs/experiments/templates/ab2d_spec_v2/polynomial_domain_scaffold_compact.py` | `8aadbb6a9eb7a591e4bcbe2d5300e44a8b5ebb1f215451411cea076c85a7ed1b` |
| evidence | `docs/experiments/templates/ab2d_spec_v2/fraction_api_signature_card.md` | `4aaca01072b24d7688a70d309d53022d41425889ee905b3b61d5cec6fa23e39a` |
| evidence | `docs/experiments/templates/ab2d_spec_v2/polynomial_api_signature_card.md` | `c2188e6133254f65f073b4da7cc52243013a945b6a0c22d7eaa0847c86c6440b` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q03_prime_factor_selection.txt` | `c956a2a44c3fd9140b6cf0a456ca6c9be05edf181c270367ef38b5b84555f863` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q01_negative_integer_power.txt` | `c35bade2203f604df9a893d692deb38fd82bc8899dfeba56893b4966f699290b` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q09_divisor_multiple_intersection.txt` | `121936689c850cfca329f2c605b90159bef31fea727950e221004d37e23f03c2` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt` | `07834f7481b95ac7bf03eab19b339d0094c312b01eb6c3f0be4d345ef64688dc` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q02_polynomial_division_remainder.txt` | `6519e47182f1bc18b1d2be6919de8fb4a674bd05884c96d748f18e91ff91648a` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt` | `dcae6133350560dce6afb58b968f780d77003c1d27fc66562fe8d8cd7c7829d9` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_polynomial_division_l1.txt` | `f94f4bdfe0ac93412a9239feee82ce612f19b21adf5b8937be3a0f845d956f9c` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_polynomial_factor_roots_l1.txt` | `f964fcf6767715d080db4c660c0d87fa02f58d75fb9cbeacf2ffbd34191dd04b` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q10_ordered_quadratic_roots_radical.txt` | `15601ab1ed75054ddb60ba5d91cd1bcc88250f78d4f78b94b03e6ab98157e2e1` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q04_radical_simplification.txt` | `3c4fb3e875ca39aa1ac8dcbb6004fd897a32717867992a87620b1a46fbbba701` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce113_q11_rationalize_denominator.txt` | `1089e14bff6d728ee94f9c6551e9469fd8c685830c393d119dd4a01bc04d43e7` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_radical_simplification_l1.txt` | `41020a535d5116a6075bfdb126eede46b763385498ce7e4c5c5c79eafd2c3481` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q05_exact_fraction_expression.txt` | `5fcface8323398af41c3ad69a79f44554a4ea4a4c1338f1e46450a565f078828` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q12_independent_probability_fraction.txt` | `12d4f290ea1ba1e4d212da8caa8cc9df80a10c87bb043d2fd8294391778d9a48` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce113_q01_negative_fraction_subtraction.txt` | `0da97fd94d049db659321a60e253b21007aa38de1dba22edde05ebd48bc2347d` |
| evidence | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_exact_rational_expression_l1.txt` | `a69b56dbc115527e4b3481363595caa57bbcb7cf0f0729b77ecb948ce9647d57` |


> **Note (C10/U5):** `ab2d_spec_v2/prompts/*.txt` evidence SHA-256 values above are **file-byte** hashes. On this working tree the files contain CRLF, so byte hashes differ from `manifest.json` `exact_prompt_sha256`. After LF normalization, all 16 prompts match the manifest. See registry `ab2d_spec_v2_prompt_hash_dual`.

## Runtime binding (Math16)

- Executor: `scripts/run_math16_latex_v1_gemini_live.py::_execute_generate_all_ops`
- Evaluator orchestrator: `scripts/evaluate_math16_pilot02_full_v4.py`
- Injected into every candidate namespace: `IntegerOps`, `FractionOps`, `RadicalOps`, `PolynomialOps`
- Model **need not import**; import still works if written.
- Scaffold under Ab2d+spec is **prompt-text** injection (template), not runtime code prepend.
- If the model redefines an Ops class/name, it overwrites the injected binding (not blocked).

## Symbol counts

### Per prompt condition

- Ab2d+api total symbols: **49** (classes 4, methods 43, globals 2)
- Ab2d+spec total symbols: **49** (classes 4, methods 43, globals 2)

### Class methods by home domain (same under both conditions; 43 runtime methods)

| Domain | Runtime methods | Ab2d+api exposed methods | Ab2d+spec exposed methods |
|---|---:|---:|---:|
| Integer | 7 | 3 | 0 |
| Fraction | 8 | 5 | 5 |
| Radical | 17 | 3 | 1 |
| Polynomial | 11 | 4 | 2 |

### Status counts

| Status | Ab2d+api | Ab2d+spec |
|---|---:|---:|
| `EXPOSED_AND_AVAILABLE` | 19 | 11 |
| `AVAILABLE_NOT_EXPOSED` | 30 | 38 |
| `EXPOSED_NOT_AVAILABLE` | 0 | 0 |
| `LEGACY_ONLY` | 0 | 0 |

## Contract candidates (EXPOSED_AND_AVAILABLE ∧ allow_call ∧ SUPPORTED_PUBLIC)

### Ab2d+api

- `FractionOps.add`
- `FractionOps.create`
- `FractionOps.mul`
- `FractionOps.sub`
- `FractionOps.to_latex`
- `IntegerOps.fmt_num`
- `IntegerOps.is_divisible`
- `IntegerOps.safe_eval`
- `PolynomialOps.div_qr`
- `PolynomialOps.factor_quadratic_exact`
- `PolynomialOps.format_latex`
- `PolynomialOps.mul`
- `RadicalOps.format_expression`
- `RadicalOps.format_term`
- `RadicalOps.simplify_term`

### Ab2d+spec (current v2 formal)

- `FractionOps.add`
- `FractionOps.create`
- `FractionOps.from_parts`
- `FractionOps.mul`
- `FractionOps.sub`
- `PolynomialOps.div_qr`
- `PolynomialOps.format_latex`
- `RadicalOps.simplify_term`

## Ab2d+api symbol inventory

| domain | canonical_name | type | status | prompt | runtime | allow_call | contract_candidate | signature | return | definition |
|---|---|---|---|---|---|---|---|---|---|---|
| Integer | `IntegerOps` | domain_class | EXPOSED_AND_AVAILABLE | True | True | True | True | `N/A (class)` | N/A (class) | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps` | domain_class | EXPOSED_AND_AVAILABLE | True | True | True | True | `N/A (class)` | N/A (class) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps` | domain_class | EXPOSED_AND_AVAILABLE | True | True | True | True | `N/A (class)` | N/A (class) | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps` | domain_class | EXPOSED_AND_AVAILABLE | True | True | True | True | `N/A (class)` | N/A (class) | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.add` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(a, b)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.create` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(value)` | Fraction  # not JSON serializable; use the to_exact adapter | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.div` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(a, b)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.from_parts` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(numerator, denominator=1)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.mul` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(a, b)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.sub` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(a, b)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.to_exact` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(value)` | int \| str  # integer or irreducible 'p/q' | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.to_latex` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(val, mixed=False)` | str | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.add` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(a, b)` | int | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.fmt_num` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(n)` | str | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.is_divisible` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(a, b)` | bool | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.op_to_latex` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(op_str)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.random_nonzero` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(min_val, max_val)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.safe_eval` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(expr)` | int \| float  # bool and container results raise ValueError | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.sub` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(a, b)` | int | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.add` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, c2)` | list[number]  # operand-dependent coefficient type; highest degree first | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.coeffs_from_py_expression` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(expression, var='x')` | list[Fraction]  # highest degree first | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.div_qr` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(dividend_coefficients, divisor_coefficients)` | tuple[list[int \| str], list[int \| str]]  # quotient,remainder | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.factor_quadratic_exact` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(a, b, c)` | list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; N | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.format_latex` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(coeffs, var='x')` | str | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.format_plain` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeffs, var='x')` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.mul` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(c1, c2)` | list[int \| float \| Fraction]  # operand-dependent; highest degree first | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.normalize` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeffs)` | list[number]  # highest degree first; leading zeros removed | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.random_poly` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(degree, range_val=(-5, 5))` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.sub` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, c2)` | list[number]  # operand-dependent coefficient type; highest degree first | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.to_degree_map` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeffs)` | dict[str, int \| str]  # descending degree insertion order | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.add_dicts` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms1, terms2)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.add_term` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms_dict, coeff, radicand)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.create` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(inner)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.div_terms` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, r1, c2, r2)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.format_expression` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(terms_dict, denominator=1)` | str  # complete compound-radical LaTeX | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.format_term` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(coeff, radicand, is_first=True)` | str  # complete single-term LaTeX including coefficient/sign | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.format_term_unsimplified` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeff, radicand, is_first=True, wrap_negative_non_leading=False, is_leading=None)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.get_prime_factors` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(n)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.is_perfect_square` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(n)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.mul_terms` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, r1, c2, r2)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.multiply_dicts` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms1, terms2)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.normalize_term_list` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms)` | list[dict]  # sorted; keys coefficient,radicand | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.rationalize_linear_denominator` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(numerator, denom_rational, denom_radical_coeff, radicand)` | tuple[int \| Fraction, int \| Fraction, int] | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.simplify` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeff, radicand)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.simplify_root` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(radicand)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.simplify_term` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(coeff, radicand)` | tuple[int \| Fraction, int]  # semantic (coefficient, square-free radicand) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.to_latex` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(expr)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| UNRESOLVED | `get_domain_helpers_code` | global_function | AVAILABLE_NOT_EXPOSED | False | False | False | False | `(domains, stub_mode=True)` | UNRESOLVED (not Math16 model-facing) | `core/prompts/domain_function_library.py` |
| UNRESOLVED | `get_required_domains` | global_function | AVAILABLE_NOT_EXPOSED | False | False | False | False | `(skill_id)` | UNRESOLVED (not Math16 model-facing) | `core/prompts/domain_function_library.py` |

## Ab2d+spec symbol inventory (ab2d_spec_v2)

| domain | canonical_name | type | status | prompt | runtime | allow_call | contract_candidate | signature | return | definition |
|---|---|---|---|---|---|---|---|---|---|---|
| Integer | `IntegerOps` | domain_class | AVAILABLE_NOT_EXPOSED | False | True | False | False | `N/A (class)` | N/A (class) | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps` | domain_class | EXPOSED_AND_AVAILABLE | True | True | True | True | `N/A (class)` | N/A (class) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps` | domain_class | EXPOSED_AND_AVAILABLE | True | True | True | True | `N/A (class)` | N/A (class) | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps` | domain_class | EXPOSED_AND_AVAILABLE | True | True | True | True | `N/A (class)` | N/A (class) | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.add` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(a, b)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.create` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(value)` | Fraction  # not JSON serializable; use the to_exact adapter | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.div` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(a, b)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.from_parts` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(numerator, denominator=1)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.mul` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(a, b)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.sub` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(a, b)` | Fraction | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.to_exact` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(value)` | int \| str  # integer or irreducible 'p/q' | `core/prompts/domain_function_library.py` |
| Fraction | `FractionOps.to_latex` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(val, mixed=False)` | str | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.add` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(a, b)` | int | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.fmt_num` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(n)` | str | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.is_divisible` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(a, b)` | bool | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.op_to_latex` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(op_str)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.random_nonzero` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(min_val, max_val)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.safe_eval` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(expr)` | int \| float  # bool and container results raise ValueError | `core/prompts/domain_function_library.py` |
| Integer | `IntegerOps.sub` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(a, b)` | int | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.add` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, c2)` | list[number]  # operand-dependent coefficient type; highest degree first | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.coeffs_from_py_expression` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(expression, var='x')` | list[Fraction]  # highest degree first | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.div_qr` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(dividend_coefficients, divisor_coefficients)` | tuple[list[int \| str], list[int \| str]]  # quotient,remainder | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.factor_quadratic_exact` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(a, b, c)` | list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; N | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.format_latex` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(coeffs, var='x')` | str | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.format_plain` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeffs, var='x')` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.mul` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, c2)` | list[int \| float \| Fraction]  # operand-dependent; highest degree first | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.normalize` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeffs)` | list[number]  # highest degree first; leading zeros removed | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.random_poly` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(degree, range_val=(-5, 5))` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.sub` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, c2)` | list[number]  # operand-dependent coefficient type; highest degree first | `core/prompts/domain_function_library.py` |
| Polynomial | `PolynomialOps.to_degree_map` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeffs)` | dict[str, int \| str]  # descending degree insertion order | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.add_dicts` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms1, terms2)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.add_term` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms_dict, coeff, radicand)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.create` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(inner)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.div_terms` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, r1, c2, r2)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.format_expression` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms_dict, denominator=1)` | str  # complete compound-radical LaTeX | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.format_term` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeff, radicand, is_first=True)` | str  # complete single-term LaTeX including coefficient/sign | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.format_term_unsimplified` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeff, radicand, is_first=True, wrap_negative_non_leading=False, is_leading=None)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.get_prime_factors` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(n)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.is_perfect_square` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(n)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.mul_terms` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(c1, r1, c2, r2)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.multiply_dicts` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms1, terms2)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.normalize_term_list` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(terms)` | list[dict]  # sorted; keys coefficient,radicand | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.rationalize_linear_denominator` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(numerator, denom_rational, denom_radical_coeff, radicand)` | tuple[int \| Fraction, int \| Fraction, int] | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.simplify` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(coeff, radicand)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.simplify_root` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(radicand)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.simplify_term` | class_method | EXPOSED_AND_AVAILABLE | True | True | True | True | `(coeff, radicand)` | tuple[int \| Fraction, int]  # semantic (coefficient, square-free radicand) | `core/prompts/domain_function_library.py` |
| Radical | `RadicalOps.to_latex` | class_method | AVAILABLE_NOT_EXPOSED | False | True | False | False | `(expr)` | UNRESOLVED (no DOMAIN_API_SSOT; see runtime only) | `core/prompts/domain_function_library.py` |
| UNRESOLVED | `get_domain_helpers_code` | global_function | AVAILABLE_NOT_EXPOSED | False | False | False | False | `(domains, stub_mode=True)` | UNRESOLVED (not Math16 model-facing) | `core/prompts/domain_function_library.py` |
| UNRESOLVED | `get_required_domains` | global_function | AVAILABLE_NOT_EXPOSED | False | False | False | False | `(skill_id)` | UNRESOLVED (not Math16 model-facing) | `core/prompts/domain_function_library.py` |

## Per-task exposure map

### Ab2d+api

| task_id | domain | exposed methods |
|---|---|---|
| `ce111_nonchoice_q01_part1_exponential_growth` | Integer | `IntegerOps.safe_eval`, `IntegerOps.fmt_num` |
| `ce111_q02_polynomial_division_remainder` | Polynomial | `PolynomialOps.div_qr`, `PolynomialOps.format_latex` |
| `ce111_q03_prime_factor_selection` | Integer | `IntegerOps.is_divisible`, `IntegerOps.safe_eval` |
| `ce111_q05_exact_fraction_expression` | Fraction | `FractionOps.create`, `FractionOps.add`, `FractionOps.to_latex` |
| `ce111_q08_polynomial_factor_parameter_recovery` | Polynomial | `PolynomialOps.mul`, `FractionOps.create` |
| `ce111_q10_ordered_quadratic_roots_radical` | Radical | `RadicalOps.simplify_term`, `FractionOps.create`, `RadicalOps.format_expression` |
| `ce112_q01_negative_integer_power` | Integer | `IntegerOps.safe_eval`, `IntegerOps.fmt_num` |
| `ce112_q04_radical_simplification` | Radical | `RadicalOps.simplify_term`, `RadicalOps.format_term` |
| `ce112_q09_divisor_multiple_intersection` | Integer | `IntegerOps.is_divisible`, `IntegerOps.safe_eval` |
| `ce112_q12_independent_probability_fraction` | Fraction | `FractionOps.create`, `FractionOps.mul`, `FractionOps.to_latex` |
| `ce113_q01_negative_fraction_subtraction` | Fraction | `FractionOps.create`, `FractionOps.sub`, `FractionOps.to_latex` |
| `ce113_q11_rationalize_denominator` | Radical | `FractionOps.create`, `FractionOps.mul`, `FractionOps.add` |
| `ce115_calc_exact_rational_expression_l1` | Fraction | `FractionOps.create`, `FractionOps.mul`, `FractionOps.add` |
| `ce115_calc_polynomial_division_l1` | Polynomial | `PolynomialOps.div_qr` |
| `ce115_calc_polynomial_factor_roots_l1` | Polynomial | `PolynomialOps.factor_quadratic_exact`, `FractionOps.create` |
| `ce115_calc_radical_simplification_l1` | Radical | `RadicalOps.simplify_term` |

### Ab2d+spec

| task_id | domain | native_only | cards | exposed methods |
|---|---|---|---|---|
| `ce111_nonchoice_q01_part1_exponential_growth` | Integer | True | False | (none) |
| `ce111_q02_polynomial_division_remainder` | Polynomial | False | True | `PolynomialOps.div_qr`, `PolynomialOps.format_latex` |
| `ce111_q03_prime_factor_selection` | Integer | True | False | (none) |
| `ce111_q05_exact_fraction_expression` | Fraction | False | True | `FractionOps.add`, `FractionOps.create`, `FractionOps.from_parts`, `FractionOps.sub` |
| `ce111_q08_polynomial_factor_parameter_recovery` | Polynomial | True | True | `PolynomialOps.format_latex` |
| `ce111_q10_ordered_quadratic_roots_radical` | Radical | False | False | `RadicalOps.simplify_term` |
| `ce112_q01_negative_integer_power` | Integer | True | False | (none) |
| `ce112_q04_radical_simplification` | Radical | False | False | `RadicalOps.simplify_term` |
| `ce112_q09_divisor_multiple_intersection` | Integer | True | False | (none) |
| `ce112_q12_independent_probability_fraction` | Fraction | False | True | `FractionOps.add`, `FractionOps.create`, `FractionOps.from_parts`, `FractionOps.mul` |
| `ce113_q01_negative_fraction_subtraction` | Fraction | False | True | `FractionOps.add`, `FractionOps.create`, `FractionOps.from_parts`, `FractionOps.sub` |
| `ce113_q11_rationalize_denominator` | Radical | True | False | (none) |
| `ce115_calc_exact_rational_expression_l1` | Fraction | False | False | `FractionOps.add`, `FractionOps.create`, `FractionOps.mul`, `FractionOps.sub` |
| `ce115_calc_polynomial_division_l1` | Polynomial | False | False | `PolynomialOps.div_qr` |
| `ce115_calc_polynomial_factor_roots_l1` | Polynomial | True | False | (none) |
| `ce115_calc_radical_simplification_l1` | Radical | False | False | `RadicalOps.simplify_term` |

## Freeze preparation (not frozen yet)

This inventory is a **draft**. Future freeze should lock the evidence sources listed in the registry `freeze_preparation.future_freeze_should_lock` and pin their SHA-256 together with HEAD.

- Machine registry: `docs/experiments/manifests/math16_domain_api_contract_registry_v1.json`
- Consistency audit: `docs/experiments/reports/math16_prompt_runtime_api_consistency_audit_v1.md`

