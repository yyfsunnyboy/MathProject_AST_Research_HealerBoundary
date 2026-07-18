"""Offline analysis for Math16 Gemini 48-cell run. Read-only on freeze assets."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
FREEZE_REPORT = ROOT / "docs/experiments/results/math16_latex_v1_freeze_closeout_report.json"
POOL = ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json"
EXPECTED_HEAD = "f7439a9a6bad70a70437b71b6afb7938dc7b90d7"
EXPECTED_HASHES = {
    "pool_identity_hash": "2ff41465d818d7e3d9b990a27ad2a1535e72c271bb04b2a37abe29cec1824636",
    "final_manifest_hash": "a4fc49b035cb6fed2d7a6946e241dc3ef36ed66f1a9fc09b3ecee5714a28a591",
    "task_freeze_hash": "349dfb2f786a4aa029453d844cac7eca07deb24a777ba1be4ef70f7002882e14",
    "manifest_file_sha256": "8f2d6b4a9bc55e2ba8d5c00b372b8421ba89463b9a0802865ff791ffce1c3b9e",
}
PASS = "PASSED"
RANK = {
    "PASSED": 3,
    "ANSWER_INCORRECT": 1,
    "INTRINSIC_SAFETY": 1,
    "PARSE_MINOR": 1,
    "EXECUTION_FAILURE": 0,
    "SCHEMA_FAILURE": 0,
    "API_FAILURE": 0,
    "MISSING": -1,
}


def load_artifacts() -> list[dict]:
    rows = []
    for cell_dir in sorted((RUN / "cells").iterdir()):
        art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
        art["_dir"] = str(cell_dir)
        art["_raw"] = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
        art["_prompt"] = (cell_dir / "prompt.txt").read_text(encoding="utf-8")
        code_path = cell_dir / "extracted_candidate.py"
        art["_code"] = code_path.read_text(encoding="utf-8") if code_path.exists() else None
        rows.append(art)
    return rows


def integrity(rows: list[dict]) -> dict:
    ids = [r["cell_id"] for r in rows]
    freeze = json.loads(FREEZE_REPORT.read_text(encoding="utf-8"))
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    file_sha = hashlib.sha256(POOL.read_bytes()).hexdigest()
    got_hashes = {
        "pool_identity_hash": pool["pool_identity_hash"],
        "final_manifest_hash": pool["manifest_content_sha256"],
        "task_freeze_hash": pool["task_freeze_hash"],
        "manifest_file_sha256": file_sha,
    }
    run_manifest = json.loads((RUN / "manifest.json").read_text(encoding="utf-8"))
    prompt_rows = [
        {"task_id": r["task_id"], "condition": r["condition"], "prompt_sha256": r["prompt_hash"]}
        for r in sorted(rows, key=lambda x: (x["task_id"], x["condition"]))
    ]
    # freeze report order follows pool task_ids × conditions
    expected_prompt = freeze["prompt_hashes_48"]
    # rebuild in freeze order
    by_key = {(r["task_id"], r["condition"]): r["prompt_hash"] for r in rows}
    rebuilt = [
        {"task_id": e["task_id"], "condition": e["condition"], "prompt_sha256": by_key[(e["task_id"], e["condition"])]}
        for e in expected_prompt
    ]
    prompt_match = rebuilt == expected_prompt
    component = freeze.get("all_hashes") or freeze.get("component_hashes") or {}
    parse_ok = True
    try:
        json.loads((RUN / "cell_results.json").read_text(encoding="utf-8"))
        json.loads((RUN / "summary.json").read_text(encoding="utf-8"))
        for line in (RUN / "cell_journal.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                json.loads(line)
    except Exception as exc:  # noqa: BLE001
        parse_ok = False
        parse_err = str(exc)
    else:
        parse_err = None

    accounting = []
    for r in rows:
        accounting.append(
            {
                "cell_id": r["cell_id"],
                "first_attempt_evaluator_outcome": r.get("first_attempt_evaluator_outcome"),
                "evaluator_status": r.get("evaluator_status"),
                "pipeline_correction_applied": (r.get("pipeline_correction") or {}).get("applied"),
                "healer_attempted": (r.get("healer") or {}).get("attempted"),
                "healer_enabled": (r.get("healer") or {}).get("enabled"),
                "overwritten": r.get("first_attempt_evaluator_outcome") != r.get("evaluator_status"),
            }
        )

    return {
        "n_artifacts": len(rows),
        "unique_cell_ids": len(set(ids)),
        "duplicate_cell_ids": [k for k, v in Counter(ids).items() if v > 1],
        "hashes_match_expected": got_hashes == EXPECTED_HASHES,
        "got_hashes": got_hashes,
        "run_freeze_hashes": run_manifest.get("freeze_hashes"),
        "run_freeze_hashes_match": run_manifest.get("freeze_hashes") == EXPECTED_HASHES,
        "prompt_hashes_match_freeze_report": prompt_match,
        "component_hashes_from_freeze": component,
        "json_parse_ok": parse_ok,
        "json_parse_error": parse_err,
        "accounting_overwrite_count": sum(1 for a in accounting if a["overwritten"]),
        "pipeline_applied_count": sum(1 for a in accounting if a["pipeline_correction_applied"]),
        "healer_attempted_count": sum(1 for a in accounting if a["healer_attempted"]),
        "expected_head": EXPECTED_HEAD,
        "pool_id": pool["pool_id"],
    }


def paired(rows: list[dict]) -> dict:
    by_task = defaultdict(dict)
    for r in rows:
        by_task[r["task_id"]][r["condition"]] = r["evaluator_status"]

    def cmp(a: str, b: str) -> str:
        ra, rb = RANK.get(a, -1), RANK.get(b, -1)
        if ra < rb:
            return "improved"
        if ra > rb:
            return "regressed"
        if a == b:
            return "unchanged_same_status"
        return "unchanged_rank"

    pairs = {"Ab1->Ab2g": [], "Ab1->Ab2d": [], "Ab2g->Ab2d": []}
    for tid, st in sorted(by_task.items()):
        pairs["Ab1->Ab2g"].append({"task_id": tid, "from": st.get("ab1"), "to": st.get("ab2g"), "change": cmp(st.get("ab1"), st.get("ab2g"))})
        pairs["Ab1->Ab2d"].append({"task_id": tid, "from": st.get("ab1"), "to": st.get("ab2d"), "change": cmp(st.get("ab1"), st.get("ab2d"))})
        pairs["Ab2g->Ab2d"].append({"task_id": tid, "from": st.get("ab2g"), "to": st.get("ab2d"), "change": cmp(st.get("ab2g"), st.get("ab2d"))})

    summary = {}
    for name, items in pairs.items():
        summary[name] = {
            "improved": [x["task_id"] for x in items if x["change"] == "improved"],
            "regressed": [x["task_id"] for x in items if x["change"] == "regressed"],
            "unchanged": [x["task_id"] for x in items if x["change"].startswith("unchanged")],
            "detail": items,
        }
    return summary


def forensic_cell(r: dict, pool_by_id: dict) -> dict:
    details = r.get("evaluator_details") or {}
    returned = details.get("returned_value")
    expected = details.get("expected_answer") or r.get("expected_answer")
    runtime_error = details.get("runtime_error") or details.get("oracle_error")
    question = None
    if isinstance(returned, dict):
        question = returned.get("question_text")
    code = r.get("_code") or ""
    adoption = r.get("adoption_status")
    # heuristics
    uses_domain = bool(re.search(r"(PolynomialOps|FractionOps|RadicalOps|IntegerOps)\.", code or ""))
    imports_domain = "domain_function_library" in (code or "")
    category = r.get("evaluator_status")
    suspicion = "model_math_or_codegen"
    validity = "VALID_MODEL_OUTCOME"
    notes = []

    if category == "ANSWER_INCORRECT":
        notes.append("oracle rejected correct_answer vs expected")
        # check if submitted nearly right / schema shape issues
        if isinstance(returned, dict) and isinstance(returned.get("correct_answer"), dict):
            ca = returned["correct_answer"]
            if "quotient" in ca and "remainder" in str(ca):
                notes.append("submitted includes quotient fields; remainder-only contract may be involved")
            if set(ca.keys()) - set(["remainder", "canonical_latex"]) and r["task_id"].endswith("remainder"):
                suspicion = "needs_schema_review"
                validity = "NEEDS_REVIEW"
        suspicion = suspicion if suspicion != "needs_schema_review" else suspicion
    elif category == "INTRINSIC_SAFETY":
        notes.append(f"oracle_error={runtime_error or details.get('oracle_error')}")
        # often latex/identity drift in math16 wrappers
        if "math16 identity drift" in str(details):
            suspicion = "evaluator_identity_wiring"
            validity = "INVALID_EVALUATOR"
            notes.append("math16 identity drift suggests evaluator expected freeze identity mismatch")
        elif details.get("oracle_error"):
            # inspect further in special cases
            suspicion = "model_or_oracle_payload"
            validity = "NEEDS_REVIEW"
    elif category == "EXECUTION_FAILURE":
        notes.append(f"runtime_error={runtime_error}")
        if "NameError" in str(runtime_error) or "not defined" in str(runtime_error):
            if uses_domain or "PolynomialOps" in str(runtime_error) or "RadicalOps" in str(runtime_error):
                suspicion = "ab2d_namespace_or_import"
                validity = "NEEDS_REVIEW"
                notes.append("possible missing domain injection or failed import")
            else:
                suspicion = "model_codegen_runtime"
        else:
            suspicion = "model_codegen_runtime"
    elif category == "PARSE_MINOR":
        suspicion = "model_codegen_syntax"
        notes.append(details.get("parse_error"))
    elif category == "SCHEMA_FAILURE":
        suspicion = "model_schema"
        validity = "VALID_MODEL_OUTCOME"

    # Ab2d toolbox interference signals
    ab2d_notes = []
    if r["condition"] == "ab2d":
        if isinstance(adoption, dict):
            ab2d_notes.append(
                {
                    "classification": adoption.get("classification"),
                    "missing_operations": adoption.get("missing_operations"),
                    "irrelevant_api_calls": adoption.get("irrelevant_api_calls"),
                    "called_apis": adoption.get("called_apis") or adoption.get("called_domain_apis"),
                    "domain_library_adopted": adoption.get("domain_library_adopted"),
                }
            )
            if adoption.get("classification") in {
                "REQUIRED_OPERATION_NOT_COVERED",
                "INVALID_API_CALL",
                "ASSEMBLY_SCAN_UNAVAILABLE",
            }:
                notes.append(f"ab2d_adoption={adoption.get('classification')}")

    pool_task = pool_by_id.get(r["task_id"], {})
    return {
        "cell_id": r["cell_id"],
        "task_id": r["task_id"],
        "condition": r["condition"],
        "domain_ops": r.get("domain_ops"),
        "evaluator_status": category,
        "failure_category": r.get("failure_category"),
        "actual_question_from_model": question,
        "math16_question_text": pool_task.get("math16_question_text") or r.get("math16_question_text"),
        "expected_answer": expected if expected is not None else r.get("expected_answer"),
        "submitted_correct_answer": returned.get("correct_answer") if isinstance(returned, dict) else None,
        "submitted_oracle_payload": returned.get("oracle_payload") if isinstance(returned, dict) else None,
        "runtime_or_oracle_error": runtime_error or details.get("oracle_error") or details.get("parse_error"),
        "code_excerpt": (code or "")[:1200],
        "uses_domain_api": uses_domain,
        "imports_domain_library": imports_domain,
        "ab2d_adoption": ab2d_notes,
        "suspicion": suspicion,
        "validity": validity,
        "notes": notes,
        "gates": r.get("gates") or details.get("evaluation_gates"),
        "latex_g6": r.get("latex_g6"),
        "api_attempts": r.get("api_attempts"),
        "token_metadata": r.get("token_metadata"),
        "duration_metadata": r.get("duration_metadata"),
        "prompt_hash": r.get("prompt_hash"),
    }


def special_checks(rows: list[dict], pool_by_id: dict, forensics: list[dict]) -> dict:
    by = {(r["task_id"], r["condition"]): r for r in rows}
    out = {}

    # q02
    q02 = [f for f in forensics if f["task_id"] == "ce111_q02_polynomial_division_remainder"]
    q02_common = all(f["evaluator_status"] == "ANSWER_INCORRECT" for f in q02) and len(q02) == 3
    q02_answers = [f["submitted_correct_answer"] for f in q02]
    # Check if evaluator would accept a normalized remainder
    from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle

    pool_q02 = pool_by_id["ce111_q02_polynomial_division_remainder"]
    gold = evaluate_math_task_oracle(
        pool_q02["oracle_type"], pool_q02["oracle_payload"], pool_q02["correct_answer"]
    )
    # try common alternates
    alts = [
        {"remainder": "4x", "canonical_latex": "4x"},
        {"remainder": "4*x", "canonical_latex": "4x"},
        {"remainder_coefficients": [4, 0], "canonical_latex": "4x"},
        {"remainder": [4, 0], "canonical_latex": "4x"},
    ]
    alt_results = {
        json.dumps(a, sort_keys=True): evaluate_math_task_oracle(
            pool_q02["oracle_type"], pool_q02["oracle_payload"], a
        )["is_correct"]
        for a in alts
    }
    out["q02"] = {
        "all_three_answer_incorrect": q02_common,
        "submitted_answers": q02_answers,
        "gold_oracle_accepts_freeze_correct_answer": gold["is_correct"],
        "alternate_forms_accepted": alt_results,
        "verdict": None,
    }
    # decide
    if q02_common and all(
        isinstance(a, dict) and a.get("remainder") not in (None, "4x") for a in q02_answers
    ):
        out["q02"]["verdict"] = "common_model_error_wrong_remainder"
    elif q02_common and any(
        isinstance(a, dict) and ("4x" in str(a) or a.get("remainder") == "4x") for a in q02_answers
    ):
        out["q02"]["verdict"] = "possible_schema_or_normalization_issue"
    else:
        out["q02"]["verdict"] = "mixed_or_needs_manual"

    # refine with actual content
    model_wrong = []
    schemaish = []
    for f in q02:
        ca = f["submitted_correct_answer"]
        if isinstance(ca, dict) and ca.get("remainder") == "4x" and ca.get("canonical_latex") == "4x":
            schemaish.append(f["condition"])
        else:
            model_wrong.append({"condition": f["condition"], "submitted": ca})
    if model_wrong and not schemaish:
        out["q02"]["verdict"] = "common_model_error"
        out["q02"]["validity"] = "VALID_MODEL_OUTCOME"
    elif schemaish:
        out["q02"]["verdict"] = "evaluator_or_schema_false_negative"
        out["q02"]["validity"] = "INVALID_EVALUATOR"
    out["q02"]["model_wrong_detail"] = model_wrong

    # q08
    q08_task = pool_by_id["ce111_q08_polynomial_factor_parameter_recovery"]
    q08_cells = [r for r in rows if r["task_id"] == q08_task["task_id"]]
    out["q08"] = {
        "freeze_correct_answer": q08_task["correct_answer"],
        "factor_order_policy": q08_task.get("factor_order_policy"),
        "oracle_payload": q08_task["oracle_payload"],
        "cells": [
            {
                "condition": r["condition"],
                "evaluator_status": r["evaluator_status"],
                "submitted": (r.get("evaluator_details") or {}).get("returned_value", {}).get("correct_answer")
                if isinstance((r.get("evaluator_details") or {}).get("returned_value"), dict)
                else None,
            }
            for r in q08_cells
        ],
        "strict_template_in_prompt": all("strict_source_template" in r.get("_prompt", "") for r in q08_cells),
        "legacy_wrong_absent_from_freeze_correct": q08_task["correct_answer"] == -12,
    }

    # q10
    q10 = pool_by_id["ce111_q10_ordered_quadratic_roots_radical"]
    from agent_tools.finals_rebuild.math16_oracles import normalize_compound_radical

    larger = normalize_compound_radical(q10["oracle_payload"]["larger_root"])
    smaller = normalize_compound_radical(q10["oracle_payload"]["smaller_root"])
    q10_cells = [r for r in rows if r["task_id"] == q10["task_id"]]
    out["q10"] = {
        "larger_coeff": larger[1],
        "smaller_coeff": smaller[1],
        "nested_payload": True,
        "cells": [
            {
                "condition": r["condition"],
                "evaluator_status": r["evaluator_status"],
                "submitted": (r.get("evaluator_details") or {}).get("returned_value", {}).get("correct_answer")
                if isinstance((r.get("evaluator_details") or {}).get("returned_value"), dict)
                else None,
                "oracle_error": (r.get("evaluator_details") or {}).get("oracle_error"),
            }
            for r in q10_cells
        ],
    }

    # q12
    q12 = pool_by_id["ce112_q12_independent_probability_fraction"]
    out["q12"] = {
        "transformation_level": q12["provenance"].get("transformation_level"),
        "cells": [
            {"condition": r["condition"], "evaluator_status": r["evaluator_status"]}
            for r in rows
            if r["task_id"] == q12["task_id"]
        ],
    }

    # q11
    q11 = pool_by_id["ce113_q11_rationalize_denominator"]
    out["q11"] = {
        "reuse_policy": q11.get("reuse_policy"),
        "historical_v2_reference_only": q11["provenance"].get("historical_v2_reference_only"),
        "cells": [
            {"condition": r["condition"], "evaluator_status": r["evaluator_status"], "run_id": r.get("run_id")}
            for r in rows
            if r["task_id"] == q11["task_id"]
        ],
        "no_v2_paths_in_artifacts": all(
            "v2" not in r.get("run_id", "") and "contract_aligned_v2" not in r.get("_dir", "")
            for r in rows
            if r["task_id"] == q11["task_id"]
        ),
    }

    # Ab2d failures
    ab2d_fail = [f for f in forensics if f["condition"] == "ab2d"]
    out["ab2d_failures"] = ab2d_fail
    return out


def main() -> None:
    rows = load_artifacts()
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    pool_by_id = {t["task_id"]: t for t in pool["tasks"]}
    integ = integrity(rows)

    # full table
    table = []
    for r in sorted(rows, key=lambda x: (x["task_id"], x["condition"])):
        table.append(
            {
                "cell_id": r["cell_id"],
                "task_id": r["task_id"],
                "domain_ops": r.get("domain_ops"),
                "condition": r["condition"],
                "evaluator_status": r["evaluator_status"],
                "failure_category": r.get("failure_category"),
                "prompt_hash": r.get("prompt_hash"),
                "api_attempts": len(r.get("api_attempts") or []),
                "wall_clock_seconds": (r.get("duration_metadata") or {}).get("wall_clock_seconds"),
                "total_token_count": (r.get("token_metadata") or {}).get("total_token_count"),
                "prompt_token_count": (r.get("token_metadata") or {}).get("prompt_token_count"),
                "candidates_token_count": (r.get("token_metadata") or {}).get("candidates_token_count"),
                "latex_g6_status": (r.get("latex_g6") or {}).get("status"),
                "first_attempt_evaluator_outcome": r.get("first_attempt_evaluator_outcome"),
                "pipeline_correction_applied": (r.get("pipeline_correction") or {}).get("applied"),
                "healer_enabled": (r.get("healer") or {}).get("enabled"),
                "healer_attempted": (r.get("healer") or {}).get("attempted"),
            }
        )

    non_pass = [r for r in rows if r["evaluator_status"] != PASS]
    forensics = [forensic_cell(r, pool_by_id) for r in non_pass]
    # deepen q02/intrinsic with oracle re-eval notes already in special
    special = special_checks(rows, pool_by_id, forensics)

    # refine validity using special + deeper inspection of INTRINSIC_SAFETY
    for f in forensics:
        if f["evaluator_status"] == "INTRINSIC_SAFETY":
            err = str(f.get("runtime_or_oracle_error") or "")
            # Check submitted vs freeze using audit payload
            task = pool_by_id[f["task_id"]]
            submitted = f["submitted_correct_answer"]
            from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle

            if submitted is not None:
                v = evaluate_math_task_oracle(task["oracle_type"], task["oracle_payload"], submitted)
                f["re_eval_is_correct"] = v.get("is_correct")
                f["re_eval_error"] = v.get("error")
                f["re_eval_expected"] = v.get("expected_answer")
                if v.get("is_correct"):
                    f["validity"] = "INVALID_EVALUATOR"
                    f["suspicion"] = "runner_or_oracle_wiring_false_negative"
                    f["notes"].append("re-eval with audit oracle_payload accepts submitted answer")
                elif "identity drift" in str(v.get("error") or ""):
                    f["validity"] = "INVALID_EVALUATOR"
                    f["suspicion"] = "math16_identity_hardcode_bug"
                else:
                    # still model wrong or schema
                    if v.get("error"):
                        f["validity"] = "NEEDS_REVIEW"
                    else:
                        f["validity"] = "VALID_MODEL_OUTCOME"
                        f["suspicion"] = "model_answer_incorrect_via_intrinsic_path"

    # Ab2d EXECUTION NameError check
    for f in forensics:
        if f["condition"] == "ab2d" and f["evaluator_status"] == "EXECUTION_FAILURE":
            err = str(f.get("runtime_or_oracle_error") or "")
            if "PolynomialOps" in err or "RadicalOps" in err or "NameError" in err:
                # runner injects all ops; if still NameError, model code bug or import shadowing
                if "not defined" in err and not f["imports_domain_library"]:
                    f["notes"].append("NameError without importing domain library; runner injects Ops into ns")
                    f["validity"] = "VALID_MODEL_OUTCOME"
                    f["suspicion"] = "model_failed_to_use_injected_or_imported_ops"

    # apply q02 special validity
    if special["q02"].get("validity"):
        for f in forensics:
            if f["task_id"] == "ce111_q02_polynomial_division_remainder":
                f["validity"] = special["q02"]["validity"]
                f["suspicion"] = special["q02"]["verdict"]

    paired_report = paired(rows)

    # treatment x outcome
    tx = defaultdict(Counter)
    for r in rows:
        tx[r["condition"]][r["evaluator_status"]] += 1
    dx = defaultdict(lambda: defaultdict(Counter))
    for r in rows:
        dx[r["domain_ops"]][r["condition"]][r["evaluator_status"]] += 1

    # G1-G6
    g6_counter = Counter((r.get("latex_g6") or {}).get("status") for r in rows)
    gate_fail = Counter()
    for r in rows:
        gates = r.get("gates") or (r.get("evaluator_details") or {}).get("evaluation_gates") or {}
        if isinstance(gates, dict):
            for gname, gval in gates.items():
                if isinstance(gval, dict) and gval.get("status") == "FAIL":
                    gate_fail[gname] += 1

    # tokens/duration
    durations = [((r.get("duration_metadata") or {}).get("wall_clock_seconds") or 0) for r in rows]
    tokens = [((r.get("token_metadata") or {}).get("total_token_count") or 0) for r in rows]
    attempts = [len(r.get("api_attempts") or []) for r in rows]

    validity_counts = Counter(f["validity"] for f in forensics)
    # passed cells are VALID_MODEL_OUTCOME
    validity_counts["VALID_MODEL_OUTCOME"] += sum(1 for r in rows if r["evaluator_status"] == PASS)

    production_bugs = [f for f in forensics if f["validity"] in {"INVALID_EVALUATOR", "INVALID_CONTRACT", "INVALID_INFRASTRUCTURE"}]
    needs_review = [f for f in forensics if f["validity"] == "NEEDS_REVIEW"]

    analysis = {
        "run_id": "gemini35flash_math16_latex_v1_ab123_run_001",
        "integrity": integ,
        "treatment_x_outcome": {k: dict(v) for k, v in tx.items()},
        "domain_x_treatment_x_outcome": {
            d: {c: dict(st) for c, st in conds.items()} for d, conds in dx.items()
        },
        "paired_comparisons": {
            k: {
                "improved": v["improved"],
                "regressed": v["regressed"],
                "unchanged": v["unchanged"],
            }
            for k, v in paired_report.items()
        },
        "paired_detail": paired_report,
        "g6_status_counts": dict(g6_counter),
        "gate_fail_counts": dict(gate_fail),
        "api_attempts": {
            "total_attempts": sum(attempts),
            "cells_with_retry": sum(1 for a in attempts if a > 1),
            "max_attempts": max(attempts) if attempts else 0,
        },
        "duration_token": {
            "wall_clock_total_seconds": sum(durations),
            "wall_clock_mean_seconds": (sum(durations) / len(durations)) if durations else 0,
            "token_total": sum(tokens),
            "token_mean": (sum(tokens) / len(tokens)) if tokens else 0,
        },
        "itt_accounting": {
            "first_attempt_fixed": True,
            "pipeline_correction_applied_count": integ["pipeline_applied_count"],
            "healer_attempted_count": integ["healer_attempted_count"],
            "overwrite_count": integ["accounting_overwrite_count"],
        },
        "special_checks": {
            "q02": special["q02"],
            "q08": special["q08"],
            "q10": special["q10"],
            "q12": special["q12"],
            "q11": special["q11"],
        },
        "validity_counts": dict(validity_counts),
        "production_bug_cells": [
            {"cell_id": f["cell_id"], "validity": f["validity"], "suspicion": f["suspicion"], "notes": f["notes"]}
            for f in production_bugs
        ],
        "needs_review_cells": [
            {"cell_id": f["cell_id"], "validity": f["validity"], "suspicion": f["suspicion"], "notes": f["notes"]}
            for f in needs_review
        ],
        "commit_allowed": integ["hashes_match_expected"]
        and integ["prompt_hashes_match_freeze_report"]
        and integ["json_parse_ok"]
        and integ["unique_cell_ids"] == 48
        and not production_bugs,
        "forensics_non_passed": forensics,
        "full_cell_table": table,
    }

    # write outputs
    (RUN / "analysis_summary.json").write_text(
        json.dumps({k: v for k, v in analysis.items() if k not in {"forensics_non_passed", "paired_detail", "full_cell_table"}}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (RUN / "full_cell_table.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (RUN / "full_cell_table.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(table[0].keys()))
        w.writeheader()
        w.writerows(table)
    (RUN / "forensic_report.json").write_text(json.dumps(forensics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RUN / "paired_comparison_report.json").write_text(json.dumps(paired_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (RUN / "validity_report.json").write_text(
        json.dumps(
            {
                "validity_counts": dict(validity_counts),
                "production_bug_cells": analysis["production_bug_cells"],
                "needs_review_cells": analysis["needs_review_cells"],
                "commit_allowed": analysis["commit_allowed"],
                "special_checks": analysis["special_checks"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (RUN / "analysis_full.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # markdown summary
    md = []
    md.append("# Math16 Gemini 48-cell analysis\n")
    md.append(f"- run_id: `{analysis['run_id']}`\n")
    md.append(f"- commit_allowed: **{analysis['commit_allowed']}**\n")
    md.append(f"- integrity hashes match: {integ['hashes_match_expected']}; prompt hashes match: {integ['prompt_hashes_match_freeze_report']}\n")
    md.append("\n## Treatment × outcome\n")
    md.append("```json\n" + json.dumps(analysis["treatment_x_outcome"], indent=2) + "\n```\n")
    md.append("\n## Paired comparisons\n")
    for k, v in analysis["paired_comparisons"].items():
        md.append(f"### {k}\n")
        md.append(f"- improved: {v['improved']}\n")
        md.append(f"- regressed: {v['regressed']}\n")
        md.append(f"- unchanged: {v['unchanged']}\n")
    md.append("\n## Validity\n")
    md.append(f"- counts: {analysis['validity_counts']}\n")
    md.append(f"- production_bug_cells: {len(analysis['production_bug_cells'])}\n")
    md.append(f"- needs_review_cells: {len(analysis['needs_review_cells'])}\n")
    md.append("\n## Special\n")
    md.append(f"- q02 verdict: {special['q02'].get('verdict')}\n")
    md.append(f"- q08 correct_answer freeze: {special['q08']['freeze_correct_answer']}\n")
    md.append(f"- q10 coeffs +/-: {special['q10']['larger_coeff']}/{special['q10']['smaller_coeff']}\n")
    md.append(f"- q12 transformation_level: {special['q12']['transformation_level']}\n")
    md.append(f"- q11 reuse_policy: {special['q11']['reuse_policy']}\n")
    md.append("\n## Non-PASSED forensics (short)\n")
    for f in forensics:
        md.append(
            f"- `{f['cell_id']}`: {f['evaluator_status']} | validity={f['validity']} | suspicion={f['suspicion']} | submitted={f['submitted_correct_answer']!r} | err={f.get('runtime_or_oracle_error')!r}\n"
        )
    (RUN / "analysis_summary.md").write_text("".join(md), encoding="utf-8")

    print(json.dumps({
        "commit_allowed": analysis["commit_allowed"],
        "production_bugs": len(production_bugs),
        "needs_review": len(needs_review),
        "treatment_x_outcome": analysis["treatment_x_outcome"],
        "q02_verdict": special["q02"].get("verdict"),
        "paired": analysis["paired_comparisons"],
        "validity_counts": dict(validity_counts),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
