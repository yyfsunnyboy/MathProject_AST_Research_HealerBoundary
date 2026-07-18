"""Single source of truth for Math16 Ab2d Domain API model-facing contracts.

Prompt DOMAIN lines must be rendered from this registry. Do not maintain a
parallel handwritten returns string in TASK_DOMAIN_APIS.
"""
from __future__ import annotations

from typing import Any

LIBRARY = "core.prompts.domain_function_library"

# Model-facing return strings are the SSOT text embedded in prompts.
DOMAIN_API_SSOT: dict[str, dict[str, Any]] = {
    "PolynomialOps.div_qr": {
        "name": "PolynomialOps.div_qr",
        "import": LIBRARY,
        "signature": "(dividend_coefficients, divisor_coefficients)",
        "returns_model_facing": (
            "tuple[list, list]  # (quotient_coefficients, remainder_coefficients)"
        ),
        "return_contract": {
            "container": "tuple",
            "length": 2,
            "elements": [
                {"name": "quotient_coefficients", "type": "list"},
                {"name": "remainder_coefficients", "type": "list"},
            ],
            "json_safe": True,
        },
        "usage_example": (
            "q, r = PolynomialOps.div_qr([6, 0, 6], [1, -4])  # q=[6,24], r=[102]"
        ),
    },
    "PolynomialOps.factor_quadratic_exact": {
        "name": "PolynomialOps.factor_quadratic_exact",
        "import": LIBRARY,
        "signature": "(a, b, c)",
        "returns_model_facing": (
            "list[dict, dict]  # fixed length 2; each dict has keys "
            "x_coefficient and constant (int or irreducible 'p/q' str); "
            "NOT a 3-tuple of (roots, factorization_latex, roots_latex)"
        ),
        "return_contract": {
            "container": "list",
            "length": 2,
            "element": {
                "type": "dict",
                "required_keys": ("x_coefficient", "constant"),
                "value_types": ("int", "str"),
            },
            "ordering": (
                "two linear factors; root order is not guaranteed — "
                "compute roots as -constant/x_coefficient then sort if needed"
            ),
            "json_safe": True,
        },
        "usage_example": (
            "factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)\n"
            "# -> [{'x_coefficient': 1, 'constant': -2}, "
            "{'x_coefficient': 1, 'constant': 6}]\n"
            "roots = sorted(-Fraction(f['constant']) / Fraction(f['x_coefficient']) "
            "for f in factors)"
        ),
    },
    "PolynomialOps.format_latex": {
        "name": "PolynomialOps.format_latex",
        "import": LIBRARY,
        "signature": "(coeffs, var='x')",
        "returns_model_facing": "str",
        "return_contract": {"container": "str", "json_safe": True},
        "usage_example": "PolynomialOps.format_latex([4, 0])  # '4x'",
    },
    "PolynomialOps.mul": {
        "name": "PolynomialOps.mul",
        "import": LIBRARY,
        "signature": "(c1, c2)",
        "returns_model_facing": (
            "list[int | str]  # coefficient list, highest degree first"
        ),
        "return_contract": {
            "container": "list",
            "length": "variable",
            "element_types": ("int", "str"),
            "json_safe": True,
        },
        "usage_example": "PolynomialOps.mul([3, 2], [1, -7])  # [3, -19, -14]",
    },
    "FractionOps.create": {
        "name": "FractionOps.create",
        "import": LIBRARY,
        "signature": "(value)",
        "returns_model_facing": "Fraction",
        "return_contract": {
            "container": "Fraction",
            "json_safe": False,
            "json_note": "integer-valued Fraction may be normalized at Math16 JSON boundary",
        },
        "usage_example": "FractionOps.create(6)  # Fraction(6, 1)",
    },
    "FractionOps.add": {
        "name": "FractionOps.add",
        "import": LIBRARY,
        "signature": "(a, b)",
        "returns_model_facing": "Fraction",
        "return_contract": {"container": "Fraction", "json_safe": False},
        "usage_example": "FractionOps.add(Fraction(1, 2), Fraction(1, 3))",
    },
    "FractionOps.sub": {
        "name": "FractionOps.sub",
        "import": LIBRARY,
        "signature": "(a, b)",
        "returns_model_facing": "Fraction",
        "return_contract": {"container": "Fraction", "json_safe": False},
        "usage_example": "FractionOps.sub(Fraction(3, 7), Fraction(-1, 4))",
    },
    "FractionOps.mul": {
        "name": "FractionOps.mul",
        "import": LIBRARY,
        "signature": "(a, b)",
        "returns_model_facing": "Fraction",
        "return_contract": {"container": "Fraction", "json_safe": False},
        "usage_example": "FractionOps.mul(Fraction(2, 6), Fraction(1, 5))",
    },
    "FractionOps.to_latex": {
        "name": "FractionOps.to_latex",
        "import": LIBRARY,
        "signature": "(val, mixed=False)",
        "returns_model_facing": "str",
        "return_contract": {"container": "str", "json_safe": True},
        "usage_example": r"FractionOps.to_latex(Fraction(3, 5))  # '\frac{3}{5}'",
    },
    "IntegerOps.is_divisible": {
        "name": "IntegerOps.is_divisible",
        "import": LIBRARY,
        "signature": "(a, b)",
        "returns_model_facing": "bool",
        "return_contract": {"container": "bool", "json_safe": True},
        "usage_example": "IntegerOps.is_divisible(156, 13)  # True",
    },
    "IntegerOps.safe_eval": {
        "name": "IntegerOps.safe_eval",
        "import": LIBRARY,
        "signature": "(expr)",
        "returns_model_facing": "int | float  # numeric result of a safe arithmetic expression",
        "return_contract": {
            "container": "union",
            "types": ("int", "float"),
            "json_safe": True,
        },
        "usage_example": 'IntegerOps.safe_eval("(-3)**3")  # -27',
    },
    "IntegerOps.fmt_num": {
        "name": "IntegerOps.fmt_num",
        "import": LIBRARY,
        "signature": "(n)",
        "returns_model_facing": "str",
        "return_contract": {"container": "str", "json_safe": True},
        "usage_example": 'IntegerOps.fmt_num(-3)  # "(-3)"',
    },
    "RadicalOps.simplify_term": {
        "name": "RadicalOps.simplify_term",
        "import": LIBRARY,
        "signature": "(coeff, radicand)",
        "returns_model_facing": (
            "tuple[int | Fraction, int]  # (outer_coefficient, square_free_radicand)"
        ),
        "return_contract": {
            "container": "tuple",
            "length": 2,
            "elements": [
                {"name": "outer_coefficient", "types": ("int", "Fraction")},
                {"name": "square_free_radicand", "type": "int"},
            ],
            "json_safe": "partial",
        },
        "usage_example": "RadicalOps.simplify_term(1, 12)  # (2, 3)",
    },
    "RadicalOps.to_latex": {
        "name": "RadicalOps.to_latex",
        "import": LIBRARY,
        "signature": "(expr)",
        "returns_model_facing": "str",
        "return_contract": {"container": "str", "json_safe": True},
        "usage_example": "RadicalOps.to_latex(...)",
    },
}


def render_api_prompt_line(api_name: str) -> str:
    contract = DOMAIN_API_SSOT[api_name]
    return (
        f"- `{contract['name']}` | import: `{contract['import']}` | "
        f"signature: `{contract['signature']}` | returns: {contract['returns_model_facing']}"
    )


def require_ssot(api_name: str) -> dict[str, Any]:
    if api_name not in DOMAIN_API_SSOT:
        raise KeyError(f"Domain API missing from SSOT: {api_name}")
    return DOMAIN_API_SSOT[api_name]
