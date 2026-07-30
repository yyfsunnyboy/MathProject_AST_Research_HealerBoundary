# -*- coding: utf-8 -*-
"""Gemini 3.5 Flash C4→C5a Tier D D3→D1 FAIL-gated authoritative replay.

Namespace: gemini_fail_gated_authoritative_v1
Input: authoritative C4 final sources (PASS preserved; FAIL gated; counts from C4 closure).
Pipeline: fixed RULE_ORDER = (D3, D1). No D5/D2. No model calls.
"""
from __future__ import annotations

import ast
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    CURRENT_TIER,
    LAYER_ROLE,
    RULE_ID_D1,
    RULE_ID_D3,
    RULE_ORDER,
    d1,
    d3,
    run_tier_d_d3_d1_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.common import OPS_NAMES  # noqa: E402
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.preflight_math16_method2_all_cell import classify_transition  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

NS = "gemini_fail_gated_authoritative_v1"
AUTHORITY = "AUTHORITATIVE_FAIL_GATED_CUMULATIVE_V1"

C4_CLOSURE = ROOT / f"docs/experiments/manifests/math16_c4_final_source_closure_{NS}.json"
RESULTS = ROOT / f"docs/experiments/results/math16_c4_c5a_tier_d_d3_d1_reproducibility_{NS}"

OUT_SUPPLY = (
    ROOT / f"docs/experiments/manifests/math16_c4_c5a_tier_d_d3_d1_residual_supply_{NS}.json"
)
OUT_SUPPLY_MD = (
    ROOT / f"docs/experiments/reports/math16_c4_c5a_tier_d_d3_d1_residual_supply_{NS}.md"
)
OUT_REPLAY = (
    ROOT / f"docs/experiments/manifests/math16_c4_c5a_tier_d_d3_d1_reproducibility_{NS}.json"
)
OUT_REPLAY_MD = (
    ROOT / f"docs/experiments/reports/math16_c4_c5a_tier_d_d3_d1_reproducibility_{NS}.md"
)
OUT_C5A = ROOT / f"docs/experiments/manifests/math16_c5a_final_source_closure_{NS}.json"
OUT_C5A_MD = ROOT / f"docs/experiments/reports/math16_c5a_final_source_closure_{NS}.md"

FREEZE_FILES = [
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/__init__.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/pipeline.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/rule_d3_syntax_residue_quarantine.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/rule_d1_ops_shadow_removal.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/types.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/common.py",
    "docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md",
    "docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json",
]

EXPECTED_ORDER = (RULE_ID_D3, RULE_ID_D1)
FORMAL_ACTIVE_PHRASE = (
    "以 frozen scaffold 注入的正式 Ops implementation，"
    "取代模型自訂的 active shadow implementation。"
)


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


def verify_c4(c4: dict[str, Any]) -> tuple[int, int]:
    if c4.get("authority_status") != AUTHORITY:
        raise RuntimeError(f"C4_NOT_AUTHORITATIVE: {c4.get('authority_status')}")
    if c4.get("namespace") != NS:
        raise RuntimeError(f"C4_WRONG_NAMESPACE: {c4.get('namespace')}")
    v = c4["validation"]
    if not v.get("passed"):
        raise RuntimeError("C4_CLOSURE_NOT_PASSED")
    expected_pass = int(v.get("c4_pass"))
    expected_fail = int(v.get("c4_fail"))
    if v.get("n_cells") != 320 or expected_pass + expected_fail != 320:
        raise RuntimeError(f"C4_COUNTS_DRIFT: {v}")
    ids = [c["cell_id"] for c in c4["cells"]]
    if len(ids) != 320 or len(set(ids)) != 320:
        raise RuntimeError("C4_IDENTITY_FAILURE")
    pass_n = fail_n = prior_pass = 0
    for cell in c4["cells"]:
        path = ROOT / cell["c4_final_source_path"]
        if not path.exists():
            raise RuntimeError(f"MISSING_C4_SOURCE: {cell['cell_id']}")
        if sha256_path(path) != cell["c4_final_source_sha256"]:
            raise RuntimeError(f"C4_SHA_DRIFT: {cell['cell_id']}")
        if "NONAUTHORITATIVE" in cell["c4_final_source_path"] or "all_cell" in cell[
            "c4_final_source_path"
        ]:
            # exploratory all-cell paths must not be used
            if "fail_gated_authoritative" not in cell["c4_final_source_path"]:
                raise RuntimeError(f"NONAUTHORITATIVE_SOURCE: {cell['cell_id']}")
        if cell["c4_outcome"] == "PASSED":
            pass_n += 1
            if cell["source_origin"] != "PRIOR_PASS_PRESERVED":
                raise RuntimeError(f"PASS_ORIGIN_DRIFT: {cell['cell_id']}")
            prior_pass += 1
        elif cell["c4_outcome"] == "FAILED":
            fail_n += 1
        else:
            raise RuntimeError(f"BAD_C4_OUTCOME: {cell['cell_id']}")
    if pass_n != expected_pass or fail_n != expected_fail or prior_pass != expected_pass:
        raise RuntimeError(f"C4_PASS_FAIL_ORIGIN: {pass_n}/{fail_n}/{prior_pass}")
    return pass_n, fail_n


def freeze_audit() -> dict[str, Any]:
    if tuple(RULE_ORDER) != EXPECTED_ORDER:
        raise RuntimeError(f"RULE_ORDER_DRIFT: {RULE_ORDER}")
    files = {rel: {"sha256": sha256_path(ROOT / rel)} for rel in FREEZE_FILES}
    return {
        "current_tier": CURRENT_TIER,
        "layer_role": LAYER_ROLE,
        "rule_order": list(RULE_ORDER),
        "rule_order_matches_frozen": True,
        "d5_d2_executed": False,
        "files": files,
    }


def static_status_from_rule_result(step: Any) -> str:
    """Map apply_once audit to census ELIGIBLE / AMBIGUOUS_ABSTAIN / INELIGIBLE."""
    if step.applied:
        return "ELIGIBLE"
    if step.triggered and step.abstained:
        return "AMBIGUOUS_ABSTAIN"
    return "INELIGIBLE"


def classify_shadow_binding(source: str, shadow_name: str) -> dict[str, Any]:
    """AST evidence: is shadow actively bound by Ops calls on execution path?"""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {
            "shadow_binding_class": "MIXED_OR_UNRESOLVED",
            "reason": "source_not_parseable",
            "active_calls": [],
        }

    # Collect generate bodies (unique preferred)
    generates = [
        n
        for n in tree.body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "generate"
    ]
    bodies: list[ast.AST] = list(generates) if generates else list(tree.body)

    active_calls: list[dict[str, Any]] = []
    for body_root in bodies:
        for n in ast.walk(body_root):
            if not isinstance(n, ast.Call):
                continue
            f = n.func
            if (
                isinstance(f, ast.Attribute)
                and isinstance(f.value, ast.Name)
                and f.value.id == shadow_name
            ):
                active_calls.append(
                    {
                        "fqname": f"{shadow_name}.{f.attr}",
                        "lineno": getattr(n, "lineno", None),
                        "in_generate": any(
                            isinstance(g, (ast.FunctionDef, ast.AsyncFunctionDef))
                            and n in ast.walk(g)
                            for g in generates
                        )
                        if generates
                        else False,
                    }
                )

    if active_calls:
        return {
            "shadow_binding_class": "ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API",
            "reason": "ops_calls_lexically_bound_to_local_shadow",
            "active_calls": active_calls,
            "formal_phrase": FORMAL_ACTIVE_PHRASE,
        }
    # shadow present but unused on generate path
    shadows = d1._shadow_nodes(tree)  # noqa: SLF001 — census reuse of frozen collector
    if any(s["name"] == shadow_name for s in shadows):
        return {
            "shadow_binding_class": "DEAD_SHADOW_REMOVAL",
            "reason": "shadow_present_but_no_ops_call_on_execution_path",
            "active_calls": [],
        }
    return {
        "shadow_binding_class": "MIXED_OR_UNRESOLVED",
        "reason": "shadow_not_found_or_unresolved",
        "active_calls": [],
    }


def run_all(c4: dict[str, Any], *, c4_pass: int, c4_fail: int) -> dict[str, Any]:
    if RESULTS.exists():
        shutil.rmtree(RESULTS)
    pre_dir = RESULTS / "pre_sources"
    post_dir = RESULTS / "post_sources"
    mid_dir = RESULTS / "d3_post_sources"
    pre_dir.mkdir(parents=True)
    post_dir.mkdir(parents=True)
    mid_dir.mkdir(parents=True)

    tasks = tasks_by_id()
    _, api_policy_map = _load_family_and_api_policy()
    rows: list[dict[str, Any]] = []
    census_rows: list[dict[str, Any]] = []

    for index, cell in enumerate(c4["cells"], start=1):
        cid = cell["cell_id"]
        pre_path = ROOT / cell["c4_final_source_path"]
        pre_source = pre_path.read_text(encoding="utf-8")
        gated = cell["c4_outcome"] == "FAILED"

        d3_static = {"status": "PRIOR_PASS_NOT_SCANNED", "abstention_reason": "prior_pass_preserved_no_scan"}
        d1_static = {"status": "PRIOR_PASS_NOT_SCANNED", "abstention_reason": "prior_pass_preserved_no_scan"}
        d3_pipe = {"triggered": False, "modified": False, "abstained": True, "applied": False}
        d1_pipe = {"triggered": False, "modified": False, "abstained": True, "applied": False}
        shadow_class = None
        shadow_evidence: dict[str, Any] = {}
        pipeline_audit = None
        selected_rule = ""
        rules_fired: list[str] = []
        mid_source = pre_source
        post_source = pre_source

        if not gated:
            origin = "PRIOR_PASS_PRESERVED"
            pre_score = {
                "status": "PASSED",
                "classifier_outcome": "inherited_prior_pass",
                "primary_failure_layer": None,
                "failure_subtype": None,
            }
            post_score = dict(pre_score)
            eligible_any = False
            triggered = False
            modified = False
            abstained = True
        else:
            # Static census on C4 source (answer-blind)
            d3_step = d3.apply_once(pre_source)
            d1_step = d1.apply_once(pre_source)
            d3_static = {
                "status": static_status_from_rule_result(d3_step),
                "abstention_reason": d3_step.abstention_reason or (
                    "eligible" if d3_step.applied else None
                ),
                "triggered_flag": bool(d3_step.triggered),
                "applied_flag": bool(d3_step.applied),
            }
            d1_static = {
                "status": static_status_from_rule_result(d1_step),
                "abstention_reason": d1_step.abstention_reason or (
                    "eligible" if d1_step.applied else None
                ),
                "triggered_flag": bool(d1_step.triggered),
                "applied_flag": bool(d1_step.applied),
                "extras": d1_step.extras,
            }

            # Fixed pipeline D3→D1; D1 sees D3 post-source
            pipe = run_tier_d_d3_d1_pipeline(pre_source)
            pipeline_audit = pipe.to_audit_dict() if hasattr(pipe, "to_audit_dict") else None
            post_source = pipe.post_source if not pipe.rolled_back else pre_source
            rules_fired = list(pipe.rules_fired or [])
            selected_rule = pipe.selected_rule or ""

            # Reconstruct mid (D3-only) for lineage / shadow class on D1 input
            d3_only = d3.apply_once(pre_source)
            mid_source = d3_only.source_out if d3_only.applied else pre_source

            # Per-rule pipeline-realized from logs
            logs = pipe.rule_logs or []
            d3_log = next((x for x in logs if x.get("rule_id") == RULE_ID_D3), {})
            d1_log = next((x for x in logs if x.get("rule_id") == RULE_ID_D1), {})
            d3_pipe = {
                "triggered": bool(d3_log.get("triggered") or d3_log.get("applied")),
                "modified": bool(d3_log.get("applied")),
                "abstained": bool(d3_log.get("abstained")) and not bool(d3_log.get("applied")),
                "applied": bool(d3_log.get("applied")),
                "abstention_reason": d3_log.get("abstention_reason"),
            }
            d1_pipe = {
                "triggered": bool(d1_log.get("triggered") or d1_log.get("applied")),
                "modified": bool(d1_log.get("applied")),
                "abstained": bool(d1_log.get("abstained")) and not bool(d1_log.get("applied")),
                "applied": bool(d1_log.get("applied")),
                "abstention_reason": d1_log.get("abstention_reason"),
                "ast_node_location": d1_log.get("ast_node_location"),
            }

            if d1_pipe["modified"]:
                loc = d1_pipe.get("ast_node_location") or {}
                sname = loc.get("name") or (d1_log.get("extras") or {}).get("shadow_names", [None])[0]
                # Classify on D1 input source (after D3)
                if sname:
                    shadow_evidence = classify_shadow_binding(mid_source, sname)
                    shadow_class = shadow_evidence["shadow_binding_class"]

            modified = post_source != pre_source
            triggered = bool(rules_fired) or d3_pipe["triggered"] or d1_pipe["triggered"]
            abstained = not modified
            eligible_any = d3_static["status"] == "ELIGIBLE" or d1_static["status"] == "ELIGIBLE"
            if modified:
                origin = "TIER_D_D3_D1_POST_SOURCE"
            else:
                origin = "PRIOR_FAIL_UNCHANGED"

            task = tasks[cell["task_id"]]
            frozen_params = frozen_for_prompt(task)["oracle_payload"]
            api_policy = api_policy_map[cell["task_id"]]
            pre_score = score_source(
                pre_source, task=task, frozen_params=frozen_params, api_policy=api_policy
            )
            post_score = score_source(
                post_source, task=task, frozen_params=frozen_params, api_policy=api_policy
            )
            if pre_score["status"] != "FAILED":
                raise RuntimeError(f"GATED_PRE_NOT_FAIL: {cid}")

        if not gated:
            assert post_source == pre_source
            assert sha256_text(post_source) == sha256_text(pre_source)

        (pre_dir / f"{cid}.py").write_bytes(pre_source.encode("utf-8"))
        (post_dir / f"{cid}.py").write_bytes(post_source.encode("utf-8"))
        (mid_dir / f"{cid}.py").write_bytes(mid_source.encode("utf-8"))

        transition = classify_transition(pre_score["status"], post_score["status"])
        pre_parse = parses(pre_source)
        post_parse = parses(post_source)
        pre_exec = is_executable_obs(pre_score) if gated else True
        post_exec = is_executable_obs(post_score) if gated else True
        parse_gain = (not pre_parse) and post_parse
        execution_gain = (not pre_exec) and post_exec
        blocker_removal = (
            modified
            and transition != "verified_rescue"
            and (parse_gain or execution_gain)
        )
        overlap_static = (
            gated
            and d3_static["status"] == "ELIGIBLE"
            and d1_static["status"] == "ELIGIBLE"
        )

        census_rows.append(
            {
                "cell_id": cid,
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "gated_into_healer": gated,
                "c4_final_source_path": cell["c4_final_source_path"],
                "c4_final_source_sha256": cell["c4_final_source_sha256"],
                "d3_static_status": d3_static["status"],
                "d3_static_reason": d3_static.get("abstention_reason"),
                "d1_static_status": d1_static["status"],
                "d1_static_reason": d1_static.get("abstention_reason"),
                "overlap_static_d3_d1": overlap_static,
                "pass_fail_used_for_eligibility": False,
            }
        )

        rows.append(
            {
                "cell_id": cid,
                "model": "gemini-3.5-flash",
                "model_group": "gemini",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c4_outcome": cell["c4_outcome"],
                "c4_final_source_path": cell["c4_final_source_path"],
                "c4_final_source_sha256": cell["c4_final_source_sha256"],
                "pre_source_path": str((pre_dir / f"{cid}.py").relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "d3_post_source_path": str((mid_dir / f"{cid}.py").relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "post_source_path": str((post_dir / f"{cid}.py").relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "pre_source_sha256": sha256_text(pre_source),
                "d3_post_source_sha256": sha256_text(mid_source),
                "post_source_sha256": sha256_text(post_source),
                "gated_into_healer": gated,
                "d3_static_status": d3_static["status"],
                "d1_static_status": d1_static["status"],
                "d3_static_reason": d3_static.get("abstention_reason"),
                "d1_static_reason": d1_static.get("abstention_reason"),
                "overlap_static_d3_d1": overlap_static,
                "d3_pipeline": d3_pipe,
                "d1_pipeline": d1_pipe,
                "rules_fired": rules_fired,
                "selected_rule": selected_rule,
                "rule_order": list(RULE_ORDER),
                "eligible_any": eligible_any,
                "triggered": triggered,
                "modified": modified,
                "abstained": abstained,
                "shadow_binding_class": shadow_class,
                "shadow_binding_evidence": shadow_evidence,
                "pre_status": pre_score["status"],
                "post_status": post_score["status"],
                "c5a_outcome": post_score["status"],
                "transition": transition,
                "parse_gain": parse_gain,
                "execution_gain": execution_gain,
                "blocker_removal_only": blocker_removal,
                "source_origin": origin,
                "pipeline_audit": pipeline_audit,
                "evaluator_used_for_selection": False,
                "model_calls": 0,
                "d5_d2_executed": False,
            }
        )
        if index % 40 == 0:
            print(f"[c4_c5a {index}/320]")

    write_jsonl(RESULTS / "census_journal.jsonl", census_rows)
    write_jsonl(RESULTS / "transition_journal.jsonl", rows)

    # Second deterministic replay
    mismatches = []
    for cell, first in zip(c4["cells"], rows):
        cid = cell["cell_id"]
        pre = (ROOT / cell["c4_final_source_path"]).read_text(encoding="utf-8")
        if cell["c4_outcome"] == "PASSED":
            post = pre
        else:
            pipe = run_tier_d_d3_d1_pipeline(pre)
            post = pipe.post_source if not pipe.rolled_back else pre
        if sha256_text(post) != first["post_source_sha256"]:
            mismatches.append({"cell_id": cid, "field": "post_source_sha256"})
        if cell["c4_outcome"] == "PASSED" and first["post_source_sha256"] != first[
            "pre_source_sha256"
        ]:
            mismatches.append({"cell_id": cid, "field": "pass_sha_changed"})
    second = {
        "second_replay_mismatches": len(mismatches),
        "zero_diff": len(mismatches) == 0,
        "sample": mismatches[:20],
    }
    write_json(RESULTS / "deterministic_second_replay.json", second)
    if mismatches:
        raise RuntimeError(f"SECOND_REPLAY_DIFF: {len(mismatches)}")

    gated_rows = [r for r in rows if r["gated_into_healer"]]
    pass_rows = [r for r in rows if not r["gated_into_healer"]]
    if len(gated_rows) != c4_fail or len(pass_rows) != c4_pass:
        raise RuntimeError(f"GATE_COUNTS: {len(gated_rows)}/{len(pass_rows)}")
    for r in pass_rows:
        if r["pre_source_sha256"] != r["post_source_sha256"]:
            raise RuntimeError(f"PASS_SHA_CHANGED: {r['cell_id']}")
        if r["source_origin"] != "PRIOR_PASS_PRESERVED":
            raise RuntimeError(f"PASS_ORIGIN: {r['cell_id']}")
        if r["modified"]:
            raise RuntimeError(f"PASS_MODIFIED: {r['cell_id']}")

    pass_pass_mod = sum(
        1
        for r in rows
        if r["modified"] and r["pre_status"] == "PASSED" and r["post_status"] == "PASSED"
    )
    if pass_pass_mod != 0:
        raise RuntimeError(f"PASS_PASS_MOD: {pass_pass_mod}")

    def rule_static_counts(key: str) -> dict[str, int]:
        c = Counter(r[key] for r in gated_rows)
        return {
            "ELIGIBLE": c.get("ELIGIBLE", 0),
            "AMBIGUOUS_ABSTAIN": c.get("AMBIGUOUS_ABSTAIN", 0),
            "INELIGIBLE": c.get("INELIGIBLE", 0),
        }

    d3_static_counts = rule_static_counts("d3_static_status")
    d1_static_counts = rule_static_counts("d1_static_status")
    d3_trig = sum(1 for r in gated_rows if r["d3_pipeline"]["triggered"])
    d3_mod = sum(1 for r in gated_rows if r["d3_pipeline"]["modified"])
    d3_abs = sum(1 for r in gated_rows if r["d3_pipeline"]["abstained"])
    d1_trig = sum(1 for r in gated_rows if r["d1_pipeline"]["triggered"])
    d1_mod = sum(1 for r in gated_rows if r["d1_pipeline"]["modified"])
    d1_abs = sum(1 for r in gated_rows if r["d1_pipeline"]["abstained"])
    overlap_n = sum(1 for r in gated_rows if r["overlap_static_d3_d1"])
    overlap_ids = [r["cell_id"] for r in gated_rows if r["overlap_static_d3_d1"]]

    transitions = Counter(r["transition"] for r in rows)
    c5a_pass = sum(r["post_status"] == "PASSED" for r in rows)
    shadow_counts = Counter(
        r["shadow_binding_class"] for r in rows if r.get("shadow_binding_class")
    )
    rescue_shadow = [
        {
            "cell_id": r["cell_id"],
            "shadow_binding_class": r["shadow_binding_class"],
            "evidence": r.get("shadow_binding_evidence"),
            "rules_fired": r["rules_fired"],
        }
        for r in rows
        if r["transition"] == "verified_rescue"
    ]

    summary = {
        "phase": "Gemini 3.5 Flash C4→C5a Tier D D3→D1 fail-gated authoritative",
        "status": "COMPLETE",
        "authority_status": AUTHORITY,
        "namespace": NS,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "rule_order": list(RULE_ORDER),
        "cells": 320,
        "gated_fail_count": c4_fail,
        "preserved_pass_count": c4_pass,
        "pass_pass_modified": pass_pass_mod,
        "d3": {
            "static": d3_static_counts,
            "pipeline_realized_triggered": d3_trig,
            "modified": d3_mod,
            "abstained": d3_abs,
        },
        "d1": {
            "static": d1_static_counts,
            "pipeline_realized_triggered": d1_trig,
            "modified": d1_mod,
            "abstained": d1_abs,
        },
        "overlap_static_d3_d1": overlap_n,
        "overlap_ids": overlap_ids,
        "fixed_sequence": "D3_THEN_D1",
        "triggered": sum(r["triggered"] for r in rows),
        "modified": sum(r["modified"] for r in rows),
        "abstained": sum(r["abstained"] for r in rows),
        "c4_pass_observed": c4_pass,
        "c5a_pass": c5a_pass,
        "c5a_fail": 320 - c5a_pass,
        "transitions": {
            "verified_rescue": transitions.get("verified_rescue", 0),
            "regression": transitions.get("regression", 0),
            "preserved_pass": transitions.get("preserved_pass", 0),
            "still_failed": transitions.get("still_failed", 0),
        },
        "modified_still_failed": sum(
            1 for r in rows if r["modified"] and r["transition"] == "still_failed"
        ),
        "blocker_removal_only": sum(1 for r in rows if r["blocker_removal_only"]),
        "parse_gain": sum(r["parse_gain"] for r in rows),
        "execution_gain": sum(r["execution_gain"] for r in rows),
        "shadow_binding_class_counts": dict(shadow_counts),
        "verified_rescue_ids": [
            r["cell_id"] for r in rows if r["transition"] == "verified_rescue"
        ],
        "rescue_shadow_binding": rescue_shadow,
        "regression_ids": [r["cell_id"] for r in rows if r["transition"] == "regression"],
        "d5_d2_executed": False,
        "model_calls": 0,
        "deterministic_second_replay": second,
    }
    write_json(RESULTS / "summary.json", summary)
    return {
        "summary": summary,
        "rows": rows,
        "census_rows": census_rows,
        "second": second,
        "freeze": freeze_audit(),
    }


def write_outputs(c4: dict[str, Any], out: dict[str, Any]) -> None:
    summary = out["summary"]
    c4_pass = summary["preserved_pass_count"]
    c4_fail = summary["gated_fail_count"]
    supply = {
        "status": f"math16_c4_c5a_tier_d_d3_d1_residual_supply_{NS}",
        "verdict": "TIER_D_D3_D1_FAIL_GATED_CENSUS_COMPLETE",
        "authority_status": AUTHORITY,
        "namespace": NS,
        "head": head_sha(),
        "input": {
            "c4_closure": str(C4_CLOSURE.relative_to(ROOT)).replace("\\", "/"),
            "pool": f"C4_FAIL_{c4_fail}",
            "preserved_pass": c4_pass,
            "gating": "FAIL_ONLY",
        },
        "rule_order": list(RULE_ORDER),
        "aggregate": {
            "gated_fail": c4_fail,
            "preserved_pass": c4_pass,
            "d3_static": summary["d3"]["static"],
            "d1_static": summary["d1"]["static"],
            "d3_pipeline_realized_triggered": summary["d3"]["pipeline_realized_triggered"],
            "d3_modified": summary["d3"]["modified"],
            "d3_abstained": summary["d3"]["abstained"],
            "d1_pipeline_realized_triggered": summary["d1"]["pipeline_realized_triggered"],
            "d1_modified": summary["d1"]["modified"],
            "d1_abstained": summary["d1"]["abstained"],
            "overlap_static": summary["overlap_static_d3_d1"],
            "overlap_ids": summary["overlap_ids"],
            "fixed_sequence": "D3_THEN_D1",
        },
        "cells": out["census_rows"],
        "rule_freeze_audit": out["freeze"],
        "declarations": [
            "fail_only_gate",
            "prior_pass_not_scanned",
            "no_d5_d2",
            "no_model_calls",
            "evaluator_blind_selection",
        ],
    }
    write_json(OUT_SUPPLY, supply)
    write_text(
        OUT_SUPPLY_MD,
        "\n".join(
            [
                f"# Math16 C4→C5a Tier D D3→D1 Residual Supply — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **Pool:** C4 FAIL-only **{c4_fail}** (PASS {c4_pass} preserved)",
                f"> **Order:** `{list(RULE_ORDER)}`",
                "",
                f"## D3 static (among gated {c4_fail})",
                "",
                f"- ELIGIBLE／AMBIGUOUS／INELIGIBLE: **{summary['d3']['static']['ELIGIBLE']}／{summary['d3']['static']['AMBIGUOUS_ABSTAIN']}／{summary['d3']['static']['INELIGIBLE']}**",
                f"- pipeline triggered／modified／abstained: **{summary['d3']['pipeline_realized_triggered']}／{summary['d3']['modified']}／{summary['d3']['abstained']}**",
                "",
                f"## D1 static (among gated {c4_fail})",
                "",
                f"- ELIGIBLE／AMBIGUOUS／INELIGIBLE: **{summary['d1']['static']['ELIGIBLE']}／{summary['d1']['static']['AMBIGUOUS_ABSTAIN']}／{summary['d1']['static']['INELIGIBLE']}**",
                f"- pipeline triggered／modified／abstained: **{summary['d1']['pipeline_realized_triggered']}／{summary['d1']['modified']}／{summary['d1']['abstained']}**",
                "",
                f"- Static overlap D3∧D1: **{summary['overlap_static_d3_d1']}**",
                f"- Fixed sequence: **D3→D1**",
                "",
            ]
        )
        + "\n",
    )

    replay = {
        "status": f"math16_c4_c5a_tier_d_d3_d1_reproducibility_{NS}",
        "verdict": "C4_C5A_TIER_D_D3_D1_GEMINI_FAIL_GATED_COMPLETE",
        "authority_status": AUTHORITY,
        "namespace": NS,
        "head": head_sha(),
        "results_root": str(RESULTS.relative_to(ROOT)).replace("\\", "/"),
        "rule_order": list(RULE_ORDER),
        "summary": summary,
        "deterministic_second_replay": out["second"],
        "rule_freeze_audit": out["freeze"],
        "formal_active_shadow_phrase": FORMAL_ACTIVE_PHRASE,
        "model_calls": 0,
        "d5_d2_executed": False,
    }
    write_json(OUT_REPLAY, replay)
    write_text(
        OUT_REPLAY_MD,
        "\n".join(
            [
                f"# Math16 C4→C5a Tier D D3→D1 Reproducibility — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{head_sha()}`",
                f"> **Order:** D3→D1 (fixed)",
                "",
                "## Core counts",
                "",
                f"- gated FAIL／preserved PASS: **{c4_fail}／{c4_pass}**",
                f"- C4 PASS／C5a PASS: **{c4_pass}／{summary['c5a_pass']}**",
                f"- verified_rescue／regression: **{summary['transitions']['verified_rescue']}／{summary['transitions']['regression']}**",
                f"- parse_gain／execution_gain／blocker_removal／modified_still_failed: **{summary['parse_gain']}／{summary['execution_gain']}／{summary['blocker_removal_only']}／{summary['modified_still_failed']}**",
                f"- PASS→PASS modification: **{summary['pass_pass_modified']}**",
                f"- D1 shadow classes: `{summary['shadow_binding_class_counts']}`",
                f"- Second replay zero-diff: **{out['second']['zero_diff']}**",
                "",
                "## Active shadow formal phrase",
                "",
                f"> {FORMAL_ACTIVE_PHRASE}",
                "",
                "## Declarations",
                "",
                "- D5／D2 executed: **No**",
                "- Model calls: **0**",
                "- Commit／push: **No**",
                "",
            ]
        )
        + "\n",
    )

    cells = []
    for cell, r in zip(c4["cells"], out["rows"]):
        cells.append(
            {
                "cell_id": cell["cell_id"],
                "model": "gemini-3.5-flash",
                "model_group": "gemini",
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "c4_outcome": cell["c4_outcome"],
                "c4_final_source_path": cell["c4_final_source_path"],
                "c4_final_source_sha256": cell["c4_final_source_sha256"],
                "c5a_final_source_path": r["post_source_path"],
                "c5a_final_source_sha256": r["post_source_sha256"],
                "c5a_outcome": r["post_status"],
                "source_origin": r["source_origin"],
                "gated_into_healer": r["gated_into_healer"],
                "modified": r["modified"],
                "transition": r["transition"],
                "rules_fired": r["rules_fired"],
                "shadow_binding_class": r.get("shadow_binding_class"),
            }
        )
    c5a = {
        "status": f"math16_c5a_final_source_closure_{NS}",
        "verdict": "C5A_FINAL_SOURCE_CLOSURE_PASSED",
        "definition": "C5a = C4 + Tier D D3→D1 (FAIL-only gate; no D5/D2)",
        "authority_status": AUTHORITY,
        "namespace": NS,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "head": head_sha(),
        "validation": {
            "n_cells": 320,
            "unique_ids": 320,
            "duplicate_ids": 0,
            "c4_pass": c4_pass,
            "c5a_pass": summary["c5a_pass"],
            "c5a_fail": summary["c5a_fail"],
            "gated_fail_count": c4_fail,
            "preserved_pass_count": c4_pass,
            "pass_pass_modified": 0,
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
            "authoritative_fail_gated",
            "no_model_calls",
            "prior_pass_not_scanned",
            "fixed_order_d3_then_d1",
            "no_d5_d2",
        ],
    }
    write_json(OUT_C5A, c5a)
    write_text(
        OUT_C5A_MD,
        "\n".join(
            [
                f"# Math16 C5a Final-Source Closure — {NS}",
                "",
                f"> **verdict:** `{c5a['verdict']}`",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{c5a['head']}`",
                "",
                f"- Cells: **320**; C5a PASS/FAIL: **{summary['c5a_pass']}/{summary['c5a_fail']}**",
                f"- verified_rescue／regression: **{summary['transitions']['verified_rescue']}／{summary['transitions']['regression']}**",
                f"- origins: `{c5a['validation']['origin_counts']}`",
                "",
            ]
        )
        + "\n",
    )


def main() -> int:
    print("== C4 input ==")
    c4 = json.loads(C4_CLOSURE.read_text(encoding="utf-8"))
    c4_pass, c4_fail = verify_c4(c4)
    print(f"C4 ok {c4_pass}/{c4_fail}")
    freeze = freeze_audit()
    print("freeze ok", freeze["rule_order"])

    print("== C4→C5a Tier D D3→D1 ==")
    out = run_all(c4, c4_pass=c4_pass, c4_fail=c4_fail)
    summary = out["summary"]
    print(
        json.dumps(
            {
                "c5a_pass": summary["c5a_pass"],
                "rescue": summary["transitions"]["verified_rescue"],
                "regression": summary["transitions"]["regression"],
                "d3_static_eligible": summary["d3"]["static"]["ELIGIBLE"],
                "d3_trig_mod": [
                    summary["d3"]["pipeline_realized_triggered"],
                    summary["d3"]["modified"],
                ],
                "d1_static_eligible": summary["d1"]["static"]["ELIGIBLE"],
                "d1_trig_mod": [
                    summary["d1"]["pipeline_realized_triggered"],
                    summary["d1"]["modified"],
                ],
                "overlap": summary["overlap_static_d3_d1"],
                "pass_pass": summary["pass_pass_modified"],
                "shadow": summary["shadow_binding_class_counts"],
                "second_zero_diff": summary["deterministic_second_replay"]["zero_diff"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    write_outputs(c4, out)
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
