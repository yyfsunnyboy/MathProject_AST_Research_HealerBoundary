---
name: domain-api-contract-v2
description: Generated typed Domain API reference for formal Ab2d/Qwen prompts.
---

# Generated from domain_api_ssot.py; do not edit by hand.
## FractionOps.add
- `FractionOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- Inputs: a,b: Fraction
- Shape: `{"json_safe": false, "type": "Fraction"}`
- Normalization: to_exact before correct_answer
- Example: `FractionOps.add(Fraction(1,2), Fraction(1,3))`

## FractionOps.create
- `FractionOps.create` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: Fraction  # not JSON serializable; use the to_exact adapter
- Inputs: int, finite float, legal numeric str, or Fraction; bool forbidden
- Shape: `{"json_safe": false, "type": "Fraction"}`
- Normalization: FractionOps.to_exact before correct_answer
- Example: `FractionOps.create("3/5")  # Fraction(3, 5)`

## FractionOps.div
- `FractionOps.div` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- Inputs: a,b: Fraction; b != 0
- Shape: `{"json_safe": false, "type": "Fraction"}`
- Normalization: to_exact before correct_answer
- Example: `FractionOps.div(Fraction(1,2), Fraction(1,3))`

## FractionOps.from_parts
- `FractionOps.from_parts` | import: `core.prompts.domain_function_library` | signature: `(numerator, denominator=1)` | returns: Fraction
- Inputs: numerator,denominator: int; bool forbidden; denominator != 0
- Shape: `{"json_safe": false, "type": "Fraction"}`
- Normalization: to_exact before correct_answer
- Example: `FractionOps.from_parts(6,3)  # Fraction(2,1)`

## FractionOps.mul
- `FractionOps.mul` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- Inputs: a,b: Fraction
- Shape: `{"json_safe": false, "type": "Fraction"}`
- Normalization: to_exact before correct_answer
- Example: `FractionOps.mul(Fraction(1,2), Fraction(1,3))`

## FractionOps.sub
- `FractionOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: Fraction
- Inputs: a,b: Fraction
- Shape: `{"json_safe": false, "type": "Fraction"}`
- Normalization: to_exact before correct_answer
- Example: `FractionOps.sub(Fraction(3,7), Fraction(-1,4))`

## FractionOps.to_exact
- `FractionOps.to_exact` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int | str  # integer or irreducible 'p/q'
- Inputs: int, Fraction, or legal exact string; bool/float forbidden
- Shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
- Normalization: official Fraction-to-JSON adapter
- Example: `FractionOps.to_exact(Fraction(3,2))  # '3/2'`

## FractionOps.to_latex
- `FractionOps.to_latex` | import: `core.prompts.domain_function_library` | signature: `(val, mixed=False)` | returns: str
- Inputs: exact value; mixed: bool
- Shape: `{"json_safe": true, "type": "str"}`
- Normalization: presentation only; not semantic serialization
- Example: `FractionOps.to_latex(Fraction(3,5))  # '\frac{3}{5}'`

## IntegerOps.add
- `IntegerOps.add` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
- Inputs: a,b: int; bool forbidden
- Shape: `{"json_safe": true, "type": "int"}`
- Normalization: none
- Example: `IntegerOps.add(2, 3)  # 5`

## IntegerOps.fmt_num
- `IntegerOps.fmt_num` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: str
- Inputs: ordered numeric n
- Shape: `{"json_safe": true, "type": "str"}`
- Normalization: presentation only
- Example: `IntegerOps.fmt_num(-3)  # "(-3)"`

## IntegerOps.is_divisible
- `IntegerOps.is_divisible` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: bool
- Inputs: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
- Shape: `{"json_safe": true, "type": "bool"}`
- Normalization: not an answer integer
- Example: `IntegerOps.is_divisible(156, 13)  # True`

## IntegerOps.positive_divisors
- `IntegerOps.positive_divisors` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: list[int]  # ascending positive divisors
- Inputs: non-bool int n>0; no other task filters
- Shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
- Normalization: filter multiples in model assembly if needed
- Example: `IntegerOps.positive_divisors(12)  # [1,2,3,4,6,12]`

## IntegerOps.prime_factorization
- `IntegerOps.prime_factorization` | import: `core.prompts.domain_function_library` | signature: `(n)` | returns: dict[int, int]  # prime -> exponent; ±1 -> {}
- Inputs: non-bool int; n!=0; factors abs(n)
- Shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
- Normalization: no selected/answer field
- Example: `IntegerOps.prime_factorization(12)  # {2:2, 3:1}`

## IntegerOps.safe_eval
- `IntegerOps.safe_eval` | import: `core.prompts.domain_function_library` | signature: `(expr)` | returns: int | float  # bool and container results raise ValueError
- Inputs: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
- Shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
- Normalization: exact-int contracts must require type(value) is int; floats are never coerced to int
- Example: `IntegerOps.safe_eval("(-3)**3")  # -27`

## IntegerOps.sub
- `IntegerOps.sub` | import: `core.prompts.domain_function_library` | signature: `(a, b)` | returns: int
- Inputs: a,b: int; bool forbidden
- Shape: `{"json_safe": true, "type": "int"}`
- Normalization: none
- Example: `IntegerOps.sub(2, 3)  # -1`

## PolynomialOps.add
- `PolynomialOps.add` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
- Inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
- Shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
- Normalization: use to_exact per Fraction coefficient before JSON
- Example: `PolynomialOps.add([1,2],[3,4])  # [4,6]`

## PolynomialOps.coeffs_from_py_expression
- `PolynomialOps.coeffs_from_py_expression` | import: `core.prompts.domain_function_library` | signature: `(expression, var='x')` | returns: list[Fraction]  # highest degree first
- Inputs: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
- Shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
- Normalization: to_degree_map or to_exact per coefficient
- Example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`

## PolynomialOps.div_qr
- `PolynomialOps.div_qr` | import: `core.prompts.domain_function_library` | signature: `(dividend_coefficients, divisor_coefficients)` | returns: tuple[list[int | str], list[int | str]]  # quotient,remainder
- Inputs: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
- Shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
- Normalization: already exact JSON leaves
- Example: `PolynomialOps.div_qr([6,0,6],[1,-4])  # ([6,24],[102])`

## PolynomialOps.factor_quadratic_exact
- `PolynomialOps.factor_quadratic_exact` | import: `core.prompts.domain_function_library` | signature: `(a, b, c)` | returns: list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple
- Inputs: exact rational a,b,c; a nonzero; rational roots required
- Shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
- Normalization: already JSON safe
- Example: `PolynomialOps.factor_quadratic_exact(1,4,-12)`

## PolynomialOps.format_latex
- `PolynomialOps.format_latex` | import: `core.prompts.domain_function_library` | signature: `(coeffs, var='x')` | returns: str
- Inputs: highest-degree-first numeric coefficients; bool forbidden
- Shape: `{"json_safe": true, "type": "str"}`
- Normalization: presentation only
- Example: `PolynomialOps.format_latex([4,0])  # '4x'`

## PolynomialOps.mul
- `PolynomialOps.mul` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[int | float | Fraction]  # operand-dependent; highest degree first
- Inputs: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
- Shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
- Normalization: Fraction coefficients require to_exact; exact tasks must not use float
- Example: `PolynomialOps.mul([3,2],[13,-7])  # [39,5,-14]`

## PolynomialOps.normalize
- `PolynomialOps.normalize` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: list[number]  # highest degree first; leading zeros removed
- Inputs: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
- Shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
- Normalization: preserves coefficient types
- Example: `PolynomialOps.normalize([0,2,1])  # [2,1]`

## PolynomialOps.sub
- `PolynomialOps.sub` | import: `core.prompts.domain_function_library` | signature: `(c1, c2)` | returns: list[number]  # operand-dependent coefficient type; highest degree first
- Inputs: coefficient lists with mutually arithmetic-compatible values; bool forbidden
- Shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
- Normalization: use to_exact per Fraction coefficient before JSON
- Example: `PolynomialOps.sub([1,2],[3,4])  # [-2,-2]`

## PolynomialOps.to_degree_map
- `PolynomialOps.to_degree_map` | import: `core.prompts.domain_function_library` | signature: `(coeffs)` | returns: dict[str, int | str]  # descending degree insertion order
- Inputs: non-empty exact coefficient list
- Shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
- Normalization: official polynomial JSON adapter
- Example: `PolynomialOps.to_degree_map([1,0,-1])`

## RadicalOps.add_linear_radicals
- `RadicalOps.add_linear_radicals` | import: `core.prompts.domain_function_library` | signature: `(term_a, term_b)` | returns: dict  # LinearRadical JSON-safe ints
- Inputs: two LinearRadical dicts with identical positive radicand
- Shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
- Normalization: rejects mismatched radicand or zero result coefficient
- Example: `RadicalOps.add_linear_radicals({"rational":1,"radical_coefficient":1,"radicand":2},{"rational":3,"radical_coefficient":-1,"radicand":2})`

## RadicalOps.exact_integer
- `RadicalOps.exact_integer` | import: `core.prompts.domain_function_library` | signature: `(value)` | returns: int  # rejects non-integral rationals
- Inputs: non-bool int, integral Fraction, or integral 'p/q' string
- Shape: `{"json_safe": true, "type": "int"}`
- Normalization: never returns str union
- Example: `RadicalOps.exact_integer(Fraction(4,1))  # 4`

## RadicalOps.format_expression
- `RadicalOps.format_expression` | import: `core.prompts.domain_function_library` | signature: `(terms_dict, denominator=1)` | returns: str  # complete compound-radical LaTeX
- Inputs: mapping radicand->coefficient; exact denominator
- Shape: `{"json_safe": true, "type": "str"}`
- Normalization: presentation only
- Example: `RadicalOps.format_expression({1:6,3:-1})  # '6 - \sqrt{3}'`

## RadicalOps.format_linear_radical
- `RadicalOps.format_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term)` | returns: str  # presentation LaTeX
- Inputs: LinearRadical dict
- Shape: `{"json_safe": true, "type": "str"}`
- Normalization: presentation only
- Example: `RadicalOps.format_linear_radical({"rational":1,"radical_coefficient":1,"radicand":2})  # "1+\sqrt{2}"`

## RadicalOps.format_term
- `RadicalOps.format_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand, is_first=True)` | returns: str  # complete single-term LaTeX including coefficient/sign
- Inputs: semantic coefficient and radicand
- Shape: `{"json_safe": true, "type": "str"}`
- Normalization: presentation only
- Example: `RadicalOps.format_term(3,15)  # '3\sqrt{15}'`

## RadicalOps.normalize_term_list
- `RadicalOps.normalize_term_list` | import: `core.prompts.domain_function_library` | signature: `(terms)` | returns: list[dict]  # sorted; keys coefficient,radicand
- Inputs: list/tuple of pairs or coefficient/radicand dicts
- Shape: `{"element": {"required_keys": ["coefficient", "radicand"], "type": "dict", "value_types": {"coefficient": ["int", "str"], "radicand": ["int"]}}, "json_safe": true, "length": "variable", "ordering": "ascending radicand", "type": "list"}`
- Normalization: official radical semantic JSON adapter
- Example: `RadicalOps.normalize_term_list([(1,12)])`

## RadicalOps.rationalize_linear_denominator
- `RadicalOps.rationalize_linear_denominator` | import: `core.prompts.domain_function_library` | signature: `(numerator, denom_rational, denom_radical_coeff, radicand)` | returns: tuple[int | Fraction, int | Fraction, int]
- Inputs: exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator
- Shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 3, "type": "tuple"}`
- Normalization: RadicalOps.exact_integer on integral leaves before JSON
- Example: `RadicalOps.rationalize_linear_denominator(1,2,1,3)`

## RadicalOps.scale_linear_radical
- `RadicalOps.scale_linear_radical` | import: `core.prompts.domain_function_library` | signature: `(term, k)` | returns: dict  # LinearRadical JSON-safe ints
- Inputs: term LinearRadical dict; k nonzero non-bool int
- Shape: `{"json_safe": true, "required_keys": ["rational", "radical_coefficient", "radicand"], "type": "dict", "value_types": {"radical_coefficient": ["int"], "radicand": ["int"], "rational": ["int"]}}`
- Normalization: rejects k==0 and zero radical_coefficient
- Example: `RadicalOps.scale_linear_radical({"rational":1,"radical_coefficient":1,"radicand":2}, 2)`

## RadicalOps.simplify_term
- `RadicalOps.simplify_term` | import: `core.prompts.domain_function_library` | signature: `(coeff, radicand)` | returns: tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)
- Inputs: exact coeff; radicand non-bool non-negative int, or non-negative Fraction (converted); radicand<0 raises ValueError (no silent abs)
- Shape: `{"elements": [{"types": ["int", "Fraction"]}, {"type": "int"}], "json_safe": "partial", "length": 2, "type": "tuple"}`
- Normalization: normalize_term_list or to_exact before JSON
- Example: `RadicalOps.simplify_term(1,12)  # (2,3)`
