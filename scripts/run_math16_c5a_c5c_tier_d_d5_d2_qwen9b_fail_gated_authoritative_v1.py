# -*- coding: utf-8 -*-
"""9B C5a→C5b (D5) then C5b→C5c (D2) FAIL-gated authoritative.

Namespace: qwen9b_fail_gated_authoritative_v1
- D5: TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1 (score≥8, margin≥2)
- D2: TIER_D_DUPLICATE_DEFINITION_SELECTION_V1
Separate census/replay/closure per layer. No model calls. No D3/D1 re-run.
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
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    CURRENT_TIER,
    LAYER_ROLE,
    RULE_ID_D2,
    RULE_ID_D5,
    d2,
    d5,
    run_tier_d_d2_pipeline,
    run_tier_d_d5_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.ranking import (  # noqa: E402
    MIN_MARGIN,
    MIN_SCORE,
)
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.preflight_math16_method2_all_cell import classify_transition  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

NS = "qwen9b_fail_gated_authoritative_v1"
AUTHORITY = "AUTHORITATIVE_FAIL_GATED_CUMULATIVE_V1"

C5A_CLOSURE = ROOT / f"docs/experiments/manifests/math16_c5a_final_source_closure_{NS}.json"

FREEZE_D5 = [
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/rule_d5_ranked_domain_method_binding.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/ranking.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/pipeline.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/types.py",
    "docs/experiments/manifests/math16_ab2d_task_contract_matrix_v1.json",
    "docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md",
]
FREEZE_D2 = [
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/rule_d2_duplicate_definition_selection.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/ranking.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/pipeline.py",
    "agent_tools/finals_rebuild/aggressive_healer_tier_d/types.py",
    "docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md",
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


def static_status(step: Any) -> str:
    if step.applied:
        return "ELIGIBLE"
    if step.triggered and step.abstained:
        return "AMBIGUOUS_ABSTAIN"
    return "INELIGIBLE"


def verify_prior_closure(
    closure: dict[str, Any],
    *,
    outcome_key: str,
    path_key: str,
    sha_key: str,
    expected_pass: int,
    expected_fail: int,
    label: str,
) -> None:
    if closure.get("authority_status") != AUTHORITY:
        raise RuntimeError(f"{label}_NOT_AUTHORITATIVE: {closure.get('authority_status')}")
    if closure.get("namespace") != NS:
        raise RuntimeError(f"{label}_WRONG_NS: {closure.get('namespace')}")
    v = closure["validation"]
    if not v.get("passed"):
        raise RuntimeError(f"{label}_NOT_PASSED")
    if v.get("n_cells") != 320:
        raise RuntimeError(f"{label}_N_CELLS")
    ids = [c["cell_id"] for c in closure["cells"]]
    if len(ids) != 320 or len(set(ids)) != 320:
        raise RuntimeError(f"{label}_IDENTITY")
    pass_n = fail_n = prior_pass = 0
    for cell in closure["cells"]:
        path = ROOT / cell[path_key]
        if not path.exists():
            raise RuntimeError(f"{label}_MISSING: {cell['cell_id']}")
        if sha256_path(path) != cell[sha_key]:
            raise RuntimeError(f"{label}_SHA: {cell['cell_id']}")
        if "fail_gated_authoritative" not in cell[path_key]:
            raise RuntimeError(f"{label}_NONAUTH_PATH: {cell['cell_id']}")
        if cell[outcome_key] == "PASSED":
            pass_n += 1
            if cell.get("source_origin") == "PRIOR_PASS_PRESERVED" or cell[outcome_key] == "PASSED":
                # C5a PASS may be PRIOR_PASS_PRESERVED or could theoretically be rescued;
                # for C5a all PASS are preserved from C4 (rescue=0). Accept PRIOR_PASS_PRESERVED
                # or any PASS that we will preserve going forward.
                if cell.get("source_origin") == "PRIOR_PASS_PRESERVED":
                    prior_pass += 1
        elif cell[outcome_key] == "FAILED":
            fail_n += 1
        else:
            raise RuntimeError(f"{label}_BAD_OUTCOME: {cell['cell_id']}")
    if pass_n != expected_pass or fail_n != expected_fail:
        raise RuntimeError(f"{label}_COUNTS: {pass_n}/{fail_n}")


def freeze_audit(files: list[str], rule_id: str) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "current_tier": CURRENT_TIER,
        "layer_role": LAYER_ROLE,
        "min_score": MIN_SCORE,
        "min_margin": MIN_MARGIN,
        "files": {rel: {"sha256": sha256_path(ROOT / rel)} for rel in files},
        "note": "Frozen Tier D Development slice; thresholds not altered.",
    }


def run_single_rule_layer(
    *,
    layer_tag: str,
    rule_id: str,
    prior_closure: dict[str, Any],
    prior_outcome_key: str,
    prior_path_key: str,
    prior_sha_key: str,
    next_outcome_key: str,
    next_path_key: str,
    next_sha_key: str,
    expected_prior_pass: int,
    expected_prior_fail: int,
    apply_static: Callable[..., Any],
    run_pipeline: Callable[..., Any],
    freeze_files: list[str],
    results_dirname: str,
    origin_if_modified: str,
) -> dict[str, Any]:
    results_root = ROOT / "docs/experiments/results" / results_dirname
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

    prior_pass = sum(1 for c in prior_closure["cells"] if c[prior_outcome_key] == "PASSED")
    prior_fail = sum(1 for c in prior_closure["cells"] if c[prior_outcome_key] == "FAILED")
    if prior_pass != expected_prior_pass or prior_fail != expected_prior_fail:
        raise RuntimeError(f"{layer_tag}_PRIOR:{prior_pass}/{prior_fail}")

    for index, cell in enumerate(prior_closure["cells"], start=1):
        cid = cell["cell_id"]
        pre_path = ROOT / cell[prior_path_key]
        pre_source = pre_path.read_text(encoding="utf-8")
        if sha256_path(pre_path) != cell[prior_sha_key]:
            raise RuntimeError(f"PRE_SHA:{cid}")
        gated = cell[prior_outcome_key] == "FAILED"

        if not gated:
            post_source = pre_source
            elig_status = "PRIOR_PASS_NOT_SCANNED"
            abstention_reason = "prior_pass_preserved_no_scan"
            triggered = False
            modified = False
            abstained = True
            eligible = False
            origin = "PRIOR_PASS_PRESERVED"
            rule_audit = None
            pipeline_audit = None
            pre_score = {
                "status": "PASSED",
                "classifier_outcome": "inherited_prior_pass",
                "primary_failure_layer": None,
                "failure_subtype": None,
            }
            post_score = dict(pre_score)
        else:
            step = apply_static(cell=cell, source=pre_source)
            elig_status = static_status(step)
            abstention_reason = step.abstention_reason or (
                "eligible" if step.applied else None
            )
            eligible = elig_status == "ELIGIBLE"
            pipe = run_pipeline(cell=cell, source=pre_source)
            pipeline_audit = pipe.to_audit_dict() if hasattr(pipe, "to_audit_dict") else None
            if pipe.rolled_back:
                post_source = pre_source
                triggered = bool(pipe.rules_fired) or any(
                    log.get("triggered") for log in (pipe.rule_logs or [])
                )
                modified = False
                abstained = True
            else:
                post_source = pipe.post_source
                modified = post_source != pre_source
                logs = pipe.rule_logs or []
                log0 = logs[0] if logs else {}
                triggered = bool(log0.get("triggered") or log0.get("applied") or pipe.rules_fired)
                abstained = not modified
            rule_audit = step.to_audit_dict() if hasattr(step, "to_audit_dict") else None
            origin = origin_if_modified if modified else "PRIOR_FAIL_UNCHANGED"

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
                raise RuntimeError(f"GATED_PRE_NOT_FAIL:{cid}")

        if not gated and (
            post_source != pre_source or sha256_text(post_source) != sha256_text(pre_source)
        ):
            raise RuntimeError(f"PASS_MUTATED:{cid}")

        (pre_dir / f"{cid}.py").write_bytes(pre_source.encode("utf-8"))
        (post_dir / f"{cid}.py").write_bytes(post_source.encode("utf-8"))

        transition = classify_transition(pre_score["status"], post_score["status"])
        pre_parse = parses(pre_source)
        post_parse = parses(post_source)
        pre_exec = is_executable_obs(pre_score) if gated else True
        post_exec = is_executable_obs(post_score) if gated else True
        parse_gain = (not pre_parse) and post_parse
        execution_gain = (not pre_exec) and post_exec
        blocker_removal = (
            modified and transition != "verified_rescue" and (parse_gain or execution_gain)
        )

        census_rows.append(
            {
                "cell_id": cid,
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "seed": cell["seed"],
                "gated_into_healer": gated,
                "status": elig_status,
                "abstention_reason": abstention_reason,
                "eligible": eligible,
                "rule_id": rule_id,
                "pass_fail_used_for_eligibility": False,
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
                prior_outcome_key: cell[prior_outcome_key],
                prior_path_key: cell[prior_path_key],
                prior_sha_key: cell[prior_sha_key],
                "pre_source_path": str((pre_dir / f"{cid}.py").relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "post_source_path": str((post_dir / f"{cid}.py").relative_to(ROOT)).replace(
                    "\\", "/"
                ),
                "pre_source_sha256": sha256_text(pre_source),
                "post_source_sha256": sha256_text(post_source),
                "gated_into_healer": gated,
                "eligibility_status": elig_status,
                "abstention_reason": abstention_reason,
                "eligible": eligible,
                "triggered": triggered,
                "modified": modified,
                "abstained": abstained,
                "rule_id": rule_id,
                "rule_audit": rule_audit,
                "pipeline_audit": pipeline_audit,
                "pre_status": pre_score["status"],
                "post_status": post_score["status"],
                next_outcome_key: post_score["status"],
                "transition": transition,
                "parse_gain": parse_gain,
                "execution_gain": execution_gain,
                "blocker_removal_only": blocker_removal,
                "source_origin": origin,
                "evaluator_used_for_selection": False,
                "model_calls": 0,
            }
        )
        if index % 40 == 0:
            print(f"[{layer_tag} {index}/320]")

    write_jsonl(results_root / "census_journal.jsonl", census_rows)
    write_jsonl(results_root / "transition_journal.jsonl", rows)

    # second replay
    mismatches = []
    for cell, first in zip(prior_closure["cells"], rows):
        pre = (ROOT / cell[prior_path_key]).read_text(encoding="utf-8")
        if cell[prior_outcome_key] == "PASSED":
            post = pre
        else:
            pipe = run_pipeline(cell=cell, source=pre)
            post = pre if pipe.rolled_back else pipe.post_source
        if sha256_text(post) != first["post_source_sha256"]:
            mismatches.append({"cell_id": cell["cell_id"], "field": "post_source_sha256"})
        if cell[prior_outcome_key] == "PASSED" and first["pre_source_sha256"] != first[
            "post_source_sha256"
        ]:
            mismatches.append({"cell_id": cell["cell_id"], "field": "pass_sha"})
    second = {
        "second_replay_mismatches": len(mismatches),
        "zero_diff": len(mismatches) == 0,
        "sample": mismatches[:20],
    }
    write_json(results_root / "deterministic_second_replay.json", second)
    if mismatches:
        raise RuntimeError(f"{layer_tag}_SECOND_DIFF:{len(mismatches)}")

    gated_rows = [r for r in rows if r["gated_into_healer"]]
    pass_rows = [r for r in rows if not r["gated_into_healer"]]
    if len(gated_rows) != expected_prior_fail or len(pass_rows) != expected_prior_pass:
        raise RuntimeError(f"{layer_tag}_GATE:{len(gated_rows)}/{len(pass_rows)}")
    for r in pass_rows:
        if r["pre_source_sha256"] != r["post_source_sha256"]:
            raise RuntimeError(f"PASS_SHA:{r['cell_id']}")
        if r["source_origin"] != "PRIOR_PASS_PRESERVED" or r["modified"]:
            raise RuntimeError(f"PASS_ORIGIN:{r['cell_id']}")

    pass_pass_mod = sum(
        1
        for r in rows
        if r["modified"] and r["pre_status"] == "PASSED" and r["post_status"] == "PASSED"
    )
    if pass_pass_mod != 0:
        raise RuntimeError(f"PASS_PASS:{pass_pass_mod}")

    status_counts = Counter(r["eligibility_status"] for r in gated_rows)
    transitions = Counter(r["transition"] for r in rows)
    next_pass = sum(r["post_status"] == "PASSED" for r in rows)
    summary = {
        "phase": f"9B {layer_tag} fail-gated authoritative",
        "status": "COMPLETE",
        "authority_status": AUTHORITY,
        "namespace": NS,
        "rule_id": rule_id,
        "cells": 320,
        "gated_fail_count": len(gated_rows),
        "preserved_pass_count": len(pass_rows),
        "eligibility_among_gated": {
            "ELIGIBLE": status_counts.get("ELIGIBLE", 0),
            "AMBIGUOUS_ABSTAIN": status_counts.get("AMBIGUOUS_ABSTAIN", 0),
            "INELIGIBLE": status_counts.get("INELIGIBLE", 0),
        },
        "triggered": sum(r["triggered"] for r in rows),
        "modified": sum(r["modified"] for r in rows),
        "abstained": sum(r["abstained"] for r in rows),
        "next_pass": next_pass,
        "next_fail": 320 - next_pass,
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
        "pass_pass_modified": pass_pass_mod,
        "verified_rescue_ids": [
            r["cell_id"] for r in rows if r["transition"] == "verified_rescue"
        ],
        "regression_ids": [r["cell_id"] for r in rows if r["transition"] == "regression"],
        "eligible_ids": [r["cell_id"] for r in rows if r["eligible"]],
        "min_score": MIN_SCORE,
        "min_margin": MIN_MARGIN,
        "model_calls": 0,
        "deterministic_second_replay": second,
    }
    write_json(results_root / "summary.json", summary)

    closure_cells = []
    for r in rows:
        closure_cells.append(
            {
                "cell_id": r["cell_id"],
                "model": "qwen3.5:9b",
                "model_group": "qwen9b",
                "task_id": r["task_id"],
                "condition": r["condition"],
                "seed": r["seed"],
                prior_outcome_key: r[prior_outcome_key],
                prior_path_key: r[prior_path_key],
                prior_sha_key: r[prior_sha_key],
                next_path_key: r["post_source_path"],
                next_sha_key: r["post_source_sha256"],
                next_outcome_key: r["post_status"],
                "source_origin": r["source_origin"],
                "gated_into_healer": r["gated_into_healer"],
                "eligibility_status": r["eligibility_status"],
                "modified": r["modified"],
                "transition": r["transition"],
            }
        )

    return {
        "summary": summary,
        "rows": rows,
        "census_rows": census_rows,
        "second": second,
        "results_root": results_root,
        "closure_cells": closure_cells,
        "freeze": freeze_audit(freeze_files, rule_id),
    }


def write_layer(
    *,
    layer_short: str,
    rule_id: str,
    out: dict[str, Any],
    closure_status: str,
    closure_verdict: str,
    definition: str,
    pass_key: str,
    fail_key: str,
) -> None:
    s = out["summary"]
    write_json(
        ROOT
        / "docs/experiments/manifests"
        / f"math16_{layer_short}_residual_supply_{NS}.json",
        {
            "status": f"math16_{layer_short}_residual_supply_{NS}",
            "authority_status": AUTHORITY,
            "namespace": NS,
            "rule_id": rule_id,
            "head": head_sha(),
            "aggregate": {
                "gated_fail": s["gated_fail_count"],
                "preserved_pass": s["preserved_pass_count"],
                "eligibility_among_gated": s["eligibility_among_gated"],
                "triggered": s["triggered"],
                "modified": s["modified"],
                "abstained": s["abstained"],
                "eligible_ids": s["eligible_ids"],
            },
            "cells": out["census_rows"],
            "rule_freeze_audit": out["freeze"],
            "min_score": MIN_SCORE,
            "min_margin": MIN_MARGIN,
        },
    )
    write_text(
        ROOT
        / "docs/experiments/reports"
        / f"math16_{layer_short}_residual_supply_{NS}.md",
        "\n".join(
            [
                f"# Math16 {layer_short} Residual Supply — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **rule_id:** `{rule_id}`",
                "",
                f"- gated FAIL／preserved PASS: **{s['gated_fail_count']}／{s['preserved_pass_count']}**",
                f"- ELIGIBLE／AMBIGUOUS／INELIGIBLE: **{s['eligibility_among_gated']['ELIGIBLE']}／{s['eligibility_among_gated']['AMBIGUOUS_ABSTAIN']}／{s['eligibility_among_gated']['INELIGIBLE']}**",
                f"- triggered／modified／abstained: **{s['triggered']}／{s['modified']}／{s['abstained']}**",
                "",
            ]
        )
        + "\n",
    )
    write_json(
        ROOT
        / "docs/experiments/manifests"
        / f"math16_{layer_short}_reproducibility_{NS}.json",
        {
            "status": f"math16_{layer_short}_reproducibility_{NS}",
            "verdict": f"{layer_short.upper()}_FAIL_GATED_AUTHORITATIVE_COMPLETE",
            "authority_status": AUTHORITY,
            "namespace": NS,
            "rule_id": rule_id,
            "head": head_sha(),
            "results_root": str(out["results_root"].relative_to(ROOT)).replace("\\", "/"),
            "summary": s,
            "deterministic_second_replay": out["second"],
            "rule_freeze_audit": out["freeze"],
            "model_calls": 0,
        },
    )
    write_text(
        ROOT
        / "docs/experiments/reports"
        / f"math16_{layer_short}_reproducibility_{NS}.md",
        "\n".join(
            [
                f"# Math16 {layer_short} Reproducibility — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **rule_id:** `{rule_id}`",
                f"> **HEAD:** `{head_sha()}`",
                "",
                f"- next PASS／FAIL: **{s['next_pass']}／{s['next_fail']}**",
                f"- eligible／modified／rescue／regression: **{s['eligibility_among_gated']['ELIGIBLE']}／{s['modified']}／{s['transitions']['verified_rescue']}／{s['transitions']['regression']}**",
                f"- parse／execution／blocker／modified_still_failed: **{s['parse_gain']}／{s['execution_gain']}／{s['blocker_removal_only']}／{s['modified_still_failed']}**",
                f"- PASS→PASS: **{s['pass_pass_modified']}**",
                f"- second replay zero-diff: **{out['second']['zero_diff']}**",
                "",
            ]
        )
        + "\n",
    )
    closure = {
        "status": closure_status,
        "verdict": closure_verdict,
        "definition": definition,
        "authority_status": AUTHORITY,
        "namespace": NS,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "head": head_sha(),
        "validation": {
            "n_cells": 320,
            "unique_ids": 320,
            "duplicate_ids": 0,
            pass_key: s["next_pass"],
            fail_key: s["next_fail"],
            "gated_fail_count": s["gated_fail_count"],
            "preserved_pass_count": s["preserved_pass_count"],
            "pass_pass_modified": 0,
            "verified_rescue": s["transitions"]["verified_rescue"],
            "regression": s["transitions"]["regression"],
            "preserved_pass": s["transitions"]["preserved_pass"],
            "still_failed": s["transitions"]["still_failed"],
            "origin_counts": dict(
                Counter(c["source_origin"] for c in out["closure_cells"])
            ),
            "no_missing_duplicate_fallback": True,
            "passed": True,
        },
        "cells": out["closure_cells"],
        "declarations": [
            "authoritative_fail_gated",
            "no_model_calls",
            "prior_pass_not_scanned",
            "thresholds_unchanged",
        ],
    }
    write_json(ROOT / "docs/experiments/manifests" / f"{closure_status}.json", closure)
    write_text(
        ROOT / "docs/experiments/reports" / f"{closure_status}.md",
        "\n".join(
            [
                f"# {closure_verdict} — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{head_sha()}`",
                "",
                f"- PASS/FAIL: **{s['next_pass']}/{s['next_fail']}**",
                f"- origins: `{closure['validation']['origin_counts']}`",
                "",
            ]
        )
        + "\n",
    )


def apply_d5_static(*, cell: dict[str, Any], source: str):
    return d5.apply_once(
        source, task_id=cell["task_id"], condition=cell["condition"]
    )


def run_d5_pipe(*, cell: dict[str, Any], source: str):
    return run_tier_d_d5_pipeline(
        source, task_id=cell["task_id"], condition=cell["condition"]
    )


def apply_d2_static(*, cell: dict[str, Any], source: str):
    return d2.apply_once(source)


def run_d2_pipe(*, cell: dict[str, Any], source: str):
    return run_tier_d_d2_pipeline(source)


def main() -> int:
    if MIN_SCORE != 8 or MIN_MARGIN != 2:
        raise RuntimeError(f"THRESHOLD_DRIFT: {MIN_SCORE}/{MIN_MARGIN}")

    print("== C5a input ==")
    c5a = json.loads(C5A_CLOSURE.read_text(encoding="utf-8"))
    verify_prior_closure(
        c5a,
        outcome_key="c5a_outcome",
        path_key="c5a_final_source_path",
        sha_key="c5a_final_source_sha256",
        expected_pass=102,
        expected_fail=218,
        label="C5A",
    )
    print("C5a ok 102/218")

    print("== C5a→C5b D5 ==")
    d5_out = run_single_rule_layer(
        layer_tag="C5A_C5B_D5",
        rule_id=RULE_ID_D5,
        prior_closure=c5a,
        prior_outcome_key="c5a_outcome",
        prior_path_key="c5a_final_source_path",
        prior_sha_key="c5a_final_source_sha256",
        next_outcome_key="c5b_outcome",
        next_path_key="c5b_final_source_path",
        next_sha_key="c5b_final_source_sha256",
        expected_prior_pass=102,
        expected_prior_fail=218,
        apply_static=apply_d5_static,
        run_pipeline=run_d5_pipe,
        freeze_files=FREEZE_D5,
        results_dirname=f"math16_c5a_c5b_tier_d_d5_reproducibility_{NS}",
        origin_if_modified="TIER_D_D5_POST_SOURCE",
    )
    write_layer(
        layer_short="c5a_c5b_tier_d_d5",
        rule_id=RULE_ID_D5,
        out=d5_out,
        closure_status=f"math16_c5b_final_source_closure_{NS}",
        closure_verdict="C5B_FINAL_SOURCE_CLOSURE_PASSED",
        definition="C5b = C5a + Tier D D5 Ranked Domain Method Binding (FAIL-only)",
        pass_key="c5b_pass",
        fail_key="c5b_fail",
    )
    print(
        "C5b",
        d5_out["summary"]["next_pass"],
        "elig",
        d5_out["summary"]["eligibility_among_gated"]["ELIGIBLE"],
        "mod",
        d5_out["summary"]["modified"],
        "rescue",
        d5_out["summary"]["transitions"]["verified_rescue"],
    )

    c5b = json.loads(
        (
            ROOT
            / "docs/experiments/manifests"
            / f"math16_c5b_final_source_closure_{NS}.json"
        ).read_text(encoding="utf-8")
    )
    c5b_pass = c5b["validation"]["c5b_pass"]
    c5b_fail = c5b["validation"]["c5b_fail"]

    print("== C5b→C5c D2 ==")
    d2_out = run_single_rule_layer(
        layer_tag="C5B_C5C_D2",
        rule_id=RULE_ID_D2,
        prior_closure=c5b,
        prior_outcome_key="c5b_outcome",
        prior_path_key="c5b_final_source_path",
        prior_sha_key="c5b_final_source_sha256",
        next_outcome_key="c5c_outcome",
        next_path_key="c5c_final_source_path",
        next_sha_key="c5c_final_source_sha256",
        expected_prior_pass=c5b_pass,
        expected_prior_fail=c5b_fail,
        apply_static=apply_d2_static,
        run_pipeline=run_d2_pipe,
        freeze_files=FREEZE_D2,
        results_dirname=f"math16_c5b_c5c_tier_d_d2_reproducibility_{NS}",
        origin_if_modified="TIER_D_D2_POST_SOURCE",
    )
    write_layer(
        layer_short="c5b_c5c_tier_d_d2",
        rule_id=RULE_ID_D2,
        out=d2_out,
        closure_status=f"math16_c5c_final_source_closure_{NS}",
        closure_verdict="C5C_FINAL_SOURCE_CLOSURE_PASSED",
        definition="C5c = C5b + Tier D D2 Duplicate Definition Selection (FAIL-only)",
        pass_key="c5c_pass",
        fail_key="c5c_fail",
    )
    print(
        "C5c",
        d2_out["summary"]["next_pass"],
        "elig",
        d2_out["summary"]["eligibility_among_gated"]["ELIGIBLE"],
        "mod",
        d2_out["summary"]["modified"],
        "rescue",
        d2_out["summary"]["transitions"]["verified_rescue"],
    )

    chain = {
        "status": f"math16_c5a_c5c_tier_d_d5_d2_chain_{NS}",
        "authority_status": AUTHORITY,
        "namespace": NS,
        "head": head_sha(),
        "pass_curve_c0_c5c": {
            "C0": 101,
            "C1": 101,
            "C2": 102,
            "C3": 102,
            "C4": 102,
            "C5a": 102,
            "C5b": d5_out["summary"]["next_pass"],
            "C5c": d2_out["summary"]["next_pass"],
        },
        "d5": {
            "gated_fail": d5_out["summary"]["gated_fail_count"],
            "eligible": d5_out["summary"]["eligibility_among_gated"]["ELIGIBLE"],
            "modified": d5_out["summary"]["modified"],
            "rescue": d5_out["summary"]["transitions"]["verified_rescue"],
            "regression": d5_out["summary"]["transitions"]["regression"],
            "parse_gain": d5_out["summary"]["parse_gain"],
            "execution_gain": d5_out["summary"]["execution_gain"],
            "blocker_removal_only": d5_out["summary"]["blocker_removal_only"],
            "modified_still_failed": d5_out["summary"]["modified_still_failed"],
            "c5b_pass": d5_out["summary"]["next_pass"],
            "c5b_fail": d5_out["summary"]["next_fail"],
            "pass_pass_modified": d5_out["summary"]["pass_pass_modified"],
        },
        "d2": {
            "gated_fail": d2_out["summary"]["gated_fail_count"],
            "eligible": d2_out["summary"]["eligibility_among_gated"]["ELIGIBLE"],
            "modified": d2_out["summary"]["modified"],
            "rescue": d2_out["summary"]["transitions"]["verified_rescue"],
            "regression": d2_out["summary"]["transitions"]["regression"],
            "parse_gain": d2_out["summary"]["parse_gain"],
            "execution_gain": d2_out["summary"]["execution_gain"],
            "blocker_removal_only": d2_out["summary"]["blocker_removal_only"],
            "modified_still_failed": d2_out["summary"]["modified_still_failed"],
            "c5c_pass": d2_out["summary"]["next_pass"],
            "c5c_fail": d2_out["summary"]["next_fail"],
            "pass_pass_modified": d2_out["summary"]["pass_pass_modified"],
        },
        "model_calls": 0,
        "other_tier_d_rules_added": False,
    }
    write_json(
        ROOT
        / "docs/experiments/manifests"
        / f"math16_c5a_c5c_tier_d_d5_d2_chain_{NS}.json",
        chain,
    )
    write_text(
        ROOT
        / "docs/experiments/reports"
        / f"math16_c5a_c5c_tier_d_d5_d2_chain_{NS}.md",
        "\n".join(
            [
                f"# Math16 C5a→C5c Tier D D5→D2 Chain — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{head_sha()}`",
                "",
                f"- PASS curve C0→C5c: `{chain['pass_curve_c0_c5c']}`",
                f"- D5: eligible／modified／rescue = **{chain['d5']['eligible']}／{chain['d5']['modified']}／{chain['d5']['rescue']}**; C5b PASS=**{chain['d5']['c5b_pass']}**",
                f"- D2: eligible／modified／rescue = **{chain['d2']['eligible']}／{chain['d2']['modified']}／{chain['d2']['rescue']}**; C5c PASS=**{chain['d2']['c5c_pass']}**",
                "",
            ]
        )
        + "\n",
    )
    print("DONE")
    print(json.dumps(chain["pass_curve_c0_c5c"], ensure_ascii=False, indent=2))
    print(json.dumps({"d5": chain["d5"], "d2": chain["d2"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
