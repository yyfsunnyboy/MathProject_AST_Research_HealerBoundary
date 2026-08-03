# Domain API coverage: PolynomialOps (V2)

SUPPORTED_PUBLIC count: **9**
Missing required fields: **0**
Executable-example local-execution failures: **0**
Rendered-in-prompt vs SSOT mismatches: **0**

## `PolynomialOps.add`
- import: `core.prompts.domain_function_library`
- signature: `(c1, c2)`
- input constraints: coefficient lists with mutually arithmetic-compatible values; bool forbidden
- return type: `list[number]  # operand-dependent coefficient type; highest degree first`
- return shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
- JSON boundary: use to_exact per Fraction coefficient before JSON
- example: `PolynomialOps.add([1, 2], [3, 4])  # [4, 6]`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `PolynomialOps.coeffs_from_py_expression`
- import: `core.prompts.domain_function_library`
- signature: `(expression, var='x')`
- input constraints: restricted polynomial expression using integer constants,+,-,*,nonnegative integer **
- return type: `list[Fraction]  # highest degree first`
- return shape: `{"element_types": ["Fraction"], "json_safe": false, "length": "degree+1", "ordering": "highest degree first", "type": "list"}`
- JSON boundary: to_degree_map or to_exact per coefficient
- example: `PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `PolynomialOps.div_qr`
- import: `core.prompts.domain_function_library`
- signature: `(dividend_coefficients, divisor_coefficients)`
- input constraints: non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor
- return type: `tuple[list[int | str], list[int | str]]  # quotient,remainder`
- return shape: `{"elements": [{"element_types": ["int", "str"], "type": "list"}, {"element_types": ["int", "str"], "type": "list"}], "json_safe": true, "length": 2, "ordering": "highest degree first", "type": "tuple"}`
- JSON boundary: already exact JSON leaves
- example: `PolynomialOps.div_qr([2, 0, 2], [1, 1])`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `PolynomialOps.factor_quadratic_exact`
- import: `core.prompts.domain_function_library`
- signature: `(a, b, c)`
- input constraints: exact rational a,b,c; a nonzero; rational roots required
- return type: `list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple`
- return shape: `{"element": {"required_keys": ["x_coefficient", "constant"], "type": "dict", "value_types": ["int", "str"]}, "json_safe": true, "length": 2, "ordering": "deterministic implementation order; consumers must not infer sorted roots", "type": "list"}`
- JSON boundary: already JSON safe
- example: `PolynomialOps.factor_quadratic_exact(1, -5, 6)`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `PolynomialOps.format_latex`
- import: `core.prompts.domain_function_library`
- signature: `(coeffs, var='x')`
- input constraints: highest-degree-first numeric coefficients; bool forbidden
- return type: `str`
- return shape: `{"json_safe": true, "type": "str"}`
- JSON boundary: presentation only
- example: `PolynomialOps.format_latex([2, 0])  # '2x'`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `PolynomialOps.mul`
- import: `core.prompts.domain_function_library`
- signature: `(c1, c2)`
- input constraints: coefficient lists containing arithmetic-compatible int,float,Fraction; empty operand -> [0]; bool forbidden
- return type: `list[int | float | Fraction]  # operand-dependent; highest degree first`
- return shape: `{"element_types": ["int", "float", "Fraction"], "json_safe": "operand-dependent", "length": "len(c1)+len(c2)-1 before leading-zero normalization", "ordering": "highest degree first", "type": "list"}`
- JSON boundary: Fraction coefficients require to_exact; exact tasks must not use float
- example: `PolynomialOps.mul([1, 1], [1, -1])  # [1, 0, -1]`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `PolynomialOps.normalize`
- import: `core.prompts.domain_function_library`
- signature: `(coeffs)`
- input constraints: coefficient sequence; empty or all-zero -> [0]; bool coefficients forbidden
- return type: `list[number]  # highest degree first; leading zeros removed`
- return shape: `{"json_safe": "operand-dependent", "length": "variable", "ordering": "highest degree first", "type": "list"}`
- JSON boundary: preserves coefficient types
- example: `PolynomialOps.normalize([0, 2, 1])  # [2, 1]`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `PolynomialOps.sub`
- import: `core.prompts.domain_function_library`
- signature: `(c1, c2)`
- input constraints: coefficient lists with mutually arithmetic-compatible values; bool forbidden
- return type: `list[number]  # operand-dependent coefficient type; highest degree first`
- return shape: `{"json_safe": "operand-dependent", "length": "max operand length after normalization", "ordering": "highest degree first", "type": "list"}`
- JSON boundary: use to_exact per Fraction coefficient before JSON
- example: `PolynomialOps.sub([1, 2], [3, 4])  # [-2, -2]`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `PolynomialOps.to_degree_map`
- import: `core.prompts.domain_function_library`
- signature: `(coeffs)`
- input constraints: non-empty exact coefficient list
- return type: `dict[str, int | str]  # descending degree insertion order`
- return shape: `{"json_safe": true, "keys": "decimal degree strings", "ordering": "descending numeric degree insertion order", "type": "dict", "values": ["int", "str"]}`
- JSON boundary: official polynomial JSON adapter
- example: `PolynomialOps.to_degree_map([1, 0, -1])`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**
