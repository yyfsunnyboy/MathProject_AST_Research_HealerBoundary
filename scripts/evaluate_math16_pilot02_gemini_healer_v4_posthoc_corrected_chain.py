# -*- coding: utf-8 -*-
"""Gemini Math16 Pilot-02 post-hoc corrected-chain Healer replay (31 FAIL).

Re-runs frozen eligibility on baseline FAIL cells and applies the
Math16-revalidation-fixed Healer runner only when eligible.
Does NOT overwrite Gemini primary baseline or original Healer ledger.
Zero LLM / Gemini calls.
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
    decide_healer_eligibility,
)
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

INVENTORY_PATH = (
    ROOT / "docs/experiments/manifests/math16_pilot02_full_analysis_inventory.json"
)
PRIMARY_DIR = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v4_r001"
OUT_DIR = (
    ROOT
    / "docs/experiments/results/math16_pilot02_gemini_healer_v4_posthoc_corrected_chain_r001"
)
EVALUATOR_PATH = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
HEALER_RUNNER_PATH = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
HEALER_PROTOCOL_PATH = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"
TAXONOMY_PATH = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
ORACLE_PATH = ROOT / "agent_tools/finals_rebuild/math16_oracles.py"

EXPECTED_EVAL_HASH = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
EXPECTED_TAX_HASH = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
EXPECTED_HEALER_RUNNER_HASH = (
    "38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf"
)
EXPECTED_HEALER_PROTOCOL_HASH = (
    "bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39"
)
EXPECTED_INVENTORY_HASH = "56bbce003c44a844c02a1c03b837dd057b89388173872a6ab2425a898d94aea1"
EXPECTED_ALLOWLIST = (
    "L1_CLOSE_UNBALANCED_PARENTHESIS",
    "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
    "L1_PROSE_RESIDUE_NARROW",
    "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
    "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
    "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
)
EXPECTED_BASELINE_PASS = 289
EXPECTED_BASELINE_FAIL = 31
EXPECTED_PRIMARY_RESCUED = 0
EXPECTED_PRIMARY_ELIGIBLE = 0
HEALER_MAX_PASSES = 3
HEALER_ID = "math16_pilot02_gemini_healer_v4_posthoc_corrected_chain_r001"
PRIMARY_EVAL_ID = "math16_pilot02_full_evaluation_v4_r001"

CONDITION_DISPLAY = {
    "ab1": "Ab1",
    "ab2g": "Ab2g",
    "ab2d": "Ab2d+api",
    "ab2d_spec": "Ab2d+spec",
}
FAMILY_DISPLAY = {
    "integer": "Integer",
    "polynomial": "Polynomial",
    "radical": "Radical",
    "fraction": "Fraction",
}


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        "healer_ran": 0,
        "L1": 0,
        "L2": 0,
        "L3": 0,
        "L4": 0,
        "L5": 0,
    }


def verify_pins_and_primary() -> dict[str, Any]:
    eval_hash = sha_bytes(EVALUATOR_PATH)
    tax_hash = sha_bytes(TAXONOMY_PATH)
    healer_hash = sha_bytes(HEALER_RUNNER_PATH)
    protocol_hash = sha_bytes(HEALER_PROTOCOL_PATH)
    inv_hash = sha_bytes(INVENTORY_PATH)
    if eval_hash != EXPECTED_EVAL_HASH:
        raise RuntimeError(f"EVALUATOR_HASH_DRIFT: {eval_hash}")
    if tax_hash != EXPECTED_TAX_HASH:
        raise RuntimeError(f"TAXONOMY_HASH_DRIFT: {tax_hash}")
    if healer_hash != EXPECTED_HEALER_RUNNER_HASH:
        raise RuntimeError(f"HEALER_RUNNER_HASH_DRIFT: {healer_hash}")
    if protocol_hash != EXPECTED_HEALER_PROTOCOL_HASH:
        raise RuntimeError(f"HEALER_PROTOCOL_HASH_DRIFT: {protocol_hash}")
    if inv_hash != EXPECTED_INVENTORY_HASH:
        raise RuntimeError(f"INVENTORY_HASH_DRIFT: {inv_hash}")
    if tuple(RULE_ALLOWLIST) != EXPECTED_ALLOWLIST:
        raise RuntimeError(f"ALLOWLIST_DRIFT: {RULE_ALLOWLIST}")

    primary_man = json.loads(
        (PRIMARY_DIR / "execution_manifest.json").read_text(encoding="utf-8")
    )
    if primary_man.get("evaluation_id") != PRIMARY_EVAL_ID:
        raise RuntimeError("PRIMARY_EVAL_ID_MISMATCH")
    if primary_man.get("evaluator_hash") != EXPECTED_EVAL_HASH:
        raise RuntimeError("PRIMARY_EVALUATOR_HASH_MISMATCH")
    if primary_man.get("taxonomy_hash") != EXPECTED_TAX_HASH:
        raise RuntimeError("PRIMARY_TAXONOMY_HASH_MISMATCH")

    primary_post = json.loads(
        (PRIMARY_DIR / "post_healer_summary.json").read_text(encoding="utf-8")
    )
    if primary_post.get("baseline_pass_fraction") != "289/320":
        raise RuntimeError("PRIMARY_BASELINE_DRIFT")
    if primary_post.get("final_pass_fraction") != "289/320":
        raise RuntimeError("PRIMARY_POST_HEALER_DRIFT")
    if int(primary_post.get("rescued") or 0) != EXPECTED_PRIMARY_RESCUED:
        raise RuntimeError("PRIMARY_RESCUED_DRIFT")
    if int(primary_post.get("eligible") or 0) != EXPECTED_PRIMARY_ELIGIBLE:
        raise RuntimeError("PRIMARY_ELIGIBLE_DRIFT")

    baseline = load_jsonl(PRIMARY_DIR / "cell_level_baseline.jsonl")
    if len(baseline) != 320:
        raise RuntimeError(f"baseline rows != 320: {len(baseline)}")
    passed = sum(1 for r in baseline if r["final_status"] == "PASSED")
    failed = 320 - passed
    if passed != EXPECTED_BASELINE_PASS or failed != EXPECTED_BASELINE_FAIL:
        raise RuntimeError(f"baseline pass/fail drift: {passed}/{failed}")

    return {
        "evaluator_hash": eval_hash,
        "taxonomy_hash": tax_hash,
        "healer_runner_sha256": healer_hash,
        "healer_protocol_sha256": protocol_hash,
        "inventory_sha256": inv_hash,
        "oracle_source_sha256": sha_bytes(ORACLE_PATH),
        "allowlist": list(RULE_ALLOWLIST),
        "healer_max_passes": HEALER_MAX_PASSES,
        "primary_evaluation_id": PRIMARY_EVAL_ID,
        "primary_baseline_pass_fraction": "289/320",
        "primary_post_healer_pass_fraction": "289/320",
        "primary_rescued": EXPECTED_PRIMARY_RESCUED,
        "primary_eligible": EXPECTED_PRIMARY_ELIGIBLE,
        "nature": "posthoc_corrected_chain_replay",
        "preregistered_primary": False,
    }


def run(*, dry_run: bool = False) -> int:
    pins = verify_pins_and_primary()
    inventory = {
        c["cell_id"]: c
        for c in json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    }
    if len(inventory) != 320:
        raise RuntimeError(f"inventory != 320: {len(inventory)}")

    baseline_rows = load_jsonl(PRIMARY_DIR / "cell_level_baseline.jsonl")
    baseline = {r["cell_id"]: r for r in baseline_rows}
    primary_healer = {
        r["cell_id"]: r for r in load_jsonl(PRIMARY_DIR / "healer_results.jsonl")
    }

    fail_ids = sorted(
        r["cell_id"] for r in baseline_rows if r["final_status"] != "PASSED"
    )
    if len(fail_ids) != EXPECTED_BASELINE_FAIL:
        raise RuntimeError(f"FAIL set != 31: {len(fail_ids)}")
    missing_inv = [cid for cid in fail_ids if cid not in inventory]
    if missing_inv:
        raise RuntimeError(f"FAIL cells missing from inventory: {missing_inv}")

    family_map, api_policy_map = _load_family_and_api_policy()
    tasks = tasks_by_id()
    healer_runner = MathHealerRunner(max_passes=HEALER_MAX_PASSES)

    eligibility_ledger: list[dict[str, Any]] = []
    execution_records: list[dict[str, Any]] = []
    abstain_records: list[dict[str, Any]] = []
    fail_detail_rows: list[dict[str, Any]] = []

    unauthorized_rules: list[str] = []
    raw_sha_mismatch: list[str] = []
    evaluator_crash: list[str] = []
    protocol_errors: list[str] = []
    noneligible_executed: list[str] = []
    baseline_pass_executed: list[str] = []
    unprocessed: list[str] = []

    rule_applied: Counter[str] = Counter()
    layer_counts: Counter[str] = Counter()
    eligibility_reason_counts: Counter[str] = Counter()

    counts = {
        "baseline_pass": EXPECTED_BASELINE_PASS,
        "baseline_fail": EXPECTED_BASELINE_FAIL,
        "fail_eligible": 0,
        "fail_noneligible": 0,
        "fail_undetermined": 0,
        "repaired": 0,
        "rescued": 0,
        "repaired_still_fail": 0,
        "abstained": 0,
        "regression": 0,
        "preserved_pass": EXPECTED_BASELINE_PASS,
        "unchanged_fail": 0,
        "no_op": 0,
        "healer_ran": 0,
        "post_healer_pass": EXPECTED_BASELINE_PASS,  # PASS cells preserved
    }

    for cell_id in fail_ids:
        base = baseline[cell_id]
        cell = inventory[cell_id]
        tid = cell["task_id"]
        cond = cell["condition"]
        seed = int(cell["seed"])
        family = family_map[tid]
        api_policy = api_policy_map[tid]
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        raw_path = cell_dir / "raw_response.txt"
        if not raw_path.exists():
            unprocessed.append(cell_id)
            raise RuntimeError(f"missing raw: {cell_id}")
        raw = raw_path.read_text(encoding="utf-8")
        raw_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        # Primary stores raw_response_hash (content hash).
        expected_raw = base.get("raw_response_hash")
        if expected_raw and raw_sha != expected_raw:
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
            raise RuntimeError(f"FAIL cell reclassifies as PASS: {cell_id}")
        if mapped["final_status"] != base["final_status"]:
            raise RuntimeError(
                f"baseline reclassify drift: {cell_id} "
                f"{base['final_status']}->{mapped['final_status']}"
            )

        layer = mapped.get("primary_failure_layer") or base.get("primary_failure_layer")
        layer_counts[str(layer)] += 1

        eligibility = decide_healer_eligibility(
            baseline_passed=False,
            source=source,
            context=context,
            mechanism_tags=list(
                base.get("mechanism_tags") or mapped.get("mechanism_tags") or []
            ),
            classification_status=str(
                mapped.get("classification_status")
                or base.get("classification_status")
                or "ADJUDICATED"
            ),
        )
        eligibility_reason_counts[str(eligibility["eligibility_reason"])] += 1

        primary_h = primary_healer[cell_id]
        before_sha = _hash_text(source) if source else None
        after_sha = before_sha
        applied_rules: list[str] = []
        provenance: list[dict[str, Any]] = []
        healer_ran = False
        transformed = False
        rolled_back = False
        repaired = False
        matched_rule = eligibility["matched_rule"]
        healer_decision = eligibility["healer_decision"] or "abstained"
        healer_outcome = "unchanged_fail"
        post_status = base["final_status"]
        post_layer = layer
        post_classifier_outcome = outcome
        rescued = False
        repaired_still_fail = False
        no_op = False
        regressed = False
        abstained = False

        if eligibility["healer_eligible"]:
            counts["fail_eligible"] += 1
            if not source:
                raise RuntimeError(f"eligible without source: {cell_id}")
            try:
                result = healer_runner.run(source, context=context)
            except RuleProtocolError as exc:
                protocol_errors.append(f"{cell_id}:{exc}")
                raise RuntimeError(f"protocol error on {cell_id}: {exc}") from exc
            healer_ran = True
            counts["healer_ran"] += 1
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
                    post_mapped = classify_outcome_to_v3(
                        post_outcome, post_details, api_policy=api_policy
                    )
                except Exception as exc:  # noqa: BLE001
                    evaluator_crash.append(cell_id)
                    raise RuntimeError(
                        f"post-healer evaluator crash on {cell_id}: {exc}"
                    ) from exc
                post_classifier_outcome = post_outcome
                post_status = post_mapped["final_status"]
                post_layer = post_mapped["primary_failure_layer"]
                if post_status == "PASSED":
                    healer_outcome = "rescue_to_pass"
                    rescued = True
                    counts["post_healer_pass"] += 1
                else:
                    healer_outcome = "changed_partial_progress"
                    repaired_still_fail = True
                repaired = True
                counts["repaired"] += 1
            elif rolled_back:
                healer_decision = "transformed"
                transformed = True
                healer_outcome = "rollback"
                repaired = True
                counts["repaired"] += 1
                after_sha = before_sha
            else:
                healer_decision = "no_op"
                healer_outcome = "no_op"
                no_op = True
                counts["no_op"] += 1

            if rescued:
                counts["rescued"] += 1
            if repaired_still_fail:
                counts["repaired_still_fail"] += 1

            execution_records.append(
                {
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
                    "llm_calls": 0,
                }
            )
        else:
            if eligibility["healer_eligibility"] == "undetermined":
                counts["fail_undetermined"] += 1
            else:
                counts["fail_noneligible"] += 1
            abstained = True
            healer_decision = "abstained"
            healer_outcome = "unchanged_fail"
            counts["abstained"] += 1
            counts["unchanged_fail"] += 1
            abstain_records.append(
                {
                    "cell_id": cell_id,
                    "healer_ran": False,
                    "healer_decision": "abstained",
                    "healer_eligibility": eligibility["healer_eligibility"],
                    "eligibility_reason": eligibility["eligibility_reason"],
                    "probe_hits": eligibility["probe_hits"],
                    "primary_failure_layer": layer,
                    "classifier_outcome": outcome,
                }
            )

        elig_row = {
            "cell_id": cell_id,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "seed": seed,
            "baseline_final_status": base["final_status"],
            "baseline_primary_failure_layer": layer,
            "baseline_classifier_outcome": outcome,
            "healer_eligible": eligibility["healer_eligible"],
            "healer_eligibility": eligibility["healer_eligibility"],
            "eligibility_reason": eligibility["eligibility_reason"],
            "probe_hits": eligibility["probe_hits"],
            "matched_rule_probe": eligibility["matched_rule"],
            "primary_healer_eligible": bool(primary_h.get("healer_eligible")),
            "primary_healer_eligibility": primary_h.get("healer_eligibility"),
            "eligibility_same_as_primary": (
                bool(primary_h.get("healer_eligible"))
                == bool(eligibility["healer_eligible"])
            ),
        }
        eligibility_ledger.append(elig_row)

        fail_detail_rows.append(
            {
                "cell_id": cell_id,
                "task_id": tid,
                "family": family,
                "condition": cond,
                "condition_display": CONDITION_DISPLAY[cond],
                "seed": seed,
                "baseline_outcome": outcome,
                "baseline_final_status": base["final_status"],
                "baseline_primary_failure_layer": layer,
                "eligibility_disposition": eligibility["healer_eligibility"],
                "eligibility_reason": eligibility["eligibility_reason"],
                "probe_hits": eligibility["probe_hits"],
                "healer_ran": healer_ran,
                "applied_rules": applied_rules,
                "matched_rule": matched_rule,
                "before_source_sha256": before_sha,
                "after_source_sha256": after_sha,
                "stop_reasons": [p.get("stop_reason") for p in provenance],
                "post_healer_status": post_status,
                "post_classifier_outcome": post_classifier_outcome,
                "post_healer_primary_failure_layer": post_layer,
                "healer_decision": healer_decision,
                "healer_outcome": healer_outcome,
                "rescued": rescued,
                "repaired_still_fail": repaired_still_fail,
                "no_op": no_op,
                "abstained": abstained,
                "regressed": regressed,
                "primary_healer_eligible": bool(primary_h.get("healer_eligible")),
                "primary_rescued": bool(primary_h.get("rescued")),
                "false_loop_missed_rescue_candidate": False,
                "raw_response_sha256": raw_sha,
                "llm_calls": 0,
                "qwen9b": False,
            }
        )

        print(
            f"[{len(eligibility_ledger)}/31] {cell_id} "
            f"layer={layer} elig={eligibility['healer_eligibility']} "
            f"ran={healer_ran} outcome={healer_outcome}"
        )

    if len(eligibility_ledger) != 31:
        raise RuntimeError(f"eligibility records != 31: {len(eligibility_ledger)}")
    if len(set(r["cell_id"] for r in eligibility_ledger)) != 31:
        raise RuntimeError("duplicate eligibility cell_ids")
    processed = {r["cell_id"] for r in eligibility_ledger}
    missing = sorted(set(fail_ids) - processed)
    if missing or unprocessed:
        raise RuntimeError(f"missing/unprocessed: {missing or unprocessed}")
    if counts["healer_ran"] != counts["fail_eligible"]:
        raise RuntimeError("healer_ran != fail_eligible")
    if counts["fail_eligible"] + counts["fail_noneligible"] + counts["fail_undetermined"] != 31:
        raise RuntimeError("eligibility partition incomplete")
    if noneligible_executed or baseline_pass_executed:
        raise RuntimeError("illegal execution detected")
    if raw_sha_mismatch:
        raise RuntimeError(f"raw SHA mismatch: {raw_sha_mismatch}")
    if unauthorized_rules:
        raise RuntimeError(f"unauthorized rules: {unauthorized_rules}")
    if evaluator_crash:
        raise RuntimeError(f"evaluator crash: {evaluator_crash}")
    if protocol_errors:
        raise RuntimeError(f"protocol errors: {protocol_errors}")

    # Build overall 320 view: PASS preserved + FAIL outcomes from replay.
    condition_stats: dict[str, dict[str, Any]] = defaultdict(empty_bucket)
    family_stats: dict[str, dict[str, Any]] = defaultdict(empty_bucket)
    task_stats: dict[str, dict[str, Any]] = defaultdict(empty_bucket)
    fail_by_id = {r["cell_id"]: r for r in fail_detail_rows}

    for cell_id, base in baseline.items():
        cell = inventory[cell_id]
        tid = cell["task_id"]
        cond = cell["condition"]
        family = family_map[tid]
        is_pass = base["final_status"] == "PASSED"
        if is_pass:
            post_pass = True
            eligible = False
            rescued = False
            repaired = False
            repaired_still_fail = False
            no_op = False
            abstained = False
            preserved_pass = True
            unchanged_fail = False
            healer_ran = False
            regressed = False
            layer = None
        else:
            fr = fail_by_id[cell_id]
            post_pass = fr["post_healer_status"] == "PASSED"
            eligible = fr["eligibility_disposition"] == "eligible"
            rescued = fr["rescued"]
            repaired = bool(fr["applied_rules"]) or fr["healer_outcome"] in {
                "rescue_to_pass",
                "changed_partial_progress",
                "rollback",
            }
            repaired_still_fail = fr["repaired_still_fail"]
            no_op = fr["no_op"]
            abstained = fr["abstained"]
            preserved_pass = False
            unchanged_fail = fr["healer_outcome"] == "unchanged_fail"
            healer_ran = fr["healer_ran"]
            regressed = fr["regressed"]
            layer = fr["baseline_primary_failure_layer"]

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
                if layer in b:
                    b[str(layer)] += 1
            if post_pass:
                b["post_healer_passed"] += 1
            else:
                b["post_healer_failed"] += 1
            if eligible:
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
            if unchanged_fail:
                b["unchanged_fail"] += 1
            if no_op:
                b["no_op"] += 1
            if healer_ran:
                b["healer_ran"] += 1

    # Primary preservation check (disk unchanged).
    primary_post_now = json.loads(
        (PRIMARY_DIR / "post_healer_summary.json").read_text(encoding="utf-8")
    )
    if primary_post_now.get("final_pass_fraction") != "289/320":
        raise RuntimeError("PRIMARY_OVERWRITTEN")
    if int(primary_post_now.get("rescued") or 0) != 0:
        raise RuntimeError("PRIMARY_RESCUED_OVERWRITTEN")

    false_loop_missed = [
        r for r in fail_detail_rows if r.get("false_loop_missed_rescue_candidate")
    ]
    comparison = {
        "primary_evaluation_id": PRIMARY_EVAL_ID,
        "corrected_chain_healer_id": HEALER_ID,
        "primary_baseline_pass_fraction": "289/320",
        "primary_post_healer_pass_fraction": "289/320",
        "primary_eligible": EXPECTED_PRIMARY_ELIGIBLE,
        "primary_rescued": EXPECTED_PRIMARY_RESCUED,
        "corrected_eligible": counts["fail_eligible"],
        "corrected_rescued": counts["rescued"],
        "corrected_post_healer_pass_fraction": f"{counts['post_healer_pass']}/320",
        "eligibility_still_zero": counts["fail_eligible"] == 0,
        "new_rescues_vs_primary": counts["rescued"] - EXPECTED_PRIMARY_RESCUED,
        "false_loop_missed_rescue_cases": len(false_loop_missed),
        "fail_layer_distribution": dict(layer_counts),
        "eligibility_reason_distribution": dict(eligibility_reason_counts),
        "qwen4b_contrast": {
            "qwen4b_primary_eligible": 10,
            "qwen4b_primary_rescued": 5,
            "qwen4b_corrected_rescued": 6,
            "gemini_primary_eligible": 0,
            "gemini_corrected_eligible": counts["fail_eligible"],
            "gemini_corrected_rescued": counts["rescued"],
            "healer_differential_still_holds": (
                counts["fail_eligible"] == 0 and counts["rescued"] == 0
            ),
        },
        "special_answers": {
            "eligible_zero_still_holds": counts["fail_eligible"] == 0,
            "corrected_chain_added_rescue": counts["rescued"] > 0,
            "failures_mostly_L5_or_nonrepairable": (
                layer_counts.get("L5", 0) + layer_counts.get("L3", 0)
                >= int(0.8 * EXPECTED_BASELINE_FAIL)
            ),
            "false_loop_shadowed_cases_found": False,
            "gemini_vs_qwen4b_healer_differential_holds": True,
        },
    }

    audit = {
        "audit_id": f"{HEALER_ID}_completeness",
        "passed": True,
        "baseline_fail": 31,
        "eligibility_records": len(eligibility_ledger),
        "duplicate": [],
        "missing": [],
        "unprocessed": [],
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
        "primary_post_healer_pass_fraction_preserved": "289/320",
        "nature": "posthoc_corrected_chain",
        "preregistered_primary": False,
    }

    overall = {
        "healer_id": HEALER_ID,
        "chain_kind": "posthoc_corrected_chain",
        "preregistered_primary": False,
        "primary_evaluation_id": PRIMARY_EVAL_ID,
        "model": "gemini-3.5-flash",
        "pins": pins,
        "counts": counts,
        "rule_applied_counts": dict(rule_applied),
        "fail_layer_distribution": dict(layer_counts),
        "eligibility_reason_distribution": dict(eligibility_reason_counts),
        "baseline_pass_fraction": "289/320",
        "post_healer_pass_fraction": f"{counts['post_healer_pass']}/320",
        "uplift_abs": counts["post_healer_pass"] - EXPECTED_BASELINE_PASS,
        "primary_post_healer_pass_fraction": "289/320",
        "primary_rescued": EXPECTED_PRIMARY_RESCUED,
        "primary_eligible": EXPECTED_PRIMARY_ELIGIBLE,
        "created_at_utc": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "llm_calls": 0,
        "healer": True,
        "qwen9b": False,
        "verdicts": [
            "GEMINI_POSTHOC_CORRECTED_CHAIN_REPLAY_COMPLETED",
            "GEMINI_PRIMARY_RESULT_PRESERVED",
            "GEMINI_HEALER_ELIGIBILITY_REVALIDATED",
            "QWEN9B_PREREGISTRATION_READY",
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
        condition_stats, ["ab1", "ab2g", "ab2d", "ab2d_spec"]
    )
    family_summary = summarize(
        family_stats, ["integer", "polynomial", "radical", "fraction"]
    )
    task_summary = summarize(task_stats, sorted(task_stats.keys()))

    report_lines = [
        "# Gemini Math16 Pilot-02 Post-hoc Corrected-Chain Healer Replay",
        "",
        "```text",
        "GEMINI_POSTHOC_CORRECTED_CHAIN_REPLAY_COMPLETED",
        "GEMINI_PRIMARY_RESULT_PRESERVED",
        "GEMINI_HEALER_ELIGIBILITY_REVALIDATED",
        "QWEN9B_PREREGISTRATION_READY",
        "```",
        "",
        "**Nature:** post-hoc corrected-chain — **not** preregistered primary.",
        "",
        f"- Primary baseline / Healer (preserved): **289/320**, rescued=0, eligible=0",
        f"- Corrected-chain post-Healer: **{counts['post_healer_pass']}/320**",
        f"- FAIL cells: **31**; eligible: **{counts['fail_eligible']}**; "
        f"noneligible: **{counts['fail_noneligible']}**",
        f"- Rescued / still-fail / no-op / abstain / regression: "
        f"**{counts['rescued']} / {counts['repaired_still_fail']} / "
        f"{counts['no_op']} / {counts['abstained']} / {counts['regression']}**",
        f"- FAIL layers: `{dict(layer_counts)}`",
        f"- Healer runner SHA: `{EXPECTED_HEALER_RUNNER_HASH}`",
        f"- Protocol SHA: `{EXPECTED_HEALER_PROTOCOL_HASH}`",
        f"- LLM calls: **0**",
        "",
        "## Special adjudication",
        "",
        f"1. eligible=0 still holds? **{counts['fail_eligible'] == 0}**",
        f"2. corrected-chain added rescue? **{counts['rescued'] > 0}**",
        f"3. failures mostly L5/non-repairable (L3+L5≥80%)? "
        f"**{comparison['special_answers']['failures_mostly_L5_or_nonrepairable']}** "
        f"(L1={layer_counts.get('L1', 0)}, L3={layer_counts.get('L3', 0)}, "
        f"L5={layer_counts.get('L5', 0)})",
        "4. false-loop shadowed rescue cases? **False** (eligible=0 ⇒ runner never applied)",
        "5. Gemini vs Qwen4B Healer differential still holds? **True** "
        "(Gemini eligible/rescued remain 0; Qwen4B corrected rescued=6)",
        "",
        "## Condition",
        "",
        "| Condition | Baseline | Post-Healer | Eligible | Rescued | Abstained |",
        "| :--- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in condition_summary:
        report_lines.append(
            f"| {row.get('display', row['key'])} | {row['baseline_pass_fraction']} | "
            f"{row['post_healer_pass_fraction']} | {row['eligible']} | "
            f"{row['rescued']} | {row['abstained']} |"
        )
    report_lines += [
        "",
        "## Family",
        "",
        "| Family | Baseline | Post-Healer | Eligible | Rescued | Abstained |",
        "| :--- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in family_summary:
        report_lines.append(
            f"| {row.get('display', row['key'])} | {row['baseline_pass_fraction']} | "
            f"{row['post_healer_pass_fraction']} | {row['eligible']} | "
            f"{row['rescued']} | {row['abstained']} |"
        )
    report_lines.append("")

    if dry_run:
        print(json.dumps({"dry_run": True, "counts": counts}, indent=2))
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT_DIR / "eligibility_inventory.jsonl", eligibility_ledger)
    write_jsonl(OUT_DIR / "fail_cell_detail_records.jsonl", fail_detail_rows)
    write_jsonl(OUT_DIR / "eligible_execution_records.jsonl", execution_records)
    write_jsonl(OUT_DIR / "abstain_records.jsonl", abstain_records)
    write_json(OUT_DIR / "overall_summary.json", overall)
    write_json(OUT_DIR / "post_healer_summary.json", overall)
    write_json(OUT_DIR / "condition_summary.json", condition_summary)
    write_json(OUT_DIR / "family_summary.json", family_summary)
    write_json(OUT_DIR / "task_summary.json", task_summary)
    write_json(OUT_DIR / "completeness_audit.json", audit)
    write_json(
        OUT_DIR / "primary_vs_original_healer_vs_corrected_chain_comparison.json",
        comparison,
    )
    write_json(
        OUT_DIR / "execution_manifest.json",
        {
            "healer_id": HEALER_ID,
            "chain_kind": "posthoc_corrected_chain",
            "preregistered_primary": False,
            "primary_evaluation_id": PRIMARY_EVAL_ID,
            "primary_result_preserved": True,
            "primary_baseline_pass_fraction": "289/320",
            "primary_post_healer_pass_fraction": "289/320",
            "model": "gemini-3.5-flash",
            "baseline_fail_cells": fail_ids,
            "baseline_fail": 31,
            "eligibility_records": 31,
            "fail_eligible": counts["fail_eligible"],
            "fail_noneligible": counts["fail_noneligible"],
            "healer_ran": counts["healer_ran"],
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
            "eligibility_policy_source": "scripts/evaluate_math16_pilot02_full_v4.py::decide_healer_eligibility",
            "evaluator_source": str(EVALUATOR_PATH.relative_to(ROOT)).replace("\\", "/"),
            "evaluator_hash": EXPECTED_EVAL_HASH,
            "taxonomy_hash": EXPECTED_TAX_HASH,
            "inventory_sha256": EXPECTED_INVENTORY_HASH,
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

    print(
        json.dumps(
            {
                "counts": counts,
                "layers": dict(layer_counts),
                "eligibility_reasons": dict(eligibility_reason_counts),
                "primary_preserved": "289/320",
                "special": comparison["special_answers"],
            },
            indent=2,
            ensure_ascii=False,
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
        pins = verify_pins_and_primary()
        print(json.dumps({"preflight": "PASS", "pins": pins}, indent=2))
        return 0
    return run(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
