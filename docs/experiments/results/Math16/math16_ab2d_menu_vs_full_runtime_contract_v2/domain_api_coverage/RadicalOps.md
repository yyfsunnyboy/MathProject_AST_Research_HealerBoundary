# Domain API coverage: RadicalOps (V2)

SUPPORTED_PUBLIC count: **9**
Missing required fields: **0**
Executable-example local-execution failures: **0**
Rendered-in-prompt vs SSOT mismatches: **0**

## `RadicalOps.add_linear_radicals`
- import: `core.prompts.domain_function_library`
- signature: `(term_a, term_b)`
- input constraints: two LinearRadical dicts with identical positive radicand
- return type: `dict  # LinearRadical JSON-safe ints`
- return shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
- JSON boundary: rejects mismatched radicand or zero result coefficient
- example: `RadicalOps.add_linear_radicals({"rational": 1, "radical_coefficient": 1, "radicand": 2},{"rational": 3, "radical_coefficient": 1, "radicand": 2})`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `RadicalOps.exact_integer`
- import: `core.prompts.domain_function_library`
- signature: `(value)`
- input constraints: non-bool int, integral Fraction, or integral 'p/q' string
- return type: `int  # rejects non-integral rationals`
- return shape: `{"json_safe": true, "type": "int"}`
- JSON boundary: never returns str union
- example: `RadicalOps.exact_integer(Fraction(4, 1))  # 4`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `RadicalOps.format_expression`
- import: `core.prompts.domain_function_library`
- signature: `(terms_dict, denominator=1)`
- input constraints: mapping radicand->coefficient; exact denominator
- return type: `str  # complete compound-radical LaTeX`
- return shape: `{"json_safe": true, "type": "str"}`
- JSON boundary: presentation only
- example: `RadicalOps.format_expression({1: 6, 3: -1})  # '6 - \sqrt{3}'`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `RadicalOps.format_linear_radical`
- import: `core.prompts.domain_function_library`
- signature: `(term)`
- input constraints: LinearRadical dict
- return type: `str  # presentation LaTeX`
- return shape: `{"json_safe": true, "type": "str"}`
- JSON boundary: presentation only
- example: `RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2})  # "1+\sqrt{2}"`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `RadicalOps.format_term`
- import: `core.prompts.domain_function_library`
- signature: `(coeff, radicand, is_first=True)`
- input constraints: semantic coefficient and radicand
- return type: `str  # complete single-term LaTeX including coefficient/sign`
- return shape: `{"json_safe": true, "type": "str"}`
- JSON boundary: presentation only
- example: `RadicalOps.format_term(2, 3)  # '2\sqrt{3}'`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `RadicalOps.normalize_term_list`
- import: `core.prompts.domain_function_library`
- signature: `(terms)`
- input constraints: list/tuple of pairs or coefficient/radicand dicts
- return type: `list[dict]  # sorted; keys coefficient,radicand`
- return shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
- JSON boundary: official radical semantic JSON adapter
- example: `RadicalOps.normalize_term_list([(1, 12)])`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `RadicalOps.rationalize_linear_denominator`
- import: `core.prompts.domain_function_library`
- signature: `(numerator, denom_rational, denom_radical_coeff, radicand)`
- input constraints: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
- return type: `tuple[int | Fraction, int | Fraction, int]`
- return shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
- JSON boundary: RadicalOps.exact_integer on integral leaves before JSON
- example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `RadicalOps.scale_linear_radical`
- import: `core.prompts.domain_function_library`
- signature: `(term, k)`
- input constraints: term LinearRadical dict; k nonzero non-bool int
- return type: `dict  # LinearRadical JSON-safe ints`
- return shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
- JSON boundary: rejects k==0 and zero radical_coefficient
- example: `RadicalOps.scale_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}, 2)`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `RadicalOps.simplify_term`
- import: `core.prompts.domain_function_library`
- signature: `(coeff, radicand)`
- input constraints: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
- return type: `tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)`
- return shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
- JSON boundary: normalize_term_list or to_exact before JSON
- example: `RadicalOps.simplify_term(1, 12)  # (2, 3)`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**
