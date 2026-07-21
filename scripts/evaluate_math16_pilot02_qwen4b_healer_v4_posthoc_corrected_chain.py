# -*- coding: utf-8 -*-
"""Post-hoc corrected-chain replay for Qwen4B primary eligible cells (n=10).

Uses the Math16-revalidation-fixed Healer runner. Does NOT overwrite primary
healer_v4_r001 (83/320). Does NOT call run() on noneligible or baseline PASS.
Zero LLM calls.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_research_healer_protocol import (  # noqa: E402
    RuleProtocolError,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (  # noqa: E402
    RULE_ALLOWLIST,
    MathHealerRunner,
)
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _hash_text,
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
EVIDENCE_FREEZE = (
    ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_generation_evidence_freeze_v1.json"
)
BASELINE_DIR = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001"
PRIMARY_DIR = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001"
OUT_DIR = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001"
)
EVALUATOR_PATH = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
HEALER_RUNNER_PATH = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
HEALER_PROTOCOL_PATH = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"
TAXONOMY_PATH = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
ORACLE_PATH = ROOT / "agent_tools/finals_rebuild/math16_oracles.py"

EXPECTED_CLOSURE = "7dd3ba5f7e7a38e7ad20142e8c5c5b2e84c20df1b7f5abcf5701c23d24172a22"
EXPECTED_EVAL_HASH = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
EXPECTED_TAX_HASH = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
EXPECTED_HEALER_RUNNER_HASH = (
    "38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf"
)
EXPECTED_HEALER_PROTOCOL_HASH = (
    "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"
)
EXPECTED_ALLOWLIST = (
    "L1_CLOSE_UNBALANCED_PARENTHESIS",
    "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
    "L1_PROSE_RESIDUE_NARROW",
    "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
    "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
    "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
)
EXPECTED_ELIGIBLE = 10
EXPECTED_NONELIGIBLE = 232
PRIMARY_POST_HEALER_PASS = 83
PRIMARY_RESCUED = 5
HEALER_MAX_PASSES = 3
HEALER_ID = "math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001"
PRIMARY_HEALER_ID = "math16_pilot02_qwen4b_healer_v4_r001"
CELL_A_RADICAL = (
    "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301"
)
CELL_B_Q09 = (
    "qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072001"
)

CONDITION_DISPLAY = {
    "ab1": "Ab1",
    "ab2g": "Ab2g",
    "ab2d": "Ab2d+api",
    "ab2d_spec_v2": "Ab2d+spec-v2",
}
FAMILY_DISPLAY = {
    "integer": "Integer",
    "polynomial": "Polynomial",
    "radical": "Radical",
    "fraction": "Fraction",
}


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_lf(path: Path) -> str:
    return hashlib.sha256(
        path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
    ).hexdigest()


def sha_json(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def verify_pins() -> dict[str, Any]:
    freeze = json.loads(EVIDENCE_FREEZE.read_text(encoding="utf-8"))
    if freeze["corpus_sha_closure"] != EXPECTED_CLOSURE:
        raise RuntimeError("CORPUS_SHA_CLOSURE_MISMATCH")
    eval_hash = sha_bytes(EVALUATOR_PATH)
    tax_hash = sha_bytes(TAXONOMY_PATH)
    healer_hash = sha_bytes(HEALER_RUNNER_PATH)
    protocol_hash = sha_bytes(HEALER_PROTOCOL_PATH)
    if eval_hash != EXPECTED_EVAL_HASH:
        raise RuntimeError(f"EVALUATOR_HASH_DRIFT: {eval_hash}")
    if tax_hash != EXPECTED_TAX_HASH:
        raise RuntimeError(f"TAXONOMY_HASH_DRIFT: {tax_hash}")
    if healer_hash != EXPECTED_HEALER_RUNNER_HASH:
        raise RuntimeError(f"HEALER_RUNNER_HASH_DRIFT: {healer_hash}")
    if protocol_hash != EXPECTED_HEALER_PROTOCOL_HASH:
        raise RuntimeError(f"HEALER_PROTOCOL_HASH_DRIFT: {protocol_hash}")
    if tuple(RULE_ALLOWLIST) != EXPECTED_ALLOWLIST:
        raise RuntimeError(f"ALLOWLIST_DRIFT: {RULE_ALLOWLIST}")

    primary_overall = json.loads(
        (PRIMARY_DIR / "overall_summary.json").read_text(encoding="utf-8")
    )
    if primary_overall["baseline_pass_fraction"] != "78/320":
        raise RuntimeError("PRIMARY_BASELINE_DRIFT")
    if primary_overall["post_healer_pass_fraction"] != "83/320":
        raise RuntimeError("PRIMARY_POST_HEALER_DRIFT")
    if primary_overall["counts"]["rescued"] != PRIMARY_RESCUED:
        raise RuntimeError("PRIMARY_RESCUED_DRIFT")
    if primary_overall["counts"]["fail_eligible"] != EXPECTED_ELIGIBLE:
        raise RuntimeError("PRIMARY_ELIGIBLE_DRIFT")
    if primary_overall["counts"]["fail_noneligible"] != EXPECTED_NONELIGIBLE:
        raise RuntimeError("PRIMARY_NONELIGIBLE_DRIFT")

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    records = []
    for cell in plan:
        d = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        ap, pp, rp = d / "artifact.json", d / "prompt.txt", d / "raw_response.txt"
        records.append(
            {
                "cell_id": cell["cell_id"],
                "artifact_sha256": sha_bytes(ap),
                "prompt_sha256_file": sha_lf(pp),
                "raw_response_sha256": sha_bytes(rp),
                "plan_prompt_sha256": cell["prompt_sha256"],
                "generation_status": str(
                    json.loads(ap.read_text(encoding="utf-8")).get("generation_status")
                ),
            }
        )
    recomputed = sha_json(sorted(records, key=lambda r: r["cell_id"]))
    if recomputed != EXPECTED_CLOSURE:
        raise RuntimeError(f"CORPUS_SHA_RECOMPUTE_MISMATCH: {recomputed}")

    return {
        "corpus_sha_closure": EXPECTED_CLOSURE,
        "evaluator_hash": eval_hash,
        "taxonomy_hash": tax_hash,
        "healer_runner_sha256": healer_hash,
        "healer_protocol_sha256": protocol_hash,
        "allowlist": list(RULE_ALLOWLIST),
        "healer_max_passes": HEALER_MAX_PASSES,
        "expected_eligible": EXPECTED_ELIGIBLE,
        "expected_noneligible": EXPECTED_NONELIGIBLE,
        "primary_healer_id": PRIMARY_HEALER_ID,
        "primary_post_healer_pass_fraction": "83/320",
        "primary_rescued": PRIMARY_RESCUED,
        "nature": "posthoc_corrected_chain_replay",
        "preregistered_primary": False,
    }


def load_baseline() -> dict[str, dict[str, Any]]:
    rows = load_jsonl(BASELINE_DIR / "cell_level_baseline.jsonl")
    if len(rows) != 320:
        raise RuntimeError(f"baseline rows != 320: {len(rows)}")
    index = {r["cell_id"]: r for r in rows}
    if len(index) != 320:
        raise RuntimeError("duplicate baseline cell_ids")
    passed = sum(1 for r in rows if r["final_status"] == "PASSED")
    if passed != 78:
        raise RuntimeError(f"baseline pass drift: {passed}")
    return index


def empty_bucket() -> dict[str, Any]:
    return {
        "total": 0,
        "baseline_passed": 0,
        "baseline_failed": 0,
        "post_healer_passed": 0,
        "post_healer_failed": 0,
        "eligible": 0,
        "repaired": 0,
        "rescued": 0,
        "repaired_still_fail": 0,
        "regressed": 0,
        "abstained": 0,
        "preserved_pass": 0,
        "unchanged_fail": 0,
        "no_op": 0,
    }


def disposition_label(row: dict[str, Any]) -> str:
    if row.get("rescued"):
        return "rescued"
    if row.get("repaired_still_fail"):
        return "repaired_still_fail"
    if row.get("no_op"):
        return "no_op"
    if row.get("regressed"):
        return "regression"
    return str(row.get("healer_outcome") or "unknown")


def run(*, dry_run: bool = False) -> int:
    pins = verify_pins()
    baseline = load_baseline()
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    plan_by_id = {c["cell_id"]: c for c in plan}
    family_map, api_policy_map = _load_family_and_api_policy()
    tasks = tasks_by_id()
    healer_runner = MathHealerRunner(max_passes=HEALER_MAX_PASSES)

    primary_elig = load_jsonl(PRIMARY_DIR / "eligibility_inventory.jsonl")
    primary_exec = {
        r["cell_id"]: r
        for r in load_jsonl(PRIMARY_DIR / "eligible_execution_records.jsonl")
    }
    primary_healer = {
        r["cell_id"]: r for r in load_jsonl(PRIMARY_DIR / "healer_results.jsonl")
    }
    primary_post = {
        r["cell_id"]: r for r in load_jsonl(PRIMARY_DIR / "post_healer_scoring.jsonl")
    }

    eligible_ids = sorted(
        r["cell_id"] for r in primary_elig if r.get("healer_eligible") is True
    )
    if len(eligible_ids) != EXPECTED_ELIGIBLE:
        raise RuntimeError(f"primary eligible != 10: {len(eligible_ids)}")
    if set(eligible_ids) != set(primary_exec):
        raise RuntimeError("primary eligible IDs != execution records")
    if CELL_A_RADICAL not in eligible_ids or CELL_B_Q09 not in eligible_ids:
        raise RuntimeError("expected Cell A/B missing from primary eligible set")

    unauthorized_rules: list[str] = []
    raw_sha_mismatch: list[str] = []
    evaluator_crash: list[str] = []
    protocol_errors: list[str] = []
    illegal_run_attempts: list[str] = []
    noneligible_executed: list[str] = []
    baseline_pass_executed: list[str] = []

    replay_records: list[dict[str, Any]] = []
    execution_records: list[dict[str, Any]] = []
    transformed_artifacts: list[dict[str, Any]] = []
    rule_applied: Counter[str] = Counter()

    eligible_set = set(eligible_ids)

    # Replay ONLY the 10 primary-eligible cells.
    for cell_id in eligible_ids:
        cell = plan_by_id[cell_id]
        base = baseline[cell_id]
        if base["final_status"] == "PASSED":
            baseline_pass_executed.append(cell_id)
            raise RuntimeError(f"eligible cell is baseline PASS: {cell_id}")
        tid = cell["task_id"]
        cond = cell["condition"]
        seed = int(cell["seed"])
        family = family_map[tid]
        api_policy = api_policy_map[tid]
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        raw_path = cell_dir / "raw_response.txt"
        raw = raw_path.read_text(encoding="utf-8")
        raw_sha = sha_bytes(raw_path)
        if raw_sha != base.get("raw_response_sha256"):
            raw_sha_mismatch.append(cell_id)

        task = tasks[tid]
        frozen_params = frozen_for_prompt(task)["oracle_payload"]
        context = {"task": task, "frozen": frozen_params}

        try:
            outcome, source, details = classify_math16_response(
                raw,
                frozen_params=frozen_params,
                audit_oracle_payload=task["oracle_payload"],
                task=task,
            )
            mapped = classify_outcome_to_v3(outcome, details, api_policy=api_policy)
        except Exception as exc:  # noqa: BLE001
            evaluator_crash.append(cell_id)
            raise RuntimeError(f"evaluator crash on {cell_id}: {exc}") from exc

        if mapped["final_status"] == "PASSED":
            raise RuntimeError(f"eligible cell reclassifies as PASS: {cell_id}")
        assert source is not None

        before_sha = _hash_text(source)
        after_sha = before_sha
        applied_rules: list[str] = []
        provenance: list[dict[str, Any]] = []
        repaired_source = None
        transformed = False
        rolled_back = False
        matched_rule = primary_exec[cell_id].get("matched_rule")
        healer_decision = "no_op"
        healer_outcome = "no_op"
        post_status = base["final_status"]
        post_layer = base.get("primary_failure_layer")
        post_classifier_outcome = outcome
        post_mapped = mapped

        try:
            result = healer_runner.run(source, context=context)
        except RuleProtocolError as exc:
            protocol_errors.append(f"{cell_id}:{exc}")
            raise RuntimeError(f"protocol error on {cell_id}: {exc}") from exc

        provenance = [
            {
                "pass_index": p.pass_index,
                "selected_rule_id": p.selected_rule_id,
                "changed": p.changed,
                "final_status": p.final_status,
                "stop_reason": p.stop_reason,
            }
            for p in result.provenance
        ]
        for p in result.provenance:
            if p.selected_rule_id and p.selected_rule_id not in RULE_ALLOWLIST:
                unauthorized_rules.append(f"{cell_id}:{p.selected_rule_id}")
            if p.changed and p.selected_rule_id:
                applied_rules.append(p.selected_rule_id)
                rule_applied[p.selected_rule_id] += 1
        changed = any(p.changed for p in result.provenance)
        rolled_back = bool(result.rolled_back)
        if changed and not rolled_back:
            transformed = True
            healer_decision = "transformed"
            repaired_source = result.output_source
            after_sha = _hash_text(repaired_source)
            matched_rule = next(
                (p.selected_rule_id for p in result.provenance if p.changed),
                matched_rule,
            )
            try:
                post_outcome, _ps, post_details = classify_math16_response(
                    repaired_source,
                    frozen_params=frozen_params,
                    audit_oracle_payload=task["oracle_payload"],
                    task=task,
                )
                post_classifier_outcome = post_outcome
                post_mapped = classify_outcome_to_v3(
                    post_outcome, post_details, api_policy=api_policy
                )
            except Exception as exc:  # noqa: BLE001
                evaluator_crash.append(cell_id)
                raise RuntimeError(f"post-healer evaluator crash on {cell_id}: {exc}") from exc
            post_status = post_mapped["final_status"]
            post_layer = post_mapped["primary_failure_layer"]
            if post_status == "PASSED":
                healer_outcome = "rescue_to_pass"
            else:
                healer_outcome = "changed_partial_progress"
        elif rolled_back:
            healer_decision = "transformed"
            transformed = True
            healer_outcome = "rollback"
            after_sha = before_sha
        else:
            healer_decision = "no_op"
            healer_outcome = "no_op"

        rescued = healer_outcome == "rescue_to_pass"
        repaired_still_fail = healer_outcome == "changed_partial_progress"
        no_op = healer_outcome == "no_op"
        regressed = False
        repaired = transformed and healer_outcome in {
            "rescue_to_pass",
            "changed_partial_progress",
            "rollback",
            "regression",
        }

        primary_row = primary_exec[cell_id]
        primary_disposition = disposition_label(primary_row)
        new_disposition = disposition_label(
            {
                "rescued": rescued,
                "repaired_still_fail": repaired_still_fail,
                "no_op": no_op,
                "regressed": regressed,
                "healer_outcome": healer_outcome,
            }
        )
        same_as_primary = (
            primary_row.get("healer_outcome") == healer_outcome
            and bool(primary_row.get("rescued")) == rescued
            and bool(primary_row.get("no_op")) == no_op
            and primary_row.get("post_healer_status") == post_status
            and list(primary_row.get("applied_rules") or []) == applied_rules
        )
        noop_to_rescue = bool(primary_row.get("no_op")) and rescued

        exec_row = {
            "cell_id": cell_id,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "seed": seed,
            "healer_ran": True,
            "matched_rule": matched_rule,
            "applied_rules": applied_rules,
            "healer_decision": healer_decision,
            "healer_outcome": healer_outcome,
            "before_source_sha256": before_sha,
            "after_source_sha256": after_sha,
            "stop_reasons": [p.get("stop_reason") for p in provenance],
            "post_healer_status": post_status,
            "post_classifier_outcome": post_classifier_outcome,
            "post_healer_primary_failure_layer": post_layer,
            "rescued": rescued,
            "repaired_still_fail": repaired_still_fail,
            "no_op": no_op,
            "regressed": regressed,
            "rolled_back": rolled_back,
            "transformed": transformed,
            "repaired": repaired,
            "provenance": provenance,
            "raw_response_sha256": raw_sha,
            "primary_disposition": primary_disposition,
            "primary_healer_outcome": primary_row.get("healer_outcome"),
            "primary_post_healer_status": primary_row.get("post_healer_status"),
            "primary_applied_rules": list(primary_row.get("applied_rules") or []),
            "primary_stop_reasons": list(primary_row.get("stop_reasons") or []),
            "new_disposition": new_disposition,
            "same_as_primary": same_as_primary,
            "noop_to_rescue": noop_to_rescue,
            "llm_calls": 0,
        }
        execution_records.append(exec_row)
        replay_records.append(exec_row)

        if repaired_source is not None:
            transformed_artifacts.append(
                {
                    "cell_id": cell_id,
                    "before_source_sha256": before_sha,
                    "after_source_sha256": after_sha,
                    "applied_rules": applied_rules,
                    "artifact_storage": "sha_only_not_committed_py",
                }
            )

        print(
            f"[replay {len(execution_records)}/10] {cell_id} "
            f"primary={primary_disposition} -> {new_disposition} "
            f"post={post_status} same={same_as_primary}"
        )

    if len(execution_records) != EXPECTED_ELIGIBLE:
        raise RuntimeError(f"replayed != 10: {len(execution_records)}")
    replay_ids = [r["cell_id"] for r in execution_records]
    if len(set(replay_ids)) != 10:
        raise RuntimeError("duplicate replay cell_ids")
    missing = sorted(set(eligible_ids) - set(replay_ids))
    if missing:
        raise RuntimeError(f"missing replay cells: {missing}")

    # Build corrected-chain 320 ledger: copy primary for non-replayed; overlay 10.
    replay_by_id = {r["cell_id"]: r for r in execution_records}
    healer_results: list[dict[str, Any]] = []
    post_scoring: list[dict[str, Any]] = []
    condition_stats: dict[str, dict[str, Any]] = defaultdict(empty_bucket)
    family_stats: dict[str, dict[str, Any]] = defaultdict(empty_bucket)
    task_stats: dict[str, dict[str, Any]] = defaultdict(empty_bucket)

    counts = {
        "baseline_pass": 0,
        "baseline_fail": 0,
        "fail_eligible": 0,
        "fail_noneligible": 0,
        "fail_undetermined": 0,
        "repaired": 0,
        "rescued": 0,
        "repaired_still_fail": 0,
        "abstained": 0,
        "regression": 0,
        "preserved_pass": 0,
        "unchanged_fail": 0,
        "no_op": 0,
        "healer_ran": 0,
        "post_healer_pass": 0,
    }

    for cell in plan:
        cell_id = cell["cell_id"]
        primary_h = primary_healer[cell_id]
        primary_p = primary_post[cell_id]
        base_status = primary_h["baseline_final_status"]
        is_pass = base_status == "PASSED"
        family = primary_h["family"]
        cond = primary_h["condition"]
        tid = primary_h["task_id"]

        if cell_id in eligible_set:
            if is_pass:
                baseline_pass_executed.append(cell_id)
                raise RuntimeError(f"PASS in eligible set: {cell_id}")
            rr = replay_by_id[cell_id]
            healer_ran = True
            counts["healer_ran"] += 1
            counts["fail_eligible"] += 1
            post_status = rr["post_healer_status"]
            healer_outcome = rr["healer_outcome"]
            rescued = rr["rescued"]
            repaired_still_fail = rr["repaired_still_fail"]
            no_op = rr["no_op"]
            regressed = rr["regressed"]
            abstained = False
            preserved_pass = False
            repaired = rr["repaired"]
            healer_row = {
                **{k: primary_h[k] for k in primary_h if k not in {
                    "healer_ran",
                    "healer_decision",
                    "matched_rule",
                    "applied_rules",
                    "transformed",
                    "repaired",
                    "rolled_back",
                    "before_source_sha256",
                    "after_source_sha256",
                    "repaired_source_sha256",
                    "healer_outcome",
                    "post_healer_status",
                    "post_healer_primary_failure_layer",
                    "post_classifier_outcome",
                    "rescued",
                    "regressed",
                    "preserved_pass",
                    "abstained",
                    "repaired_still_fail",
                    "no_op",
                    "provenance",
                }},
                "healer_ran": True,
                "healer_decision": rr["healer_decision"],
                "matched_rule": rr["matched_rule"],
                "applied_rules": rr["applied_rules"],
                "transformed": rr["transformed"],
                "repaired": repaired,
                "rolled_back": rr["rolled_back"],
                "before_source_sha256": rr["before_source_sha256"],
                "after_source_sha256": rr["after_source_sha256"],
                "repaired_source_sha256": (
                    rr["after_source_sha256"] if rr["transformed"] and not rr["rolled_back"] else None
                ),
                "healer_outcome": healer_outcome,
                "post_healer_status": post_status,
                "post_healer_primary_failure_layer": rr["post_healer_primary_failure_layer"],
                "post_classifier_outcome": rr["post_classifier_outcome"],
                "rescued": rescued,
                "regressed": regressed,
                "preserved_pass": False,
                "abstained": False,
                "repaired_still_fail": repaired_still_fail,
                "no_op": no_op,
                "provenance": rr["provenance"],
                "chain_kind": "posthoc_corrected_replay",
                "llm_calls": 0,
                "qwen9b": False,
            }
            post_row = {
                **{k: primary_p[k] for k in primary_p if k not in {
                    "post_healer_final_status",
                    "post_healer_primary_failure_layer",
                    "post_classifier_outcome",
                    "rescued",
                    "regressed",
                    "healer_outcome",
                }},
                "post_healer_final_status": post_status,
                "post_healer_primary_failure_layer": rr["post_healer_primary_failure_layer"],
                "post_classifier_outcome": rr["post_classifier_outcome"],
                "rescued": rescued,
                "regressed": regressed,
                "healer_outcome": healer_outcome,
                "chain_kind": "posthoc_corrected_replay",
                "llm_calls": 0,
            }
        else:
            # Non-eligible / baseline PASS: inherit primary; never call runner.
            if primary_h.get("healer_ran"):
                if not is_pass:
                    noneligible_executed.append(cell_id)
                else:
                    baseline_pass_executed.append(cell_id)
                raise RuntimeError(f"primary illegally ran healer: {cell_id}")
            healer_row = {**primary_h, "chain_kind": "inherited_from_primary"}
            post_row = {**primary_p, "chain_kind": "inherited_from_primary"}
            post_status = healer_row["post_healer_status"]
            healer_outcome = healer_row["healer_outcome"]
            rescued = bool(healer_row.get("rescued"))
            repaired_still_fail = bool(healer_row.get("repaired_still_fail"))
            no_op = bool(healer_row.get("no_op"))
            regressed = bool(healer_row.get("regressed"))
            abstained = bool(healer_row.get("abstained"))
            preserved_pass = bool(healer_row.get("preserved_pass"))
            repaired = bool(healer_row.get("repaired"))
            healer_ran = False
            if is_pass:
                counts["baseline_pass"] += 1
            else:
                counts["baseline_fail"] += 1
                counts["fail_noneligible"] += 1

        if cell_id in eligible_set:
            counts["baseline_fail"] += 1

        if post_status == "PASSED":
            counts["post_healer_pass"] += 1
        if repaired:
            counts["repaired"] += 1
        if rescued:
            counts["rescued"] += 1
        if repaired_still_fail:
            counts["repaired_still_fail"] += 1
        if abstained:
            counts["abstained"] += 1
        if no_op:
            counts["no_op"] += 1
        if regressed:
            counts["regression"] += 1
        if preserved_pass:
            counts["preserved_pass"] += 1
        if healer_outcome == "unchanged_fail":
            counts["unchanged_fail"] += 1

        for store, key in (
            (condition_stats, cond),
            (family_stats, family),
            (task_stats, tid),
        ):
            b = store[key]
            b["total"] += 1
            if is_pass:
                b["baseline_passed"] += 1
            else:
                b["baseline_failed"] += 1
            if post_status == "PASSED":
                b["post_healer_passed"] += 1
            else:
                b["post_healer_failed"] += 1
            if cell_id in eligible_set:
                b["eligible"] += 1
            if repaired:
                b["repaired"] += 1
            if rescued:
                b["rescued"] += 1
            if repaired_still_fail:
                b["repaired_still_fail"] += 1
            if regressed:
                b["regressed"] += 1
            if abstained:
                b["abstained"] += 1
            if preserved_pass:
                b["preserved_pass"] += 1
            if healer_outcome == "unchanged_fail":
                b["unchanged_fail"] += 1
            if no_op:
                b["no_op"] = b.get("no_op", 0) + 1

        healer_results.append(healer_row)
        post_scoring.append(post_row)

    # Integrity gates
    if counts["baseline_pass"] != 78:
        raise RuntimeError(f"baseline_pass != 78: {counts['baseline_pass']}")
    if counts["baseline_fail"] != 242:
        raise RuntimeError(f"baseline_fail != 242: {counts['baseline_fail']}")
    if counts["fail_eligible"] != 10:
        raise RuntimeError(f"fail_eligible != 10: {counts['fail_eligible']}")
    if counts["fail_noneligible"] != 232:
        raise RuntimeError(f"fail_noneligible != 232: {counts['fail_noneligible']}")
    if counts["healer_ran"] != 10:
        raise RuntimeError(f"healer_ran != 10: {counts['healer_ran']}")
    if counts["abstained"] != 232:
        raise RuntimeError(f"abstained != 232: {counts['abstained']}")
    if counts["preserved_pass"] != 78:
        raise RuntimeError(f"preserved_pass != 78: {counts['preserved_pass']}")
    if raw_sha_mismatch:
        raise RuntimeError(f"raw SHA mismatch: {raw_sha_mismatch}")
    if unauthorized_rules:
        raise RuntimeError(f"unauthorized rules: {unauthorized_rules}")
    if evaluator_crash:
        raise RuntimeError(f"evaluator crash: {evaluator_crash}")
    if protocol_errors:
        raise RuntimeError(f"protocol errors: {protocol_errors}")
    if noneligible_executed or baseline_pass_executed or illegal_run_attempts:
        raise RuntimeError("illegal execution detected")

    # Primary ledger must remain untouched on disk.
    primary_overall_now = json.loads(
        (PRIMARY_DIR / "overall_summary.json").read_text(encoding="utf-8")
    )
    if primary_overall_now["post_healer_pass_fraction"] != "83/320":
        raise RuntimeError("PRIMARY_OVERWRITTEN")
    if primary_overall_now["counts"]["rescued"] != 5:
        raise RuntimeError("PRIMARY_RESCUED_OVERWRITTEN")

    diffs = [r for r in execution_records if not r["same_as_primary"]]
    comparison = {
        "primary_healer_id": PRIMARY_HEALER_ID,
        "corrected_chain_healer_id": HEALER_ID,
        "primary_post_healer_pass_fraction": "83/320",
        "corrected_post_healer_pass_fraction": f"{counts['post_healer_pass']}/320",
        "primary_rescued": PRIMARY_RESCUED,
        "corrected_rescued": counts["rescued"],
        "replayed": 10,
        "same_as_primary": sum(1 for r in execution_records if r["same_as_primary"]),
        "changed_vs_primary": len(diffs),
        "noop_to_rescue_cells": [r["cell_id"] for r in execution_records if r["noop_to_rescue"]],
        "per_cell": [
            {
                "cell_id": r["cell_id"],
                "primary_disposition": r["primary_disposition"],
                "new_disposition": r["new_disposition"],
                "primary_healer_outcome": r["primary_healer_outcome"],
                "new_healer_outcome": r["healer_outcome"],
                "primary_post_healer_status": r["primary_post_healer_status"],
                "new_post_healer_status": r["post_healer_status"],
                "primary_applied_rules": r["primary_applied_rules"],
                "new_applied_rules": r["applied_rules"],
                "primary_stop_reasons": r["primary_stop_reasons"],
                "new_stop_reasons": r["stop_reasons"],
                "before_source_sha256": r["before_source_sha256"],
                "after_source_sha256": r["after_source_sha256"],
                "same_as_primary": r["same_as_primary"],
                "noop_to_rescue": r["noop_to_rescue"],
                "explanation": (
                    "Math16 revalidation false-loop fix retained wrap; formal PASS"
                    if r["cell_id"] == CELL_A_RADICAL and r["noop_to_rescue"]
                    else (
                        "false-loop rollback removed; unwrap retained but safe_eval NameError remains FAIL"
                        if r["cell_id"] == CELL_B_Q09 and not r["same_as_primary"]
                        else ("identical to primary" if r["same_as_primary"] else "UNEXPLAINED_DRIFT")
                    )
                ),
            }
            for r in execution_records
        ],
    }
    unexplained = [
        c for c in comparison["per_cell"] if c["explanation"] == "UNEXPLAINED_DRIFT"
    ]
    if unexplained:
        raise RuntimeError(
            "UNEXPLAINED_DRIFT_IN_NON_FOCUS_CELLS: "
            + json.dumps(unexplained, ensure_ascii=False)
        )

    audit = {
        "audit_id": f"{HEALER_ID}_completeness",
        "passed": True,
        "replayed": 10,
        "duplicate": [],
        "missing": [],
        "noneligible_executed": [],
        "baseline_pass_executed": [],
        "unauthorized_rule": unauthorized_rules,
        "evaluator_crash": evaluator_crash,
        "protocol_error": protocol_errors,
        "raw_sha_mismatch": raw_sha_mismatch,
        "model_calls": 0,
        "llm_calls": 0,
        "qwen9b": False,
        "primary_overwritten": False,
        "primary_post_healer_pass_fraction_preserved": "83/320",
        "nature": "posthoc_corrected_chain",
        "preregistered_primary": False,
    }

    overall = {
        "healer_id": HEALER_ID,
        "chain_kind": "posthoc_corrected_chain",
        "preregistered_primary": False,
        "primary_healer_id": PRIMARY_HEALER_ID,
        "baseline_evaluation_id": "math16_pilot02_qwen4b_evaluation_v4_r001",
        "pins": pins,
        "counts": counts,
        "rule_applied_counts": dict(rule_applied),
        "baseline_pass_fraction": "78/320",
        "post_healer_pass_fraction": f"{counts['post_healer_pass']}/320",
        "uplift_abs": counts["post_healer_pass"] - 78,
        "primary_post_healer_pass_fraction": "83/320",
        "primary_rescued": PRIMARY_RESCUED,
        "ledger": {
            "baseline_pass": counts["baseline_pass"],
            "fail_eligible": counts["fail_eligible"],
            "fail_noneligible": counts["fail_noneligible"],
            "repaired": counts["repaired"],
            "rescued": counts["rescued"],
            "repaired_still_fail": counts["repaired_still_fail"],
            "no_op": counts["no_op"],
            "abstained": counts["abstained"],
            "regression": counts["regression"],
            "preserved_pass": counts["preserved_pass"],
            "unchanged_fail": counts["unchanged_fail"],
        },
        "created_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "llm_calls": 0,
        "ab3": True,
        "healer": True,
        "qwen9b": False,
        "verdicts": [
            "QWEN4B_POSTHOC_HEALER_REPLAY_COMPLETED",
            "QWEN4B_CORRECTED_CHAIN_RESULTS_FROZEN",
            "QWEN4B_PRIMARY_RESULT_PRESERVED",
            "QWEN4B_QWEN9B_COMPARISON_READY",
        ],
    }

    def summarize(store: dict[str, dict[str, Any]], order: list[str]) -> list[dict[str, Any]]:
        out = []
        for key in order:
            v = store[key]
            item = {"key": key, **v}
            if key in CONDITION_DISPLAY:
                item["display"] = CONDITION_DISPLAY[key]
            if key in FAMILY_DISPLAY:
                item["display"] = FAMILY_DISPLAY[key]
            item["baseline_pass_fraction"] = f"{v['baseline_passed']}/{v['total']}"
            item["post_healer_pass_fraction"] = f"{v['post_healer_passed']}/{v['total']}"
            out.append(item)
        return out

    condition_summary = summarize(
        condition_stats, ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]
    )
    family_summary = summarize(
        family_stats, ["integer", "polynomial", "radical", "fraction"]
    )
    task_summary = summarize(task_stats, sorted(task_stats.keys()))

    report_lines = [
        "# Qwen4B Pilot-02 Post-hoc Corrected-Chain Healer Replay",
        "",
        "```text",
        "QWEN4B_POSTHOC_HEALER_REPLAY_COMPLETED",
        "QWEN4B_CORRECTED_CHAIN_RESULTS_FROZEN",
        "QWEN4B_PRIMARY_RESULT_PRESERVED",
        "QWEN4B_QWEN9B_COMPARISON_READY",
        "```",
        "",
        "**Nature:** post-hoc corrected-chain — **not** preregistered primary.",
        "",
        f"- Primary post-Healer (preserved): **83/320** (rescued={PRIMARY_RESCUED})",
        f"- Corrected-chain post-Healer: **{counts['post_healer_pass']}/320**",
        f"- Replayed eligible only: **10**",
        f"- Noneligible executed: **0**",
        f"- Rescued / repaired-still-fail / no-op / regression: "
        f"**{counts['rescued']} / {counts['repaired_still_fail']} / {counts['no_op']} / {counts['regression']}**",
        f"- Healer runner SHA: `{EXPECTED_HEALER_RUNNER_HASH}`",
        f"- Protocol SHA: `{EXPECTED_HEALER_PROTOCOL_HASH}`",
        f"- LLM calls: **0**",
        "",
        "## Primary vs corrected-chain (eligible 10)",
        "",
        "| Cell | Primary | Corrected | Same |",
        "| :--- | :--- | :--- | :---: |",
    ]
    for c in comparison["per_cell"]:
        report_lines.append(
            f"| `{c['cell_id']}` | {c['primary_disposition']} | "
            f"{c['new_disposition']} | {str(c['same_as_primary']).lower()} |"
        )
    report_lines += [
        "",
        "## Condition",
        "",
        "| Condition | Baseline | Post-Healer | Eligible | Rescued |",
        "| :--- | ---: | ---: | ---: | ---: |",
    ]
    for row in condition_summary:
        report_lines.append(
            f"| {row.get('display', row['key'])} | {row['baseline_pass_fraction']} | "
            f"{row['post_healer_pass_fraction']} | {row['eligible']} | {row['rescued']} |"
        )
    report_lines += [
        "",
        "## Family",
        "",
        "| Family | Baseline | Post-Healer | Eligible | Rescued |",
        "| :--- | ---: | ---: | ---: | ---: |",
    ]
    for row in family_summary:
        report_lines.append(
            f"| {row.get('display', row['key'])} | {row['baseline_pass_fraction']} | "
            f"{row['post_healer_pass_fraction']} | {row['eligible']} | {row['rescued']} |"
        )
    report_lines.append("")

    if dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "counts": counts,
                    "comparison_changed": comparison["changed_vs_primary"],
                },
                indent=2,
            )
        )
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT_DIR / "eligible_replay_records.jsonl", replay_records)
    write_jsonl(OUT_DIR / "eligible_execution_records.jsonl", execution_records)
    write_jsonl(OUT_DIR / "healer_results.jsonl", healer_results)
    write_jsonl(OUT_DIR / "post_healer_scoring.jsonl", post_scoring)
    write_json(OUT_DIR / "transformed_artifacts_index.json", transformed_artifacts)
    write_json(OUT_DIR / "overall_summary.json", overall)
    write_json(OUT_DIR / "post_healer_summary.json", overall)
    write_json(OUT_DIR / "condition_summary.json", condition_summary)
    write_json(OUT_DIR / "family_summary.json", family_summary)
    write_json(OUT_DIR / "task_summary.json", task_summary)
    write_json(OUT_DIR / "completeness_audit.json", audit)
    write_json(OUT_DIR / "primary_vs_corrected_chain_comparison.json", comparison)
    write_json(
        OUT_DIR / "execution_manifest.json",
        {
            "healer_id": HEALER_ID,
            "chain_kind": "posthoc_corrected_chain",
            "preregistered_primary": False,
            "primary_healer_id": PRIMARY_HEALER_ID,
            "primary_result_preserved": True,
            "primary_post_healer_pass_fraction": "83/320",
            "eligible_cell_ids": eligible_ids,
            "replayed": 10,
            "noneligible_executed": 0,
            "baseline_pass_executed": 0,
            "healer_rule_pack_source": str(
                HEALER_RUNNER_PATH.relative_to(ROOT)
            ).replace("\\", "/"),
            "healer_runner_sha256": EXPECTED_HEALER_RUNNER_HASH,
            "healer_protocol_sha256": EXPECTED_HEALER_PROTOCOL_HASH,
            "healer_allowlist": list(RULE_ALLOWLIST),
            "healer_max_passes": HEALER_MAX_PASSES,
            "external_eligibility_prefilter": True,
            "eligibility_source": "primary_frozen_eligibility_inventory",
            "expected_fail_eligible": EXPECTED_ELIGIBLE,
            "expected_fail_noneligible": EXPECTED_NONELIGIBLE,
            "evaluator_source": str(EVALUATOR_PATH.relative_to(ROOT)).replace("\\", "/"),
            "evaluator_hash": EXPECTED_EVAL_HASH,
            "taxonomy_hash": EXPECTED_TAX_HASH,
            "corpus_sha_closure": EXPECTED_CLOSURE,
            "llm_calls": 0,
            "qwen9b": False,
            "baseline_overwritten": False,
            "raw_modified": False,
            "primary_overwritten": False,
            "noneligible_direct_run": False,
        },
    )
    (OUT_DIR / "report.md").write_text(
        "\n".join(report_lines).rstrip() + "\n", encoding="utf-8", newline="\n"
    )

    # Soft assertion: expected corrected-chain is 84/320 if only radical flips.
    print(
        json.dumps(
            {
                "counts": counts,
                "rule_applied": dict(rule_applied),
                "changed_vs_primary": comparison["changed_vs_primary"],
                "noop_to_rescue": comparison["noop_to_rescue_cells"],
                "primary_preserved": "83/320",
            },
            indent=2,
        )
    )
    print(f"Wrote {OUT_DIR}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    if args.preflight_only:
        pins = verify_pins()
        print(json.dumps({"preflight": "PASS", "pins": pins}, indent=2))
        return 0
    return run(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
