"""Typed Domain API SSOT for Math16 Ab2d and future local-model runs.

Only ``SUPPORTED_PUBLIC`` entries may be routed into model-facing prompts.
The method inventory is explicit so adding a callable to a toolbox class is
a reviewed contract change rather than an accidental prompt expansion.
"""
from __future__ import annotations

import inspect
import json
from fractions import Fraction
from typing import Any

from core.prompts.domain_function_library import FractionOps, IntegerOps, PolynomialOps, RadicalOps

LIBRARY = "core.prompts.domain_function_library"
TOOLBOX_CLASSES = (IntegerOps, FractionOps, RadicalOps, PolynomialOps)

SUPPORTED_PUBLIC = "SUPPORTED_PUBLIC"
INTERNAL = "INTERNAL"
DEPRECATED = "DEPRECATED"
DUPLICATE = "DUPLICATE"

# Every callable that is public by Python naming convention is classified.
API_CLASSIFICATION: dict[str, str] = {
    # IntegerOps (9)
    "IntegerOps.add": SUPPORTED_PUBLIC,
    "IntegerOps.sub": SUPPORTED_PUBLIC,
    "IntegerOps.op_to_latex": INTERNAL,
    "IntegerOps.fmt_num": SUPPORTED_PUBLIC,
    "IntegerOps.random_nonzero": INTERNAL,
    "IntegerOps.is_divisible": SUPPORTED_PUBLIC,
    "IntegerOps.prime_factorization": SUPPORTED_PUBLIC,
    "IntegerOps.positive_divisors": SUPPORTED_PUBLIC,
    "IntegerOps.safe_eval": SUPPORTED_PUBLIC,
    # FractionOps (8)
    "FractionOps.create": SUPPORTED_PUBLIC,
    "FractionOps.to_latex": SUPPORTED_PUBLIC,
    "FractionOps.add": SUPPORTED_PUBLIC,
    "FractionOps.sub": SUPPORTED_PUBLIC,
    "FractionOps.mul": SUPPORTED_PUBLIC,
    "FractionOps.div": SUPPORTED_PUBLIC,
    "FractionOps.from_parts": SUPPORTED_PUBLIC,
    "FractionOps.to_exact": SUPPORTED_PUBLIC,
    # RadicalOps (21)
    "RadicalOps.create": DEPRECATED,
    "RadicalOps.is_perfect_square": INTERNAL,
    "RadicalOps.to_latex": DEPRECATED,
    "RadicalOps.add_term": INTERNAL,
    "RadicalOps.mul_terms": INTERNAL,
    "RadicalOps.div_terms": INTERNAL,
    "RadicalOps.get_prime_factors": INTERNAL,
    "RadicalOps.simplify_term": SUPPORTED_PUBLIC,
    "RadicalOps.simplify": DUPLICATE,
    "RadicalOps.format_term": SUPPORTED_PUBLIC,
    "RadicalOps.format_term_unsimplified": INTERNAL,
    "RadicalOps.format_expression": SUPPORTED_PUBLIC,
    "RadicalOps.add_dicts": INTERNAL,
    "RadicalOps.multiply_dicts": INTERNAL,
    "RadicalOps.simplify_root": DUPLICATE,
    "RadicalOps.normalize_term_list": SUPPORTED_PUBLIC,
    "RadicalOps.rationalize_linear_denominator": SUPPORTED_PUBLIC,
    "RadicalOps.scale_linear_radical": SUPPORTED_PUBLIC,
    "RadicalOps.add_linear_radicals": SUPPORTED_PUBLIC,
    "RadicalOps.format_linear_radical": SUPPORTED_PUBLIC,
    "RadicalOps.exact_integer": SUPPORTED_PUBLIC,
    # PolynomialOps (11)
    "PolynomialOps.normalize": SUPPORTED_PUBLIC,
    "PolynomialOps.format_latex": SUPPORTED_PUBLIC,
    "PolynomialOps.format_plain": INTERNAL,
    "PolynomialOps.add": SUPPORTED_PUBLIC,
    "PolynomialOps.sub": SUPPORTED_PUBLIC,
    "PolynomialOps.mul": SUPPORTED_PUBLIC,
    "PolynomialOps.random_poly": INTERNAL,
    "PolynomialOps.div_qr": SUPPORTED_PUBLIC,
    "PolynomialOps.coeffs_from_py_expression": SUPPORTED_PUBLIC,
    "PolynomialOps.to_degree_map": SUPPORTED_PUBLIC,
    "PolynomialOps.factor_quadratic_exact": SUPPORTED_PUBLIC,
}


def _c(signature: str, returns: str, *, inputs: str, shape: dict[str, Any],
       normalization: str, example: str) -> dict[str, Any]:
    return {
        "import": LIBRARY, "signature": signature,
        "returns_model_facing": returns, "input_constraints": inputs,
        "return_contract": shape, "normalization_responsibility": normalization,
        "usage_example": example,
    }


# Exact typed contracts for the supported surface.  Prompt rendering intentionally
# remains compact; detailed fields feed tests, preflight, and generated docs.
DOMAIN_API_SSOT: dict[str, dict[str, Any]] = {
    "IntegerOps.add": _c("(a, b)", "int", inputs="a,b: int; bool forbidden",
        shape={"type":"int","json_safe":True}, normalization="none", example="IntegerOps.add(2, 3)  # 5"),
    "IntegerOps.sub": _c("(a, b)", "int", inputs="a,b: int; bool forbidden",
        shape={"type":"int","json_safe":True}, normalization="none", example="IntegerOps.sub(2, 3)  # -1"),
    "IntegerOps.fmt_num": _c("(n)", "str", inputs="ordered numeric n",
        shape={"type":"str","json_safe":True}, normalization="presentation only", example='IntegerOps.fmt_num(-3)  # "(-3)"'),
    "IntegerOps.is_divisible": _c("(a, b)", "bool", inputs="integer-like a,b; b=0 returns False",
        shape={"type":"bool","json_safe":True}, normalization="not an answer integer", example="IntegerOps.is_divisible(156, 13)  # True"),
    "IntegerOps.prime_factorization": _c("(n)", "dict[int, int]  # prime -> exponent; ±1 -> {}",
        inputs="non-bool int; n!=0; factors abs(n)",
        shape={"type":"dict","keys":"positive primes","values":"positive int exponents","json_safe":True},
        normalization="no selected/answer field", example="IntegerOps.prime_factorization(12)  # {2:2, 3:1}"),
    "IntegerOps.positive_divisors": _c("(n)", "list[int]  # ascending positive divisors",
        inputs="non-bool int n>0; no other task filters",
        shape={"type":"list","element_types":["int"],"ordering":"ascending","json_safe":True},
        normalization="filter multiples in model assembly if needed", example="IntegerOps.positive_divisors(12)  # [1,2,3,4,6,12]"),
    "IntegerOps.safe_eval": _c("(expr)", "int | float  # bool and container results raise ValueError",
        inputs="arithmetic expression string using literals,+,-,*,/,//,%,**,abs,sum,min,max; trusted generated input only",
        shape={"type":"union","types":["int","float"],"json_safe":True,"forbidden_types":["bool","tuple","list","dict"]},
        normalization="exact-int contracts must require type(value) is int; floats are never coerced to int",
        example='IntegerOps.safe_eval("(-3)**3")  # -27'),
    "FractionOps.create": _c("(value)", "Fraction  # not JSON serializable; use the to_exact adapter",
        inputs="int, finite float, legal numeric str, or Fraction; bool forbidden",
        shape={"type":"Fraction","json_safe":False}, normalization="FractionOps.to_exact before correct_answer", example='FractionOps.create("3/5")  # Fraction(3, 5)'),
    "FractionOps.to_latex": _c("(val, mixed=False)", "str", inputs="exact value; mixed: bool",
        shape={"type":"str","json_safe":True}, normalization="presentation only; not semantic serialization", example=r"FractionOps.to_latex(Fraction(3,5))  # '\frac{3}{5}'"),
    "FractionOps.add": _c("(a, b)", "Fraction", inputs="a,b: Fraction",
        shape={"type":"Fraction","json_safe":False}, normalization="to_exact before correct_answer", example="FractionOps.add(Fraction(1,2), Fraction(1,3))"),
    "FractionOps.sub": _c("(a, b)", "Fraction", inputs="a,b: Fraction",
        shape={"type":"Fraction","json_safe":False}, normalization="to_exact before correct_answer", example="FractionOps.sub(Fraction(3,7), Fraction(-1,4))"),
    "FractionOps.mul": _c("(a, b)", "Fraction", inputs="a,b: Fraction",
        shape={"type":"Fraction","json_safe":False}, normalization="to_exact before correct_answer", example="FractionOps.mul(Fraction(1,2), Fraction(1,3))"),
    "FractionOps.div": _c("(a, b)", "Fraction", inputs="a,b: Fraction; b != 0",
        shape={"type":"Fraction","json_safe":False}, normalization="to_exact before correct_answer", example="FractionOps.div(Fraction(1,2), Fraction(1,3))"),
    "FractionOps.from_parts": _c("(numerator, denominator=1)", "Fraction", inputs="numerator,denominator: int; bool forbidden; denominator != 0",
        shape={"type":"Fraction","json_safe":False}, normalization="to_exact before correct_answer", example="FractionOps.from_parts(6,3)  # Fraction(2,1)"),
    "FractionOps.to_exact": _c("(value)", "int | str  # integer or irreducible 'p/q'", inputs="int, Fraction, or legal exact string; bool/float forbidden",
        shape={"type":"union","types":["int","str"],"string_schema":"^-?[0-9]+/[1-9][0-9]*$","json_safe":True}, normalization="official Fraction-to-JSON adapter", example="FractionOps.to_exact(Fraction(3,2))  # '3/2'"),
    "RadicalOps.simplify_term": _c("(coeff, radicand)", "tuple[int | Fraction, int]  # semantic (coefficient, square-free radicand)", inputs="exact coeff; non-negative int or Fraction radicand",
        shape={"type":"tuple","length":2,"elements":[{"types":["int","Fraction"]},{"type":"int"}],"json_safe":"partial"}, normalization="normalize_term_list or to_exact before JSON", example="RadicalOps.simplify_term(1,12)  # (2,3)"),
    "RadicalOps.format_term": _c("(coeff, radicand, is_first=True)", "str  # complete single-term LaTeX including coefficient/sign", inputs="semantic coefficient and radicand",
        shape={"type":"str","json_safe":True}, normalization="presentation only", example=r"RadicalOps.format_term(3,15)  # '3\sqrt{15}'"),
    "RadicalOps.format_expression": _c("(terms_dict, denominator=1)", "str  # complete compound-radical LaTeX", inputs="mapping radicand->coefficient; exact denominator",
        shape={"type":"str","json_safe":True}, normalization="presentation only", example=r"RadicalOps.format_expression({1:6,3:-1})  # '6 - \sqrt{3}'"),
    "RadicalOps.normalize_term_list": _c("(terms)", "list[dict]  # sorted; keys coefficient,radicand", inputs="list/tuple of pairs or coefficient/radicand dicts",
        shape={"type":"list","length":"variable","element":{"type":"dict","required_keys":["coefficient","radicand"],"value_types":{"coefficient":["int","str"],"radicand":["int"]}},"ordering":"ascending radicand","json_safe":True}, normalization="official radical semantic JSON adapter", example="RadicalOps.normalize_term_list([(1,12)])"),
    "RadicalOps.rationalize_linear_denominator": _c("(numerator, denom_rational, denom_radical_coeff, radicand)", "tuple[int | Fraction, int | Fraction, int]", inputs="exact rational coefficients; positive nonsquare radicand; nonzero conjugate denominator",
        shape={"type":"tuple","length":3,"elements":[{"types":["int","Fraction"]},{"types":["int","Fraction"]},{"type":"int"}],"json_safe":"partial"}, normalization="RadicalOps.exact_integer on integral leaves before JSON", example="RadicalOps.rationalize_linear_denominator(1,2,1,3)"),
    "RadicalOps.scale_linear_radical": _c("(term, k)", "dict  # LinearRadical JSON-safe ints",
        inputs="term LinearRadical dict; k nonzero non-bool int",
        shape={"type":"dict","required_keys":["rational","radical_coefficient","radicand"],"value_types":{"rational":["int"],"radical_coefficient":["int"],"radicand":["int"]},"json_safe":True},
        normalization="rejects k==0 and zero radical_coefficient", example='RadicalOps.scale_linear_radical({"rational":1,"radical_coefficient":1,"radicand":2}, 2)'),
    "RadicalOps.add_linear_radicals": _c("(term_a, term_b)", "dict  # LinearRadical JSON-safe ints",
        inputs="two LinearRadical dicts with identical positive radicand",
        shape={"type":"dict","required_keys":["rational","radical_coefficient","radicand"],"value_types":{"rational":["int"],"radical_coefficient":["int"],"radicand":["int"]},"json_safe":True},
        normalization="rejects mismatched radicand or zero result coefficient", example='RadicalOps.add_linear_radicals({"rational":1,"radical_coefficient":1,"radicand":2},{"rational":3,"radical_coefficient":-1,"radicand":2})'),
    "RadicalOps.format_linear_radical": _c("(term)", "str  # presentation LaTeX",
        inputs="LinearRadical dict",
        shape={"type":"str","json_safe":True}, normalization="presentation only", example=r'RadicalOps.format_linear_radical({"rational":1,"radical_coefficient":1,"radicand":2})  # "1+\sqrt{2}"'),
    "RadicalOps.exact_integer": _c("(value)", "int  # rejects non-integral rationals",
        inputs="non-bool int, integral Fraction, or integral 'p/q' string",
        shape={"type":"int","json_safe":True}, normalization="never returns str union", example="RadicalOps.exact_integer(Fraction(4,1))  # 4"),
    "PolynomialOps.normalize": _c("(coeffs)", "list[number]  # highest degree first; leading zeros removed", inputs="non-empty coefficient sequence",
        shape={"type":"list","length":"variable","ordering":"highest degree first","json_safe":"operand-dependent"}, normalization="preserves coefficient types", example="PolynomialOps.normalize([0,2,1])  # [2,1]"),
    "PolynomialOps.format_latex": _c("(coeffs, var='x')", "str", inputs="highest-degree-first numeric coefficients",
        shape={"type":"str","json_safe":True}, normalization="presentation only", example="PolynomialOps.format_latex([4,0])  # '4x'"),
    "PolynomialOps.add": _c("(c1, c2)", "list[number]  # operand-dependent coefficient type; highest degree first", inputs="coefficient lists with mutually arithmetic-compatible values",
        shape={"type":"list","length":"max operand length after normalization","ordering":"highest degree first","json_safe":"operand-dependent"}, normalization="use to_exact per Fraction coefficient before JSON", example="PolynomialOps.add([1,2],[3,4])  # [4,6]"),
    "PolynomialOps.sub": _c("(c1, c2)", "list[number]  # operand-dependent coefficient type; highest degree first", inputs="coefficient lists with mutually arithmetic-compatible values",
        shape={"type":"list","length":"max operand length after normalization","ordering":"highest degree first","json_safe":"operand-dependent"}, normalization="use to_exact per Fraction coefficient before JSON", example="PolynomialOps.sub([1,2],[3,4])  # [-2,-2]"),
    "PolynomialOps.mul": _c("(c1, c2)", "list[int | float | Fraction]  # operand-dependent; highest degree first", inputs="non-empty coefficient lists containing arithmetic-compatible int,float,Fraction; bool unsupported",
        shape={"type":"list","length":"len(c1)+len(c2)-1 before leading-zero normalization","element_types":["int","float","Fraction"],"ordering":"highest degree first","json_safe":"operand-dependent"}, normalization="Fraction coefficients require to_exact; exact tasks must not use float", example="PolynomialOps.mul([3,2],[13,-7])  # [39,5,-14]"),
    "PolynomialOps.div_qr": _c("(dividend_coefficients, divisor_coefficients)", "tuple[list[int | str], list[int | str]]  # quotient,remainder", inputs="non-empty exact coefficient lists: int,Fraction,or p/q; no bool/float; nonzero divisor",
        shape={"type":"tuple","length":2,"elements":[{"type":"list","element_types":["int","str"]},{"type":"list","element_types":["int","str"]}],"ordering":"highest degree first","json_safe":True}, normalization="already exact JSON leaves", example="PolynomialOps.div_qr([6,0,6],[1,-4])  # ([6,24],[102])"),
    "PolynomialOps.coeffs_from_py_expression": _c("(expression, var='x')", "list[Fraction]  # highest degree first", inputs="restricted polynomial expression using integer constants,+,-,*,nonnegative integer **",
        shape={"type":"list","length":"degree+1","element_types":["Fraction"],"ordering":"highest degree first","json_safe":False}, normalization="to_degree_map or to_exact per coefficient", example="PolynomialOps.coeffs_from_py_expression('(x+1)*(x-1)')"),
    "PolynomialOps.to_degree_map": _c("(coeffs)", "dict[str, int | str]  # descending degree insertion order", inputs="non-empty exact coefficient list",
        shape={"type":"dict","keys":"decimal degree strings","values":["int","str"],"ordering":"descending numeric degree insertion order","json_safe":True}, normalization="official polynomial JSON adapter", example="PolynomialOps.to_degree_map([1,0,-1])"),
    "PolynomialOps.factor_quadratic_exact": _c("(a, b, c)", "list[dict, dict]  # fixed length 2; keys x_coefficient,constant; int or 'p/q'; NOT a 3-tuple", inputs="exact rational a,b,c; a nonzero; rational roots required",
        shape={"type":"list","length":2,"element":{"type":"dict","required_keys":["x_coefficient","constant"],"value_types":["int","str"]},"ordering":"deterministic implementation order; consumers must not infer sorted roots","json_safe":True}, normalization="already JSON safe", example="PolynomialOps.factor_quadratic_exact(1,4,-12)"),
}

for _name, _contract in DOMAIN_API_SSOT.items():
    _contract["name"] = _name
    _contract["classification"] = SUPPORTED_PUBLIC


def runtime_public_inventory() -> list[str]:
    return sorted(f"{cls.__name__}.{name}" for cls in TOOLBOX_CLASSES for name, value in cls.__dict__.items() if not name.startswith("_") and callable(value))


def validate_inventory() -> list[str]:
    actual = set(runtime_public_inventory())
    declared = set(API_CLASSIFICATION)
    errors = [f"inventory_missing:{x}" for x in sorted(actual - declared)]
    errors += [f"inventory_stale:{x}" for x in sorted(declared - actual)]
    errors += [f"supported_missing_contract:{x}" for x, c in API_CLASSIFICATION.items() if c == SUPPORTED_PUBLIC and x not in DOMAIN_API_SSOT]
    errors += [f"nonpublic_in_contract:{x}" for x in DOMAIN_API_SSOT if API_CLASSIFICATION.get(x) != SUPPORTED_PUBLIC]
    return errors


def render_api_prompt_line(api_name: str) -> str:
    contract = require_ssot(api_name)
    return f"- `{api_name}` | import: `{contract['import']}` | signature: `{contract['signature']}` | returns: {contract['returns_model_facing']}"


def render_supported_api_reference(api_names: list[str] | None = None) -> str:
    names = sorted(api_names or DOMAIN_API_SSOT)
    blocks = ["# Generated from domain_api_ssot.py; do not edit by hand."]
    for name in names:
        c = require_ssot(name)
        blocks.extend([f"## {name}", render_api_prompt_line(name), f"- Inputs: {c['input_constraints']}", f"- Shape: `{json.dumps(c['return_contract'], ensure_ascii=False, sort_keys=True)}`", f"- Normalization: {c['normalization_responsibility']}", f"- Example: `{c['usage_example']}`", ""])
    return "\n".join(blocks).rstrip() + "\n"


def require_ssot(api_name: str) -> dict[str, Any]:
    if API_CLASSIFICATION.get(api_name) != SUPPORTED_PUBLIC:
        raise KeyError(f"Domain API is not SUPPORTED_PUBLIC: {api_name}")
    return DOMAIN_API_SSOT[api_name]


def callable_for(api_name: str):
    cls_name, method_name = api_name.split(".", 1)
    cls = {c.__name__: c for c in TOOLBOX_CLASSES}[cls_name]
    return getattr(cls, method_name)
