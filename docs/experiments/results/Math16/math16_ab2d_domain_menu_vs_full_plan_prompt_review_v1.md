# Math16 Ab2d+domain-menu vs Ab2d+full-plan Prompt Review v1

Status: **read-only audit artifact regenerated after full-plan fairness fix** (no model calls).

- Git HEAD at generation: see ending status of rebuild session
- Method 1: `Ab2d+domain-menu` (`ab2d_domain_menu`) — unchanged
- Method 2: `Ab2d+full-plan` (`ab2d_full`) — rebuilt: full domain API menu; no derived_scaffold; Processing steps only contrast
- Fairness checklist verdict: **PROMPTS_READY_FOR_HUMAN_REVIEW**
- Prior review preserved at: `docs/experiments/results/Math16/math16_ab2d_domain_menu_vs_full_plan_prompt_review_v1_BEFORE_FAIRNESS_FIX.md`
- Prior full-plan SHA snapshot: `docs/experiments/results/Math16/ab2d_full_prompt_sha_before_fairness_fix_v1.json`

## FORMAL_PROMPT_SOURCE_PATHS

| Method | Formal runner | Prompt path |
|--------|---------------|-------------|
| domain-menu | `scripts/run_math16_ab2d_domain_menu_gemini_formal.py` | `docs/experiments/prompts/ab2d_domain_menu/prompts/{task_id}.txt` |
| full-plan | `scripts/run_math16_ab2d_full_gemini_formal.py` | `docs/experiments/prompts/ab2d_full/prompts/{task_id}.txt` |

### Byte-match vs inventories

- domain-menu vs manifest: **PASS**
- full-plan vs prompt_freeze (all_match_builder=True): **PASS**

## TASK_BY_TASK_PROMPT_INDEX

| task_id | domain | method1 SHA-256 | method2 SHA-256 |
|---------|--------|-----------------|-----------------|
| `ce115_calc_polynomial_division_l1` | `PolynomialOps` | `9e735588d318628797bf3b003972ba13498f2014366a1c1cef11570a39367607` | `f37c9c5ff77ed7b4deb91bb9e495aea364b99ddf2778b25898f4a7ec11dee24f` |
| `ce115_calc_polynomial_factor_roots_l1` | `PolynomialOps` | `eebb08fb846df0a8f308765ade36772e392013e105c0f3c81daeadb6b3e247c4` | `d38ccbed3152982579cd5e464ab97ee6f3c905e3c652ab827a7bfe1a2df74cd3` |
| `ce115_calc_exact_rational_expression_l1` | `FractionOps` | `831193c0aa23758deda405a6d3eb30272136c8f6fd7fa8cec5941a9109d965e8` | `c56f17118b24853f42033c8f8f5f976b1f97d4b2e2547fd7de26f1cde9956b87` |
| `ce115_calc_radical_simplification_l1` | `RadicalOps` | `fe61cd337100d9ece6868cff0bd7f93d7e76a28510ffb5fbbacd034a32e58473` | `9ce7118e83c790d785de6d07d2e2d4bad7c2d171a5013d7217413fde5ce48475` |
| `ce111_q02_polynomial_division_remainder` | `PolynomialOps` | `7b5612143100eb49d25388a752280f9519db31f1188648f205148ca45c4c6e43` | `2a3d5f208cfa37c7819dcd1f5933e64d01ed58b73d7700f8f37e9f23fbd704c8` |
| `ce111_q08_polynomial_factor_parameter_recovery` | `PolynomialOps` | `86b2a57c410ef01e529a2415712ae784c4447bfa09625fb9da1a56dc11ae94a2` | `1de69e53f799da9f4d75c648db2dc02c184bad75227fccf65b549d6747bc6c6c` |
| `ce111_q03_prime_factor_selection` | `IntegerOps` | `67fffa8b4b443bb3a2772d3647bd08f8fc373c8741dee9f79e266604d61e486e` | `e2bbfe0c2a10590d790539a5ed947659bde76da2dbc47735af9b24dbed5cbbf8` |
| `ce112_q01_negative_integer_power` | `IntegerOps` | `8a0cbd3c75aef342d86bed21fb2cbb0c924d49ac644ba9611efabafbd1b792ef` | `28316145dae82cc09e33cc2de732a69f96e9658510f9a822a6064e1e5ffe3d95` |
| `ce112_q09_divisor_multiple_intersection` | `IntegerOps` | `9e6756e2dac0414f6b2d69b423f2077c9bd514e49f171263bd374d1a2f45bb4e` | `15a07b36e4807462ec2fb1ccdbdc899ff4882c661a1bdc10784b102b90b1e40f` |
| `ce111_nonchoice_q01_part1_exponential_growth` | `IntegerOps` | `e8ccbf8709ceaab0633daa071bd54fe787a67b34a26c37c852cf33d6f7b21f67` | `d88e3becd6f4cd35bded8aacfbbe2eb33dfd39d823294b1fde22803559a5d6c2` |
| `ce111_q05_exact_fraction_expression` | `FractionOps` | `ac1eb3f529cb45a58a426b4d2bfc57a823d4ff9757ab738c4dab16d61e2a8375` | `b78c0c06d5d3aa41e6bd36a3e55c6c34d0f145f48b67d96cdc448f4905f2fd7e` |
| `ce113_q01_negative_fraction_subtraction` | `FractionOps` | `c9fe9333195578b1ae14b1763e5ec9bc02a2f1f80b248a59d19dd131c76b86a8` | `a558b9b1d1be2162bf06c3b6e38eef42763704f5c47eb520cd259f02e1c572b2` |
| `ce112_q12_independent_probability_fraction` | `FractionOps` | `5110e0e344af83da2bcd0cfe3fdd486a3d79073764b60621ce2a4e0b46f4703f` | `e62f008b7cce301a4b57b397d7e7279bc0e4f450df2db6d85a102d64f119c7b1` |
| `ce112_q04_radical_simplification` | `RadicalOps` | `0e824d552ded8d07d15dd3367f7a98a424d7e64a3e56650cf1c5bcb0e8d0c25f` | `374b74a6c4c84ef28dc4b44ab325b54a766d5f33989fab2e6d6cc4c7384422fc` |
| `ce111_q10_ordered_quadratic_roots_radical` | `RadicalOps` | `5419a3ebc38e402140803afeb71ccb3fa385a5da9f07c6a4166a306ed91b336a` | `e82f5abefd86507f685fb40f392d089bc00eb2b6efcafc463c305b8321c33d73` |
| `ce113_q11_rationalize_denominator` | `RadicalOps` | `1992b663e3a5f69d94c3526f04eabfc0c2b10109c129c937ca5124e1aa90b2b3` | `0044b36e585078c5a9ca7c1f443f073b1395656d0a3b36e1c76f29616e7133d2` |

### Paths

- `ce115_calc_polynomial_division_l1`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_polynomial_division_l1.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_polynomial_division_l1.txt`
- `ce115_calc_polynomial_factor_roots_l1`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_polynomial_factor_roots_l1.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_polynomial_factor_roots_l1.txt`
- `ce115_calc_exact_rational_expression_l1`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_exact_rational_expression_l1.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_exact_rational_expression_l1.txt`
- `ce115_calc_radical_simplification_l1`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_radical_simplification_l1.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_radical_simplification_l1.txt`
- `ce111_q02_polynomial_division_remainder`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q02_polynomial_division_remainder.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce111_q02_polynomial_division_remainder.txt`
- `ce111_q08_polynomial_factor_parameter_recovery`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt`
- `ce111_q03_prime_factor_selection`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q03_prime_factor_selection.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce111_q03_prime_factor_selection.txt`
- `ce112_q01_negative_integer_power`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q01_negative_integer_power.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce112_q01_negative_integer_power.txt`
- `ce112_q09_divisor_multiple_intersection`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q09_divisor_multiple_intersection.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce112_q09_divisor_multiple_intersection.txt`
- `ce111_nonchoice_q01_part1_exponential_growth`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt`
- `ce111_q05_exact_fraction_expression`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q05_exact_fraction_expression.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce111_q05_exact_fraction_expression.txt`
- `ce113_q01_negative_fraction_subtraction`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce113_q01_negative_fraction_subtraction.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce113_q01_negative_fraction_subtraction.txt`
- `ce112_q12_independent_probability_fraction`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q12_independent_probability_fraction.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce112_q12_independent_probability_fraction.txt`
- `ce112_q04_radical_simplification`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q04_radical_simplification.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce112_q04_radical_simplification.txt`
- `ce111_q10_ordered_quadratic_roots_radical`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q10_ordered_quadratic_roots_radical.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce111_q10_ordered_quadratic_roots_radical.txt`
- `ce113_q11_rationalize_denominator`
  - method1: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce113_q11_rationalize_denominator.txt`
  - method2: `docs/experiments/prompts/ab2d_full/prompts/ce113_q11_rationalize_denominator.txt`

## FAIRNESS_COMPARISON

| Criterion | Result | Notes |
|-----------|--------|-------|
| task description identical | **PASS** | |
| frozen_params identical | **PASS** | |
| API implementation library identical | **PASS** | `domain_function_library` |
| domain_ops label identical | **PASS** | |
| domain API method surface identical | **PASS** | full domain SUPPORTED_PUBLIC both sides |
| domain API block byte-identical | **PASS** | markers + menu body |
| derived_scaffold present in either method | **PASS** | both absent from prompts |
| difference only task-specific Processing steps | **PASS** | full = menu + steps |
| output contract three keys both | **PASS** | shared domain-menu contract block |
| evaluator identical | **PASS** | |

### Per-task SHA before/after (full-plan)

| task_id | before SHA | after SHA |
|---------|------------|-----------|
| `ce115_calc_polynomial_division_l1` | `b95bde393d5ae1265a77ea130f7c5099689c74e415a974bac6d060c00960113a` | `f37c9c5ff77ed7b4deb91bb9e495aea364b99ddf2778b25898f4a7ec11dee24f` |
| `ce115_calc_polynomial_factor_roots_l1` | `268714a33f9cc4a4a75616f1f93d865cb0fadd16b53fd430edf2ce137ddbb1a7` | `d38ccbed3152982579cd5e464ab97ee6f3c905e3c652ab827a7bfe1a2df74cd3` |
| `ce115_calc_exact_rational_expression_l1` | `fc95648ee72559fb74669b0bb169a1723202618e72071ed5bec8454b64146b8a` | `c56f17118b24853f42033c8f8f5f976b1f97d4b2e2547fd7de26f1cde9956b87` |
| `ce115_calc_radical_simplification_l1` | `5346aa605f6f409b449379fcbdea4ec74fdfacf68342664f97b07bb2610f3f17` | `9ce7118e83c790d785de6d07d2e2d4bad7c2d171a5013d7217413fde5ce48475` |
| `ce111_q02_polynomial_division_remainder` | `f3ed68da6d6faa3d9f668641f1c229bbe1b5de5e55f66c4260af0d1e964b9985` | `2a3d5f208cfa37c7819dcd1f5933e64d01ed58b73d7700f8f37e9f23fbd704c8` |
| `ce111_q08_polynomial_factor_parameter_recovery` | `3cda39ad771454c3861a721d96a4311b9723afe58b93adf5e82343ecff9b73f0` | `1de69e53f799da9f4d75c648db2dc02c184bad75227fccf65b549d6747bc6c6c` |
| `ce111_q03_prime_factor_selection` | `83b3fc9ab6cfd8fe52f820bdeaf39f020b812850f66e927bffd3abc82c8cd259` | `e2bbfe0c2a10590d790539a5ed947659bde76da2dbc47735af9b24dbed5cbbf8` |
| `ce112_q01_negative_integer_power` | `9570e54e41e04a1178f741a349df06cf43854846123ad719041a4d4b6058dfda` | `28316145dae82cc09e33cc2de732a69f96e9658510f9a822a6064e1e5ffe3d95` |
| `ce112_q09_divisor_multiple_intersection` | `7bc834fcab6bb3f359ded846311eeb9db5b591b117e73223727a354b071369f0` | `15a07b36e4807462ec2fb1ccdbdc899ff4882c661a1bdc10784b102b90b1e40f` |
| `ce111_nonchoice_q01_part1_exponential_growth` | `00bed9ff6b68652512f58a1791aa82a4750aa67ed48db81599b0577975daf673` | `d88e3becd6f4cd35bded8aacfbbe2eb33dfd39d823294b1fde22803559a5d6c2` |
| `ce111_q05_exact_fraction_expression` | `305f180e15df88500cf3cfb78988ec7277d69d04350a78dbb2d38b366f5d1cd3` | `b78c0c06d5d3aa41e6bd36a3e55c6c34d0f145f48b67d96cdc448f4905f2fd7e` |
| `ce113_q01_negative_fraction_subtraction` | `5c4ee11da9fc18b57fc397bc1a5a8a2fc1e3656cb39ab6ef96a1d81ea388ba0a` | `a558b9b1d1be2162bf06c3b6e38eef42763704f5c47eb520cd259f02e1c572b2` |
| `ce112_q12_independent_probability_fraction` | `17c720ba834cac17148335df4bfc328da2f3f8ee2a37e1153c8c238eff218015` | `e62f008b7cce301a4b57b397d7e7279bc0e4f450df2db6d85a102d64f119c7b1` |
| `ce112_q04_radical_simplification` | `9423dccf36aecc25130ab5151822155b68fcb1c95c114b4bac2f307634682ce3` | `374b74a6c4c84ef28dc4b44ab325b54a766d5f33989fab2e6d6cc4c7384422fc` |
| `ce111_q10_ordered_quadratic_roots_radical` | `61d3f0bd5845d3f37706fb3171278e1fc388ff75360f92c40f67fb94f37507b3` | `e82f5abefd86507f685fb40f392d089bc00eb2b6efcafc463c305b8321c33d73` |
| `ce113_q11_rationalize_denominator` | `6b77d3112ddbb6a2c428846899acb2b0cf1f8654e9f5f7d3671a8065fcbbda2d` | `0044b36e585078c5a9ca7c1f443f073b1395656d0a3b36e1c76f29616e7133d2` |

## DOMAIN_MENU_AUDIT

- solution-plan hits: 0 (menu should have none beyond shared text)
- answer leak hits: 0
- cross-domain: 0

## FULL_PLAN_AUDIT

- Processing steps present: 16/16
- derived_scaffold in prompts: 0
- answer leak hits: 0
- cross-domain: 0

## ANSWER_LEAKAGE_AUDIT

- domain-menu: NO
- full-plan: NO

## CROSS_DOMAIN_ISOLATION

- domain-menu: PASS
- full-plan: PASS

## Unexpected defects

- none

---

## Per-task full prompts

## Task `ce115_calc_polynomial_division_l1` (`PolynomialOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_polynomial_division_l1.txt`
- Method1 SHA-256: `9e735588d318628797bf3b003972ba13498f2014366a1c1cef11570a39367607`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_polynomial_division_l1.txt`
- Method2 SHA-256: `f37c9c5ff77ed7b4deb91bb9e495aea364b99ddf2778b25898f4a7ec11dee24f`
- Method1 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`
- Method2 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: PolynomialOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: PolynomialOps

This menu lists every SUPPORTED_PUBLIC method on `PolynomialOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`

- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
  inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
  returns_shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
  boundary: to_degree_map or to_exact per coefficient
  example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  returns_shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
  boundary: already exact JSON leaves
  example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`

- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  returns_shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
  boundary: already JSON safe
  example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `PolynomialOps.format_latex([2, 0])  # '2x'`

- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  returns_shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: Fraction coefficients require to_exact; exact tasks must not use float
  example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`

- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
  inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
  boundary: preserves coefficient types
  example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`

- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`

- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
  inputs: non-empty exact coefficient list
  returns_shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
  boundary: official polynomial JSON adapter
  example: `PolynomialOps.to_degree_map([1, 0, -1])`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce115_calc_polynomial_division_l1`
domain_ops: `PolynomialOps`
skill_id: `math16_polynomial_division_general`

## Frozen task description (use as question_text)
將多項式
\[
6x^2+6
\]
除以
\[
x-4,
\]
求商式與餘式。

## frozen_params (oracle_payload must equal this object)
{
  "dividend_coefficients": [
    6,
    0,
    6
  ],
  "divisor_coefficients": [
    1,
    -4
  ]
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: PolynomialOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: PolynomialOps

This menu lists every SUPPORTED_PUBLIC method on `PolynomialOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`

- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
  inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
  returns_shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
  boundary: to_degree_map or to_exact per coefficient
  example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  returns_shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
  boundary: already exact JSON leaves
  example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`

- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  returns_shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
  boundary: already JSON safe
  example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `PolynomialOps.format_latex([2, 0])  # '2x'`

- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  returns_shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: Fraction coefficients require to_exact; exact tasks must not use float
  example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`

- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
  inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
  boundary: preserves coefficient types
  example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`

- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`

- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
  inputs: non-empty exact coefficient list
  returns_shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
  boundary: official polynomial JSON adapter
  example: `PolynomialOps.to_degree_map([1, 0, -1])`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce115_calc_polynomial_division_l1`
domain_ops: `PolynomialOps`
skill_id: `math16_polynomial_division_general`

## Frozen task description (use as question_text)
將多項式
\[
6x^2+6
\]
除以
\[
x-4,
\]
求商式與餘式。

## frozen_params (oracle_payload must equal this object)
{
  "dividend_coefficients": [
    6,
    0,
    6
  ],
  "divisor_coefficients": [
    1,
    -4
  ]
}

## Processing steps
1) Call PolynomialOps.div_qr on frozen coefficients.
2) Optionally format latex.
3) Assemble coefficient lists into correct_answer.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce115_calc_polynomial_factor_roots_l1` (`PolynomialOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_polynomial_factor_roots_l1.txt`
- Method1 SHA-256: `eebb08fb846df0a8f308765ade36772e392013e105c0f3c81daeadb6b3e247c4`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_polynomial_factor_roots_l1.txt`
- Method2 SHA-256: `d38ccbed3152982579cd5e464ab97ee6f3c905e3c652ab827a7bfe1a2df74cd3`
- Method1 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`
- Method2 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: PolynomialOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: PolynomialOps

This menu lists every SUPPORTED_PUBLIC method on `PolynomialOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`

- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
  inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
  returns_shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
  boundary: to_degree_map or to_exact per coefficient
  example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  returns_shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
  boundary: already exact JSON leaves
  example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`

- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  returns_shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
  boundary: already JSON safe
  example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `PolynomialOps.format_latex([2, 0])  # '2x'`

- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  returns_shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: Fraction coefficients require to_exact; exact tasks must not use float
  example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`

- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
  inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
  boundary: preserves coefficient types
  example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`

- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`

- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
  inputs: non-empty exact coefficient list
  returns_shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
  boundary: official polynomial JSON adapter
  example: `PolynomialOps.to_degree_map([1, 0, -1])`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce115_calc_polynomial_factor_roots_l1`
domain_ops: `PolynomialOps`
skill_id: `math16_polynomial_factor_roots`

## Frozen task description (use as question_text)
將一元二次方程式
\[
x^2+4x-12=0
\]
的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。

## frozen_params (oracle_payload must equal this object)
{
  "quadratic_coefficients": [
    1,
    4,
    -12
  ]
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: PolynomialOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: PolynomialOps

This menu lists every SUPPORTED_PUBLIC method on `PolynomialOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`

- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
  inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
  returns_shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
  boundary: to_degree_map or to_exact per coefficient
  example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  returns_shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
  boundary: already exact JSON leaves
  example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`

- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  returns_shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
  boundary: already JSON safe
  example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `PolynomialOps.format_latex([2, 0])  # '2x'`

- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  returns_shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: Fraction coefficients require to_exact; exact tasks must not use float
  example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`

- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
  inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
  boundary: preserves coefficient types
  example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`

- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`

- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
  inputs: non-empty exact coefficient list
  returns_shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
  boundary: official polynomial JSON adapter
  example: `PolynomialOps.to_degree_map([1, 0, -1])`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce115_calc_polynomial_factor_roots_l1`
domain_ops: `PolynomialOps`
skill_id: `math16_polynomial_factor_roots`

## Frozen task description (use as question_text)
將一元二次方程式
\[
x^2+4x-12=0
\]
的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。

## frozen_params (oracle_payload must equal this object)
{
  "quadratic_coefficients": [
    1,
    4,
    -12
  ]
}

## Processing steps
1) factor_quadratic_exact(a,b,c).
2) Convert factors to roots and sort ascending.
3) Return roots (latex optional).
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce115_calc_exact_rational_expression_l1` (`FractionOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_exact_rational_expression_l1.txt`
- Method1 SHA-256: `831193c0aa23758deda405a6d3eb30272136c8f6fd7fa8cec5941a9109d965e8`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_exact_rational_expression_l1.txt`
- Method2 SHA-256: `c56f17118b24853f42033c8f8f5f976b1f97d4b2e2547fd7de26f1cde9956b87`
- Method1 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`
- Method2 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: FractionOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: FractionOps

This menu lists every SUPPORTED_PUBLIC method on `FractionOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: FractionOps.to_exact before correct_answer
  example: `FractionOps.create("2/7")  # Fraction(2, 7)`

- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction; b != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`

- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`

- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  returns_shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
  boundary: official Fraction-to-JSON adapter
  example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`

- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only; not semantic serialization
  example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce115_calc_exact_rational_expression_l1`
domain_ops: `FractionOps`
skill_id: `math16_exact_rational_expression`

## Frozen task description (use as question_text)
精確計算
\[
2.79\times 89.3-\left(-0.21\times 89.3\right).
\]
答案不得使用近似值。

## frozen_params (oracle_payload must equal this object)
{
  "products": [
    {
      "left": "2.79",
      "right": "89.3",
      "sign": 1
    },
    {
      "left": "-0.21",
      "right": "89.3",
      "sign": -1
    }
  ]
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: FractionOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: FractionOps

This menu lists every SUPPORTED_PUBLIC method on `FractionOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: FractionOps.to_exact before correct_answer
  example: `FractionOps.create("2/7")  # Fraction(2, 7)`

- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction; b != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`

- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`

- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  returns_shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
  boundary: official Fraction-to-JSON adapter
  example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`

- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only; not semantic serialization
  example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce115_calc_exact_rational_expression_l1`
domain_ops: `FractionOps`
skill_id: `math16_exact_rational_expression`

## Frozen task description (use as question_text)
精確計算
\[
2.79\times 89.3-\left(-0.21\times 89.3\right).
\]
答案不得使用近似值。

## frozen_params (oracle_payload must equal this object)
{
  "products": [
    {
      "left": "2.79",
      "right": "89.3",
      "sign": 1
    },
    {
      "left": "-0.21",
      "right": "89.3",
      "sign": -1
    }
  ]
}

## Processing steps
1) FractionOps.create each operand string.
2) Multiply and accumulate with signs.
3) FractionOps.to_exact for value.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce115_calc_radical_simplification_l1` (`RadicalOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_radical_simplification_l1.txt`
- Method1 SHA-256: `fe61cd337100d9ece6868cff0bd7f93d7e76a28510ffb5fbbacd034a32e58473`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_radical_simplification_l1.txt`
- Method2 SHA-256: `9ce7118e83c790d785de6d07d2e2d4bad7c2d171a5013d7217413fde5ce48475`
- Method1 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`
- Method2 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: RadicalOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: RadicalOps

This menu lists every SUPPORTED_PUBLIC method on `RadicalOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects mismatched radicand or zero result coefficient
  example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`

- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: never returns str union
  example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`

- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
  inputs: mapping radicand->coefficient; exact denominator
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`

- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`

- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`

- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
  inputs: list/tuple of pairs or coefficient/radicand dicts
  returns_shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
  boundary: official radical semantic JSON adapter
  example: `RadicalOps.normalize_term_list([(1, 12)])`

- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
  boundary: RadicalOps.exact_integer on integral leaves before JSON
  example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`

- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects k==0 and zero radical_coefficient
  example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`

- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
  boundary: normalize_term_list or to_exact before JSON
  example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce115_calc_radical_simplification_l1`
domain_ops: `RadicalOps`
skill_id: `math16_radical_simplification`

## Frozen task description (use as question_text)
將
\[
\sqrt{27}
\]
化為最簡根式 \(a\sqrt{b}\)，其中 \(a\) 為正整數，且 \(b\) 不含大於 \(1\) 的完全平方因數。

## frozen_params (oracle_payload must equal this object)
{
  "radicand": 27
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: RadicalOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: RadicalOps

This menu lists every SUPPORTED_PUBLIC method on `RadicalOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects mismatched radicand or zero result coefficient
  example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`

- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: never returns str union
  example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`

- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
  inputs: mapping radicand->coefficient; exact denominator
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`

- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`

- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`

- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
  inputs: list/tuple of pairs or coefficient/radicand dicts
  returns_shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
  boundary: official radical semantic JSON adapter
  example: `RadicalOps.normalize_term_list([(1, 12)])`

- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
  boundary: RadicalOps.exact_integer on integral leaves before JSON
  example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`

- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects k==0 and zero radical_coefficient
  example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`

- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
  boundary: normalize_term_list or to_exact before JSON
  example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce115_calc_radical_simplification_l1`
domain_ops: `RadicalOps`
skill_id: `math16_radical_simplification`

## Frozen task description (use as question_text)
將
\[
\sqrt{27}
\]
化為最簡根式 \(a\sqrt{b}\)，其中 \(a\) 為正整數，且 \(b\) 不含大於 \(1\) 的完全平方因數。

## frozen_params (oracle_payload must equal this object)
{
  "radicand": 27
}

## Processing steps
1) simplify_term(1, radicand).
2) Pack coefficient/radicand; optional format_term.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce111_q02_polynomial_division_remainder` (`PolynomialOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q02_polynomial_division_remainder.txt`
- Method1 SHA-256: `7b5612143100eb49d25388a752280f9519db31f1188648f205148ca45c4c6e43`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q02_polynomial_division_remainder.txt`
- Method2 SHA-256: `2a3d5f208cfa37c7819dcd1f5933e64d01ed58b73d7700f8f37e9f23fbd704c8`
- Method1 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`
- Method2 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: PolynomialOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: PolynomialOps

This menu lists every SUPPORTED_PUBLIC method on `PolynomialOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`

- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
  inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
  returns_shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
  boundary: to_degree_map or to_exact per coefficient
  example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  returns_shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
  boundary: already exact JSON leaves
  example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`

- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  returns_shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
  boundary: already JSON safe
  example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `PolynomialOps.format_latex([2, 0])  # '2x'`

- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  returns_shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: Fraction coefficients require to_exact; exact tasks must not use float
  example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`

- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
  inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
  boundary: preserves coefficient types
  example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`

- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`

- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
  inputs: non-empty exact coefficient list
  returns_shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
  boundary: official polynomial JSON adapter
  example: `PolynomialOps.to_degree_map([1, 0, -1])`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q02_polynomial_division_remainder`
domain_ops: `PolynomialOps`
skill_id: `math16_polynomial_division_remainder_only`

## Frozen task description (use as question_text)
計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。

## frozen_params (oracle_payload must equal this object)
{
  "dividend_coefficients": [
    6,
    4,
    0
  ],
  "divisor_coefficients": [
    2,
    0,
    0
  ]
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: PolynomialOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: PolynomialOps

This menu lists every SUPPORTED_PUBLIC method on `PolynomialOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`

- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
  inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
  returns_shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
  boundary: to_degree_map or to_exact per coefficient
  example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  returns_shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
  boundary: already exact JSON leaves
  example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`

- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  returns_shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
  boundary: already JSON safe
  example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `PolynomialOps.format_latex([2, 0])  # '2x'`

- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  returns_shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: Fraction coefficients require to_exact; exact tasks must not use float
  example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`

- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
  inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
  boundary: preserves coefficient types
  example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`

- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`

- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
  inputs: non-empty exact coefficient list
  returns_shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
  boundary: official polynomial JSON adapter
  example: `PolynomialOps.to_degree_map([1, 0, -1])`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q02_polynomial_division_remainder`
domain_ops: `PolynomialOps`
skill_id: `math16_polynomial_division_remainder_only`

## Frozen task description (use as question_text)
計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。

## frozen_params (oracle_payload must equal this object)
{
  "dividend_coefficients": [
    6,
    4,
    0
  ],
  "divisor_coefficients": [
    2,
    0,
    0
  ]
}

## Processing steps
1) div_qr frozen coefficients.
2) Keep remainder only; format_latex if needed.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce111_q08_polynomial_factor_parameter_recovery` (`PolynomialOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt`
- Method1 SHA-256: `86b2a57c410ef01e529a2415712ae784c4447bfa09625fb9da1a56dc11ae94a2`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt`
- Method2 SHA-256: `1de69e53f799da9f4d75c648db2dc02c184bad75227fccf65b549d6747bc6c6c`
- Method1 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`
- Method2 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: PolynomialOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: PolynomialOps

This menu lists every SUPPORTED_PUBLIC method on `PolynomialOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`

- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
  inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
  returns_shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
  boundary: to_degree_map or to_exact per coefficient
  example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  returns_shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
  boundary: already exact JSON leaves
  example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`

- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  returns_shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
  boundary: already JSON safe
  example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `PolynomialOps.format_latex([2, 0])  # '2x'`

- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  returns_shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: Fraction coefficients require to_exact; exact tasks must not use float
  example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`

- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
  inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
  boundary: preserves coefficient types
  example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`

- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`

- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
  inputs: non-empty exact coefficient list
  returns_shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
  boundary: official polynomial JSON adapter
  example: `PolynomialOps.to_degree_map([1, 0, -1])`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q08_polynomial_factor_parameter_recovery`
domain_ops: `PolynomialOps`
skill_id: `math16_polynomial_factor_parameter_recovery`

## Frozen task description (use as question_text)
已知
\[
39x^2+5x-14=(3x+a)(bx+c),
\]
其中 \(a,b,c\) 均為整數，求 \(a+2c\)。

## frozen_params (oracle_payload must equal this object)
{
  "factor_order_policy": "strict_source_template",
  "quadratic_coefficients": [
    39,
    5,
    -14
  ],
  "template_left_x_coefficient": 3
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: PolynomialOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: PolynomialOps

This menu lists every SUPPORTED_PUBLIC method on `PolynomialOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`

- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
  inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
  returns_shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
  boundary: to_degree_map or to_exact per coefficient
  example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  returns_shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
  boundary: already exact JSON leaves
  example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`

- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  returns_shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
  boundary: already JSON safe
  example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`

- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `PolynomialOps.format_latex([2, 0])  # '2x'`

- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  returns_shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: Fraction coefficients require to_exact; exact tasks must not use float
  example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`

- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
  inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
  boundary: preserves coefficient types
  example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`

- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
  inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
  returns_shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
  boundary: use to_exact per Fraction coefficient before JSON
  example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`

- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
  inputs: non-empty exact coefficient list
  returns_shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
  boundary: official polynomial JSON adapter
  example: `PolynomialOps.to_degree_map([1, 0, -1])`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"dividend_coefficients": [2, 0, 2], "divisor_coefficients": [1, 1]}
    q, r = PolynomialOps.div_qr(
        frozen["dividend_coefficients"], frozen["divisor_coefficients"]
    )
    return {
        "question_text": "example stem",
        "correct_answer": {
            "quotient_coefficients": q,
            "remainder_coefficients": r,
            "quotient_latex": PolynomialOps.format_latex(q),
            "remainder_latex": PolynomialOps.format_latex(r),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q08_polynomial_factor_parameter_recovery`
domain_ops: `PolynomialOps`
skill_id: `math16_polynomial_factor_parameter_recovery`

## Frozen task description (use as question_text)
已知
\[
39x^2+5x-14=(3x+a)(bx+c),
\]
其中 \(a,b,c\) 均為整數，求 \(a+2c\)。

## frozen_params (oracle_payload must equal this object)
{
  "factor_order_policy": "strict_source_template",
  "quadratic_coefficients": [
    39,
    5,
    -14
  ],
  "template_left_x_coefficient": 3
}

## Processing steps
1) factor_quadratic_exact.
2) Swap so left x_coefficient equals template_left_x_coefficient.
3) Extract a,b,c and compute a+2*c with native arithmetic.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce111_q03_prime_factor_selection` (`IntegerOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q03_prime_factor_selection.txt`
- Method1 SHA-256: `67fffa8b4b443bb3a2772d3647bd08f8fc373c8741dee9f79e266604d61e486e`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q03_prime_factor_selection.txt`
- Method2 SHA-256: `e2bbfe0c2a10590d790539a5ed947659bde76da2dbc47735af9b24dbed5cbbf8`
- Method1 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`
- Method2 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: IntegerOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: IntegerOps

This menu lists every SUPPORTED_PUBLIC method on `IntegerOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.add(10, 20)  # 30`

- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
  inputs: ordered numeric n
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `IntegerOps.fmt_num(-2)  # "(-2)"`

- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  returns_shape: `{"json_safe": true, "type": "bool"}`
  boundary: not an answer integer
  example: `IntegerOps.is_divisible(21, 7)  # True`

- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  returns_shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
  boundary: filter multiples in model assembly if needed
  example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`

- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  returns_shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
  boundary: no selected/answer field
  example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`

- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
  inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
  returns_shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
  boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
  example: `IntegerOps.safe_eval("2**4")  # 16`

- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.sub(30, 8)  # 22`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q03_prime_factor_selection`
domain_ops: `IntegerOps`
skill_id: `math16_prime_factor_selection`

## Frozen task description (use as question_text)
下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？

## frozen_params (oracle_payload must equal this object)
{
  "candidates": [
    11,
    12,
    13,
    14
  ],
  "n": 156
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: IntegerOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: IntegerOps

This menu lists every SUPPORTED_PUBLIC method on `IntegerOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.add(10, 20)  # 30`

- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
  inputs: ordered numeric n
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `IntegerOps.fmt_num(-2)  # "(-2)"`

- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  returns_shape: `{"json_safe": true, "type": "bool"}`
  boundary: not an answer integer
  example: `IntegerOps.is_divisible(21, 7)  # True`

- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  returns_shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
  boundary: filter multiples in model assembly if needed
  example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`

- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  returns_shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
  boundary: no selected/answer field
  example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`

- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
  inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
  returns_shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
  boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
  example: `IntegerOps.safe_eval("2**4")  # 16`

- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.sub(30, 8)  # 22`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q03_prime_factor_selection`
domain_ops: `IntegerOps`
skill_id: `math16_prime_factor_selection`

## Frozen task description (use as question_text)
下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？

## frozen_params (oracle_payload must equal this object)
{
  "candidates": [
    11,
    12,
    13,
    14
  ],
  "n": 156
}

## Processing steps
1) IntegerOps.prime_factorization(n).
2) Choose the candidate that appears as a prime key.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce112_q01_negative_integer_power` (`IntegerOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q01_negative_integer_power.txt`
- Method1 SHA-256: `8a0cbd3c75aef342d86bed21fb2cbb0c924d49ac644ba9611efabafbd1b792ef`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce112_q01_negative_integer_power.txt`
- Method2 SHA-256: `28316145dae82cc09e33cc2de732a69f96e9658510f9a822a6064e1e5ffe3d95`
- Method1 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`
- Method2 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: IntegerOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: IntegerOps

This menu lists every SUPPORTED_PUBLIC method on `IntegerOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.add(10, 20)  # 30`

- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
  inputs: ordered numeric n
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `IntegerOps.fmt_num(-2)  # "(-2)"`

- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  returns_shape: `{"json_safe": true, "type": "bool"}`
  boundary: not an answer integer
  example: `IntegerOps.is_divisible(21, 7)  # True`

- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  returns_shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
  boundary: filter multiples in model assembly if needed
  example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`

- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  returns_shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
  boundary: no selected/answer field
  example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`

- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
  inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
  returns_shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
  boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
  example: `IntegerOps.safe_eval("2**4")  # 16`

- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.sub(30, 8)  # 22`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce112_q01_negative_integer_power`
domain_ops: `IntegerOps`
skill_id: `math16_negative_integer_power`

## Frozen task description (use as question_text)
計算
\[
(-3)^3.
\]

## frozen_params (oracle_payload must equal this object)
{
  "base": -3,
  "exponent": 3
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: IntegerOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: IntegerOps

This menu lists every SUPPORTED_PUBLIC method on `IntegerOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.add(10, 20)  # 30`

- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
  inputs: ordered numeric n
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `IntegerOps.fmt_num(-2)  # "(-2)"`

- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  returns_shape: `{"json_safe": true, "type": "bool"}`
  boundary: not an answer integer
  example: `IntegerOps.is_divisible(21, 7)  # True`

- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  returns_shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
  boundary: filter multiples in model assembly if needed
  example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`

- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  returns_shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
  boundary: no selected/answer field
  example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`

- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
  inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
  returns_shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
  boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
  example: `IntegerOps.safe_eval("2**4")  # 16`

- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.sub(30, 8)  # 22`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce112_q01_negative_integer_power`
domain_ops: `IntegerOps`
skill_id: `math16_negative_integer_power`

## Frozen task description (use as question_text)
計算
\[
(-3)^3.
\]

## frozen_params (oracle_payload must equal this object)
{
  "base": -3,
  "exponent": 3
}

## Processing steps
1) Compute base ** exponent with native arithmetic.
2) Return bare int.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce112_q09_divisor_multiple_intersection` (`IntegerOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q09_divisor_multiple_intersection.txt`
- Method1 SHA-256: `9e6756e2dac0414f6b2d69b423f2077c9bd514e49f171263bd374d1a2f45bb4e`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce112_q09_divisor_multiple_intersection.txt`
- Method2 SHA-256: `15a07b36e4807462ec2fb1ccdbdc899ff4882c661a1bdc10784b102b90b1e40f`
- Method1 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`
- Method2 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: IntegerOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: IntegerOps

This menu lists every SUPPORTED_PUBLIC method on `IntegerOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.add(10, 20)  # 30`

- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
  inputs: ordered numeric n
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `IntegerOps.fmt_num(-2)  # "(-2)"`

- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  returns_shape: `{"json_safe": true, "type": "bool"}`
  boundary: not an answer integer
  example: `IntegerOps.is_divisible(21, 7)  # True`

- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  returns_shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
  boundary: filter multiples in model assembly if needed
  example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`

- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  returns_shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
  boundary: no selected/answer field
  example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`

- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
  inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
  returns_shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
  boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
  example: `IntegerOps.safe_eval("2**4")  # 16`

- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.sub(30, 8)  # 22`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce112_q09_divisor_multiple_intersection`
domain_ops: `IntegerOps`
skill_id: `math16_divisor_multiple_intersection`

## Frozen task description (use as question_text)
有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？

## frozen_params (oracle_payload must equal this object)
{
  "divisor_of": 216,
  "multiple_of": 18
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: IntegerOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: IntegerOps

This menu lists every SUPPORTED_PUBLIC method on `IntegerOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.add(10, 20)  # 30`

- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
  inputs: ordered numeric n
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `IntegerOps.fmt_num(-2)  # "(-2)"`

- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  returns_shape: `{"json_safe": true, "type": "bool"}`
  boundary: not an answer integer
  example: `IntegerOps.is_divisible(21, 7)  # True`

- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  returns_shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
  boundary: filter multiples in model assembly if needed
  example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`

- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  returns_shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
  boundary: no selected/answer field
  example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`

- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
  inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
  returns_shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
  boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
  example: `IntegerOps.safe_eval("2**4")  # 16`

- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.sub(30, 8)  # 22`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce112_q09_divisor_multiple_intersection`
domain_ops: `IntegerOps`
skill_id: `math16_divisor_multiple_intersection`

## Frozen task description (use as question_text)
有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？

## frozen_params (oracle_payload must equal this object)
{
  "divisor_of": 216,
  "multiple_of": 18
}

## Processing steps
1) positive_divisors(divisor_of).
2) Keep values divisible by multiple_of.
3) Return {"count": len(valid)}.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce111_nonchoice_q01_part1_exponential_growth` (`IntegerOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt`
- Method1 SHA-256: `e8ccbf8709ceaab0633daa071bd54fe787a67b34a26c37c852cf33d6f7b21f67`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt`
- Method2 SHA-256: `d88e3becd6f4cd35bded8aacfbbe2eb33dfd39d823294b1fde22803559a5d6c2`
- Method1 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`
- Method2 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: IntegerOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: IntegerOps

This menu lists every SUPPORTED_PUBLIC method on `IntegerOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.add(10, 20)  # 30`

- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
  inputs: ordered numeric n
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `IntegerOps.fmt_num(-2)  # "(-2)"`

- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  returns_shape: `{"json_safe": true, "type": "bool"}`
  boundary: not an answer integer
  example: `IntegerOps.is_divisible(21, 7)  # True`

- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  returns_shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
  boundary: filter multiples in model assembly if needed
  example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`

- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  returns_shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
  boundary: no selected/answer field
  example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`

- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
  inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
  returns_shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
  boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
  example: `IntegerOps.safe_eval("2**4")  # 16`

- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.sub(30, 8)  # 22`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_nonchoice_q01_part1_exponential_growth`
domain_ops: `IntegerOps`
skill_id: `math16_exponential_growth_generation_count`

## Frozen task description (use as question_text)
從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。

## frozen_params (oracle_payload must equal this object)
{
  "days": 15,
  "hours_per_generation": 20,
  "initial": 1,
  "split_factor": 4
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: IntegerOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: IntegerOps

This menu lists every SUPPORTED_PUBLIC method on `IntegerOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.add(10, 20)  # 30`

- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
  inputs: ordered numeric n
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `IntegerOps.fmt_num(-2)  # "(-2)"`

- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  returns_shape: `{"json_safe": true, "type": "bool"}`
  boundary: not an answer integer
  example: `IntegerOps.is_divisible(21, 7)  # True`

- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  returns_shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
  boundary: filter multiples in model assembly if needed
  example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`

- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  returns_shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
  boundary: no selected/answer field
  example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`

- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
  inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
  returns_shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
  boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
  example: `IntegerOps.safe_eval("2**4")  # 16`

- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
  inputs: a,b: int; bool forbidden
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: none
  example: `IntegerOps.sub(30, 8)  # 22`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"n": 12, "candidates": [2, 7, 11]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_nonchoice_q01_part1_exponential_growth`
domain_ops: `IntegerOps`
skill_id: `math16_exponential_growth_generation_count`

## Frozen task description (use as question_text)
從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。

## frozen_params (oracle_payload must equal this object)
{
  "days": 15,
  "hours_per_generation": 20,
  "initial": 1,
  "split_factor": 4
}

## Processing steps
1) total_hours = days * 24.
2) Ensure divisible by hours_per_generation.
3) k = total_hours // hours_per_generation; return {"k": k}.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce111_q05_exact_fraction_expression` (`FractionOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q05_exact_fraction_expression.txt`
- Method1 SHA-256: `ac1eb3f529cb45a58a426b4d2bfc57a823d4ff9757ab738c4dab16d61e2a8375`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q05_exact_fraction_expression.txt`
- Method2 SHA-256: `b78c0c06d5d3aa41e6bd36a3e55c6c34d0f145f48b67d96cdc448f4905f2fd7e`
- Method1 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`
- Method2 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: FractionOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: FractionOps

This menu lists every SUPPORTED_PUBLIC method on `FractionOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: FractionOps.to_exact before correct_answer
  example: `FractionOps.create("2/7")  # Fraction(2, 7)`

- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction; b != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`

- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`

- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  returns_shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
  boundary: official Fraction-to-JSON adapter
  example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`

- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only; not semantic serialization
  example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q05_exact_fraction_expression`
domain_ops: `FractionOps`
skill_id: `math16_exact_fraction_expression`

## Frozen task description (use as question_text)
精確計算
\[
\frac{9}{22}+\frac{11}{18}
-\left(\frac{23}{22}-\frac{7}{18}\right).
\]
答案須化為最簡分數。

## frozen_params (oracle_payload must equal this object)
{
  "expression": "9/22 + 11/18 - (23/22 - 7/18)"
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: FractionOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: FractionOps

This menu lists every SUPPORTED_PUBLIC method on `FractionOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: FractionOps.to_exact before correct_answer
  example: `FractionOps.create("2/7")  # Fraction(2, 7)`

- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction; b != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`

- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`

- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  returns_shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
  boundary: official Fraction-to-JSON adapter
  example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`

- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only; not semantic serialization
  example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q05_exact_fraction_expression`
domain_ops: `FractionOps`
skill_id: `math16_exact_fraction_expression`

## Frozen task description (use as question_text)
精確計算
\[
\frac{9}{22}+\frac{11}{18}
-\left(\frac{23}{22}-\frac{7}{18}\right).
\]
答案須化為最簡分數。

## frozen_params (oracle_payload must equal this object)
{
  "expression": "9/22 + 11/18 - (23/22 - 7/18)"
}

## Processing steps
1) From the frozen expression, construct each fraction leaf with FractionOps.from_parts.
2) Evaluate the expression tree with FractionOps.add and FractionOps.sub (outer subtraction of the parenthesized difference).
3) Return numerator/denominator (+ optional FractionOps.to_latex).
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce113_q01_negative_fraction_subtraction` (`FractionOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce113_q01_negative_fraction_subtraction.txt`
- Method1 SHA-256: `c9fe9333195578b1ae14b1763e5ec9bc02a2f1f80b248a59d19dd131c76b86a8`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce113_q01_negative_fraction_subtraction.txt`
- Method2 SHA-256: `a558b9b1d1be2162bf06c3b6e38eef42763704f5c47eb520cd259f02e1c572b2`
- Method1 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`
- Method2 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: FractionOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: FractionOps

This menu lists every SUPPORTED_PUBLIC method on `FractionOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: FractionOps.to_exact before correct_answer
  example: `FractionOps.create("2/7")  # Fraction(2, 7)`

- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction; b != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`

- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`

- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  returns_shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
  boundary: official Fraction-to-JSON adapter
  example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`

- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only; not semantic serialization
  example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce113_q01_negative_fraction_subtraction`
domain_ops: `FractionOps`
skill_id: `math16_negative_fraction_subtraction`

## Frozen task description (use as question_text)
精確計算
\[
\frac{3}{7}-\left(-\frac{1}{4}\right).
\]
答案須化為最簡分數。

## frozen_params (oracle_payload must equal this object)
{
  "expression": "3/7 - (-1/4)"
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: FractionOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: FractionOps

This menu lists every SUPPORTED_PUBLIC method on `FractionOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: FractionOps.to_exact before correct_answer
  example: `FractionOps.create("2/7")  # Fraction(2, 7)`

- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction; b != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`

- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`

- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  returns_shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
  boundary: official Fraction-to-JSON adapter
  example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`

- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only; not semantic serialization
  example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce113_q01_negative_fraction_subtraction`
domain_ops: `FractionOps`
skill_id: `math16_negative_fraction_subtraction`

## Frozen task description (use as question_text)
精確計算
\[
\frac{3}{7}-\left(-\frac{1}{4}\right).
\]
答案須化為最簡分數。

## frozen_params (oracle_payload must equal this object)
{
  "expression": "3/7 - (-1/4)"
}

## Processing steps
1) Construct both operands from the frozen expression with FractionOps.from_parts (preserve the negative numerator).
2) Compute FractionOps.sub(left, right).
3) Return numerator/denominator (+ optional FractionOps.to_latex).
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce112_q12_independent_probability_fraction` (`FractionOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q12_independent_probability_fraction.txt`
- Method1 SHA-256: `5110e0e344af83da2bcd0cfe3fdd486a3d79073764b60621ce2a4e0b46f4703f`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce112_q12_independent_probability_fraction.txt`
- Method2 SHA-256: `e62f008b7cce301a4b57b397d7e7279bc0e4f450df2db6d85a102d64f119c7b1`
- Method1 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`
- Method2 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: FractionOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: FractionOps

This menu lists every SUPPORTED_PUBLIC method on `FractionOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: FractionOps.to_exact before correct_answer
  example: `FractionOps.create("2/7")  # Fraction(2, 7)`

- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction; b != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`

- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`

- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  returns_shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
  boundary: official Fraction-to-JSON adapter
  example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`

- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only; not semantic serialization
  example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce112_q12_independent_probability_fraction`
domain_ops: `FractionOps`
skill_id: `math16_independent_probability_fraction`

## Frozen task description (use as question_text)
第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。

## frozen_params (oracle_payload must equal this object)
{
  "p1": [
    2,
    6
  ],
  "p2": [
    1,
    5
  ]
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: FractionOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: FractionOps

This menu lists every SUPPORTED_PUBLIC method on `FractionOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: FractionOps.to_exact before correct_answer
  example: `FractionOps.create("2/7")  # Fraction(2, 7)`

- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction; b != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`

- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`

- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  returns_shape: `{"json_safe": false, "type": "Fraction"}`
  boundary: to_exact before correct_answer
  example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`

- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  returns_shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
  boundary: official Fraction-to-JSON adapter
  example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`

- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only; not semantic serialization
  example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"p1": [1, 6], "p2": [1, 3]}
    a = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    b = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    value = FractionOps.mul(a, b)
    return {
        "question_text": "example stem",
        "correct_answer": {
            "numerator": value.numerator,
            "denominator": value.denominator,
            "canonical_latex": FractionOps.to_latex(value),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce112_q12_independent_probability_fraction`
domain_ops: `FractionOps`
skill_id: `math16_independent_probability_fraction`

## Frozen task description (use as question_text)
第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。

## frozen_params (oracle_payload must equal this object)
{
  "p1": [
    2,
    6
  ],
  "p2": [
    1,
    5
  ]
}

## Processing steps
1) from_parts for p1 and p2.
2) mul; return numerator/denominator.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce112_q04_radical_simplification` (`RadicalOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q04_radical_simplification.txt`
- Method1 SHA-256: `0e824d552ded8d07d15dd3367f7a98a424d7e64a3e56650cf1c5bcb0e8d0c25f`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce112_q04_radical_simplification.txt`
- Method2 SHA-256: `374b74a6c4c84ef28dc4b44ab325b54a766d5f33989fab2e6d6cc4c7384422fc`
- Method1 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`
- Method2 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: RadicalOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: RadicalOps

This menu lists every SUPPORTED_PUBLIC method on `RadicalOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects mismatched radicand or zero result coefficient
  example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`

- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: never returns str union
  example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`

- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
  inputs: mapping radicand->coefficient; exact denominator
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`

- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`

- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`

- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
  inputs: list/tuple of pairs or coefficient/radicand dicts
  returns_shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
  boundary: official radical semantic JSON adapter
  example: `RadicalOps.normalize_term_list([(1, 12)])`

- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
  boundary: RadicalOps.exact_integer on integral leaves before JSON
  example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`

- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects k==0 and zero radical_coefficient
  example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`

- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
  boundary: normalize_term_list or to_exact before JSON
  example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce112_q04_radical_simplification`
domain_ops: `RadicalOps`
skill_id: `math16_radical_simplification_fixed`

## Frozen task description (use as question_text)
將
\[
\sqrt{135}
\]
化為最簡根式。

## frozen_params (oracle_payload must equal this object)
{
  "radicand": 135
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: RadicalOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: RadicalOps

This menu lists every SUPPORTED_PUBLIC method on `RadicalOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects mismatched radicand or zero result coefficient
  example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`

- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: never returns str union
  example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`

- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
  inputs: mapping radicand->coefficient; exact denominator
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`

- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`

- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`

- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
  inputs: list/tuple of pairs or coefficient/radicand dicts
  returns_shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
  boundary: official radical semantic JSON adapter
  example: `RadicalOps.normalize_term_list([(1, 12)])`

- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
  boundary: RadicalOps.exact_integer on integral leaves before JSON
  example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`

- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects k==0 and zero radical_coefficient
  example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`

- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
  boundary: normalize_term_list or to_exact before JSON
  example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce112_q04_radical_simplification`
domain_ops: `RadicalOps`
skill_id: `math16_radical_simplification_fixed`

## Frozen task description (use as question_text)
將
\[
\sqrt{135}
\]
化為最簡根式。

## frozen_params (oracle_payload must equal this object)
{
  "radicand": 135
}

## Processing steps
1) simplify_term(1, radicand).
2) Pack coefficient/radicand.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce111_q10_ordered_quadratic_roots_radical` (`RadicalOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q10_ordered_quadratic_roots_radical.txt`
- Method1 SHA-256: `5419a3ebc38e402140803afeb71ccb3fa385a5da9f07c6a4166a306ed91b336a`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q10_ordered_quadratic_roots_radical.txt`
- Method2 SHA-256: `e82f5abefd86507f685fb40f392d089bc00eb2b6efcafc463c305b8321c33d73`
- Method1 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`
- Method2 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: RadicalOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: RadicalOps

This menu lists every SUPPORTED_PUBLIC method on `RadicalOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects mismatched radicand or zero result coefficient
  example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`

- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: never returns str union
  example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`

- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
  inputs: mapping radicand->coefficient; exact denominator
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`

- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`

- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`

- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
  inputs: list/tuple of pairs or coefficient/radicand dicts
  returns_shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
  boundary: official radical semantic JSON adapter
  example: `RadicalOps.normalize_term_list([(1, 12)])`

- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
  boundary: RadicalOps.exact_integer on integral leaves before JSON
  example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`

- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects k==0 and zero radical_coefficient
  example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`

- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
  boundary: normalize_term_list or to_exact before JSON
  example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q10_ordered_quadratic_roots_radical`
domain_ops: `RadicalOps`
skill_id: `math16_ordered_quadratic_roots_radical`

## Frozen task description (use as question_text)
一元二次方程式
\[
(x-2)^2=3
\]
的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。

## frozen_params (oracle_payload must equal this object)
{
  "equation": "(x-2)^2=3",
  "order": "a>b",
  "target": "2a+b"
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: RadicalOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: RadicalOps

This menu lists every SUPPORTED_PUBLIC method on `RadicalOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects mismatched radicand or zero result coefficient
  example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`

- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: never returns str union
  example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`

- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
  inputs: mapping radicand->coefficient; exact denominator
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`

- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`

- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`

- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
  inputs: list/tuple of pairs or coefficient/radicand dicts
  returns_shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
  boundary: official radical semantic JSON adapter
  example: `RadicalOps.normalize_term_list([(1, 12)])`

- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
  boundary: RadicalOps.exact_integer on integral leaves before JSON
  example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`

- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects k==0 and zero radical_coefficient
  example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`

- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
  boundary: normalize_term_list or to_exact before JSON
  example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce111_q10_ordered_quadratic_roots_radical`
domain_ops: `RadicalOps`
skill_id: `math16_ordered_quadratic_roots_radical`

## Frozen task description (use as question_text)
一元二次方程式
\[
(x-2)^2=3
\]
的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。

## frozen_params (oracle_payload must equal this object)
{
  "equation": "(x-2)^2=3",
  "order": "a>b",
  "target": "2a+b"
}

## Processing steps
1) From the frozen shifted-square equation, form the two LinearRadical roots with native arithmetic; order them so the larger root is first (a > b).
2) Call RadicalOps.scale_linear_radical on the larger root with weight 2; then RadicalOps.add_linear_radicals with the smaller root.
3) Assemble the nested or flat result dict (optional RadicalOps.format_linear_radical).
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## Task `ce113_q11_rationalize_denominator` (`RadicalOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce113_q11_rationalize_denominator.txt`
- Method1 SHA-256: `1992b663e3a5f69d94c3526f04eabfc0c2b10109c129c937ca5124e1aa90b2b3`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce113_q11_rationalize_denominator.txt`
- Method2 SHA-256: `0044b36e585078c5a9ca7c1f443f073b1395656d0a3b36e1c76f29616e7133d2`
- Method1 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`
- Method2 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`

### Method 1 — Ab2d+domain-menu (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: RadicalOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: RadicalOps

This menu lists every SUPPORTED_PUBLIC method on `RadicalOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects mismatched radicand or zero result coefficient
  example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`

- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: never returns str union
  example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`

- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
  inputs: mapping radicand->coefficient; exact denominator
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`

- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`

- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`

- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
  inputs: list/tuple of pairs or coefficient/radicand dicts
  returns_shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
  boundary: official radical semantic JSON adapter
  example: `RadicalOps.normalize_term_list([(1, 12)])`

- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
  boundary: RadicalOps.exact_integer on integral leaves before JSON
  example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`

- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects k==0 and zero radical_coefficient
  example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`

- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
  boundary: normalize_term_list or to_exact before JSON
  example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce113_q11_rationalize_denominator`
domain_ops: `RadicalOps`
skill_id: `math16_rationalize_denominator_ab_sum`

## Frozen task description (use as question_text)
將
\[
\frac{9}{4-\sqrt{7}}
\]
化為 \(a+b\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)。

## frozen_params (oracle_payload must equal this object)
{
  "denominator": "4-sqrt(7)",
  "numerator": 9,
  "radicand": 7
}
```

### Method 2 — Ab2d+full-plan / `ab2d_full` (complete prompt)

```text
# Math16 Ab2d+domain-menu
Write only Python source implementing `def generate(level=1, **kwargs):`.
Use only the Domain API methods listed in the Domain API menu below for this domain.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id;
prescribed per-item API sequences (none are provided — choose APIs yourself).
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

Domain for this task: RadicalOps.

<!-- DOMAIN_API_BLOCK_BEGIN -->
# Domain API menu: RadicalOps

This menu lists every SUPPORTED_PUBLIC method on `RadicalOps`.
It is domain-general: it does not name a Math16 task, prescribe which
APIs a specific item must call, or give call order / solution steps.

## Public APIs
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects mismatched radicand or zero result coefficient
  example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`

- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  returns_shape: `{"json_safe": true, "type": "int"}`
  boundary: never returns str union
  example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`

- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
  inputs: mapping radicand->coefficient; exact denominator
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`

- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`

- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  returns_shape: `{"json_safe": true, "type": "str"}`
  boundary: presentation only
  example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`

- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
  inputs: list/tuple of pairs or coefficient/radicand dicts
  returns_shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
  boundary: official radical semantic JSON adapter
  example: `RadicalOps.normalize_term_list([(1, 12)])`

- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
  boundary: RadicalOps.exact_integer on integral leaves before JSON
  example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`

- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  returns_shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
  boundary: rejects k==0 and zero radical_coefficient
  example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`

- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  returns_shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
  boundary: normalize_term_list or to_exact before JSON
  example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`

## Generic domain code example (non-formal numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Generic illustration only — not a Math16 formal item.
    frozen = {"radicand": 50}
    coeff, rest = RadicalOps.simplify_term(1, frozen["radicand"])
    return {
        "question_text": "example stem",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(coeff, rest),
        },
        "oracle_payload": frozen,
    }
```

## Shared output contract
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
- question_text: the provided stem string (do not rebuild from scratch unless required).
- correct_answer: JSON-compatible value matching the task answer shape.
- oracle_payload: must exactly equal the frozen_params object provided in the task block.
Do not read audit payloads, evaluator expected answers, or answer tables.
<!-- DOMAIN_API_BLOCK_END -->

## Task
task_id: `ce113_q11_rationalize_denominator`
domain_ops: `RadicalOps`
skill_id: `math16_rationalize_denominator_ab_sum`

## Frozen task description (use as question_text)
將
\[
\frac{9}{4-\sqrt{7}}
\]
化為 \(a+b\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)。

## frozen_params (oracle_payload must equal this object)
{
  "denominator": "4-sqrt(7)",
  "numerator": 9,
  "radicand": 7
}

## Processing steps
1) Interpret the frozen denominator as (denom_rational) + (denom_radical_coeff)*sqrt(radicand); call RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand).
2) RadicalOps.exact_integer on both returned coefficients.
3) Native int add for final bare answer.
```

### Diff summary

- Domain API blocks are byte-identical across methods.
- Full-plan equals domain-menu plus ## Processing steps only.
- Stem and frozen_params match pool and each other.

---

## REVIEW_DOCUMENT_PATH

`docs/experiments/results/Math16/math16_ab2d_domain_menu_vs_full_plan_prompt_review_v1.md`

## FINAL_VERDICT

**PROMPTS_READY_FOR_HUMAN_REVIEW**

