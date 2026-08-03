# Domain API coverage: IntegerOps (V2)

SUPPORTED_PUBLIC count: **7**
Missing required fields: **0**
Executable-example local-execution failures: **0**
Rendered-in-prompt vs SSOT mismatches: **0**

## `IntegerOps.add`
- import: `core.prompts.domain_function_library`
- signature: `(a, b)`
- input constraints: a,b: int; bool forbidden
- return type: `int`
- return shape: `{"json_safe": true, "type": "int"}`
- JSON boundary: none
- example: `IntegerOps.add(10, 20)  # 30`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `IntegerOps.fmt_num`
- import: `core.prompts.domain_function_library`
- signature: `(n)`
- input constraints: ordered numeric n
- return type: `str`
- return shape: `{"json_safe": true, "type": "str"}`
- JSON boundary: presentation only
- example: `IntegerOps.fmt_num(-2)  # "(-2)"`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `IntegerOps.is_divisible`
- import: `core.prompts.domain_function_library`
- signature: `(a, b)`
- input constraints: non-bool int a,b; float/bool raise ValueError; b=0 returns False (not an exception)
- return type: `bool`
- return shape: `{"json_safe": true, "type": "bool"}`
- JSON boundary: not an answer integer
- example: `IntegerOps.is_divisible(21, 7)  # True`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `IntegerOps.positive_divisors`
- import: `core.prompts.domain_function_library`
- signature: `(n)`
- input constraints: non-bool int n>0; no other task filters
- return type: `list[int]  # ascending positive divisors`
- return shape: `{"element_types": ["int"], "json_safe": true, "ordering": "ascending", "type": "list"}`
- JSON boundary: filter multiples in model assembly if needed
- example: `IntegerOps.positive_divisors(12)  # [1, 2, 3, 4, 6, 12]`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `IntegerOps.prime_factorization`
- import: `core.prompts.domain_function_library`
- signature: `(n)`
- input constraints: non-bool int; n!=0; factors abs(n)
- return type: `dict[int, int]  # prime -> exponent; ±1 -> {}`
- return shape: `{"json_safe": true, "keys": "positive primes", "type": "dict", "values": "positive int exponents"}`
- JSON boundary: no selected/answer field
- example: `IntegerOps.prime_factorization(12)  # {2: 2, 3: 1}`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `IntegerOps.safe_eval`
- import: `core.prompts.domain_function_library`
- signature: `(expr)`
- input constraints: arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only
- return type: `int | float  # bool and container results raise ValueError`
- return shape: `{"forbidden_types": ["bool", "tuple", "list", "dict"], "json_safe": true, "type": "union", "types": ["int", "float"]}`
- JSON boundary: exact-int contracts must require type(value) is int; floats are never coerced to int
- example: `IntegerOps.safe_eval("2**4")  # 16`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**

## `IntegerOps.sub`
- import: `core.prompts.domain_function_library`
- signature: `(a, b)`
- input constraints: a,b: int; bool forbidden
- return type: `int`
- return shape: `{"json_safe": true, "type": "int"}`
- JSON boundary: none
- example: `IntegerOps.sub(30, 8)  # 22`
- example executes locally: **True**
- rendered-in-prompt matches SSOT: **True**
