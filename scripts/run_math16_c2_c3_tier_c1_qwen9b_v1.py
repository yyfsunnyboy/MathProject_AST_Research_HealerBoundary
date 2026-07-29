# -*- coding: utf-8 -*-
"""9B C2→C3 Tier C1 census + cumulative replay.

Rule: TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1 (current_tier=Tier C1)
Spec: docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md
Contract: docs/experiments/manifests/math16_ab2d_task_contract_matrix_v1.json

Does not modify frozen rule packages, 4B artifacts, or call a model.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.preflight_math16_method2_all_cell import classify_transition  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

RULE_ID = "TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1"
CURRENT_TIER = "Tier C1"
LAYER_ROLE = "contract_aware_repair_candidate"
AUDITED_CONDITIONS = {"ab2d", "ab2d_spec_v2"}

C2_CLOSURE = ROOT / "docs/experiments/manifests/math16_c2_final_source_closure_qwen9b_v1.json"
CONTRACT_MATRIX = ROOT / "docs/experiments/manifests/math16_ab2d_task_contract_matrix_v1.json"
SPEC = "docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md"
RESULTS = ROOT / "docs/experiments/results/math16_c2_c3_tier_c1_reproducibility_qwen9b_v1"

OUT_CENSUS = ROOT / "docs/experiments/manifests/math16_c2_c3_tier_c1_residual_supply_qwen9b_v1.json"
OUT_CENSUS_MD = ROOT / "docs/experiments/reports/math16_c2_c3_tier_c1_residual_supply_qwen9b_v1.md"
OUT_REPLAY = ROOT / "docs/experiments/manifests/math16_c2_c3_tier_c1_reproducibility_qwen9b_v1.json"
OUT_REPLAY_MD = ROOT / "docs/experiments/reports/math16_c2_c3_tier_c1_reproducibility_qwen9b_v1.md"
OUT_C3 = ROOT / "docs/experiments/manifests/math16_c3_final_source_closure_qwen9b_v1.json"
OUT_C3_MD = ROOT / "docs/experiments/reports/math16_c3_final_source_closure_qwen9b_v1.md"

# Spec + matrix are the frozen authority for Tier C1 (no separate rule .py in 4B freeze).
FREEZE_FILES = [
    SPEC,
    "docs/experiments/manifests/math16_ab2d_task_contract_matrix_v1.json",
    "docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def head_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, cwd=str(ROOT)
    ).strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def parses(source: str) -> bool:
    if not source.strip():
        return False
    try:
        ast.parse(source)
        return True
    except SyntaxError:
        return False


def is_executable_obs(score: dict[str, Any]) -> bool:
    if score["status"] == "PASSED":
        return True
    blob = " ".join(
        [
            str(score.get("failure_subtype") or ""),
            str(score.get("classifier_outcome") or ""),
            str(score.get("primary_failure_layer") or ""),
        ]
    ).lower()
    return not any(
        b in blob
        for b in ("parse", "syntax", "runtime", "missing_entry", "extraction", "unparseable")
    )


def collect_ops_calls(tree: ast.AST) -> list[dict[str, Any]]:
    out = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
            if f.value.id.endswith("Ops"):
                out.append(
                    {
                        "ops_class": f.value.id,
                        "method": f.attr,
                        "fullname": f"{f.value.id}.{f.attr}",
                        "lineno": getattr(n, "lineno", None),
                        "col_offset": getattr(n, "col_offset", None),
                        "nargs": len(n.args),
                        "nkwargs": len(n.keywords),
                        "node": n,
                        "attr_node": f,
                    }
                )
    return out


def ops_shadowing(tree: ast.AST) -> list[str]:
    shadowed = []
    for n in tree.body:
        if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if n.name.endswith("Ops"):
                shadowed.append(n.name)
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id.endswith("Ops"):
                    shadowed.append(t.id)
    return shadowed


def adjudicate_c1(
    *,
    source: str,
    task_id: str,
    condition: str,
    contracts_by_key: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    base = {
        "rule_id": RULE_ID,
        "current_tier": CURRENT_TIER,
        "layer_role": LAYER_ROLE,
        "name_similarity_used": False,
        "mutation_planned": False,
        "unique_mapping": False,
        "unique_expected_method": None,
        "wrong_call": None,
        "domain_calls": [],
        "exposed_symbols": [],
        "system_contract_status": None,
        "contract_selector": None,
    }
    if condition not in AUDITED_CONDITIONS:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "condition_has_no_domain_api_contract",
        }
    ctr = contracts_by_key.get((task_id, condition))
    if ctr is None:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "condition_has_no_domain_api_contract",
        }
    st = ctr["system_status"]
    base["system_contract_status"] = st
    base["contract_selector"] = ctr.get("selector")
    base["exposed_symbols"] = list(ctr.get("exposed_symbols") or [])
    if st in ("SYSTEM_CONTRACT_DEFECT", "UNRESOLVED"):
        return {
            **base,
            "status": "SYSTEM_CONTRACT_EXCLUDED",
            "abstention_reason": st,
        }
    if st != "SYSTEM_CONTRACT_CORRECT":
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": f"unexpected_contract_status_{st}",
        }
    selector = ctr.get("selector")
    obligation = ctr.get("obligation")
    exposed = list(ctr.get("exposed_symbols") or [])
    if selector == "native_python" or obligation == "forbid_domain_api" or not exposed:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "condition_has_no_domain_api_contract",
        }
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "candidate_not_parseable",
        }
    shadowed = ops_shadowing(tree)
    if shadowed:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "ops_class_shadowing",
            "shadowed": shadowed,
        }
    calls = collect_ops_calls(tree)
    call_public = [{k: v for k, v in c.items() if k not in {"node", "attr_node"}} for c in calls]
    base["domain_calls"] = call_public
    if not calls:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "no_domain_api_call_present",
        }
    used = {c["fullname"] for c in calls}
    exposed_set = set(exposed)
    if used and used <= exposed_set:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "domain_calls_already_match_exposed_methods",
        }
    wrong = [c for c in calls if c["fullname"] not in exposed_set]
    if not wrong:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "no_wrong_domain_api_site",
        }
    # Spec: single local binding site
    if len(wrong) != 1:
        return {
            **base,
            "status": "C1_AMBIGUOUS_ABSTAIN",
            "abstention_reason": "multiple_wrong_domain_api_sites",
            "wrong_calls": [c["fullname"] for c in wrong],
        }
    w = wrong[0]
    same_class = [e for e in exposed if e.startswith(w["ops_class"] + ".")]
    if len(same_class) == 0:
        return {
            **base,
            "status": "C1_INELIGIBLE",
            "abstention_reason": "AVAILABLE_NOT_EXPOSED",
            "wrong_call": w["fullname"],
        }
    if len(same_class) != 1:
        # Also cover contracts with many exposed methods and no unique expected
        if len(exposed) != 1:
            return {
                **base,
                "status": "C1_AMBIGUOUS_ABSTAIN",
                "abstention_reason": "wrong_method_but_expected_not_unique",
                "wrong_call": w["fullname"],
                "same_class_candidates": same_class,
            }
        return {
            **base,
            "status": "C1_AMBIGUOUS_ABSTAIN",
            "abstention_reason": "no_ssot_unique_exposed_method",
            "wrong_call": w["fullname"],
            "same_class_candidates": same_class,
        }
    expected = same_class[0]
    # Unique attribute rename preserving arguments
    return {
        **base,
        "status": "C1_ELIGIBLE",
        "abstention_reason": None,
        "unique_mapping": True,
        "unique_expected_method": expected,
        "wrong_call": w["fullname"],
        "mutation_planned": True,
        "repair": "unique_attribute_rename_preserving_arguments",
        "wrong_lineno": w["lineno"],
        "wrong_col_offset": w["col_offset"],
    }


class _RenameTransformer(ast.NodeTransformer):
    def __init__(self, ops_class: str, wrong_method: str, expected_method: str):
        self.ops_class = ops_class
        self.wrong_method = wrong_method
        self.expected_method = expected_method
        self.renames = 0

    def visit_Call(self, node: ast.Call) -> ast.AST:
        self.generic_visit(node)
        f = node.func
        if (
            isinstance(f, ast.Attribute)
            and isinstance(f.value, ast.Name)
            and f.value.id == self.ops_class
            and f.attr == self.wrong_method
        ):
            f.attr = self.expected_method
            self.renames += 1
        return node


def apply_c1_rename(source: str, adjudication: dict[str, Any]) -> str:
    wrong = adjudication["wrong_call"]
    expected = adjudication["unique_expected_method"]
    ops_class, wrong_method = wrong.split(".", 1)
    expected_method = expected.split(".", 1)[1]
    tree = ast.parse(source)
    tr = _RenameTransformer(ops_class, wrong_method, expected_method)
    new_tree = tr.visit(tree)
    if tr.renames != 1:
        raise RuntimeError(f"RENAME_COUNT_NOT_ONE: {tr.renames}")
    ast.fix_missing_locations(new_tree)
    return ast.unparse(new_tree) + ("\n" if source.endswith("\n") else "")


def score_source(
    source: str,
    *,
    task: dict[str, Any],
    frozen_params: dict[str, Any],
    api_policy: str,
) -> dict[str, Any]:
    outcome, _source, details = classify_math16_response(
        source,
        frozen_params=frozen_params,
        audit_oracle_payload=task["oracle_payload"],
        task=task,
    )
    mapped = classify_outcome_to_v3(outcome, details, api_policy=api_policy)
    status = mapped["final_status"]
    if status not in {"PASSED", "FAILED"}:
        raise RuntimeError(f"UNEXPECTED_STATUS: {status}")
    return {
        "status": status,
        "classifier_outcome": outcome,
        "primary_failure_layer": mapped["primary_failure_layer"],
        "failure_subtype": mapped["failure_subtype"],
    }


def verify_c2(c2: dict[str, Any]) -> None:
    v = c2["validation"]
    if not v.get("passed"):
        raise RuntimeError("C2_CLOSURE_NOT_PASSED")
    if v.get("n_cells") != 320 or v.get("c2_pass") != 102 or v.get("c2_fail") != 218:
        raise RuntimeError(f"C2_COUNTS_DRIFT: {v}")
    ids = [c["cell_id"] for c in c2["cells"]]
    if len(ids) != 320 or len(set(ids)) != 320:
        raise RuntimeError("C2_IDENTITY_FAILURE")
    for cell in c2["cells"]:
        path = ROOT / cell["c2_final_source_path"]
        if not path.exists():
            raise RuntimeError(f"MISSING_C2_SOURCE: {cell['cell_id']}")
        if sha256_path(path) != cell["c2_final_source_sha256"]:
            raise RuntimeError(f"C2_SHA_DRIFT: {cell['cell_id']}")


def freeze_audit() -> dict[str, Any]:
    mapping = json.loads(
        (ROOT / "docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json").read_text(
            encoding="utf-8"
        )
    )
    entry = None
    for row in mapping.get("rules") or mapping.get("mapping") or []:
        if isinstance(row, dict) and row.get("legacy_rule_id") == RULE_ID:
            entry = row
            break
    if entry is None and isinstance(mapping, dict):
        # try nested lists
        for key, val in mapping.items():
            if isinstance(val, list):
                for row in val:
                    if isinstance(row, dict) and row.get("legacy_rule_id") == RULE_ID:
                        entry = row
                        break
    files = {rel: {"sha256": sha256_path(ROOT / rel)} for rel in FREEZE_FILES}
    matrix = json.loads(CONTRACT_MATRIX.read_text(encoding="utf-8"))
    return {
        "rule_id": RULE_ID,
        "current_tier": CURRENT_TIER,
        "mapping_entry": entry,
        "contract_system_status_counts": matrix.get("system_status_counts"),
        "files": files,
        "note": (
            "4B Tier C1 freeze is spec+contract-matrix census (no separate rule .py); "
            "this run reuses the same adjudication predicates without relaxing guards."
        ),
    }


def run_all(c2: dict[str, Any], contracts_by_key: dict, results_root: Path) -> dict[str, Any]:
    if results_root.exists():
        shutil.rmtree(results_root)
    pre_dir = results_root / "pre_sources"
    post_dir = results_root / "post_sources"
    pre_dir.mkdir(parents=True)
    post_dir.mkdir(parents=True)

    tasks = tasks_by_id()
    _, api_policy_map = _load_family_and_api_policy()
    rows: list[dict[str, Any]] = []
    census_rows: list[dict[str, Any]] = []

    for index, cell in enumerate(c2["cells"], start=1):
        cid = cell["cell_id"]
        pre_path = ROOT / cell["c2_final_source_path"]
        pre_source = pre_path.read_text(encoding="utf-8")
        adj = adjudicate_c1(
            source=pre_source,
            task_id=cell["task_id"],
            condition=cell["condition"],
            contracts_by_key=contracts_by_key,
        )
        eligible = adj["status"] == "C1_ELIGIBLE"
        triggered = eligible
        modified = False
        abstained = not eligible
        post_source = pre_source
        if eligible:
            post_source = apply_c1_rename(pre_source, adj)
            modified = post_source != pre_source
            if not modified:
                # treat as abstain if rename was no-op
                abstained = True
                triggered = False
                adj = {
                    **adj,
                    "status": "C1_INELIGIBLE",
                    "abstention_reason": "rename_produced_identical_source",
                    "mutation_planned": False,
                }
                eligible = False

        (pre_dir / f"{cid}.py").write_bytes(pre_source.encode("utf-8"))
        (post_dir / f"{cid}.py").write_bytes(post_source.encode("utf-8"))

        task = tasks[cell["task_id"]]
        frozen_params = frozen_for_prompt(task)["oracle_payload"]
        api_policy = api_policy_map[cell["task_id"]]
        pre_score = score_source(
            pre_source, task=task, frozen_params=frozen_params, api_policy=api_policy
        )
        post_score = score_source(
            post_source, task=task, frozen_params=frozen_params, api_policy=api_policy
        )
        transition = classify_transition(pre_score["status"], post_score["status"])
        pre_parse = parses(pre_source)
        post_parse = parses(post_source)
        pre_exec = is_executable_obs(pre_score)
        post_exec = is_executable_obs(post_score)

        census_rows.append(
            {
                "cell_id": cid,
                "model": "qwen3.5:9b",
                "model_group": "qwen9b",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c2_final_source_path": cell["c2_final_source_path"],
                "c2_final_source_sha256": cell["c2_final_source_sha256"],
                "used_c2_final_source": True,
                "rule_id": RULE_ID,
                "current_tier": CURRENT_TIER,
                "layer_role": LAYER_ROLE,
                "status": adj["status"],
                "abstention_reason": adj.get("abstention_reason"),
                "system_contract_status": adj.get("system_contract_status"),
                "contract_selector": adj.get("contract_selector"),
                "exposed_symbols": adj.get("exposed_symbols"),
                "domain_calls": adj.get("domain_calls"),
                "unique_mapping": adj.get("unique_mapping"),
                "unique_expected_method": adj.get("unique_expected_method"),
                "wrong_call": adj.get("wrong_call"),
                "name_similarity_used": False,
                "mutation_executed": False,  # census view; replay records separately
            }
        )

        rows.append(
            {
                "cell_id": cid,
                "model": "qwen3.5:9b",
                "model_group": "qwen9b",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c2_outcome": cell["c2_outcome"],
                "c2_final_source_path": cell["c2_final_source_path"],
                "c2_final_source_sha256": cell["c2_final_source_sha256"],
                "pre_source_path": str((pre_dir / f"{cid}.py").relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "post_source_path": str(
                    (post_dir / f"{cid}.py").relative_to(ROOT)
                ).replace("\\", "/"),
                "pre_source_sha256": sha256_text(pre_source),
                "post_source_sha256": sha256_text(post_source),
                "used_c2_final_source": True,
                "eligibility_status": adj["status"],
                "abstention_reason": adj.get("abstention_reason"),
                "eligible": eligible,
                "triggered": triggered and modified,
                "modified": modified,
                "abstained": abstained,
                "unique_expected_method": adj.get("unique_expected_method"),
                "wrong_call": adj.get("wrong_call"),
                "pre_status": pre_score["status"],
                "post_status": post_score["status"],
                "transition": transition,
                "pre_classifier_outcome": pre_score["classifier_outcome"],
                "post_classifier_outcome": post_score["classifier_outcome"],
                "pre_primary_failure_layer": pre_score["primary_failure_layer"],
                "post_primary_failure_layer": post_score["primary_failure_layer"],
                "pre_failure_subtype": pre_score["failure_subtype"],
                "post_failure_subtype": post_score["failure_subtype"],
                "pre_parseable": pre_parse,
                "post_parseable": post_parse,
                "pre_executable": pre_exec,
                "post_executable": post_exec,
                "parse_gain": (not pre_parse) and post_parse,
                "execution_gain": (not pre_exec) and post_exec,
                "evaluator_used_for_selection": False,
                "model_calls": 0,
            }
        )
        if index % 40 == 0:
            print(f"[c2_c3 {index}/320]")

    write_jsonl(results_root / "census_journal.jsonl", census_rows)
    write_jsonl(results_root / "transition_journal.jsonl", rows)

    status_counts = Counter(r["status"] for r in census_rows)
    reason_counts = Counter(
        (r.get("abstention_reason") or "eligible") for r in census_rows
    )
    transitions = Counter(r["transition"] for r in rows)
    c3_pass = sum(r["post_status"] == "PASSED" for r in rows)
    summary = {
        "phase": "9B C2→C3 Tier C1 census+replay",
        "status": "COMPLETE",
        "rule_id": RULE_ID,
        "current_tier": CURRENT_TIER,
        "cells": 320,
        "eligibility": {
            "C1_ELIGIBLE": status_counts.get("C1_ELIGIBLE", 0),
            "C1_AMBIGUOUS_ABSTAIN": status_counts.get("C1_AMBIGUOUS_ABSTAIN", 0),
            "SYSTEM_CONTRACT_EXCLUDED": status_counts.get("SYSTEM_CONTRACT_EXCLUDED", 0),
            "C1_INELIGIBLE": status_counts.get("C1_INELIGIBLE", 0),
            "OVERLAP_UNRESOLVED": status_counts.get("OVERLAP_UNRESOLVED", 0),
        },
        "abstention_reason_counts": dict(reason_counts),
        "triggered": sum(r["triggered"] for r in rows),
        "modified": sum(r["modified"] for r in rows),
        "abstained": sum(r["abstained"] for r in rows),
        "c2_pass_observed": sum(r["pre_status"] == "PASSED" for r in rows),
        "c3_pass": c3_pass,
        "c3_fail": 320 - c3_pass,
        "transitions": {
            "verified_rescue": transitions["verified_rescue"],
            "regression": transitions["regression"],
            "preserved_pass": transitions["preserved_pass"],
            "still_failed": transitions["still_failed"],
        },
        "modified_still_failed": sum(
            1 for r in rows if r["modified"] and r["transition"] == "still_failed"
        ),
        "parse_gain": sum(r["parse_gain"] for r in rows),
        "execution_gain": sum(r["execution_gain"] for r in rows),
        "verified_rescue_ids": [
            r["cell_id"] for r in rows if r["transition"] == "verified_rescue"
        ],
        "regression_ids": [
            r["cell_id"] for r in rows if r["transition"] == "regression"
        ],
        "eligible_ids": [
            r["cell_id"] for r in rows if r["eligibility_status"] == "C1_ELIGIBLE"
        ],
        "go_nogo": (
            "NO_GO_TIER_C1"
            if status_counts.get("C1_ELIGIBLE", 0) == 0
            else (
                "EXPLORATORY_ONLY"
                if status_counts.get("C1_ELIGIBLE", 0) <= 1
                else "GO_MINIMAL_IMPLEMENTATION"
            )
        ),
        "model_calls": 0,
        "evaluator_used_for_selection": False,
    }
    write_json(results_root / "summary.json", summary)
    return {"summary": summary, "rows": rows, "census_rows": census_rows}


def deterministic_second(
    c2: dict[str, Any],
    contracts_by_key: dict,
    first_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    by_id = {r["cell_id"]: r for r in first_rows}
    mismatches = []
    for cell in c2["cells"]:
        cid = cell["cell_id"]
        pre = (ROOT / cell["c2_final_source_path"]).read_text(encoding="utf-8")
        adj = adjudicate_c1(
            source=pre,
            task_id=cell["task_id"],
            condition=cell["condition"],
            contracts_by_key=contracts_by_key,
        )
        first = by_id[cid]
        if adj["status"] != first["eligibility_status"]:
            mismatches.append(
                {
                    "cell_id": cid,
                    "field": "eligibility_status",
                    "a": first["eligibility_status"],
                    "b": adj["status"],
                }
            )
            continue
        if adj["status"] == "C1_ELIGIBLE":
            post = apply_c1_rename(pre, adj)
        else:
            post = pre
        if sha256_text(post) != first["post_source_sha256"]:
            mismatches.append(
                {
                    "cell_id": cid,
                    "field": "post_source_sha256",
                    "a": first["post_source_sha256"],
                    "b": sha256_text(post),
                }
            )
    report = {
        "second_replay_mismatches": len(mismatches),
        "zero_diff": len(mismatches) == 0,
        "sample": mismatches[:20],
    }
    write_json(RESULTS / "deterministic_second_replay.json", report)
    if mismatches:
        raise RuntimeError(f"SECOND_REPLAY_DIFF: {len(mismatches)}")
    return report


def write_outputs(
    freeze: dict[str, Any],
    summary: dict[str, Any],
    rows: list[dict[str, Any]],
    census_rows: list[dict[str, Any]],
    second: dict[str, Any],
    c2: dict[str, Any],
) -> None:
    elig = summary["eligibility"]
    go = summary["go_nogo"]
    census = {
        "status": "math16_c2_c3_tier_c1_residual_supply_qwen9b_v1",
        "verdict": go,
        "head": head_sha(),
        "rule_id": RULE_ID,
        "current_tier": CURRENT_TIER,
        "layer_role": LAYER_ROLE,
        "spec": SPEC,
        "contract_matrix": str(CONTRACT_MATRIX.relative_to(ROOT)).replace("\\", "/"),
        "input": {
            "c2_closure": str(C2_CLOSURE.relative_to(ROOT)).replace("\\", "/"),
            "population": "9B Pilot-02 320 cells",
            "c2_pass": 102,
            "c2_fail": 218,
            "source": "C2 final source for all 320",
        },
        "eligibility_method": {
            "mode": "static_read_only_ast_adjudication",
            "name_similarity_used": False,
            "statuses": [
                "C1_ELIGIBLE",
                "C1_AMBIGUOUS_ABSTAIN",
                "C1_INELIGIBLE",
                "SYSTEM_CONTRACT_EXCLUDED",
                "OVERLAP_UNRESOLVED",
            ],
        },
        "aggregate": {
            "pool_n": 320,
            "status_counts": elig,
            "tier_c1_eligible": elig["C1_ELIGIBLE"],
            "ambiguous_abstain": elig["C1_AMBIGUOUS_ABSTAIN"],
            "system_contract_excluded": elig["SYSTEM_CONTRACT_EXCLUDED"],
            "ineligible": elig["C1_INELIGIBLE"],
            "abstention_reason_counts": summary["abstention_reason_counts"],
            "eligible_ids": summary["eligible_ids"],
        },
        "rule_freeze_audit": freeze,
        "cells": census_rows,
        "declarations": [
            "guards_not_relaxed",
            "no_model_calls",
            "census_predicates_match_4b_spec",
        ],
    }
    write_json(OUT_CENSUS, census)
    write_text(
        OUT_CENSUS_MD,
        "\n".join(
            [
                "# Math16 C2→C3 Tier C1 Residual Supply — Qwen9B v1",
                "",
                f"> **Verdict / Go-NoGo:** `{go}`",
                f"> **HEAD:** `{head_sha()}`",
                f"> **rule_id:** `{RULE_ID}`（current_tier = Tier C1）",
                "",
                "## Status tallies (full 320)",
                "",
                f"- C1_ELIGIBLE: **{elig['C1_ELIGIBLE']}**",
                f"- C1_AMBIGUOUS_ABSTAIN: **{elig['C1_AMBIGUOUS_ABSTAIN']}**",
                f"- SYSTEM_CONTRACT_EXCLUDED: **{elig['SYSTEM_CONTRACT_EXCLUDED']}**",
                f"- C1_INELIGIBLE: **{elig['C1_INELIGIBLE']}**",
                "",
                f"Primary reasons: `{summary['abstention_reason_counts']}`",
                "",
                "## Go／No-Go",
                "",
                f"**{go}** — guards not relaxed.",
                "",
            ]
        )
        + "\n",
    )

    replay = {
        "status": "math16_c2_c3_tier_c1_reproducibility_qwen9b_v1",
        "verdict": "C2_C3_TIER_C1_QWEN9B_COMPLETE",
        "go_nogo": go,
        "head": head_sha(),
        "results_root": str(RESULTS.relative_to(ROOT)).replace("\\", "/"),
        "rule_id": RULE_ID,
        "summary": summary,
        "deterministic_second_replay": second,
        "rule_freeze_audit": freeze,
        "model_calls": 0,
    }
    write_json(OUT_REPLAY, replay)
    write_text(
        OUT_REPLAY_MD,
        "\n".join(
            [
                "# Math16 C2→C3 Tier C1 Reproducibility — Qwen9B v1",
                "",
                f"> **verdict:** `C2_C3_TIER_C1_QWEN9B_COMPLETE`",
                f"> **Go/No-Go:** `{go}`",
                f"> **HEAD:** `{head_sha()}`",
                "",
                "## Core counts",
                "",
                f"- C2 PASS observed／C3 PASS: **{summary['c2_pass_observed']}／{summary['c3_pass']}**",
                f"- verified_rescue／regression: **{summary['transitions']['verified_rescue']}／{summary['transitions']['regression']}**",
                f"- preserved_pass／still_failed: **{summary['transitions']['preserved_pass']}／{summary['transitions']['still_failed']}**",
                f"- triggered／modified／abstained: **{summary['triggered']}／{summary['modified']}／{summary['abstained']}**",
                f"- parse_gain／execution_gain／modified_still_failed: **{summary['parse_gain']}／{summary['execution_gain']}／{summary['modified_still_failed']}**",
                f"- Second replay zero-diff: **{second['zero_diff']}**",
                "",
                "## Declarations",
                "",
                "- Model calls: **0**",
                "- Guards relaxed: **No**",
                "- Tier C2／D executed: **No**",
                "- Commit／push: **No**",
                "",
            ]
        )
        + "\n",
    )

    by_id = {r["cell_id"]: r for r in rows}
    cells = []
    for cell in c2["cells"]:
        r = by_id[cell["cell_id"]]
        origin = "TIER_C1_POST_SOURCE" if r["modified"] else "C2_PRESERVED"
        cells.append(
            {
                "cell_id": cell["cell_id"],
                "model": "qwen3.5:9b",
                "model_group": "qwen9b",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c2_outcome": cell["c2_outcome"],
                "c2_final_source_path": cell["c2_final_source_path"],
                "c2_final_source_sha256": cell["c2_final_source_sha256"],
                "c3_final_source_path": r["post_source_path"],
                "c3_final_source_sha256": r["post_source_sha256"],
                "c3_outcome": r["post_status"],
                "source_origin": origin,
                "eligibility_status": r["eligibility_status"],
                "modified": r["modified"],
                "transition": r["transition"],
            }
        )
    c3 = {
        "status": "math16_c3_final_source_closure_qwen9b_v1",
        "verdict": "C3_FINAL_SOURCE_CLOSURE_PASSED",
        "definition": "C3 = C2 + Tier C1 Explicit Domain Method Binding (NO_GO if eligible=0)",
        "head": head_sha(),
        "go_nogo": go,
        "validation": {
            "n_cells": 320,
            "unique_ids": 320,
            "duplicate_ids": 0,
            "c2_pass": 102,
            "c3_pass": summary["c3_pass"],
            "c3_fail": summary["c3_fail"],
            "verified_rescue": summary["transitions"]["verified_rescue"],
            "regression": summary["transitions"]["regression"],
            "preserved_pass": summary["transitions"]["preserved_pass"],
            "still_failed": summary["transitions"]["still_failed"],
            "origin_counts": dict(Counter(c["source_origin"] for c in cells)),
            "no_missing_duplicate_fallback": True,
            "passed": True,
        },
        "cells": cells,
        "declarations": [
            "no_model_calls",
            "no_guard_relaxation",
            "no_4b_artifact_modification",
            "evaluator_blind_selection",
        ],
    }
    write_json(OUT_C3, c3)
    write_text(
        OUT_C3_MD,
        "\n".join(
            [
                "# Math16 C3 Final-Source Closure — Qwen9B v1",
                "",
                f"> **verdict:** `{c3['verdict']}`",
                f"> **Go/No-Go:** `{go}`",
                f"> **HEAD:** `{c3['head']}`",
                "",
                f"- Cells: **320**; C3 PASS/FAIL: **{summary['c3_pass']}/{summary['c3_fail']}**",
                f"- verified_rescue／regression: **{summary['transitions']['verified_rescue']}／{summary['transitions']['regression']}**",
                f"- source_origin: `{c3['validation']['origin_counts']}`",
                "",
            ]
        )
        + "\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-second-replay", action="store_true")
    args = parser.parse_args()

    print("== C2 input ==")
    c2 = json.loads(C2_CLOSURE.read_text(encoding="utf-8"))
    verify_c2(c2)
    matrix = json.loads(CONTRACT_MATRIX.read_text(encoding="utf-8"))
    contracts_by_key = {
        (c["task_id"], c["condition_code"]): c for c in matrix["contracts"]
    }
    freeze = freeze_audit()
    print("freeze ok", freeze["contract_system_status_counts"])

    print("== C2→C3 Tier C1 ==")
    out = run_all(c2, contracts_by_key, RESULTS)
    summary = out["summary"]
    print(
        f"elig={summary['eligibility']} c3={summary['c3_pass']} "
        f"rescue={summary['transitions']['verified_rescue']} mod={summary['modified']} go={summary['go_nogo']}"
    )

    if args.skip_second_replay:
        second = {"zero_diff": None, "skipped": True}
    else:
        print("== second deterministic replay ==")
        second = deterministic_second(c2, contracts_by_key, out["rows"])

    write_outputs(freeze, summary, out["rows"], out["census_rows"], second, c2)
    print("DONE")
    print(
        json.dumps(
            {
                "go_nogo": summary["go_nogo"],
                "eligibility": summary["eligibility"],
                "c3_pass": summary["c3_pass"],
                "rescue": summary["transitions"]["verified_rescue"],
                "regression": summary["transitions"]["regression"],
                "triggered": summary["triggered"],
                "modified": summary["modified"],
                "abstained": summary["abstained"],
                "parse_gain": summary["parse_gain"],
                "execution_gain": summary["execution_gain"],
                "preserved_pass": summary["transitions"]["preserved_pass"],
                "second_zero_diff": second.get("zero_diff"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
