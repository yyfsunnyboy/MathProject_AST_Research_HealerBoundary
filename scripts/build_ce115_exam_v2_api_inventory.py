"""Generate production Domain API inventory + exam operation-to-API coverage matrix (v2)."""
from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.prompts.domain_function_library import (  # noqa: E402
    FractionOps,
    IntegerOps,
    LinearSystemOps,
    PolynomialOps,
    RadicalOps,
)
from agent_tools.finals_rebuild.ce115_contract_aligned_ablation_v2 import (  # noqa: E402
    LIBRARY,
    TASK_DOMAIN_APIS,
)

OUT = ROOT / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2"
IMPORT_PATH = LIBRARY

CLASSES = {
    "FractionOps": FractionOps,
    "IntegerOps": IntegerOps,
    "RadicalOps": RadicalOps,
    "PolynomialOps": PolynomialOps,
    "LinearSystemOps": LinearSystemOps,
}


def _method_inventory(cls: type) -> list[dict[str, Any]]:
    rows = []
    for name, member in sorted(cls.__dict__.items()):
        if name.startswith("_"):
            continue
        fn = member
        if isinstance(member, staticmethod):
            fn = member.__func__
        if not callable(fn):
            continue
        try:
            sig = str(inspect.signature(fn))
        except (TypeError, ValueError):
            sig = "(?)"
        doc = (inspect.getdoc(fn) or "").splitlines()
        rows.append(
            {
                "class": cls.__name__,
                "method": name,
                "qualname": f"{cls.__name__}.{name}",
                "import_path": IMPORT_PATH,
                "signature": sig,
                "doc_first_line": doc[0] if doc else "",
                "json_compatible_return": "unknown_manual",
                "needs_serialization": name in {"to_exact", "to_degree_map", "normalize_term_list", "factor_quadratic_exact"},
            }
        )
    return rows


COVERAGE: list[dict[str, Any]] = [
    {
        "exam": "114-01",
        "task_id": "ce115_ext_114_01_power_laws_l1",
        "required_operations": [
            "parse same-base powers",
            "add exponents on multiply",
            "subtract exponents on divide",
        ],
        "production_apis": ["IntegerOps.add", "IntegerOps.sub"],
        "coverage": "full",
        "partial_only": False,
        "forces_algorithm_rewrite": False,
        "contract_gap": None,
        "notes": "v1 wrongly listed FractionOps; IntegerOps adoption is optional.",
    },
    {
        "exam": "114-02",
        "task_id": "ce115_ext_114_02_polynomial_simplify_l1",
        "required_operations": [
            "expand/simplify polynomial expression",
            "emit nested coefficients degree map",
        ],
        "production_apis": [
            "PolynomialOps.coeffs_from_py_expression",
            "PolynomialOps.to_degree_map",
        ],
        "coverage": "full",
        "partial_only": False,
        "forces_algorithm_rewrite": False,
        "contract_gap": "BASE must require top-level key coefficients (fixed in Ab1-v2)",
        "notes": "v1 DOMAIN only FractionOps — coverage gap closed by new PolynomialOps helpers.",
    },
    {
        "exam": "114-04",
        "task_id": "ce115_ext_114_04_linear_system_l1",
        "required_operations": [
            "exact 2x2 solve",
            "evaluate x+2y",
            "serialize Fraction to int/'p/q'",
            "avoid illegal signed-denominator strings",
        ],
        "production_apis": [
            "LinearSystemOps.solve_2x2",
            "LinearSystemOps.evaluate_linear",
            "FractionOps.from_parts",
            "FractionOps.to_exact",
        ],
        "coverage": "full",
        "partial_only": False,
        "forces_algorithm_rewrite": False,
        "contract_gap": None,
        "notes": "FractionOps.create removed from DOMAIN; from_parts+to_exact for exact leaves.",
    },
    {
        "exam": "114-08",
        "task_id": "ce115_ext_114_08_radical_product_l1",
        "required_operations": [
            "multiply/distribute radical terms",
            "simplify_term",
            "merge and sort by radicand",
        ],
        "production_apis": [
            "RadicalOps.simplify_term",
            "RadicalOps.normalize_term_list",
        ],
        "coverage": "full",
        "partial_only": False,
        "forces_algorithm_rewrite": False,
        "contract_gap": None,
        "notes": "normalize_term_list encodes merge/sort contract.",
    },
    {
        "exam": "113-10",
        "task_id": "ce115_ext_113_10_factorization_l1",
        "required_operations": [
            "expand expression to quadratic",
            "factor into two linear factors",
        ],
        "production_apis": [
            "PolynomialOps.coeffs_from_py_expression",
            "PolynomialOps.factor_quadratic_exact",
        ],
        "coverage": "full",
        "partial_only": False,
        "forces_algorithm_rewrite": False,
        "contract_gap": None,
        "notes": "Reusable factorization; does not leak exam common binomial.",
    },
    {
        "exam": "113-11",
        "task_id": "ce115_ext_113_11_rationalize_l1",
        "required_operations": [
            "multiply by conjugate",
            "emit a+b*sqrt(r) and value a+b",
            "JSON serialize exact leaves",
        ],
        "production_apis": [
            "RadicalOps.rationalize_linear_denominator",
            "FractionOps.to_exact",
        ],
        "coverage": "full",
        "partial_only": False,
        "forces_algorithm_rewrite": False,
        "contract_gap": None,
        "notes": "Reusable rationalization; serialization via to_exact.",
    },
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = []
    for cls in CLASSES.values():
        inventory.extend(_method_inventory(cls))
    # Mark methods referenced by v2 prompts
    referenced = set()
    for apis in TASK_DOMAIN_APIS.values():
        for api in apis:
            referenced.add(api["name"])
    for row in inventory:
        row["referenced_by_v2_exam_domain"] = row["qualname"] in referenced
        row["tests_exist"] = "see tests/finals_rebuild/test_ce115_contract_aligned_v2_domain.py"

    inv_path = OUT / "production_api_inventory.json"
    cov_path = OUT / "operation_to_api_coverage_matrix.json"
    inv_path.write_text(json.dumps({"import_path": IMPORT_PATH, "methods": inventory}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    gaps = [c for c in COVERAGE if c["coverage"] != "full"]
    cov_path.write_text(
        json.dumps(
            {
                "matrix": COVERAGE,
                "all_covered": len(gaps) == 0,
                "gaps": gaps,
                "v2_task_domain_apis": {
                    tid: [a["name"] for a in apis] for tid, apis in TASK_DOMAIN_APIS.items()
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {inv_path}")
    print(f"wrote {cov_path}")
    print(f"all_covered={len(gaps)==0} methods={len(inventory)}")


if __name__ == "__main__":
    main()
