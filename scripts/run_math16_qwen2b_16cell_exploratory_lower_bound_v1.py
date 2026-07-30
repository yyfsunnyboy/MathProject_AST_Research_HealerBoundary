# -*- coding: utf-8 -*-
"""Qwen 3.5 2B 16-cell exploratory lower-bound frozen Healer zero-model replay.

Namespace: qwen2b_16cell_exploratory_lower_bound_v1

Input: sealed smoke 16-cell raw (+ sealed timeout-rerun fill for 3 API timeouts).
Order: Tier A → B → C1 → C2 → D3 → D1 → D5 → D2 (FAIL-only, single pass).
Does not call a model, change rules/thresholds/order, modify 4B/9B/Gemini
artifacts, or mix into the three-model Round 1 primary tables.
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
from typing import Any, Callable, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_tier_a import (  # noqa: E402
    RULE_ORDER as TIER_B_RULE_ORDER,
    run_tier_a_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2 import (  # noqa: E402
    RULE_ID as TIER_C2_RULE_ID,
    run_tier_c2_default_optional_cleanup,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    RULE_ID_D1,
    RULE_ID_D2,
    RULE_ID_D3,
    RULE_ID_D5,
    run_tier_d_d2_pipeline,
    run_tier_d_d5_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    rule_d1_ops_shadow_removal as d1_mod,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    rule_d2_duplicate_definition_selection as d2_mod,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    rule_d3_syntax_residue_quarantine as d3_mod,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    rule_d5_ranked_domain_method_binding as d5_mod,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.ranking import (  # noqa: E402
    MIN_MARGIN,
    MIN_SCORE,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (  # noqa: E402
    RULE_ALLOWLIST,
    MathHealerRunner,
)
from agent_tools.finals_rebuild.extraction import extract_code  # noqa: E402
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.preflight_math16_method2_all_cell import (  # noqa: E402
    classify_transition,
    decide_eligibility,
)
from scripts.run_math16_c2_c3_tier_c1_qwen9b_v1 import (  # noqa: E402
    adjudicate_c1,
    apply_c1_rename,
)
from scripts.run_math16_c3_c4_tier_c2_qwen9b_v1 import adjudicate_c2  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

NS = "qwen2b_16cell_exploratory_lower_bound_v1"
AUTHORITY = "EXPLORATORY_LOWER_BOUND_FAIL_GATED_V1"
N_CELLS = 16
MODEL = "qwen3.5:2b"
MODEL_GROUP = "qwen2b"

SMOKE_ROOT = ROOT / (
    "docs/experiments/results/qwen35_2b_math16_four_condition_smoke_20260725_001"
)
SMOKE_MANIFEST = ROOT / (
    "docs/experiments/manifests/math16_qwen35_2b_four_condition_smoke_20260725_v1.json"
)
RERUN_ROOT = ROOT / (
    "docs/experiments/results/qwen35_2b_math16_timeout_rerun_240s_20260725_001"
)
CONTRACT_MATRIX = ROOT / "docs/experiments/manifests/math16_ab2d_task_contract_matrix_v1.json"

TIER_B_EXPECTED_ORDER = (
    "core.normalize_fullwidth_python_punctuation",
    "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1",
    "TIER_A_EMPTY_SUITE_INSERT_PASS_V1",
    "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1",
)

# Sealed timeout-rerun fill for the 3 smoke API timeouts (no new model calls).
TIMEOUT_FILL: dict[str, str] = {
    "qwen35_2b__ce115_calc_polynomial_division_l1__ab2d_spec_v2__seed_2026071301": (
        "qwen35_2b__ce115_calc_polynomial_division_l1__ab2d_spec_v2__"
        "seed_2026071301__rerun_240s"
    ),
    "qwen35_2b__ce111_q05_exact_fraction_expression__ab2g__seed_2026071301": (
        "qwen35_2b__ce111_q05_exact_fraction_expression__ab2g__"
        "seed_2026071301__rerun_240s"
    ),
    "qwen35_2b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301": (
        "qwen35_2b__ce115_calc_radical_simplification_l1__ab2g__"
        "seed_2026071301__rerun_240s"
    ),
}

LAYER_SPECS = [
    ("tier_a", "c0", "c1", "Tier A"),
    ("tier_b", "c1", "c2", "Tier B"),
    ("tier_c1", "c2", "c3", "Tier C1"),
    ("tier_c2", "c3", "c4", "Tier C2"),
    ("tier_d3", "c4", "c5_d3", "D3"),
    ("tier_d1", "c5_d3", "c5_d1", "D1"),
    ("tier_d5", "c5_d1", "c5_d5", "D5"),
    ("tier_d2", "c5_d5", "c5c", "D2"),
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


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


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


def ns_path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)


def resolve_raw_dir(cell_id: str) -> tuple[Path, str]:
    primary = SMOKE_ROOT / cell_id
    raw = primary / "raw_response.txt"
    if raw.exists() and raw.stat().st_size > 0:
        return primary, "SMOKE_PRIMARY"
    fill = TIMEOUT_FILL.get(cell_id)
    expect(fill is not None, f"MISSING_RAW_NO_FILL:{cell_id}")
    rerun = RERUN_ROOT / fill
    expect((rerun / "raw_response.txt").exists(), f"MISSING_RERUN_RAW:{cell_id}")
    return rerun, "SMOKE_TIMEOUT_RERUN_240S_FILL"


def static_status_from_step(step: Any) -> str:
    if step.applied:
        return "ELIGIBLE"
    if step.triggered and step.abstained:
        return "AMBIGUOUS_ABSTAIN"
    return "INELIGIBLE"


# ---------------------------------------------------------------------------
# C0 baseline from sealed 2B smoke (+ timeout fill)
# ---------------------------------------------------------------------------


def build_c0() -> dict[str, Any]:
    plan = json.loads(SMOKE_MANIFEST.read_text(encoding="utf-8"))
    cells_plan = plan["cells"]
    expect(len(cells_plan) == N_CELLS, f"PLAN_N:{len(cells_plan)}")
    ids = [c["cell_id"] for c in cells_plan]
    expect(len(set(ids)) == N_CELLS, "PLAN_DUP_IDS")

    smoke_summary = json.loads((SMOKE_ROOT / "summary.json").read_text(encoding="utf-8"))
    smoke_by_id = {r["cell_id"]: r for r in smoke_summary["results"]}
    expect(len(smoke_by_id) == N_CELLS, "SMOKE_SUMMARY_N")

    tasks = tasks_by_id()
    _, api_policy_map = _load_family_and_api_policy()

    raw_dir = ns_path("docs/experiments/results", f"math16_c0_baseline_{NS}", "raw_sources")
    if raw_dir.parent.exists():
        shutil.rmtree(raw_dir.parent)
    raw_dir.mkdir(parents=True)

    out_cells: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []
    pass_n = fail_n = 0
    fill_n = 0

    for cell in cells_plan:
        cid = cell["cell_id"]
        smoke_row = smoke_by_id[cid]
        raw_dir_src, lineage = resolve_raw_dir(cid)
        if lineage != "SMOKE_PRIMARY":
            fill_n += 1
        raw_path = raw_dir_src / "raw_response.txt"
        raw_text = raw_path.read_text(encoding="utf-8")
        extraction = extract_code(raw_text)
        raw_source = (
            extraction.extracted_code if extraction.extraction_status == "extracted" else ""
        )
        task = tasks[cell["task_id"]]
        frozen_params = frozen_for_prompt(task)["oracle_payload"]
        api_policy = api_policy_map[cell["task_id"]]
        score = score_source(
            raw_source, task=task, frozen_params=frozen_params, api_policy=api_policy
        )
        status = score["status"]
        if status == "PASSED":
            pass_n += 1
        else:
            fail_n += 1

        src_path = raw_dir / f"{cid}.py"
        src_path.write_bytes(raw_source.encode("utf-8"))
        rel = str(src_path.relative_to(ROOT)).replace("\\", "/")
        sha = sha256_text(raw_source)
        out_cells.append(
            {
                "cell_id": cid,
                "model": MODEL,
                "model_group": MODEL_GROUP,
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "domain": cell.get("domain"),
                "seed": cell["seed"],
                "c0_outcome": status,
                "c0_classifier_outcome": score["classifier_outcome"],
                "c0_primary_failure_layer": score["primary_failure_layer"],
                "c0_failure_subtype": score["failure_subtype"],
                "c0_final_source_path": rel,
                "c0_final_source_sha256": sha,
                "raw_response_path": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
                "extraction_status": extraction.extraction_status,
                "source_lineage": lineage,
                "smoke_status": smoke_row.get("status"),
                "smoke_outcome": smoke_row.get("outcome"),
                "source_origin": "QWEN35_2B_SMOKE_RAW_RESPONSE",
            }
        )
        lineage_rows.append(
            {
                "cell_id": cid,
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "raw_response_path": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
                "source_lineage": lineage,
                "extraction_status": extraction.extraction_status,
                "c0_outcome": status,
                "c0_final_source_sha256": sha,
                "smoke_status": smoke_row.get("status"),
                "smoke_outcome": smoke_row.get("outcome"),
            }
        )

    expect(pass_n + fail_n == N_CELLS, "C0_COUNT")
    expect(pass_n == 0 and fail_n == 16, f"C0_BASELINE_NOT_0_16:{pass_n}/{fail_n}")
    expect(fill_n == 3, f"TIMEOUT_FILL_N:{fill_n}")

    manifest = {
        "status": f"math16_c0_baseline_closure_{NS}",
        "verdict": "C0_BASELINE_CLOSURE_PASSED",
        "authority_status": AUTHORITY,
        "evidence_role": "exploratory_lower_bound",
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "namespace": NS,
        "head": head_sha(),
        "model": MODEL,
        "smoke_run_id": plan["run_id"],
        "smoke_manifest": str(SMOKE_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
        "timeout_fill_run_id": "qwen35_2b_math16_timeout_rerun_240s_20260725_001",
        "timeout_fill_cells": fill_n,
        "validation": {
            "n_cells": N_CELLS,
            "unique_ids": N_CELLS,
            "duplicate_ids": 0,
            "pass_n": pass_n,
            "fail_n": fail_n,
            "aligned_to_smoke_manifest": True,
            "passed": True,
        },
        "cells": out_cells,
        "declarations": [
            "exploratory_lower_bound",
            "no_model_calls",
            "fail_only",
            "not_three_model_primary",
            "sealed_smoke_plus_timeout_rerun_fill",
        ],
    }
    write_json(
        ns_path("docs/experiments/manifests", f"math16_c0_baseline_closure_{NS}.json"),
        manifest,
    )
    write_json(
        ns_path("docs/experiments/manifests", f"math16_16cell_lineage_{NS}.json"),
        {
            "status": f"math16_16cell_lineage_{NS}",
            "namespace": NS,
            "n_cells": N_CELLS,
            "unique_ids": N_CELLS,
            "timeout_fill_cells": fill_n,
            "cells": lineage_rows,
        },
    )
    write_jsonl(
        ns_path("docs/experiments/results", f"math16_16cell_lineage_{NS}", "lineage.jsonl"),
        lineage_rows,
    )
    write_text(
        ns_path("docs/experiments/reports", f"math16_c0_baseline_closure_{NS}.md"),
        "\n".join(
            [
                f"# Math16 C0 Baseline Closure — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}` (exploratory lower-bound)",
                f"> **HEAD:** `{head_sha()}`",
                "",
                f"- Cells: **{N_CELLS}**; PASS/FAIL: **{pass_n}／{fail_n}**",
                f"- Timeout rerun fill: **{fill_n}** sealed cells",
                "- Gating: FAIL-only cumulative exploratory chain",
                "",
            ]
        )
        + "\n",
    )
    return manifest


# ---------------------------------------------------------------------------
# Shared FAIL-gated layer
# ---------------------------------------------------------------------------


def run_fail_gated_layer(
    *,
    layer_name: str,
    prior_closure: dict[str, Any],
    prior_key: str,
    next_key: str,
    results_dirname: str,
    heal_fail_cell: Callable[..., dict[str, Any]],
    second_heal: Callable[..., str],
) -> dict[str, Any]:
    prior_outcome_key = f"{prior_key}_outcome"
    prior_path_key = f"{prior_key}_final_source_path"
    prior_sha_key = f"{prior_key}_final_source_sha256"
    next_outcome_key = f"{next_key}_outcome"
    next_path_key = f"{next_key}_final_source_path"
    next_sha_key = f"{next_key}_final_source_sha256"

    results_root = ns_path("docs/experiments/results", results_dirname)
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
    expect(prior_pass + prior_fail == N_CELLS, f"{layer_name}_PRIOR_SUM")

    for cell in prior_closure["cells"]:
        cid = cell["cell_id"]
        prior_outcome = cell[prior_outcome_key]
        pre_path = ROOT / cell[prior_path_key]
        pre_source = pre_path.read_text(encoding="utf-8")
        expect(sha256_path(pre_path) == cell[prior_sha_key], f"PRIOR_SHA_DRIFT:{cid}")

        gated = prior_outcome == "FAILED"
        if not gated:
            post_source = pre_source
            heal_info = {
                "gated_into_healer": False,
                "eligible": False,
                "eligibility_status": "PRIOR_PASS_NOT_SCANNED",
                "abstention_reason": "prior_pass_preserved_no_scan",
                "triggered": False,
                "modified": False,
                "abstained": True,
                "rule_triggered_ids": [],
                "ambiguous": False,
            }
            pre_score = {
                "status": "PASSED",
                "classifier_outcome": "inherited_prior_pass",
                "primary_failure_layer": None,
                "failure_subtype": None,
            }
            post_score = dict(pre_score)
            final_origin = "PRIOR_PASS_PRESERVED"
        else:
            heal_info = heal_fail_cell(cell=cell, pre_source=pre_source)
            post_source = heal_info["post_source"]
            if heal_info["modified"]:
                final_origin = heal_info.get(
                    "source_origin_if_modified", f"{layer_name.upper()}_POST_SOURCE"
                )
            else:
                final_origin = "PRIOR_FAIL_UNCHANGED"
            task = tasks[cell["task_id"]]
            frozen_params = frozen_for_prompt(task)["oracle_payload"]
            api_policy = api_policy_map[cell["task_id"]]
            pre_score = score_source(
                pre_source, task=task, frozen_params=frozen_params, api_policy=api_policy
            )
            post_score = score_source(
                post_source, task=task, frozen_params=frozen_params, api_policy=api_policy
            )
            expect(pre_score["status"] == "FAILED", f"GATED_PRE_NOT_FAIL:{cid}")

        expect(
            (not heal_info["modified"] and post_source == pre_source)
            or (heal_info["modified"] and post_source != pre_source),
            f"MODIFY_INVARIANT:{cid}",
        )
        if not gated:
            expect(post_source == pre_source, f"PASS_MUTATED:{cid}")

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
            heal_info["modified"]
            and transition != "verified_rescue"
            and (parse_gain or execution_gain)
        )
        elig_status = heal_info["eligibility_status"]
        ambiguous = bool(heal_info.get("ambiguous")) or (
            "AMBIGUOUS" in str(elig_status).upper()
        )

        row = {
            "cell_id": cid,
            "model": MODEL,
            "model_group": MODEL_GROUP,
            "task_id": cell["task_id"],
            "condition": cell["condition"],
            "seed": cell["seed"],
            prior_outcome_key: prior_outcome,
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
            "abstention_reason": heal_info.get("abstention_reason"),
            "eligible": bool(heal_info.get("eligible")),
            "ambiguous": ambiguous,
            "triggered": bool(heal_info.get("triggered")),
            "modified": bool(heal_info.get("modified")),
            "abstained": bool(heal_info.get("abstained")),
            "pre_status": pre_score["status"],
            "post_status": post_score["status"],
            next_outcome_key: post_score["status"],
            "transition": transition,
            "parse_gain": parse_gain,
            "execution_gain": execution_gain,
            "blocker_removal_only": blocker_removal,
            "source_origin": final_origin,
            "source_lineage": cell.get("source_lineage"),
            "evaluator_used_for_selection": False,
            "model_calls": 0,
            "rule_triggered_ids": heal_info.get("rule_triggered_ids") or [],
        }
        rows.append(row)
        census_rows.append(
            {
                "cell_id": cid,
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "gated_into_healer": gated,
                "status": elig_status,
                "abstention_reason": heal_info.get("abstention_reason"),
                "eligible": bool(heal_info.get("eligible")),
                "ambiguous": ambiguous,
            }
        )

    write_jsonl(results_root / "transition_journal.jsonl", rows)
    write_jsonl(results_root / "census_journal.jsonl", census_rows)

    mismatches = []
    for cell, first in zip(prior_closure["cells"], rows):
        cid = cell["cell_id"]
        pre = (ROOT / cell[prior_path_key]).read_text(encoding="utf-8")
        if cell[prior_outcome_key] == "PASSED":
            post = pre
        else:
            post = second_heal(cell=cell, pre_source=pre)
        if sha256_text(post) != first["post_source_sha256"]:
            mismatches.append({"cell_id": cid, "field": "post_source_sha256"})
        if cell[prior_outcome_key] == "PASSED" and first["post_source_sha256"] != first[
            "pre_source_sha256"
        ]:
            mismatches.append({"cell_id": cid, "field": "pass_sha_changed"})
    second = {
        "second_replay_mismatches": len(mismatches),
        "zero_diff": len(mismatches) == 0,
        "sample": mismatches[:20],
    }
    write_json(results_root / "deterministic_second_replay.json", second)
    expect(second["zero_diff"], f"{layer_name}_SECOND_REPLAY_DIFF:{len(mismatches)}")

    gated_n = sum(1 for r in rows if r["gated_into_healer"])
    preserved_pass_n = sum(1 for r in rows if not r["gated_into_healer"])
    next_pass = sum(1 for r in rows if r["post_status"] == "PASSED")
    expect(gated_n == prior_fail, f"{layer_name}_GATED:{gated_n}")
    expect(preserved_pass_n == prior_pass, f"{layer_name}_PRESERVED:{preserved_pass_n}")

    for r in rows:
        if not r["gated_into_healer"]:
            expect(
                r["pre_source_sha256"] == r["post_source_sha256"],
                f"PASS_SHA_CHANGED:{r['cell_id']}",
            )
            expect(r["source_origin"] == "PRIOR_PASS_PRESERVED", f"PASS_ORIGIN:{r['cell_id']}")

    status_counts = Counter(r["eligibility_status"] for r in rows if r["gated_into_healer"])
    transitions = Counter(r["transition"] for r in rows)
    pass_pass_mod = sum(
        1
        for r in rows
        if r["modified"] and r["pre_status"] == "PASSED" and r["post_status"] == "PASSED"
    )
    expect(pass_pass_mod == 0, f"{layer_name}_PASS_PASS_MOD:{pass_pass_mod}")

    summary = {
        "phase": f"Qwen2B {layer_name} exploratory lower-bound fail-gated",
        "status": "COMPLETE",
        "authority_status": AUTHORITY,
        "evidence_role": "exploratory_lower_bound",
        "namespace": NS,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "cells": N_CELLS,
        "gated_fail_count": gated_n,
        "preserved_pass_count": preserved_pass_n,
        "eligibility_among_gated": dict(status_counts),
        "eligible": sum(1 for r in rows if r["eligible"]),
        "ambiguous": sum(1 for r in rows if r["ambiguous"]),
        "triggered": sum(1 for r in rows if r["triggered"]),
        "modified": sum(1 for r in rows if r["modified"]),
        "abstained": sum(1 for r in rows if r["abstained"]),
        "prior_pass_observed": prior_pass,
        "next_pass": next_pass,
        "next_fail": N_CELLS - next_pass,
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
        "parse_gain": sum(1 for r in rows if r["parse_gain"]),
        "execution_gain": sum(1 for r in rows if r["execution_gain"]),
        "pass_pass_modified": pass_pass_mod,
        "verified_rescue_ids": [
            r["cell_id"] for r in rows if r["transition"] == "verified_rescue"
        ],
        "regression_ids": [r["cell_id"] for r in rows if r["transition"] == "regression"],
        "eligible_ids": [r["cell_id"] for r in rows if r["eligible"]],
        "model_calls": 0,
        "deterministic_second_replay": second,
    }
    write_json(results_root / "summary.json", summary)

    closure_cells = []
    for r, prior_cell in zip(rows, prior_closure["cells"]):
        closure_cells.append(
            {
                "cell_id": r["cell_id"],
                "model": MODEL,
                "model_group": MODEL_GROUP,
                "task_id": r["task_id"],
                "condition": r["condition"],
                "seed": r["seed"],
                "domain": prior_cell.get("domain"),
                "source_lineage": prior_cell.get("source_lineage"),
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
        "results_root": results_root,
        "closure_cells": closure_cells,
        "second": second,
        "prior_key": prior_key,
        "next_key": next_key,
    }


def write_layer_artifacts(*, layer_tag: str, display: str, out: dict[str, Any]) -> dict[str, Any]:
    summary = out["summary"]
    next_key = out["next_key"]
    next_pass = summary["next_pass"]
    next_fail = summary["next_fail"]

    write_json(
        ns_path("docs/experiments/manifests", f"math16_{layer_tag}_reproducibility_{NS}.json"),
        {
            "status": f"math16_{layer_tag}_reproducibility_{NS}",
            "verdict": f"{layer_tag.upper()}_EXPLORATORY_LOWER_BOUND_COMPLETE",
            "authority_status": AUTHORITY,
            "evidence_role": "exploratory_lower_bound",
            "namespace": NS,
            "gating_policy": "FAIL_ONLY_CUMULATIVE",
            "head": head_sha(),
            "results_root": str(out["results_root"].relative_to(ROOT)).replace("\\", "/"),
            "summary": summary,
            "deterministic_second_replay": out["second"],
            "model_calls": 0,
        },
    )
    write_json(
        ns_path("docs/experiments/manifests", f"math16_{layer_tag}_residual_supply_{NS}.json"),
        {
            "status": f"math16_{layer_tag}_residual_supply_{NS}",
            "namespace": NS,
            "authority_status": AUTHORITY,
            "layer": display,
            "gated_fail_count": summary["gated_fail_count"],
            "eligible": summary["eligible"],
            "ambiguous": summary["ambiguous"],
            "modified": summary["modified"],
            "abstained": summary["abstained"],
            "verified_rescue": summary["transitions"]["verified_rescue"],
            "parse_gain": summary["parse_gain"],
            "execution_gain": summary["execution_gain"],
            "blocker_removal_only": summary["blocker_removal_only"],
            "modified_still_failed": summary["modified_still_failed"],
            "regression": summary["transitions"]["regression"],
            "eligibility_among_gated": summary["eligibility_among_gated"],
        },
    )
    write_text(
        ns_path("docs/experiments/reports", f"math16_{layer_tag}_reproducibility_{NS}.md"),
        "\n".join(
            [
                f"# Math16 {display} Reproducibility — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **HEAD:** `{head_sha()}`",
                "",
                f"- gated／preserved: **{summary['gated_fail_count']}／{summary['preserved_pass_count']}**",
                f"- eligible／ambiguous／modified／abstained: "
                f"**{summary['eligible']}／{summary['ambiguous']}／"
                f"{summary['modified']}／{summary['abstained']}**",
                f"- rescue／parse／exec／blocker／msf／regression: "
                f"**{summary['transitions']['verified_rescue']}／{summary['parse_gain']}／"
                f"{summary['execution_gain']}／{summary['blocker_removal_only']}／"
                f"{summary['modified_still_failed']}／{summary['transitions']['regression']}**",
                f"- next PASS／FAIL: **{next_pass}／{next_fail}**",
                f"- second replay zero-diff: **{out['second']['zero_diff']}**",
                "",
            ]
        )
        + "\n",
    )

    closure_status = f"math16_{next_key}_final_source_closure_{NS}"
    closure = {
        "status": closure_status,
        "verdict": f"{next_key.upper()}_FINAL_SOURCE_CLOSURE_PASSED",
        "definition": f"{next_key} = prior + {display} (FAIL-only exploratory)",
        "authority_status": AUTHORITY,
        "evidence_role": "exploratory_lower_bound",
        "namespace": NS,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "head": head_sha(),
        "validation": {
            "n_cells": N_CELLS,
            "unique_ids": N_CELLS,
            "duplicate_ids": 0,
            f"{next_key}_pass": next_pass,
            f"{next_key}_fail": next_fail,
            "verified_rescue": summary["transitions"]["verified_rescue"],
            "regression": summary["transitions"]["regression"],
            "gated_fail_count": summary["gated_fail_count"],
            "preserved_pass_count": summary["preserved_pass_count"],
            "origin_counts": dict(Counter(c["source_origin"] for c in out["closure_cells"])),
            "passed": True,
        },
        "cells": out["closure_cells"],
        "declarations": [
            "exploratory_lower_bound",
            "no_model_calls",
            "fail_only",
            "not_three_model_primary",
        ],
    }
    write_json(ns_path("docs/experiments/manifests", f"{closure_status}.json"), closure)
    write_text(
        ns_path("docs/experiments/reports", f"{closure_status}.md"),
        "\n".join(
            [
                f"# {closure['verdict']} — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"- PASS/FAIL: **{next_pass}／{next_fail}**",
                "",
            ]
        )
        + "\n",
    )
    return closure


# ---------------------------------------------------------------------------
# Healers (frozen; no rule / threshold / order changes)
# ---------------------------------------------------------------------------


def heal_tier_a(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    runner = MathHealerRunner(max_passes=3)
    tasks = tasks_by_id()
    frozen = frozen_for_prompt(tasks[cell["task_id"]])["oracle_payload"]
    context = {"frozen": frozen}
    eligibility = decide_eligibility(pre_source or None, context)
    if eligibility["eligible"]:
        result = runner.run(pre_source, context=context)
        post = result.output_source
        modified = post != pre_source
        return {
            "post_source": post,
            "eligible": True,
            "eligibility_status": "TIER_A_ELIGIBLE",
            "abstention_reason": None,
            "triggered": bool(eligibility["rule_triggered"]) or modified,
            "modified": modified,
            "abstained": False,
            "source_origin_if_modified": "TIER_A_POST_SOURCE",
            "rule_triggered_ids": [
                p.selected_rule_id
                for p in result.provenance
                if p.changed and p.selected_rule_id
            ],
        }
    return {
        "post_source": pre_source,
        "eligible": False,
        "eligibility_status": "TIER_A_INELIGIBLE",
        "abstention_reason": eligibility.get("reason")
        or eligibility.get("abstention_reason")
        or "not_eligible",
        "triggered": False,
        "modified": False,
        "abstained": True,
        "rule_triggered_ids": [],
    }


def second_tier_a(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_tier_a(cell=cell, pre_source=pre_source)["post_source"]


def heal_tier_b(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    pipe = run_tier_a_pipeline(pre_source)
    post = pipe.post_source
    modified = post != pre_source
    fired = list(pipe.rules_fired or [])
    return {
        "post_source": post,
        "eligible": modified or bool(fired),
        "eligibility_status": "TIER_B_TRIGGERED" if (modified or fired) else "TIER_B_NOOP",
        "abstention_reason": None if (modified or fired) else "no_tier_b_rule_fired",
        "triggered": bool(fired) or modified,
        "modified": modified,
        "abstained": not (modified or fired),
        "source_origin_if_modified": "TIER_B_POST_SOURCE",
        "rule_triggered_ids": fired,
    }


def second_tier_b(*, cell: dict[str, Any], pre_source: str) -> str:
    return run_tier_a_pipeline(pre_source).post_source


_CONTRACTS: Optional[dict] = None


def contracts() -> dict:
    global _CONTRACTS
    if _CONTRACTS is None:
        matrix = json.loads(CONTRACT_MATRIX.read_text(encoding="utf-8"))
        _CONTRACTS = {
            (c["task_id"], c["condition_code"]): c for c in matrix["contracts"]
        }
    return _CONTRACTS


def heal_tier_c1(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    adj = adjudicate_c1(
        source=pre_source,
        task_id=cell["task_id"],
        condition=cell["condition"],
        contracts_by_key=contracts(),
    )
    if adj["status"] != "C1_ELIGIBLE":
        return {
            "post_source": pre_source,
            "eligible": False,
            "eligibility_status": adj["status"],
            "abstention_reason": adj.get("abstention_reason"),
            "triggered": False,
            "modified": False,
            "abstained": True,
            "rule_triggered_ids": [],
        }
    post = apply_c1_rename(pre_source, adj)
    modified = post != pre_source
    return {
        "post_source": post if modified else pre_source,
        "eligible": modified,
        "eligibility_status": "C1_ELIGIBLE" if modified else "C1_INELIGIBLE",
        "abstention_reason": None if modified else "rename_produced_identical_source",
        "triggered": modified,
        "modified": modified,
        "abstained": not modified,
        "source_origin_if_modified": "TIER_C1_POST_SOURCE",
        "rule_triggered_ids": ["TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1"]
        if modified
        else [],
    }


def second_tier_c1(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_tier_c1(cell=cell, pre_source=pre_source)["post_source"]


def heal_tier_c2(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    adj = adjudicate_c2(
        source=pre_source,
        task_id=cell["task_id"],
        condition=cell["condition"],
        contracts_by_key=contracts(),
    )
    if adj["status"] != "C2_ELIGIBLE":
        return {
            "post_source": pre_source,
            "eligible": False,
            "eligibility_status": adj["status"],
            "abstention_reason": adj.get("abstention_reason"),
            "triggered": False,
            "modified": False,
            "abstained": True,
            "rule_triggered_ids": [],
        }
    pipe = run_tier_c2_default_optional_cleanup(pre_source)
    ok = pipe.mutation_count == 1 and not pipe.rolled_back and pipe.post_source != pre_source
    if not ok:
        return {
            "post_source": pre_source,
            "eligible": False,
            "eligibility_status": "C2_INELIGIBLE",
            "abstention_reason": pipe.abstention_reason or "pipeline_did_not_commit_mutation",
            "triggered": False,
            "modified": False,
            "abstained": True,
            "rule_triggered_ids": [],
        }
    return {
        "post_source": pipe.post_source,
        "eligible": True,
        "eligibility_status": "C2_ELIGIBLE",
        "abstention_reason": None,
        "triggered": True,
        "modified": True,
        "abstained": False,
        "source_origin_if_modified": "TIER_C2_POST_SOURCE",
        "rule_triggered_ids": [TIER_C2_RULE_ID],
    }


def second_tier_c2(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_tier_c2(cell=cell, pre_source=pre_source)["post_source"]


def _heal_single_rule(
    *,
    pre_source: str,
    step: Any,
    origin: str,
    eligible_label: str,
) -> dict[str, Any]:
    status = static_status_from_step(step)
    ambiguous = status == "AMBIGUOUS_ABSTAIN"
    post = step.source_out if step.applied and step.source_out else pre_source
    if step.applied and post != pre_source:
        return {
            "post_source": post,
            "eligible": True,
            "eligibility_status": eligible_label,
            "abstention_reason": None,
            "triggered": True,
            "modified": True,
            "abstained": False,
            "ambiguous": False,
            "source_origin_if_modified": origin,
            "rule_triggered_ids": [step.rule_id],
        }
    return {
        "post_source": pre_source,
        "eligible": status == "ELIGIBLE",
        "eligibility_status": status if status != "ELIGIBLE" else f"{eligible_label}_NO_MUTATION",
        "abstention_reason": step.abstention_reason or status.lower(),
        "triggered": bool(step.triggered),
        "modified": False,
        "abstained": True,
        "ambiguous": ambiguous,
        "rule_triggered_ids": [step.rule_id] if step.triggered else [],
    }


def heal_d3(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    return _heal_single_rule(
        pre_source=pre_source,
        step=d3_mod.apply_once(pre_source),
        origin="TIER_D3_POST_SOURCE",
        eligible_label="D3_ELIGIBLE",
    )


def second_d3(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_d3(cell=cell, pre_source=pre_source)["post_source"]


def heal_d1(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    return _heal_single_rule(
        pre_source=pre_source,
        step=d1_mod.apply_once(pre_source),
        origin="TIER_D1_POST_SOURCE",
        eligible_label="D1_ELIGIBLE",
    )


def second_d1(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_d1(cell=cell, pre_source=pre_source)["post_source"]


def heal_d5(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    step = d5_mod.apply_once(
        pre_source, task_id=cell["task_id"], condition=cell["condition"]
    )
    status = static_status_from_step(step)
    pipe = run_tier_d_d5_pipeline(
        pre_source, task_id=cell["task_id"], condition=cell["condition"]
    )
    if pipe.rolled_back or pipe.post_source == pre_source:
        return {
            "post_source": pre_source,
            "eligible": status == "ELIGIBLE",
            "eligibility_status": status,
            "abstention_reason": step.abstention_reason or pipe.abstention_reason or status.lower(),
            "triggered": bool(step.triggered) or bool(pipe.rules_fired),
            "modified": False,
            "abstained": True,
            "ambiguous": status == "AMBIGUOUS_ABSTAIN",
            "rule_triggered_ids": [RULE_ID_D5] if step.triggered else [],
        }
    return {
        "post_source": pipe.post_source,
        "eligible": True,
        "eligibility_status": "D5_ELIGIBLE",
        "abstention_reason": None,
        "triggered": True,
        "modified": True,
        "abstained": False,
        "ambiguous": False,
        "source_origin_if_modified": "TIER_D5_POST_SOURCE",
        "rule_triggered_ids": [RULE_ID_D5],
    }


def second_d5(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_d5(cell=cell, pre_source=pre_source)["post_source"]


def heal_d2(*, cell: dict[str, Any], pre_source: str) -> dict[str, Any]:
    step = d2_mod.apply_once(pre_source)
    status = static_status_from_step(step)
    pipe = run_tier_d_d2_pipeline(pre_source)
    if pipe.rolled_back or pipe.post_source == pre_source:
        return {
            "post_source": pre_source,
            "eligible": status == "ELIGIBLE",
            "eligibility_status": status,
            "abstention_reason": step.abstention_reason or pipe.abstention_reason or status.lower(),
            "triggered": bool(step.triggered) or bool(pipe.rules_fired),
            "modified": False,
            "abstained": True,
            "ambiguous": status == "AMBIGUOUS_ABSTAIN",
            "rule_triggered_ids": [RULE_ID_D2] if step.triggered else [],
        }
    return {
        "post_source": pipe.post_source,
        "eligible": True,
        "eligibility_status": "D2_ELIGIBLE",
        "abstention_reason": None,
        "triggered": True,
        "modified": True,
        "abstained": False,
        "ambiguous": False,
        "source_origin_if_modified": "TIER_D2_POST_SOURCE",
        "rule_triggered_ids": [RULE_ID_D2],
    }


def second_d2(*, cell: dict[str, Any], pre_source: str) -> str:
    return heal_d2(cell=cell, pre_source=pre_source)["post_source"]


HEALERS = {
    "tier_a": (heal_tier_a, second_tier_a),
    "tier_b": (heal_tier_b, second_tier_b),
    "tier_c1": (heal_tier_c1, second_tier_c1),
    "tier_c2": (heal_tier_c2, second_tier_c2),
    "tier_d3": (heal_d3, second_d3),
    "tier_d1": (heal_d1, second_d1),
    "tier_d5": (heal_d5, second_d5),
    "tier_d2": (heal_d2, second_d2),
}


def write_protocol_manifest(pass_curve: list[dict[str, Any]], layer_summaries: dict) -> None:
    protocol = {
        "status": f"math16_protocol_{NS}",
        "verdict": "QWEN2B_16CELL_EXPLORATORY_LOWER_BOUND_PROTOCOL_SEALED",
        "authority_status": AUTHORITY,
        "evidence_role": "exploratory_lower_bound",
        "namespace": NS,
        "head": head_sha(),
        "model": MODEL,
        "n_cells": N_CELLS,
        "gating_policy": "FAIL_ONLY_CUMULATIVE",
        "layer_order": [x[0] for x in LAYER_SPECS],
        "fixed_sequence": "A→B→C1→C2→D3→D1→D5→D2",
        "inputs": {
            "smoke_manifest": str(SMOKE_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "smoke_results": str(SMOKE_ROOT.relative_to(ROOT)).replace("\\", "/"),
            "timeout_rerun_fill": str(RERUN_ROOT.relative_to(ROOT)).replace("\\", "/"),
            "timeout_fill_cell_ids": sorted(TIMEOUT_FILL.keys()),
        },
        "freeze_checks": {
            "tier_b_rule_order": list(TIER_B_RULE_ORDER),
            "tier_b_order_matches": list(TIER_B_RULE_ORDER) == list(TIER_B_EXPECTED_ORDER),
            "tier_a_allowlist_nonempty": bool(list(RULE_ALLOWLIST)),
            "d5_min_score": MIN_SCORE,
            "d5_min_margin": MIN_MARGIN,
            "d5_thresholds_unchanged": MIN_SCORE == 8 and MIN_MARGIN == 2,
            "rule_ids": {
                "d3": RULE_ID_D3,
                "d1": RULE_ID_D1,
                "d5": RULE_ID_D5,
                "d2": RULE_ID_D2,
            },
        },
        "pass_curve": pass_curve,
        "layer_summaries": {
            k: {
                "gated": v["gated_fail_count"],
                "eligible": v["eligible"],
                "ambiguous": v["ambiguous"],
                "modified": v["modified"],
                "abstained": v["abstained"],
                "verified_rescue": v["transitions"]["verified_rescue"],
                "parse_gain": v["parse_gain"],
                "execution_gain": v["execution_gain"],
                "blocker_removal_only": v["blocker_removal_only"],
                "modified_still_failed": v["modified_still_failed"],
                "regression": v["transitions"]["regression"],
                "next_pass": v["next_pass"],
                "second_replay_zero_diff": v["deterministic_second_replay"]["zero_diff"],
            }
            for k, v in layer_summaries.items()
        },
        "declarations": [
            "no_model_calls",
            "no_new_rules",
            "no_guard_threshold_order_changes",
            "no_round_2",
            "not_mixed_into_three_model_primary",
            "exploratory_lower_bound_only",
        ],
    }
    write_json(ns_path("docs/experiments/manifests", f"math16_protocol_{NS}.json"), protocol)
    write_text(
        ns_path("docs/experiments/reports", f"math16_protocol_{NS}.md"),
        "\n".join(
            [
                f"# Math16 Protocol — {NS}",
                "",
                f"> **AUTHORITY:** `{AUTHORITY}`",
                f"> **Evidence role:** exploratory lower-bound",
                "",
                f"- Sequence: **A→B→C1→C2→D3→D1→D5→D2**",
                f"- Cells: **{N_CELLS}** unique; FAIL-only; zero model calls",
                f"- Baseline PASS: **0／16**",
                "",
            ]
        )
        + "\n",
    )


def write_cumulative(pass_curve: list[dict[str, Any]], layer_summaries: dict) -> None:
    final_pass = pass_curve[-1]["pass"]
    total_rescue = sum(v["transitions"]["verified_rescue"] for v in layer_summaries.values())
    total_regression = sum(v["transitions"]["regression"] for v in layer_summaries.values())
    summary = {
        "status": f"math16_cumulative_summary_{NS}",
        "verdict": "QWEN2B_16CELL_EXPLORATORY_LOWER_BOUND_COMPLETE",
        "authority_status": AUTHORITY,
        "evidence_role": "exploratory_lower_bound",
        "namespace": NS,
        "head": head_sha(),
        "model": MODEL,
        "n_cells": N_CELLS,
        "baseline_pass": 0,
        "baseline_fail": 16,
        "final_pass": final_pass,
        "final_fail": N_CELLS - final_pass,
        "total_verified_rescue": total_rescue,
        "total_regression": total_regression,
        "pass_curve": pass_curve,
        "layers": {
            k: {
                "gated": v["gated_fail_count"],
                "eligible": v["eligible"],
                "ambiguous": v["ambiguous"],
                "modified": v["modified"],
                "abstained": v["abstained"],
                "verified_rescue": v["transitions"]["verified_rescue"],
                "parse_gain": v["parse_gain"],
                "execution_gain": v["execution_gain"],
                "blocker_removal_only": v["blocker_removal_only"],
                "modified_still_failed": v["modified_still_failed"],
                "regression": v["transitions"]["regression"],
                "next_pass": v["next_pass"],
                "eligibility_among_gated": v["eligibility_among_gated"],
                "second_replay_zero_diff": v["deterministic_second_replay"]["zero_diff"],
            }
            for k, v in layer_summaries.items()
        },
        "model_calls": 0,
        "declarations": [
            "no_model_calls",
            "no_new_rules",
            "no_round_2",
            "not_three_model_primary",
            "exploratory_lower_bound",
        ],
    }
    out_json = ns_path(
        "docs/experiments/results", f"math16_cumulative_{NS}", "summary.json"
    )
    write_json(out_json, summary)
    # also mirror under manifests for discoverability
    write_json(ns_path("docs/experiments/manifests", f"math16_cumulative_summary_{NS}.json"), summary)

    lines = [
        f"# Math16 Cumulative Report — {NS}",
        "",
        f"> **AUTHORITY:** `{AUTHORITY}`",
        f"> **Evidence role:** exploratory lower-bound（非三模型正式主表）",
        f"> **HEAD:** `{head_sha()}`",
        "",
        "## Headline",
        "",
        f"- Baseline → Final PASS: **0／16 → {final_pass}／16**",
        f"- Total verified rescue: **{total_rescue}**",
        f"- Total regression: **{total_regression}**",
        f"- Model calls: **0**",
        "",
        "## PASS curve",
        "",
        "| Stage | PASS | FAIL |",
        "|---|---:|---:|",
    ]
    for row in pass_curve:
        lines.append(f"| {row['stage']} | {row['pass']} | {row['fail']} |")
    lines.extend(["", "## Per-layer ledger", ""])
    lines.append(
        "| Layer | gated | eligible | ambiguous | modified | abstained | "
        "rescue | parse | exec | blocker | msf | regression |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for tag, _p, _n, display in LAYER_SPECS:
        v = layer_summaries[tag]
        lines.append(
            f"| {display} | {v['gated_fail_count']} | {v['eligible']} | {v['ambiguous']} | "
            f"{v['modified']} | {v['abstained']} | {v['transitions']['verified_rescue']} | "
            f"{v['parse_gain']} | {v['execution_gain']} | {v['blocker_removal_only']} | "
            f"{v['modified_still_failed']} | {v['transitions']['regression']} |"
        )
    lines.extend(
        [
            "",
            "## Declarations",
            "",
            "- No model calls; sealed raw only (smoke + timeout-rerun fill).",
            "- No new rules; no guard／threshold／order changes.",
            "- No Round 2; not mixed into three-model Round 1 primary tables.",
            "",
        ]
    )
    write_text(
        ns_path("docs/experiments/results", f"math16_cumulative_{NS}", "report.md"),
        "\n".join(lines) + "\n",
    )
    write_text(
        ns_path("docs/experiments/reports", f"math16_cumulative_report_{NS}.md"),
        "\n".join(lines) + "\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-cumulative-only", action="store_true")
    _ = parser.parse_args()

    expect(tuple(TIER_B_RULE_ORDER) == TIER_B_EXPECTED_ORDER, "TIER_B_ORDER_DRIFT")
    expect(bool(list(RULE_ALLOWLIST)), "TIER_A_ALLOWLIST_EMPTY")
    expect(MIN_SCORE == 8 and MIN_MARGIN == 2, "D5_THRESHOLD_DRIFT")

    print("== C0 baseline ==")
    c0 = build_c0()
    print(f"C0 PASS/FAIL {c0['validation']['pass_n']}/{c0['validation']['fail_n']}")

    pass_curve = [{"stage": "C0", "pass": 0, "fail": 16}]
    layer_summaries: dict[str, Any] = {}
    prior = c0

    for tag, prior_key, next_key, display in LAYER_SPECS:
        print(f"== {display} ==")
        heal, second = HEALERS[tag]
        out = run_fail_gated_layer(
            layer_name=tag,
            prior_closure=prior,
            prior_key=prior_key,
            next_key=next_key,
            results_dirname=f"math16_{tag}_reproducibility_{NS}",
            heal_fail_cell=heal,
            second_heal=second,
        )
        closure = write_layer_artifacts(layer_tag=tag, display=display, out=out)
        layer_summaries[tag] = out["summary"]
        pass_curve.append(
            {
                "stage": display,
                "pass": out["summary"]["next_pass"],
                "fail": out["summary"]["next_fail"],
            }
        )
        prior = closure
        print(
            f"{display}: gated={out['summary']['gated_fail_count']} "
            f"elig={out['summary']['eligible']} mod={out['summary']['modified']} "
            f"rescue={out['summary']['transitions']['verified_rescue']} "
            f"pass={out['summary']['next_pass']}"
        )

    write_protocol_manifest(pass_curve, layer_summaries)
    write_cumulative(pass_curve, layer_summaries)
    print("== DONE ==")
    print(f"Final PASS {pass_curve[-1]['pass']}/{N_CELLS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
