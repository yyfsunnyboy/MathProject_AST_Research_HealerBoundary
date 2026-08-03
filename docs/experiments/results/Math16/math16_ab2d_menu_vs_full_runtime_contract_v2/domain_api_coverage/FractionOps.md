# Domain API coverage: FractionOps (V2)

SUPPORTED_PUBLIC count: **8**
Missing required fields: **0**
Executable-example local-execution failures: **0**
Rendered-in-prompt vs SSOT mismatches: **0**

## `FractionOps.add`
- import: `core.prompts.domain_function_library`
- signature: `(a, b)`
- input constraints: a,b: Fraction
- return type: `Fraction`
- return shape: `{"json_safe": false, "type": "Fraction"}`
- JSON boundary: to_exact before correct_answer
- example: `FractionOps.add(Fraction(1, 2), Fraction(1, 3))`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `FractionOps.create`
- import: `core.prompts.domain_function_library`
- signature: `(value)`
- input constraints: int, finite float, legal numeric str, or Fraction; bool forbidden
- return type: `Fraction  # not JSON serializable; use the to_exact adapter`
- return shape: `{"json_safe": false, "type": "Fraction"}`
- JSON boundary: FractionOps.to_exact before correct_answer
- example: `FractionOps.create("2/7")  # Fraction(2, 7)`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `FractionOps.div`
- import: `core.prompts.domain_function_library`
- signature: `(a, b)`
- input constraints: a,b: Fraction; b != 0
- return type: `Fraction`
- return shape: `{"json_safe": false, "type": "Fraction"}`
- JSON boundary: to_exact before correct_answer
- example: `FractionOps.div(Fraction(1, 2), Fraction(1, 3))`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `FractionOps.from_parts`
- import: `core.prompts.domain_function_library`
- signature: `(numerator, denominator=1)`
- input constraints: numerator,denominator: int; bool forbidden; denominator != 0
- return type: `Fraction`
- return shape: `{"json_safe": false, "type": "Fraction"}`
- JSON boundary: to_exact before correct_answer
- example: `FractionOps.from_parts(6, 3)  # Fraction(2, 1)`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `FractionOps.mul`
- import: `core.prompts.domain_function_library`
- signature: `(a, b)`
- input constraints: a,b: Fraction
- return type: `Fraction`
- return shape: `{"json_safe": false, "type": "Fraction"}`
- JSON boundary: to_exact before correct_answer
- example: `FractionOps.mul(Fraction(1, 2), Fraction(1, 3))`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `FractionOps.sub`
- import: `core.prompts.domain_function_library`
- signature: `(a, b)`
- input constraints: a,b: Fraction
- return type: `Fraction`
- return shape: `{"json_safe": false, "type": "Fraction"}`
- JSON boundary: to_exact before correct_answer
- example: `FractionOps.sub(Fraction(1, 2), Fraction(1, 6))`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `FractionOps.to_exact`
- import: `core.prompts.domain_function_library`
- signature: `(value)`
- input constraints: int, Fraction, or legal exact string; bool/float forbidden
- return type: `int | str  # integer or irreducible 'p/q'`
- return shape: `{"json_safe": true, "string_schema": "^-?[0-9]+/[1-9][0-9]*$", "type": "union", "types": ["int", "str"]}`
- JSON boundary: official Fraction-to-JSON adapter
- example: `FractionOps.to_exact(Fraction(3, 2))  # '3/2'`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `FractionOps.to_latex`
- import: `core.prompts.domain_function_library`
- signature: `(val, mixed=False)`
- input constraints: exact value; mixed: bool
- return type: `str`
- return shape: `{"json_safe": true, "type": "str"}`
- JSON boundary: presentation only; not semantic serialization
- example: `FractionOps.to_latex(Fraction(2, 7))  # '\frac{2}{7}'`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**
