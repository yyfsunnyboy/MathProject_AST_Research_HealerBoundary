# Math16 Ab2d+domain-menu vs Ab2d+full-plan Prompt Review v1

Status: **read-only audit artifact** (no model calls; no frozen prompt mutations).

- Git HEAD at generation: `0441a733ee1a96843a3f513ed72a7f20be895ebf`
- Method 1 label: `Ab2d+domain-menu` (`condition=ab2d_domain_menu`)
- Method 2 label: `Ab2d+full-plan` (formal condition `ab2d_full`; prompts under `ab2d_full/prompts`)
- FINAL_VERDICT (audit): **PROMPT_FAIRNESS_DEFECT_FOUND**

## FORMAL_PROMPT_SOURCE_PATHS

| Method | Formal runner | Prompt path pattern | Evidence |
|--------|---------------|---------------------|----------|
| Ab2d+domain-menu | `scripts/run_math16_ab2d_domain_menu_gemini_formal.py` | `docs/experiments/prompts/ab2d_domain_menu/prompts/{task_id}.txt` | Runner imports `PROMPT_DIR_REL` and reports it via `--integration-check`; manifest `docs/experiments/prompts/ab2d_domain_menu/manifest.json`. Note: `--execute-api` currently blocked (skeleton), but designated formal prompt inventory is this directory. |
| Ab2d+full-plan (`ab2d_full`) | `scripts/run_math16_ab2d_full_gemini_formal.py` | `docs/experiments/prompts/ab2d_full/prompts/{task_id}.txt` | `PROMPT_DIR` at runner L56; live read at L287–288. Preregistration freeze: `artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/prompt_freeze.json` (all_match_builder=True). |

### Byte-match vs formal inventories

- domain-menu files vs manifest SHA: **PASS**
- ab2d_full files vs prompt_freeze SHA: **PASS**

## TASK_BY_TASK_PROMPT_INDEX

| task_id | domain | method1 SHA-256 | method2 SHA-256 |
|---------|--------|-----------------|-----------------|
| `ce115_calc_polynomial_division_l1` | `PolynomialOps` | `9e735588d318628797bf3b003972ba13498f2014366a1c1cef11570a39367607` | `eaae14350613c40bd7729ae3400c02956c05aec73f218eb5dcd8ac1d9a83764a` |
| `ce115_calc_polynomial_factor_roots_l1` | `PolynomialOps` | `eebb08fb846df0a8f308765ade36772e392013e105c0f3c81daeadb6b3e247c4` | `2d1806b3f5831ee364008f31ed25826f2357f8434c77a759c1e4ea81fbda9b17` |
| `ce115_calc_exact_rational_expression_l1` | `FractionOps` | `831193c0aa23758deda405a6d3eb30272136c8f6fd7fa8cec5941a9109d965e8` | `1ede9528c83a9008a47c742914e148fec27af7be669d756b739cb9c791af53e7` |
| `ce115_calc_radical_simplification_l1` | `RadicalOps` | `fe61cd337100d9ece6868cff0bd7f93d7e76a28510ffb5fbbacd034a32e58473` | `f0fb1f6164e443f941d983b8445b3c22cc9739fea6ce8cc03d5c7acf59e77508` |
| `ce111_q02_polynomial_division_remainder` | `PolynomialOps` | `7b5612143100eb49d25388a752280f9519db31f1188648f205148ca45c4c6e43` | `7f94bfff701f33cfe4a7211729637fa87442e3ab2e95471fed4f9cb1217a8f02` |
| `ce111_q08_polynomial_factor_parameter_recovery` | `PolynomialOps` | `86b2a57c410ef01e529a2415712ae784c4447bfa09625fb9da1a56dc11ae94a2` | `c009f8e965f36e0a1bc101f214a7857de08065c5b3c7f9c3e91150477fc78ca2` |
| `ce111_q03_prime_factor_selection` | `IntegerOps` | `67fffa8b4b443bb3a2772d3647bd08f8fc373c8741dee9f79e266604d61e486e` | `20576ca89bb9e34d5436188c8e9828b577a0b6ee2bb9ca6906b34c66fa97c029` |
| `ce112_q01_negative_integer_power` | `IntegerOps` | `8a0cbd3c75aef342d86bed21fb2cbb0c924d49ac644ba9611efabafbd1b792ef` | `7fd27537f6e302fee6852f9b233285c8236b897e5b368ea33fc3051c1692b541` |
| `ce112_q09_divisor_multiple_intersection` | `IntegerOps` | `9e6756e2dac0414f6b2d69b423f2077c9bd514e49f171263bd374d1a2f45bb4e` | `4c6c5e583ce2094292371b438cd299674e98e39fec604e27cc8e2c58d92dc587` |
| `ce111_nonchoice_q01_part1_exponential_growth` | `IntegerOps` | `e8ccbf8709ceaab0633daa071bd54fe787a67b34a26c37c852cf33d6f7b21f67` | `0ec59429b50e121db39ddfa493c44cbe13639b1db8dbc6c776c34d2f8df801c2` |
| `ce111_q05_exact_fraction_expression` | `FractionOps` | `ac1eb3f529cb45a58a426b4d2bfc57a823d4ff9757ab738c4dab16d61e2a8375` | `1806688f141d3f2ab10b2c880ca9661bfce288360c403770eb69e0d3ae2e9c08` |
| `ce113_q01_negative_fraction_subtraction` | `FractionOps` | `c9fe9333195578b1ae14b1763e5ec9bc02a2f1f80b248a59d19dd131c76b86a8` | `95f4d32f90da7816e9bb74e5c070d26aedb0a7de68909be1e739f6be7a16cf14` |
| `ce112_q12_independent_probability_fraction` | `FractionOps` | `5110e0e344af83da2bcd0cfe3fdd486a3d79073764b60621ce2a4e0b46f4703f` | `3f1000e5b94d8675382e8018a53fb908f0f100fe63f952d6e9f97a774e864645` |
| `ce112_q04_radical_simplification` | `RadicalOps` | `0e824d552ded8d07d15dd3367f7a98a424d7e64a3e56650cf1c5bcb0e8d0c25f` | `2868ba929d5169e1bf70fcc920bec4d16c87152659638bd1239c3998db0f1599` |
| `ce111_q10_ordered_quadratic_roots_radical` | `RadicalOps` | `5419a3ebc38e402140803afeb71ccb3fa385a5da9f07c6a4166a306ed91b336a` | `b17be4134859201d638d3b765b5549fc9344e2e2e94973dbd3c7822fd657fa97` |
| `ce113_q11_rationalize_denominator` | `RadicalOps` | `1992b663e3a5f69d94c3526f04eabfc0c2b10109c129c937ca5124e1aa90b2b3` | `31dfa808427261107326d25322f05fb405ca531d2c9d56f325d594b1ae8dbe44` |

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
| task description (stem) identical | **PASS** | Extracted stems vs pool `math16_question_text` |
| frozen_params identical | **PASS** | Extracted JSON vs pool `frozen_params` |
| API implementation library identical | **PASS** | Both use `core.prompts.domain_function_library` |
| domain_ops label identical per task | **PASS** | Same pool `domain_ops` |
| domain API method surface identical | **FAIL** | domain-menu = full domain SUPPORTED_PUBLIC; full-plan = per-task subset / native-only |
| output contract (three keys) present both | **PASS** | `question_text`, `correct_answer`, `oracle_payload` |
| evaluator identical | **PASS** | Shared `math_task_oracles` / pool oracle types |
| difference only planning/scaffold | **FAIL** | Also differs in which domain APIs are listed |

### Fairness defect note

Under the stated fairness checklist (identical domain exposure; difference only task-specific planning/scaffold), **API method-surface inequality is a fairness defect** relative to attributing effects solely to planning/scaffold. It is also the intentional method contrast between domain-menu and full-plan. Shared baselines (stem, frozen_params, evaluator, output-contract keys, same domain_ops, same runtime library) hold.

### Per-task fairness flags

| task_id | stem | frozen | API surface same | contracts | SHA inventories |
|---------|------|--------|------------------|-----------|-----------------|
| `ce115_calc_polynomial_division_l1` | True | True | False | True | True |
| `ce115_calc_polynomial_factor_roots_l1` | True | True | False | True | True |
| `ce115_calc_exact_rational_expression_l1` | True | True | False | True | True |
| `ce115_calc_radical_simplification_l1` | True | True | False | True | True |
| `ce111_q02_polynomial_division_remainder` | True | True | False | True | True |
| `ce111_q08_polynomial_factor_parameter_recovery` | True | True | False | True | True |
| `ce111_q03_prime_factor_selection` | True | True | False | True | True |
| `ce112_q01_negative_integer_power` | True | True | False | True | True |
| `ce112_q09_divisor_multiple_intersection` | True | True | False | True | True |
| `ce111_nonchoice_q01_part1_exponential_growth` | True | True | False | True | True |
| `ce111_q05_exact_fraction_expression` | True | True | False | True | True |
| `ce113_q01_negative_fraction_subtraction` | True | True | False | True | True |
| `ce112_q12_independent_probability_fraction` | True | True | False | True | True |
| `ce112_q04_radical_simplification` | True | True | False | True | True |
| `ce111_q10_ordered_quadratic_roots_radical` | True | True | False | True | True |
| `ce113_q11_rationalize_denominator` | True | True | False | True | True |

## DOMAIN_MENU_AUDIT

- Task-specific solution-plan pattern hits: **0**
  - none
- Answer/oracle leakage hits in domain/system sections: **0**
  - none
- Cross-domain Ops exposure: **0**
  - none

## FULL_PLAN_AUDIT

- Tasks with `## Processing steps`: **16/16** (expected for full-plan)
- Solution-plan pattern hits (includes processing steps): **32**
- Answer leakage hits outside stem/frozen_params: **0**
  - none detected by distinctive-token scan
- Cross-domain Ops exposure: **0**
  - none

## ANSWER_LEAKAGE_AUDIT

| Condition | Leakage found? | Detail |
|-----------|----------------|--------|
| domain-menu | NO | Domain/system sections scanned against pool correct_answer tokens |
| full-plan | NO | System/API/steps/examples scanned; stem+frozen_params excluded as inputs |

## CROSS_DOMAIN_ISOLATION

- domain-menu: **PASS**
- full-plan: **PASS**

## Unexpected defects summary

- none beyond checklist FAIL on identical API method surface (intentional contrast)

---

## Per-task full prompts

## Task `ce115_calc_polynomial_division_l1` (`PolynomialOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_polynomial_division_l1.txt`
- Method1 SHA-256: `9e735588d318628797bf3b003972ba13498f2014366a1c1cef11570a39367607`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_polynomial_division_l1.txt`
- Method2 SHA-256: `eaae14350613c40bd7729ae3400c02956c05aec73f218eb5dcd8ac1d9a83764a`
- Method1 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`
- Method2 APIs listed: `PolynomialOps.div_qr, PolynomialOps.format_latex`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: PolynomialOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce115_calc_polynomial_division_l1`
domain_ops: PolynomialOps

## Question stem (use verbatim as question_text)
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

## Allowed Domain API
- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  notes: already exact JSON leaves
- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  notes: presentation only

## Processing steps
1) Call PolynomialOps.div_qr on frozen coefficients.
2) Optionally format latex.
3) Assemble coefficient lists into correct_answer.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=9 methods (full domain); full-plan=2 methods (task-allowed subset ['PolynomialOps.div_qr', 'PolynomialOps.format_latex']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce115_calc_polynomial_factor_roots_l1` (`PolynomialOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_polynomial_factor_roots_l1.txt`
- Method1 SHA-256: `eebb08fb846df0a8f308765ade36772e392013e105c0f3c81daeadb6b3e247c4`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_polynomial_factor_roots_l1.txt`
- Method2 SHA-256: `2d1806b3f5831ee364008f31ed25826f2357f8434c77a759c1e4ea81fbda9b17`
- Method1 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`
- Method2 APIs listed: `PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: PolynomialOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce115_calc_polynomial_factor_roots_l1`
domain_ops: PolynomialOps

## Question stem (use verbatim as question_text)
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

## Allowed Domain API
- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  notes: already JSON safe
- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  notes: Fraction coefficients require to_exact; exact tasks must not use float

## Processing steps
1) factor_quadratic_exact(a,b,c).
2) Convert factors to roots and sort ascending.
3) Return roots (latex optional).

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=9 methods (full domain); full-plan=4 methods (task-allowed subset ['PolynomialOps.factor_quadratic_exact', 'PolynomialOps.mul']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce115_calc_exact_rational_expression_l1` (`FractionOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_exact_rational_expression_l1.txt`
- Method1 SHA-256: `831193c0aa23758deda405a6d3eb30272136c8f6fd7fa8cec5941a9109d965e8`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_exact_rational_expression_l1.txt`
- Method2 SHA-256: `1ede9528c83a9008a47c742914e148fec27af7be669d756b739cb9c791af53e7`
- Method1 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`
- Method2 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: FractionOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce115_calc_exact_rational_expression_l1`
domain_ops: FractionOps

## Question stem (use verbatim as question_text)
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

## Allowed Domain API
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
  inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
  notes: FractionOps.to_exact before correct_answer
- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  notes: to_exact before correct_answer
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  notes: to_exact before correct_answer
- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  notes: to_exact before correct_answer
- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
  inputs: int, Fraction, or legal exact string; bool/float forbidden
  notes: official Fraction-to-JSON adapter
- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  notes: presentation only; not semantic serialization

## Processing steps
1) FractionOps.create each operand string.
2) Multiply and accumulate with signs.
3) FractionOps.to_exact for value.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=8 methods (full domain); full-plan=7 methods (task-allowed subset ['FractionOps.create', 'FractionOps.mul', 'FractionOps.add', 'FractionOps.sub', 'FractionOps.to_exact', 'FractionOps.to_latex']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce115_calc_radical_simplification_l1` (`RadicalOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce115_calc_radical_simplification_l1.txt`
- Method1 SHA-256: `fe61cd337100d9ece6868cff0bd7f93d7e76a28510ffb5fbbacd034a32e58473`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce115_calc_radical_simplification_l1.txt`
- Method2 SHA-256: `f0fb1f6164e443f941d983b8445b3c22cc9739fea6ce8cc03d5c7acf59e77508`
- Method1 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`
- Method2 APIs listed: `RadicalOps.format_term, RadicalOps.simplify_term`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: RadicalOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce115_calc_radical_simplification_l1`
domain_ops: RadicalOps

## Question stem (use verbatim as question_text)
將
\[
\sqrt{27}
\]
化為最簡根式 \(a\sqrt{b}\)，其中 \(a\) 為正整數，且 \(b\) 不含大於 \(1\) 的完全平方因數。

## frozen_params (oracle_payload must equal this object)
{
  "radicand": 27
}

## Allowed Domain API
- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  notes: normalize_term_list or to_exact before JSON
- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  notes: presentation only

## Processing steps
1) simplify_term(1, radicand).
2) Pack coefficient/radicand; optional format_term.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=9 methods (full domain); full-plan=2 methods (task-allowed subset ['RadicalOps.simplify_term', 'RadicalOps.format_term']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce111_q02_polynomial_division_remainder` (`PolynomialOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q02_polynomial_division_remainder.txt`
- Method1 SHA-256: `7b5612143100eb49d25388a752280f9519db31f1188648f205148ca45c4c6e43`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q02_polynomial_division_remainder.txt`
- Method2 SHA-256: `7f94bfff701f33cfe4a7211729637fa87442e3ab2e95471fed4f9cb1217a8f02`
- Method1 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`
- Method2 APIs listed: `PolynomialOps.div_qr, PolynomialOps.format_latex`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: PolynomialOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce111_q02_polynomial_division_remainder`
domain_ops: PolynomialOps

## Question stem (use verbatim as question_text)
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

## Allowed Domain API
- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
  inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
  notes: already exact JSON leaves
- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
  inputs: highest-degree-first numeric coefficients; bool forbidden
  notes: presentation only

## Processing steps
1) div_qr frozen coefficients.
2) Keep remainder only; format_latex if needed.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=9 methods (full domain); full-plan=2 methods (task-allowed subset ['PolynomialOps.div_qr', 'PolynomialOps.format_latex']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce111_q08_polynomial_factor_parameter_recovery` (`PolynomialOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt`
- Method1 SHA-256: `86b2a57c410ef01e529a2415712ae784c4447bfa09625fb9da1a56dc11ae94a2`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt`
- Method2 SHA-256: `c009f8e965f36e0a1bc101f214a7857de08065c5b3c7f9c3e91150477fc78ca2`
- Method1 APIs listed: `PolynomialOps.add, PolynomialOps.coeffs_from_py_expression, PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul, PolynomialOps.normalize, PolynomialOps.sub, PolynomialOps.to_degree_map`
- Method2 APIs listed: `PolynomialOps.div_qr, PolynomialOps.factor_quadratic_exact, PolynomialOps.format_latex, PolynomialOps.mul`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: PolynomialOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce111_q08_polynomial_factor_parameter_recovery`
domain_ops: PolynomialOps

## Question stem (use verbatim as question_text)
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

## Allowed Domain API
- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
  inputs: exact rational a,b,c; a nonzero; rational roots required
  notes: already JSON safe
- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
  inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
  notes: Fraction coefficients require to_exact; exact tasks must not use float

## Processing steps
1) factor_quadratic_exact.
2) Swap so left x_coefficient equals template_left_x_coefficient.
3) Extract a,b,c and compute a+2*c with native arithmetic.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=9 methods (full domain); full-plan=4 methods (task-allowed subset ['PolynomialOps.factor_quadratic_exact', 'PolynomialOps.mul']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce111_q03_prime_factor_selection` (`IntegerOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q03_prime_factor_selection.txt`
- Method1 SHA-256: `67fffa8b4b443bb3a2772d3647bd08f8fc373c8741dee9f79e266604d61e486e`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q03_prime_factor_selection.txt`
- Method2 SHA-256: `20576ca89bb9e34d5436188c8e9828b577a0b6ee2bb9ca6906b34c66fa97c029`
- Method1 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`
- Method2 APIs listed: `IntegerOps.prime_factorization`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: IntegerOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce111_q03_prime_factor_selection`
domain_ops: IntegerOps

## Question stem (use verbatim as question_text)
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

## Allowed Domain API
- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
  inputs: non-bool int; n!=0; factors abs(n)
  notes: no selected/answer field

## Processing steps
1) IntegerOps.prime_factorization(n).
2) Choose the candidate that appears as a prime key.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {"n": 12, "candidates": [2, 5, 7]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```
```

### Diff summary

- API surface differs: menu=7 methods (full domain); full-plan=1 methods (task-allowed subset ['IntegerOps.prime_factorization']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce112_q01_negative_integer_power` (`IntegerOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q01_negative_integer_power.txt`
- Method1 SHA-256: `8a0cbd3c75aef342d86bed21fb2cbb0c924d49ac644ba9611efabafbd1b792ef`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce112_q01_negative_integer_power.txt`
- Method2 SHA-256: `7fd27537f6e302fee6852f9b233285c8236b897e5b368ea33fc3051c1692b541`
- Method1 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`
- Method2 APIs listed: `IntegerOps.prime_factorization`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: IntegerOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce112_q01_negative_integer_power`
domain_ops: IntegerOps

## Question stem (use verbatim as question_text)
計算
\[
(-3)^3.
\]

## frozen_params (oracle_payload must equal this object)
{
  "base": -3,
  "exponent": 3
}

## Allowed Domain API
- (none required; use native arithmetic only)

## Processing steps
1) Compute base ** exponent with native arithmetic.
2) Return bare int.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {"n": 12, "candidates": [2, 5, 7]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```
```

### Diff summary

- API surface differs: menu=7 methods (full domain); full-plan=1 methods (task-allowed subset native-only).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce112_q09_divisor_multiple_intersection` (`IntegerOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q09_divisor_multiple_intersection.txt`
- Method1 SHA-256: `9e6756e2dac0414f6b2d69b423f2077c9bd514e49f171263bd374d1a2f45bb4e`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce112_q09_divisor_multiple_intersection.txt`
- Method2 SHA-256: `4c6c5e583ce2094292371b438cd299674e98e39fec604e27cc8e2c58d92dc587`
- Method1 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`
- Method2 APIs listed: `IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: IntegerOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce112_q09_divisor_multiple_intersection`
domain_ops: IntegerOps

## Question stem (use verbatim as question_text)
有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？

## frozen_params (oracle_payload must equal this object)
{
  "divisor_of": 216,
  "multiple_of": 18
}

## Allowed Domain API
- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
  inputs: non-bool int n>0; no other task filters
  notes: filter multiples in model assembly if needed
- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  notes: not an answer integer

## Processing steps
1) positive_divisors(divisor_of).
2) Keep values divisible by multiple_of.
3) Return {"count": len(valid)}.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {"n": 12, "candidates": [2, 5, 7]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```
```

### Diff summary

- API surface differs: menu=7 methods (full domain); full-plan=3 methods (task-allowed subset ['IntegerOps.positive_divisors', 'IntegerOps.is_divisible']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce111_nonchoice_q01_part1_exponential_growth` (`IntegerOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt`
- Method1 SHA-256: `e8ccbf8709ceaab0633daa071bd54fe787a67b34a26c37c852cf33d6f7b21f67`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt`
- Method2 SHA-256: `0ec59429b50e121db39ddfa493c44cbe13639b1db8dbc6c776c34d2f8df801c2`
- Method1 APIs listed: `IntegerOps.add, IntegerOps.fmt_num, IntegerOps.is_divisible, IntegerOps.positive_divisors, IntegerOps.prime_factorization, IntegerOps.safe_eval, IntegerOps.sub`
- Method2 APIs listed: `IntegerOps.is_divisible, IntegerOps.prime_factorization`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: IntegerOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce111_nonchoice_q01_part1_exponential_growth`
domain_ops: IntegerOps

## Question stem (use verbatim as question_text)
從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。

## frozen_params (oracle_payload must equal this object)
{
  "days": 15,
  "hours_per_generation": 20,
  "initial": 1,
  "split_factor": 4
}

## Allowed Domain API
- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
  inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
  notes: not an answer integer

## Processing steps
1) total_hours = days * 24.
2) Ensure divisible by hours_per_generation.
3) k = total_hours // hours_per_generation; return {"k": k}.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {"n": 12, "candidates": [2, 5, 7]}
    factors = IntegerOps.prime_factorization(frozen["n"])
    chosen = [c for c in frozen["candidates"] if c in factors][0]
    return {
        "question_text": "example stem",
        "correct_answer": chosen,
        "oracle_payload": frozen,
    }
```
```

### Diff summary

- API surface differs: menu=7 methods (full domain); full-plan=2 methods (task-allowed subset ['IntegerOps.is_divisible']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce111_q05_exact_fraction_expression` (`FractionOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q05_exact_fraction_expression.txt`
- Method1 SHA-256: `ac1eb3f529cb45a58a426b4d2bfc57a823d4ff9757ab738c4dab16d61e2a8375`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q05_exact_fraction_expression.txt`
- Method2 SHA-256: `1806688f141d3f2ab10b2c880ca9661bfce288360c403770eb69e0d3ae2e9c08`
- Method1 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`
- Method2 APIs listed: `FractionOps.add, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_latex`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: FractionOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce111_q05_exact_fraction_expression`
domain_ops: FractionOps

## Question stem (use verbatim as question_text)
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

## derived_scaffold (DERIVED_NON_ORACLE_STRUCTURAL_SCAFFOLD)
Use this structure; it contains no answers.
{
  "left": {
    "left": {
      "den": 22,
      "num": 9
    },
    "op": "add",
    "right": {
      "den": 18,
      "num": 11
    }
  },
  "op": "sub",
  "right": {
    "left": {
      "den": 22,
      "num": 23
    },
    "op": "sub",
    "right": {
      "den": 18,
      "num": 7
    }
  }
}

## Allowed Domain API
- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  notes: to_exact before correct_answer
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  notes: to_exact before correct_answer
- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  notes: to_exact before correct_answer
- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  notes: presentation only; not semantic serialization

## Processing steps
1) Walk expression_tree leaves with from_parts.
2) Evaluate add/sub nodes.
3) Return numerator/denominator (+ optional latex).

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=8 methods (full domain); full-plan=5 methods (task-allowed subset ['FractionOps.from_parts', 'FractionOps.add', 'FractionOps.sub', 'FractionOps.to_latex']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- full-plan includes derived_scaffold; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce113_q01_negative_fraction_subtraction` (`FractionOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce113_q01_negative_fraction_subtraction.txt`
- Method1 SHA-256: `c9fe9333195578b1ae14b1763e5ec9bc02a2f1f80b248a59d19dd131c76b86a8`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce113_q01_negative_fraction_subtraction.txt`
- Method2 SHA-256: `95f4d32f90da7816e9bb74e5c070d26aedb0a7de68909be1e739f6be7a16cf14`
- Method1 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`
- Method2 APIs listed: `FractionOps.add, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_latex`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: FractionOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce113_q01_negative_fraction_subtraction`
domain_ops: FractionOps

## Question stem (use verbatim as question_text)
精確計算
\[
\frac{3}{7}-\left(-\frac{1}{4}\right).
\]
答案須化為最簡分數。

## frozen_params (oracle_payload must equal this object)
{
  "expression": "3/7 - (-1/4)"
}

## derived_scaffold (DERIVED_NON_ORACLE_STRUCTURAL_SCAFFOLD)
Use this structure; it contains no answers.
{
  "left": {
    "den": 7,
    "num": 3
  },
  "op": "sub",
  "right": {
    "den": 4,
    "num": -1
  }
}

## Allowed Domain API
- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  notes: to_exact before correct_answer
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  notes: to_exact before correct_answer
- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  notes: to_exact before correct_answer
- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  notes: presentation only; not semantic serialization

## Processing steps
1) Walk expression_tree with from_parts and sub.
2) Return numerator/denominator (+ optional latex).

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=8 methods (full domain); full-plan=5 methods (task-allowed subset ['FractionOps.from_parts', 'FractionOps.add', 'FractionOps.sub', 'FractionOps.to_latex']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- full-plan includes derived_scaffold; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce112_q12_independent_probability_fraction` (`FractionOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q12_independent_probability_fraction.txt`
- Method1 SHA-256: `5110e0e344af83da2bcd0cfe3fdd486a3d79073764b60621ce2a4e0b46f4703f`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce112_q12_independent_probability_fraction.txt`
- Method2 SHA-256: `3f1000e5b94d8675382e8018a53fb908f0f100fe63f952d6e9f97a774e864645`
- Method1 APIs listed: `FractionOps.add, FractionOps.create, FractionOps.div, FractionOps.from_parts, FractionOps.mul, FractionOps.sub, FractionOps.to_exact, FractionOps.to_latex`
- Method2 APIs listed: `FractionOps.from_parts, FractionOps.mul, FractionOps.to_latex`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: FractionOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce112_q12_independent_probability_fraction`
domain_ops: FractionOps

## Question stem (use verbatim as question_text)
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

## Allowed Domain API
- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
  inputs: numerator,denominator: int; bool forbidden; denominator != 0
  notes: to_exact before correct_answer
- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
  inputs: a,b: Fraction
  notes: to_exact before correct_answer
- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
  inputs: exact value; mixed: bool
  notes: presentation only; not semantic serialization

## Processing steps
1) from_parts for p1 and p2.
2) mul; return numerator/denominator.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=8 methods (full domain); full-plan=3 methods (task-allowed subset ['FractionOps.from_parts', 'FractionOps.mul', 'FractionOps.to_latex']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce112_q04_radical_simplification` (`RadicalOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce112_q04_radical_simplification.txt`
- Method1 SHA-256: `0e824d552ded8d07d15dd3367f7a98a424d7e64a3e56650cf1c5bcb0e8d0c25f`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce112_q04_radical_simplification.txt`
- Method2 SHA-256: `2868ba929d5169e1bf70fcc920bec4d16c87152659638bd1239c3998db0f1599`
- Method1 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`
- Method2 APIs listed: `RadicalOps.format_term, RadicalOps.simplify_term`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: RadicalOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce112_q04_radical_simplification`
domain_ops: RadicalOps

## Question stem (use verbatim as question_text)
將
\[
\sqrt{135}
\]
化為最簡根式。

## frozen_params (oracle_payload must equal this object)
{
  "radicand": 135
}

## Allowed Domain API
- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
  inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
  notes: normalize_term_list or to_exact before JSON
- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
  inputs: semantic coefficient and radicand
  notes: presentation only

## Processing steps
1) simplify_term(1, radicand).
2) Pack coefficient/radicand.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=9 methods (full domain); full-plan=2 methods (task-allowed subset ['RadicalOps.simplify_term', 'RadicalOps.format_term']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce111_q10_ordered_quadratic_roots_radical` (`RadicalOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce111_q10_ordered_quadratic_roots_radical.txt`
- Method1 SHA-256: `5419a3ebc38e402140803afeb71ccb3fa385a5da9f07c6a4166a306ed91b336a`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce111_q10_ordered_quadratic_roots_radical.txt`
- Method2 SHA-256: `b17be4134859201d638d3b765b5549fc9344e2e2e94973dbd3c7822fd657fa97`
- Method1 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`
- Method2 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: RadicalOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce111_q10_ordered_quadratic_roots_radical`
domain_ops: RadicalOps

## Question stem (use verbatim as question_text)
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

## derived_scaffold (DERIVED_NON_ORACLE_STRUCTURAL_SCAFFOLD)
Use this structure; it contains no answers.
{
  "center": 2,
  "equation_form": "shifted_square",
  "order": "larger_first",
  "squared_distance": 3,
  "target_weights": {
    "larger": 2,
    "smaller": 1
  }
}

## Allowed Domain API
- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: term LinearRadical dict; k nonzero non-bool int
  notes: rejects k==0 and zero radical_coefficient
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
  inputs: two LinearRadical dicts with identical positive radicand
  notes: rejects mismatched radicand or zero result coefficient
- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  notes: presentation only

## Processing steps
1) From shifted-square scaffold build larger/smaller LinearRadical.
2) scale_linear_radical(larger, weight); add_linear_radicals.
3) Assemble nested or flat result dict.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=9 methods (full domain); full-plan=5 methods (task-allowed subset ['RadicalOps.scale_linear_radical', 'RadicalOps.add_linear_radicals', 'RadicalOps.format_linear_radical']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- full-plan includes derived_scaffold; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## Task `ce113_q11_rationalize_denominator` (`RadicalOps`)

- Method1 path: `docs/experiments/prompts/ab2d_domain_menu/prompts/ce113_q11_rationalize_denominator.txt`
- Method1 SHA-256: `1992b663e3a5f69d94c3526f04eabfc0c2b10109c129c937ca5124e1aa90b2b3`
- Method2 path: `docs/experiments/prompts/ab2d_full/prompts/ce113_q11_rationalize_denominator.txt`
- Method2 SHA-256: `31dfa808427261107326d25322f05fb405ca531d2c9d56f325d594b1ae8dbe44`
- Method1 APIs listed: `RadicalOps.add_linear_radicals, RadicalOps.exact_integer, RadicalOps.format_expression, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.normalize_term_list, RadicalOps.rationalize_linear_denominator, RadicalOps.scale_linear_radical, RadicalOps.simplify_term`
- Method2 APIs listed: `RadicalOps.exact_integer, RadicalOps.format_linear_radical, RadicalOps.format_term, RadicalOps.rationalize_linear_denominator, RadicalOps.simplify_term`

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
# Math16 Ab2d+full system
Write only Python source implementing `def generate(level=1, **kwargs):`.
Return a dict with exactly three keys: question_text, correct_answer, oracle_payload.
question_text must be the provided stem string (do not rebuild LaTeX).
oracle_payload must exactly equal the frozen_params object.
correct_answer must be JSON-compatible and match the task answer shape.
Use only the listed Domain API methods from this prompt.
Domain for this task: RadicalOps.
Allowed native ops: arithmetic, comparisons, if/else, loops, list/dict, unpacking, sorting.
Forbidden: other domain public APIs; task-specific solvers; reading audit payloads;
manifest answers; evaluator expected answers; answer lookup by task_id.
Do not use Markdown fences or explanations outside the Python source.
Import Domain API from `core.prompts.domain_function_library` only as needed.

# Task `ce113_q11_rationalize_denominator`
domain_ops: RadicalOps

## Question stem (use verbatim as question_text)
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

## derived_scaffold (DERIVED_NON_ORACLE_STRUCTURAL_SCAFFOLD)
Use this structure; it contains no answers.
{
  "denom_radical_coeff": -1,
  "denom_rational": 4,
  "radicand": 7
}

## Allowed Domain API
- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
  inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
  notes: RadicalOps.exact_integer on integral leaves before JSON
- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
  inputs: non-bool int, integral Fraction, or integral 'p/q' string
  notes: never returns str union
- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
  inputs: LinearRadical dict
  notes: presentation only

## Processing steps
1) rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand).
2) exact_integer on both coefficients.
3) Native int add for final bare answer.

## Output contract
Return exactly:
{"question_text": <stem str>, "correct_answer": <task shape>, "oracle_payload": <frozen_params>}

## Generic domain example (non-task numbers)
```python
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
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
```

### Diff summary

- API surface differs: menu=9 methods (full domain); full-plan=5 methods (task-allowed subset ['RadicalOps.rationalize_linear_denominator', 'RadicalOps.exact_integer', 'RadicalOps.format_linear_radical']).
- full-plan includes task-specific ## Processing steps; domain-menu does not.
- full-plan includes derived_scaffold; domain-menu does not.
- domain-menu includes full-domain API menu block; full-plan uses Allowed Domain API subset.
- Task stem and frozen_params match across both prompts and pool.

---

## REVIEW_DOCUMENT_PATH

`docs/experiments/results/Math16/math16_ab2d_domain_menu_vs_full_plan_prompt_review_v1.md`

## FINAL_VERDICT

**PROMPT_FAIRNESS_DEFECT_FOUND**

