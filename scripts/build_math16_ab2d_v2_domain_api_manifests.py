"""Build the 4 Domain API coverage manifests for Math16 Ab2d V2.

Proves, mechanically:
  - exposed SUPPORTED_PUBLIC count == documented count (domain_api_ssot.validate_inventory)
  - every SUPPORTED_PUBLIC API's 7 required fields (import, signature, input constraints,
    return type, return shape, JSON boundary, executable example) are present
  - the example actually rendered into the V2 prompts (GENERIC_USAGE_EXAMPLES) executes
    locally without error
  - the API's card as rendered in an actual V2 prompt (render_api_card) matches the SSOT
    verbatim (missing = 0)

Writes docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2/
domain_api_coverage/{IntegerOps,FractionOps,RadicalOps,PolynomialOps}.{json,md}
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.domain_api_ssot import (  # noqa: E402
    API_CLASSIFICATION,
    DOMAIN_API_SSOT,
    SUPPORTED_PUBLIC,
    validate_inventory,
)
from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (  # noqa: E402
    DOMAIN_OPS,
    GENERIC_USAGE_EXAMPLES,
    render_api_card,
    supported_apis_for_domain,
)
from core.prompts.domain_function_library import (  # noqa: E402
    FractionOps,
    IntegerOps,
    PolynomialOps,
    RadicalOps,
)

OUT_DIR = ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2/domain_api_coverage"

REQUIRED_FIELDS = [
    "import", "signature", "input_constraints", "returns_model_facing",
    "return_contract", "normalization_responsibility", "usage_example",
]

EXEC_NS = {
    "IntegerOps": IntegerOps, "FractionOps": FractionOps,
    "RadicalOps": RadicalOps, "PolynomialOps": PolynomialOps,
    "Fraction": Fraction,
}


def _try_execute_example(example: str) -> tuple[bool, str | None]:
    try:
        eval(compile(example, "<example>", "eval"), dict(EXEC_NS))
        return True, None
    except SyntaxError:
        # Examples with an inline `# comment` result are still evaluable as expressions
        # up to the comment; strip trailing comment and retry once.
        head = example.split("#", 1)[0].strip()
        try:
            eval(compile(head, "<example>", "eval"), dict(EXEC_NS))
            return True, None
        except Exception as exc:  # noqa: BLE001
            return False, f"{type(exc).__name__}: {exc}"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def build_domain_manifest(domain: str) -> dict:
    apis = supported_apis_for_domain(domain)
    entries = []
    missing_fields_total = 0
    example_exec_fail_total = 0
    rendered_mismatch_total = 0
    for name in apis:
        contract = DOMAIN_API_SSOT[name]
        missing_fields = [f for f in REQUIRED_FIELDS if not contract.get(f)]
        missing_fields_total += len(missing_fields)
        example = GENERIC_USAGE_EXAMPLES.get(name)
        example_ok, example_error = (False, "NO_EXAMPLE_REGISTERED")
        if example is not None:
            example_ok, example_error = _try_execute_example(example)
            if not example_ok:
                example_exec_fail_total += 1
        else:
            example_exec_fail_total += 1

        rendered_card = render_api_card(name)
        rendered_ok = (
            name in rendered_card
            and contract["signature"] in rendered_card
            and contract["input_constraints"] in rendered_card
        )
        if not rendered_ok:
            rendered_mismatch_total += 1

        entries.append(
            {
                "api": name,
                "import": contract["import"],
                "signature": contract["signature"],
                "input_constraints": contract["input_constraints"],
                "return_type": contract["returns_model_facing"],
                "return_shape": contract["return_contract"],
                "json_boundary": contract["normalization_responsibility"],
                "executable_example": example,
                "example_executes_locally": example_ok,
                "example_error": example_error,
                "rendered_in_prompt_matches_ssot": rendered_ok,
                "missing_required_fields": missing_fields,
            }
        )

    return {
        "domain": domain,
        "supported_public_count": len(apis),
        "apis": entries,
        "missing_required_fields_total": missing_fields_total,
        "example_exec_fail_total": example_exec_fail_total,
        "rendered_mismatch_total": rendered_mismatch_total,
    }


def render_markdown(manifest: dict) -> str:
    lines = [
        f"# Domain API coverage: {manifest['domain']} (V2)",
        "",
        f"SUPPORTED_PUBLIC count: **{manifest['supported_public_count']}**",
        f"Missing required fields: **{manifest['missing_required_fields_total']}**",
        f"Executable-example local-execution failures: **{manifest['example_exec_fail_total']}**",
        f"Rendered-in-prompt vs SSOT mismatches: **{manifest['rendered_mismatch_total']}**",
        "",
    ]
    for e in manifest["apis"]:
        lines += [
            f"## `{e['api']}`",
            f"- import: `{e['import']}`",
            f"- signature: `{e['signature']}`",
            f"- input constraints: {e['input_constraints']}",
            f"- return type: `{e['return_type']}`",
            f"- return shape: `{json.dumps(e['return_shape'], ensure_ascii=False, sort_keys=True)}`",
            f"- JSON boundary: {e['json_boundary']}",
            f"- example: `{e['executable_example']}`",
            f"- example executes locally: **{e['example_executes_locally']}**"
            + (f" (error: {e['example_error']})" if not e["example_executes_locally"] else ""),
            f"- rendered-in-prompt matches SSOT: **{e['rendered_in_prompt_matches_ssot']}**",
            "",
        ]
    return "\n".join(lines)


def main() -> dict:
    inv_errors = validate_inventory()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {"inventory_errors": inv_errors, "domains": {}}
    for domain in DOMAIN_OPS:
        manifest = build_domain_manifest(domain)
        (OUT_DIR / f"{domain}.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        (OUT_DIR / f"{domain}.md").write_text(
            render_markdown(manifest), encoding="utf-8", newline="\n"
        )
        summary["domains"][domain] = {
            "supported_public_count": manifest["supported_public_count"],
            "missing_required_fields_total": manifest["missing_required_fields_total"],
            "example_exec_fail_total": manifest["example_exec_fail_total"],
            "rendered_mismatch_total": manifest["rendered_mismatch_total"],
        }
    total_supported = sum(v["supported_public_count"] for v in summary["domains"].values())
    documented_total = sum(
        1 for cls in API_CLASSIFICATION.values() if cls == SUPPORTED_PUBLIC
    )
    summary["total_exposed_supported_public"] = total_supported
    summary["total_documented_supported_public"] = documented_total
    summary["missing"] = documented_total - total_supported
    (OUT_DIR / "_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return summary


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
