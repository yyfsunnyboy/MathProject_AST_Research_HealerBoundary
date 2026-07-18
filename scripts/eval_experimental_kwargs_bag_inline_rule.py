"""Evaluate experimental kwargs-bag-inline rule on 113-10 + held-out regression.

Does NOT register the rule on production allowlist.
Does NOT call generation models.
Does NOT modify raw artifacts on disk.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_research_healer_rules_l2_kwargs_bag_inline_experimental import (  # noqa: E402
    RULE_ID,
    analyze_kwargs_bag_inline,
    apply,
    is_applicable,
    is_triggered,
)
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response  # noqa: E402
from agent_tools.finals_rebuild.ce115_research_healer_protocol import sha256_text  # noqa: E402

OUT = (
    ROOT
    / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2"
    / "experimental_kwargs_bag_inline_01"
)

V1_GEM = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_gemini_pilot_01/cells"
V1_QW = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_qwen_pilot_01/cells"
V2_GEM = ROOT / "docs/experiments/results/ce115_exam_ext_contract_aligned_v2_gemini_01/cells"
V2_QW = ROOT / "docs/experiments/results/ce115_exam_ext_contract_aligned_v2_qwen4b_01/cells"
MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"

TARGET_113_10 = (
    V2_QW
    / "qwen3_5_4b__ce115_ext_113_10_factorization_l1__ab2d__seed_2026071301"
)


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def load_tasks() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("task_id"):
            out[row["task_id"]] = row
    return out


def iter_cells(*roots: Path):
    for root in roots:
        if not root.exists():
            continue
        for art in sorted(root.glob("*/artifact.json")):
            yield art.parent


def cell_record(cell_dir: Path) -> dict[str, Any]:
    art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
    cand_path = cell_dir / "extracted_candidate.py"
    source = normalize(cand_path.read_text(encoding="utf-8")) if cand_path.exists() else ""
    frozen = art.get("frozen_parameters") or {}
    status = art.get("evaluator_status")
    return {
        "cell_id": art.get("cell_id") or cell_dir.name,
        "task_id": art.get("task_id"),
        "condition": art.get("condition"),
        "model": art.get("model"),
        "version": "v2" if "contract_aligned_v2" in str(cell_dir) else "v1",
        "evaluator_status": status,
        "is_pass": status == "PASSED",
        "infrastructure_valid": art.get("infrastructure_valid", True),
        "source": source,
        "frozen": frozen,
        "has_candidate": bool(source.strip()),
    }


def run_rule_on(source: str, frozen: dict[str, Any]) -> dict[str, Any]:
    ctx = {"frozen": frozen}
    applicable, guards, app_reason = is_applicable(source, ctx)
    triggered, trig_reason = is_triggered(source, ctx)
    before = sha256_text(source)
    new_source, validation, apply_reason = apply(source, ctx)
    after = sha256_text(new_source)
    changed = new_source != source
    # transactional validation already inside apply (reparse + correct_answer guard)
    return {
        "rule_id": RULE_ID,
        "layer": "L2",
        "guards": dict(guards),
        "transform": "replace_kwargs_get_empty_bag_rhs_with_literal_unique_covering_param_bag",
        "applicable": applicable,
        "triggered": triggered,
        "changed": changed,
        "reason": apply_reason if changed or triggered else trig_reason or app_reason,
        "before_hash": before,
        "after_hash": after,
        "validation": validation,
        "app_reason": app_reason,
        "trig_reason": trig_reason,
        "output_source": new_source if changed else source,
    }


def post_layers(source: str, frozen: dict[str, Any], task: dict[str, Any] | None) -> dict[str, Any]:
    """Reporting-only evaluator snapshot (not used to accept/reject the transform)."""
    if not task:
        return {"evaluator_rerun": False}
    outcome, _code, details = classify_response(
        source,
        {"oracle_payload": dict(frozen)},
        dict(task),
    )
    gates = (details or {}).get("evaluation_gates") or {}
    return {
        "evaluator_rerun": True,
        "outcome": outcome,
        "g1": (gates.get("g1_evaluability") or {}).get("status"),
        "g2": (gates.get("g2_executability") or {}).get("status"),
        "g2_exception": (gates.get("g2_executability") or {}).get("exception_type"),
        "g2_message": (gates.get("g2_executability") or {}).get("exception_message"),
        "g3": (gates.get("g3_contract_compliance") or {}).get("status"),
        "g4": (gates.get("g4_semantic_correctness") or {}).get("status"),
    }


def diagnostic_113_11(tasks: dict[str, dict[str, Any]]) -> dict[str, Any]:
    cell = (
        V2_QW
        / "qwen3_5_4b__ce115_ext_113_11_rationalize_l1__ab2d__seed_2026071301"
    )
    art = json.loads((cell / "artifact.json").read_text(encoding="utf-8"))
    source = normalize((cell / "extracted_candidate.py").read_text(encoding="utf-8"))
    frozen = art.get("frozen_parameters") or {}
    task = tasks.get(art["task_id"])

    # Static diagnostics
    tree = ast.parse(source)
    names_used = sorted(
        {
            n.id
            for n in ast.walk(tree)
            if isinstance(n, ast.Name) and n.id in {"RadicalOps", "FractionOps"}
        }
    )
    imports = [
        ast.dump(n)
        for n in tree.body
        if isinstance(n, (ast.Import, ast.ImportFrom))
    ]
    has_radical_import = "RadicalOps" in ast.dump(tree)
    # call shape
    calls = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if isinstance(n.func.value, ast.Name) and n.func.value.id == "RadicalOps":
                calls.append(
                    {
                        "attr": n.func.attr,
                        "nargs": len(n.args),
                        "keywords": [k.arg for k in n.keywords],
                    }
                )

    # Hypothetical import-only patch (diagnostic; not a healer rule)
    patched = (
        "from core.prompts.domain_function_library import RadicalOps, FractionOps\n"
        + source
    )
    # Also try with to_exact wrapping (still diagnostic, not a rule)
    patched_to_exact = patched  # keep import-only as primary diagnostic

    before = classify_response(source, {"oracle_payload": dict(frozen)}, dict(task))[0]
    after_import = classify_response(
        patched, {"oracle_payload": dict(frozen)}, dict(task)
    )
    # Second diagnostic: import + FractionOps.to_exact on a,b,value
    # Manual structural edit for diagnosis only — not proposed as general rule
    diagnostic_full = '''from core.prompts.domain_function_library import RadicalOps, FractionOps
from fractions import Fraction

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/(4 - sqrt(7))", "required_form": "a + b*sqrt(7)", "target_expression": "a + b"}
    numerator = Fraction(9)
    denom_rational = 4
    denom_radical_coeff = -1
    radicand = 7
    a, b, r = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)
    correct_answer_dict = {
        "a": FractionOps.to_exact(a),
        "b": FractionOps.to_exact(b),
        "radicand": int(r),
        "value": FractionOps.to_exact(a + b),
    }
    return {
        "question_text": "q",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params,
    }
'''
    # NOTE: diagnostic_full hardcodes exam values — marked diagnostic-only, not a rule candidate
    after_full = classify_response(
        diagnostic_full, {"oracle_payload": dict(frozen)}, dict(task)
    )

    return {
        "status": "diagnostic_only_not_allowlist",
        "cell_id": art.get("cell_id"),
        "before_outcome": before,
        "names_used_without_binding": names_used,
        "top_level_imports_dump": imports,
        "radicalops_imported": "RadicalOps" in source and "import" in source and "RadicalOps" in "".join(
            source.split("def generate")[0]
        ),
        "radical_calls": calls,
        "expected_signature": "RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand) -> tuple[Fraction, Fraction, int]",
        "call_arity_matches": all(c["attr"] == "rationalize_linear_denominator" and c["nargs"] == 4 for c in calls),
        "missing_fractionops_to_exact_in_original": "FractionOps" not in source,
        "after_import_only": {
            "outcome": after_import[0],
            "note": "import RadicalOps+FractionOps prepended; no other edits",
        },
        "after_import_and_to_exact_diagnostic_rewrite": {
            "outcome": after_full[0],
            "note": (
                "DIAGNOSTIC ONLY — uses exam-specific literals; NOT a general rule. "
                "Shows whether API call shape + to_exact can satisfy oracle when wiring is complete."
            ),
        },
        "conclusion": (
            "Original failure is NameError on RadicalOps (missing import). "
            "Call arity for rationalize_linear_denominator is structurally correct (4 args). "
            "Original also omits required FractionOps.to_exact. "
            "Import-only is insufficient for a general safe rule without also handling to_exact "
            "and without exam-specific hardcoding; no general import rule proposed this round."
        ),
    }


def unrepairable_notes() -> dict[str, Any]:
    return {
        "114-08_Ab2d": {
            "verdict": "essentially_unrepairable_deterministic",
            "machine_status": "RUNTIME_FAILURE",
            "reviewed_mechanism": "model_assembly_failure + tool_routing_gap + code_bloat",
            "reasons": [
                "Candidate defines a local RadicalOps class that shadows the production API.",
                "Local simplify_term / normalize_term_list reimplement incorrect algorithms with non-terminating/ambiguous control flow.",
                "Repair would require understanding and replacing invented domain logic — not a local structural rewrite.",
                "Beyond deterministic Healer scope (would be semantic/model-intent reconstruction).",
            ],
        },
        "114-02_Ab2d": {
            "verdict": "essentially_unrepairable_deterministic",
            "machine_status": "PARSE_MINOR",
            "reviewed_mechanism": "model_assembly_failure + code_bloat",
            "reasons": [
                "Invalid syntax in except-fallback branch (malformed ternary/if).",
                "Same class as withdrawn L1 comment-only-if precedent: restoring parse does not guarantee missing math/assembly is complete or no-op-safe.",
                "Fallback path invents sympy/manual coefficient logic; cannot deterministically know intended branch semantics.",
            ],
        },
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = load_tasks()

    # --- Target 113-10 ---
    target = cell_record(TARGET_113_10)
    target_result = run_rule_on(target["source"], target["frozen"])
    target_before_layers = post_layers(target["source"], target["frozen"], tasks.get(target["task_id"]))
    target_after_layers = (
        post_layers(target_result["output_source"], target["frozen"], tasks.get(target["task_id"]))
        if target_result["changed"]
        else None
    )
    rescue = bool(
        target_after_layers
        and target_after_layers.get("outcome") == "passed"
    )

    # --- Held-out regression: v1 36 + v2 16 ---
    heldout = []
    for cell_dir in iter_cells(V1_GEM, V1_QW, V2_GEM, V2_QW):
        rec = cell_record(cell_dir)
        if not rec["has_candidate"]:
            heldout.append(
                {
                    **{k: rec[k] for k in (
                        "cell_id", "task_id", "condition", "model", "version",
                        "evaluator_status", "is_pass", "infrastructure_valid",
                    )},
                    "skipped": True,
                    "skip_reason": "empty_candidate",
                    "triggered": False,
                    "changed": False,
                }
            )
            continue
        result = run_rule_on(rec["source"], rec["frozen"])
        heldout.append(
            {
                **{k: rec[k] for k in (
                    "cell_id", "task_id", "condition", "model", "version",
                    "evaluator_status", "is_pass", "infrastructure_valid",
                )},
                "skipped": False,
                "applicable": result["applicable"],
                "triggered": result["triggered"],
                "changed": result["changed"],
                "reason": result["reason"],
                "trig_reason": result["trig_reason"],
                "before_hash": result["before_hash"],
                "after_hash": result["after_hash"],
            }
        )

    # Regression gates
    pass_cells = [r for r in heldout if r.get("is_pass")]
    fail_cells = [r for r in heldout if not r.get("is_pass") and not r.get("skipped")]
    pass_triggered = [r for r in pass_cells if r.get("triggered") or r.get("changed")]
    # False trigger on other failures: any fail cell that is NOT the intended 113-10 v2 target
    other_fail_triggered = [
        r
        for r in fail_cells
        if (r.get("triggered") or r.get("changed"))
        and r.get("cell_id") != target["cell_id"]
    ]
    target_heldout = [r for r in heldout if r.get("cell_id") == target["cell_id"]]

    regression_pass = (len(pass_triggered) == 0 and len(other_fail_triggered) == 0)
    experimental_status = (
        "experimental_candidate"
        if regression_pass and target_result["changed"]
        else (
            "stopped_false_trigger"
            if not regression_pass
            else "stopped_no_change_on_target"
        )
    )

    summary = {
        "real_model_calls": 0,
        "rule_id": RULE_ID,
        "production_allowlist_modified": False,
        "experimental_status": experimental_status,
        "generality_self_check": {
            "no_task_id_in_guards": True,
            "no_exam_numerics_in_guards": True,
            "no_candidate_snippet_in_guards": True,
            "unique_alternative_definition": (
                "Available parameter bags := {context.frozen}. "
                "A bag covers static key-set S iff S ⊆ keys(bag). "
                "Trigger requires |covering bags| == 1."
            ),
            "note": (
                "Guards remain complete if any single-task identifiers are removed; "
                "they only mention AST shape + context.frozen coverage uniqueness."
            ),
        },
        "target_113_10": {
            "cell_id": target["cell_id"],
            "before_status": target["evaluator_status"],
            "rule_result": {k: v for k, v in target_result.items() if k != "output_source"},
            "before_layers_report_only": target_before_layers,
            "after_layers_report_only": target_after_layers,
            "rescue_to_pass": rescue,
        },
        "heldout_regression": {
            "denominator_note": "v1 Gemini18 + v1 Qwen18 + v2 Gemini8 + v2 Qwen8 (=52 artifact cells); empty candidates skipped",
            "n_cells_seen": len(heldout),
            "n_pass": len(pass_cells),
            "n_fail_with_candidate": len(fail_cells),
            "n_skipped_empty": sum(1 for r in heldout if r.get("skipped")),
            "pass_triggered_or_changed": pass_triggered,
            "other_fail_triggered_or_changed": other_fail_triggered,
            "target_row": target_heldout,
            "regression_pass": regression_pass,
            "triggered_count": sum(1 for r in heldout if r.get("triggered")),
            "changed_count": sum(1 for r in heldout if r.get("changed")),
        },
        "diagnostic_113_11": diagnostic_113_11(tasks),
        "unrepairable": unrepairable_notes(),
        "boundary_conclusion": None,
    }

    if experimental_status == "experimental_candidate":
        summary["boundary_conclusion"] = {
            "advanced": True,
            "status": "experimental_candidate",
            "note": (
                "General kwargs-empty-bag inline rule passed held-out no-op regression "
                "and changed the target cell. NOT added to production allowlist; awaits human review."
            ),
        }
    elif experimental_status == "stopped_false_trigger":
        summary["boundary_conclusion"] = {
            "advanced": False,
            "status": "stopped_false_trigger",
            "note": "Held-out misfire; rule stopped. Misfire cells retained as boundary evidence.",
            "misfires": {
                "pass_cells": pass_triggered,
                "other_fail_cells": other_fail_triggered,
            },
        }
    else:
        summary["boundary_conclusion"] = {
            "advanced": False,
            "status": experimental_status,
            "note": "No safe general change on target under stated guards, or regression gate failed.",
        }

    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "heldout_matrix.json").write_text(json.dumps(heldout, ensure_ascii=False, indent=2), encoding="utf-8")

    # Write repaired source for analysis only (not overwriting raw artifact)
    if target_result["changed"]:
        (OUT / "113_10_ab2d_repaired_candidate.py").write_text(
            target_result["output_source"], encoding="utf-8"
        )

    # Human-readable rule card
    card = f"""# Experimental rule card: `{RULE_ID}`

Status: **{experimental_status}** (production allowlist unchanged)

## 9-field provenance (target apply)

| Field | Value |
|---|---|
| rule_id | `{RULE_ID}` |
| layer | L2 |
| guards | see summary.json target_113_10.rule_result.guards |
| transform | replace `kwargs.get(K, {{}})` RHS with literal unique covering param bag |
| triggered | {target_result['triggered']} |
| changed | {target_result['changed']} |
| reason | {target_result['reason']} |
| before_hash / after_hash | `{target_result['before_hash']}` / `{target_result['after_hash']}` |
| validation | reparse_ok + correct_answer fingerprint unchanged |

## Safety argument (why unique covering bag is safe)

1. Evaluation invokes `generate(level=...)` without kwargs (empty `kwargs`).
2. Pattern `bag = kwargs.get(K, {{}})` therefore always binds `{{}}` at runtime.
3. Subsequent `bag[static_key]` reads are statically enumerated as set `S`.
4. Available parameter bags are defined as the singleton universe `{{context.frozen}}`.
5. Trigger requires `|{{ B in universe : S ⊆ keys(B) }}| == 1` (fail-closed uniqueness).
6. Transform only inlines that unique bag as a literal; invents no keys/values.
7. `correct_answer` AST/text fingerprint must be unchanged; else rollback.
8. Re-parse must succeed; else rollback.
9. Guards contain no task_id, exam numerics, or candidate snippets.

## Held-out regression

- regression_pass: {regression_pass}
- pass misfires: {len(pass_triggered)}
- other-fail misfires: {len(other_fail_triggered)}
- rescue_to_pass (report-only): {rescue}
"""
    (OUT / "RULE_CARD.md").write_text(card, encoding="utf-8")

    print(json.dumps({
        "out": str(OUT),
        "experimental_status": experimental_status,
        "regression_pass": regression_pass,
        "target_changed": target_result["changed"],
        "rescue_to_pass": rescue,
        "pass_misfires": len(pass_triggered),
        "other_fail_misfires": len(other_fail_triggered),
        "heldout_n": len(heldout),
        "real_model_calls": 0,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
