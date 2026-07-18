"""Forensic G4 on 113-10 repaired + experimental json.dumps unwrap rule.

Does NOT register on production allowlist.
Does NOT call generation models.
Does NOT modify raw artifacts on disk.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_research_healer_rules_l2_json_dumps_unwrap_experimental import (  # noqa: E402
    RULE_ID,
    apply,
    is_applicable,
    is_triggered,
)
from agent_tools.finals_rebuild.ce115_research_healer_protocol import sha256_text  # noqa: E402
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response  # noqa: E402
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle  # noqa: E402

OUT = (
    ROOT
    / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2"
    / "experimental_json_dumps_unwrap_01"
)

PRIOR = (
    ROOT
    / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2"
    / "experimental_kwargs_bag_inline_01"
)

REPAIRED = PRIOR / "113_10_ab2d_repaired_candidate.py"

V1_GEM = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_gemini_pilot_01/cells"
V1_QW = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_qwen_pilot_01/cells"
V2_GEM = ROOT / "docs/experiments/results/ce115_exam_ext_contract_aligned_v2_gemini_01/cells"
V2_QW = ROOT / "docs/experiments/results/ce115_exam_ext_contract_aligned_v2_qwen4b_01/cells"
MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"

TARGET_TASK = "ce115_ext_113_10_factorization_l1"
TARGET_CELL_V2 = (
    V2_QW / "qwen3_5_4b__ce115_ext_113_10_factorization_l1__ab2d__seed_2026071301"
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


def run_rule(source: str) -> dict[str, Any]:
    ctx: dict[str, Any] = {}
    applicable, guards, app_reason = is_applicable(source, ctx)
    triggered, trig_reason = is_triggered(source, ctx)
    before = sha256_text(source)
    new_source, validation, apply_reason = apply(source, ctx)
    after = sha256_text(new_source)
    changed = new_source != source
    return {
        "rule_id": RULE_ID,
        "layer": "L2",
        "guards": dict(guards),
        "transform": "unwrap_json_dumps_around_return_correct_answer",
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


def post_layers(source: str, frozen: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    outcome, _code, details = classify_response(
        source, {"oracle_payload": dict(frozen)}, dict(task)
    )
    gates = (details or {}).get("evaluation_gates") or {}
    return {
        "evaluator_rerun": True,
        "outcome": outcome,
        "g1": (gates.get("g1_evaluability") or {}).get("status"),
        "g2": (gates.get("g2_executability") or {}).get("status"),
        "g3": (gates.get("g3_contract_compliance") or {}).get("status"),
        "g4": (gates.get("g4_semantic_correctness") or {}).get("status"),
        "g4_reason": (gates.get("g4_semantic_correctness") or {}).get("reason"),
        "expected_answer": (details or {}).get("expected_answer"),
        "mismatch_reason": (details or {}).get("mismatch_reason"),
    }


def forensic_g4(repaired_src: str, task: dict[str, Any], frozen: dict[str, Any]) -> dict[str, Any]:
    # Execute generate in-process for value path (no model)
    ns: dict[str, Any] = {}
    exec(compile(repaired_src, str(REPAIRED), "exec"), ns, ns)
    value = ns["generate"](level=1)
    ca = value["correct_answer"]
    ca_type = type(ca).__name__
    parsed = None
    parse_ok = False
    if isinstance(ca, str):
        try:
            parsed = json.loads(ca)
            parse_ok = isinstance(parsed, dict)
        except json.JSONDecodeError:
            parsed = None
    elif isinstance(ca, dict):
        parsed = ca
        parse_ok = True

    oracle_on_raw = evaluate_math_task_oracle(task["oracle_type"], frozen, ca)
    oracle_on_parsed = (
        evaluate_math_task_oracle(task["oracle_type"], frozen, parsed) if parse_ok else None
    )

    expected = {
        "factors": [
            {"x_coefficient": 5, "constant": -2},
            {"x_coefficient": -15, "constant": 8},
        ]
    }
    # Algebraic path evidence (report-only)
    path = {
        "expression_source": "frozen_params['expression'] (inlined by prior experimental rule)",
        "api_chain": [
            "PolynomialOps.coeffs_from_py_expression(expression_str, var='x')",
            "PolynomialOps.factor_quadratic_exact(a, b, c)",
            "build factor_dict_1/2 from API list",
            "correct_answer = {'factors': [...]}",
            "return correct_answer=json.dumps(correct_answer)  # STRING WRAP",
        ],
        "api_factors_observed": parsed.get("factors") if isinstance(parsed, dict) else None,
        "expected_canonical_factors": expected["factors"],
        "algebraic_note": (
            "Predicted factors equal expected under overall sign flip of both linear factors; "
            "oracle accepts that equivalence when submitted_answer is a dict."
        ),
    }

    if isinstance(ca, str) and oracle_on_raw and not oracle_on_raw.get("is_correct") and (
        oracle_on_parsed and oracle_on_parsed.get("is_correct")
    ):
        failure_class = "a_format_wrapping"
        failure_label = (
            "格式/包裝層錯誤：值（經 json.loads + 符號翻轉等價）通過 oracle，"
            "但 correct_answer 以 json.dumps 字串回傳導致 oracle 拒收"
        )
    elif parse_ok and oracle_on_parsed and not oracle_on_parsed.get("is_correct"):
        failure_class = "b_math_algorithm"
        failure_label = "數學/演算法錯誤：dict 形態下 oracle 仍判定不正確"
    else:
        failure_class = "c_mixed_or_other"
        failure_label = "混合或其他（見 oracle 對照）"

    layers = post_layers(repaired_src, frozen, task)
    return {
        "correct_answer_runtime_type": ca_type,
        "correct_answer_raw": ca,
        "json_loads_ok": parse_ok,
        "parsed_dict": parsed,
        "expected_answer": expected,
        "oracle_on_raw_string_or_value": oracle_on_raw,
        "oracle_on_parsed_dict": oracle_on_parsed,
        "error_value_path": path,
        "failure_class": failure_class,
        "failure_label": failure_label,
        "layers_before_unwrap": layers,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = load_tasks()
    task = tasks[TARGET_TASK]
    art = json.loads((TARGET_CELL_V2 / "artifact.json").read_text(encoding="utf-8"))
    frozen = dict(art.get("frozen_parameters") or {})

    repaired_src = normalize(REPAIRED.read_text(encoding="utf-8"))
    forensic = forensic_g4(repaired_src, task, frozen)

    rule_on_repaired = run_rule(repaired_src)
    after_src = rule_on_repaired["output_source"]
    (OUT / "113_10_ab2d_repaired_then_unwrap_candidate.py").write_text(
        after_src, encoding="utf-8", newline="\n"
    )
    layers_after = post_layers(after_src, frozen, task) if rule_on_repaired["changed"] else None
    rescue = bool(layers_after and layers_after.get("outcome") == "passed")

    # Held-out regression
    cells_rows: list[dict[str, Any]] = []
    pass_misfires: list[dict[str, Any]] = []
    other_fail_misfires: list[dict[str, Any]] = []
    same_pattern_expected: list[dict[str, Any]] = []
    n_seen = n_pass = n_fail = n_skip = 0
    triggered_count = changed_count = 0

    for root, version in (
        (V1_GEM, "v1"),
        (V1_QW, "v1"),
        (V2_GEM, "v2"),
        (V2_QW, "v2"),
    ):
        if not root.exists():
            continue
        for art_path in sorted(root.glob("*/artifact.json")):
            cell_dir = art_path.parent
            a = json.loads(art_path.read_text(encoding="utf-8"))
            cand = cell_dir / "extracted_candidate.py"
            source = normalize(cand.read_text(encoding="utf-8")) if cand.exists() else ""
            status = a.get("evaluator_status")
            is_pass = status == "PASSED"
            row_base = {
                "cell_id": a.get("cell_id") or cell_dir.name,
                "task_id": a.get("task_id"),
                "condition": a.get("condition"),
                "model": a.get("model"),
                "version": version,
                "evaluator_status": status,
                "is_pass": is_pass,
            }
            if not source.strip():
                n_skip += 1
                cells_rows.append({**row_base, "skipped": True, "triggered": False, "changed": False})
                continue
            n_seen += 1
            rr = run_rule(source)
            if is_pass:
                n_pass += 1
            else:
                n_fail += 1
            if rr["triggered"]:
                triggered_count += 1
            if rr["changed"]:
                changed_count += 1
            row = {
                **row_base,
                "skipped": False,
                "applicable": rr["applicable"],
                "triggered": rr["triggered"],
                "changed": rr["changed"],
                "reason": rr["reason"],
                "before_hash": rr["before_hash"],
                "after_hash": rr["after_hash"],
            }
            cells_rows.append(row)

            is_target_lineage = (
                a.get("task_id") == TARGET_TASK
                and a.get("condition") == "ab2d"
                and "qwen" in str(a.get("model", "")).lower()
                and version == "v2"
            )

            if is_pass and (rr["triggered"] or rr["changed"]):
                pass_misfires.append(row)
            elif (not is_pass) and (rr["triggered"] or rr["changed"]):
                if is_target_lineage:
                    same_pattern_expected.append(row)
                else:
                    other_fail_misfires.append(row)

    regression_pass = len(pass_misfires) == 0 and len(other_fail_misfires) == 0
    experimental_status = (
        "experimental_candidate"
        if forensic["failure_class"] == "a_format_wrapping" and regression_pass and rule_on_repaired["changed"]
        else (
            "stopped_heldout_misfire"
            if not regression_pass
            else "diagnostic_only_or_not_advanced"
        )
    )

    summary = {
        "real_model_calls": 0,
        "rule_id": RULE_ID,
        "production_allowlist_modified": False,
        "experimental_status": experimental_status,
        "forensic_g4": forensic,
        "failure_nature": {
            "class": forensic["failure_class"],
            "label": forensic["failure_label"],
            "evidence": [
                "runtime correct_answer type is str via json.dumps",
                "oracle rejects str",
                "oracle accepts json.loads(str) dict (sign-flip equivalent)",
                "G3 PASS / G4 FAIL before unwrap",
            ],
        },
        "target_chain": {
            "input": "experimental_kwargs_bag_inline_01 repaired candidate",
            "rule_result": {k: v for k, v in rule_on_repaired.items() if k != "output_source"},
            "layers_after_unwrap_report_only": layers_after,
            "rescue_to_pass": rescue,
        },
        "heldout_regression": {
            "denominator_note": "v1 Gemini18 + v1 Qwen18 + v2 Gemini8 + v2 Qwen8 (=52); empty skipped",
            "n_cells_seen": n_seen,
            "n_pass": n_pass,
            "n_fail_with_candidate": n_fail,
            "n_skipped_empty": n_skip,
            "pass_triggered_or_changed": pass_misfires,
            "other_fail_triggered_or_changed": other_fail_misfires,
            "same_pattern_expected_triggers": same_pattern_expected,
            "regression_pass": regression_pass,
            "triggered_count": triggered_count,
            "changed_count": changed_count,
        },
        "generality_self_check": {
            "no_task_id_in_guards": True,
            "no_exam_numerics_in_guards": True,
            "no_candidate_snippet_in_guards": True,
            "unique_alternative_definition": (
                "Trigger iff return correct_answer value AST is json.dumps(<expr>) "
                "with one positional arg and only constant dumps kwargs; json imported."
            ),
            "note": "Guards remain complete without any single-task identifiers.",
        },
        "boundary_conclusion": {
            "advanced": experimental_status == "experimental_candidate",
            "status": experimental_status,
            "final_113_10": (
                "multi_layer_partially_repairable_rescue_to_pass"
                if rescue
                else (
                    "multi_layer_partially_repairable_not_rescued"
                    if experimental_status == "experimental_candidate"
                    else "stopped_or_unrepairable"
                )
            ),
            "note": (
                "Layer1 kwargs-empty-bag inline + Layer2 json.dumps unwrap. "
                "NOT added to production allowlist; awaits human review."
            ),
        },
    }

    (OUT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (OUT / "heldout_matrix.json").write_text(
        json.dumps(cells_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    rule_card = f"""# Experimental rule card: `{RULE_ID}`

Status: **{experimental_status}** (production allowlist unchanged)

## Forensic verdict on post-kwargs-inline G4

- Class: `{forensic['failure_class']}`
- {forensic['failure_label']}
- Raw type: `{forensic['correct_answer_runtime_type']}`
- Oracle on raw: `{oracle_flag(oracle_on_raw=forensic['oracle_on_raw_string_or_value'])}`
- Oracle on parsed dict: `{oracle_flag(oracle_on_raw=forensic['oracle_on_parsed_dict'])}`

## 9-field provenance (apply on repaired candidate)

| Field | Value |
|---|---|
| rule_id | `{RULE_ID}` |
| layer | L2 |
| guards | see summary.json target_chain.rule_result.guards |
| transform | unwrap `json.dumps(<expr>)` → `<expr>` on return `correct_answer` |
| triggered | {rule_on_repaired['triggered']} |
| changed | {rule_on_repaired['changed']} |
| reason | {rule_on_repaired['reason']} |
| before_hash / after_hash | `{rule_on_repaired['before_hash']}` / `{rule_on_repaired['after_hash']}` |
| validation | reparse_ok + post_unwrap_clean + correct_answer present |

## Safety argument

1. Generator contract requires `correct_answer` to be a JSON-compatible object (dict), not `str`.
2. `json.dumps(expr)` always produces `str` — structurally wrong return type.
3. Transform only removes the dumps wrapper; inner AST expression is unchanged (no invented values).
4. Guards: single `generate`, return dict, `correct_answer` is `json.dumps` with one positional arg, `import json` present.
5. No task_id / exam numerics / snippets; no oracle/evaluator used to accept/reject.
6. Transactional reparse + post-condition (no longer dumps) or rollback.

## Held-out regression

- regression_pass: {regression_pass}
- pass misfires: {len(pass_misfires)}
- other-fail misfires: {len(other_fail_misfires)}
- same-pattern expected (v2 113-10 Ab2d original): {len(same_pattern_expected)}
- rescue_to_pass after chain: {rescue}
"""
    (OUT / "RULE_CARD.md").write_text(rule_card, encoding="utf-8", newline="\n")

    forensic_md = f"""# G4 forensic: 113-10 Ab2d after kwargs-bag inline

## A. Mechanism

1. Prior experimental rule inlined empty `kwargs.get('frozen', {{}})` → frozen literal.
2. Candidate runs Domain API chain and builds a factors dict.
3. Return wraps answer as `json.dumps(correct_answer)` → **str**.
4. Oracle `exam_factorization_common_binomial` requires `dict` with `factors` list.
5. Field compare (report-only):
   - expected: `{json.dumps(forensic['expected_answer'], ensure_ascii=False)}`
   - predicted (parsed): `{json.dumps(forensic['parsed_dict'], ensure_ascii=False)}`
   - algebraically equivalent under overall sign flip; oracle accepts when typed as dict.
6. G4 fails solely because submitted type is str.

## B. Nature

**{forensic['failure_class']}** — {forensic['failure_label']}

## C/D. Follow-on

See `summary.json` / `RULE_CARD.md` for unwrap experimental rule + regression.
"""
    (OUT / "FORENSIC_G4.md").write_text(forensic_md, encoding="utf-8", newline="\n")

    print(
        json.dumps(
            {
                "out": str(OUT),
                "failure_class": forensic["failure_class"],
                "experimental_status": experimental_status,
                "regression_pass": regression_pass,
                "target_changed": rule_on_repaired["changed"],
                "rescue_to_pass": rescue,
                "pass_misfires": len(pass_misfires),
                "other_fail_misfires": len(other_fail_misfires),
                "same_pattern_expected": len(same_pattern_expected),
                "real_model_calls": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def oracle_flag(oracle_on_raw: dict[str, Any] | None) -> str:
    if not oracle_on_raw:
        return "n/a"
    return f"is_correct={oracle_on_raw.get('is_correct')}"


if __name__ == "__main__":
    main()
