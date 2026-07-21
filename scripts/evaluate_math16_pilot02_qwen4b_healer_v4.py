# -*- coding: utf-8 -*-
"""Apply frozen Ab3/Healer to Qwen4B Pilot-02 baseline FAIL cells (offline).

Uses MathHealerRunner + RULE_ALLOWLIST unchanged. Post-Healer acceptance via
the same evaluator v4 (classify_math16_response + classify_outcome_to_v3).

Does NOT overwrite baseline scoring. Does NOT modify raw. Zero LLM calls.
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

PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
EVIDENCE_FREEZE = (
    ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_generation_evidence_freeze_v1.json"
)
BASELINE_DIR = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001"
OUT_DIR = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001"
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
HEALER_MAX_PASSES = 3
HEALER_ID = "math16_pilot02_qwen4b_healer_v4_r001"

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

    sm = json.loads((BASELINE_DIR / "scoring_manifest.json").read_text(encoding="utf-8"))
    if sm["corpus_sha_closure"] != EXPECTED_CLOSURE:
        raise RuntimeError("BASELINE_MANIFEST_CORPUS_MISMATCH")
    if sm["evaluator_hash"] != EXPECTED_EVAL_HASH:
        raise RuntimeError("BASELINE_MANIFEST_EVAL_MISMATCH")
    if sm["taxonomy_hash"] != EXPECTED_TAX_HASH:
        raise RuntimeError("BASELINE_MANIFEST_TAX_MISMATCH")

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
    }


def load_baseline() -> dict[str, dict[str, Any]]:
    rows = [
        json.loads(l)
        for l in (BASELINE_DIR / "cell_level_baseline.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if l.strip()
    ]
    if len(rows) != 320:
        raise RuntimeError(f"baseline rows != 320: {len(rows)}")
    index = {r["cell_id"]: r for r in rows}
    if len(index) != 320:
        raise RuntimeError("duplicate baseline cell_ids")
    passed = sum(1 for r in rows if r["final_status"] == "PASSED")
    failed = 320 - passed
    if passed != 78 or failed != 242:
        raise RuntimeError(f"baseline pass/fail drift: {passed}/{failed}")
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


def run(*, dry_run: bool = False) -> int:
    pins = verify_pins()
    baseline = load_baseline()
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    family_map, api_policy_map = _load_family_and_api_policy()
    tasks = tasks_by_id()
    healer_runner = MathHealerRunner(max_passes=HEALER_MAX_PASSES)

    eligibility_inventory: list[dict[str, Any]] = []  # FAIL cells only (242)
    execution_records: list[dict[str, Any]] = []  # eligible run() only (10)
    abstain_records: list[dict[str, Any]] = []  # FAIL noneligible (232)
    healer_results: list[dict[str, Any]] = []  # all 320 ledger
    post_scoring: list[dict[str, Any]] = []
    transformed_artifacts: list[dict[str, Any]] = []

    unauthorized_rules: list[str] = []
    raw_sha_mismatch: list[str] = []
    evaluator_crash: list[str] = []
    protocol_errors: list[str] = []
    baseline_drift: list[dict[str, Any]] = []
    illegal_run_attempts: list[str] = []

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
    rule_applied: Counter[str] = Counter()
    fail_eligibility_done = 0

    for idx, cell in enumerate(plan):
        cell_id = cell["cell_id"]
        base = baseline[cell_id]
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
        frozen = frozen_for_prompt(task)
        frozen_params = frozen["oracle_payload"]

        try:
            outcome, source, details = classify_math16_response(
                raw,
                frozen_params=frozen_params,
                audit_oracle_payload=task["oracle_payload"],
                task=task,
            )
            mapped = classify_outcome_to_v3(outcome, details, api_policy=api_policy)
        except Exception as exc:  # noqa: BLE001 — record crash, continue audit
            evaluator_crash.append(cell_id)
            raise RuntimeError(f"evaluator crash on {cell_id}: {exc}") from exc

        if mapped["final_status"] != base["final_status"]:
            baseline_drift.append(
                {
                    "cell_id": cell_id,
                    "baseline": base["final_status"],
                    "reclassify": mapped["final_status"],
                }
            )

        is_pass = base["final_status"] == "PASSED"
        if is_pass:
            counts["baseline_pass"] += 1
        else:
            counts["baseline_fail"] += 1
            fail_eligibility_done += 1

        context = {"task": task, "frozen": frozen_params}
        eligibility = decide_healer_eligibility(
            baseline_passed=is_pass,
            source=source,
            context=context,
            mechanism_tags=list(base.get("mechanism_tags") or mapped["mechanism_tags"] or []),
            classification_status=str(
                mapped.get("classification_status")
                or base.get("classification_status")
                or "ADJUDICATED"
            ),
        )

        healer_ran = False
        transformed = False
        repaired_source = None
        before_sha = _hash_text(source) if source else None
        after_sha = before_sha
        rolled_back = False
        matched_rule = eligibility["matched_rule"]
        applied_rules: list[str] = []
        healer_decision = eligibility["healer_decision"]
        abstain_reason = None if eligibility["healer_eligible"] else eligibility["eligibility_reason"]
        post_status = base["final_status"]
        post_layer = base.get("primary_failure_layer")
        post_classifier_outcome = base.get("classifier_outcome") or outcome
        post_mapped = mapped
        healer_outcome = "preserved_pass" if is_pass else "unchanged_fail"
        provenance: list[dict[str, Any]] = []

        if eligibility["healer_eligible"]:
            if is_pass:
                illegal_run_attempts.append(f"pass_eligible:{cell_id}")
                raise RuntimeError(f"PASS cell marked eligible: {cell_id}")
            assert source is not None
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
                post_status = post_mapped["final_status"]
                post_layer = post_mapped["primary_failure_layer"]
                if is_pass and post_status != "PASSED":
                    healer_outcome = "regression"
                elif (not is_pass) and post_status == "PASSED":
                    healer_outcome = "rescue_to_pass"
                else:
                    healer_outcome = "changed_partial_progress"
            elif rolled_back:
                healer_decision = "transformed"
                transformed = True
                healer_outcome = "rollback"
                after_sha = before_sha
            else:
                # Eligible run completed but no accepted transform (e.g. loop fallback).
                healer_decision = "no_op"
                healer_outcome = "no_op"
                abstain_reason = None
        elif not is_pass:
            # FAIL noneligible: record abstain; do NOT call run().
            healer_decision = "abstained"
            abstain_reason = eligibility["eligibility_reason"]
            healer_outcome = "unchanged_fail"
        else:
            # Baseline PASS: never call run().
            healer_decision = "no_trigger"
            healer_outcome = "preserved_pass"
            abstain_reason = None

        rescued = healer_outcome == "rescue_to_pass"
        regressed = healer_outcome == "regression"
        preserved_pass = healer_outcome == "preserved_pass"
        abstained = healer_decision == "abstained"
        no_op = healer_outcome == "no_op"
        repaired = transformed and healer_outcome in {
            "rescue_to_pass",
            "changed_partial_progress",
            "rollback",
            "regression",
        }
        repaired_still_fail = healer_outcome == "changed_partial_progress"

        if post_status == "PASSED":
            counts["post_healer_pass"] += 1
        if not is_pass:
            if eligibility["healer_eligibility"] == "eligible":
                counts["fail_eligible"] += 1
            elif eligibility["healer_eligibility"] == "undetermined":
                counts["fail_undetermined"] += 1
            else:
                counts["fail_noneligible"] += 1
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
            if eligibility["healer_eligible"]:
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

        elig_row = {
            "cell_id": cell_id,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "seed": seed,
            "baseline_final_status": base["final_status"],
            "baseline_primary_failure_layer": base.get("primary_failure_layer"),
            "healer_eligible": eligibility["healer_eligible"],
            "healer_eligibility": eligibility["healer_eligibility"],
            "eligibility_reason": eligibility["eligibility_reason"],
            "probe_hits": eligibility["probe_hits"],
            "matched_rule_probe": eligibility["matched_rule"],
        }
        if not is_pass:
            eligibility_inventory.append(elig_row)
            if eligibility["healer_eligible"]:
                execution_records.append(
                    {
                        "cell_id": cell_id,
                        "healer_ran": True,
                        "matched_rule": matched_rule,
                        "applied_rules": applied_rules,
                        "healer_decision": healer_decision,
                        "healer_outcome": healer_outcome,
                        "before_source_sha256": before_sha,
                        "after_source_sha256": after_sha,
                        "stop_reasons": [p.get("stop_reason") for p in provenance],
                        "post_healer_status": post_status,
                        "rescued": rescued,
                        "repaired_still_fail": repaired_still_fail,
                        "no_op": no_op,
                        "regressed": regressed,
                    }
                )
            else:
                abstain_records.append(
                    {
                        "cell_id": cell_id,
                        "healer_ran": False,
                        "healer_decision": "abstained",
                        "abstain_reason": abstain_reason,
                        "eligibility_reason": eligibility["eligibility_reason"],
                        "probe_hits": eligibility["probe_hits"],
                    }
                )

        healer_row = {
            "cell_id": cell_id,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "condition_display": CONDITION_DISPLAY[cond],
            "seed": seed,
            "baseline_final_status": base["final_status"],
            "baseline_primary_failure_layer": base.get("primary_failure_layer"),
            "baseline_classifier_outcome": base.get("classifier_outcome"),
            "healer_ran": healer_ran,
            "healer_eligible": eligibility["healer_eligible"],
            "healer_eligibility": eligibility["healer_eligibility"],
            "eligibility_reason": eligibility["eligibility_reason"],
            "abstain_reason": abstain_reason,
            "healer_decision": healer_decision,
            "matched_rule": matched_rule,
            "applied_rules": applied_rules,
            "probe_hits": eligibility["probe_hits"],
            "transformed": transformed,
            "repaired": repaired,
            "rolled_back": rolled_back,
            "before_source_sha256": before_sha,
            "after_source_sha256": after_sha,
            "repaired_source_sha256": after_sha if transformed and repaired_source else None,
            "healer_outcome": healer_outcome,
            "post_healer_status": post_status,
            "post_healer_primary_failure_layer": post_layer,
            "post_classifier_outcome": post_classifier_outcome,
            "rescued": rescued,
            "regressed": regressed,
            "preserved_pass": preserved_pass,
            "abstained": abstained,
            "repaired_still_fail": repaired_still_fail,
            "no_op": no_op,
            "allowlist": list(RULE_ALLOWLIST),
            "max_passes": HEALER_MAX_PASSES,
            "provenance": provenance,
            "raw_response_sha256": raw_sha,
            "llm_calls": 0,
            "qwen9b": False,
        }
        healer_results.append(healer_row)

        post_row = {
            "cell_id": cell_id,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "condition_display": CONDITION_DISPLAY[cond],
            "seed": seed,
            "evaluation_revision": "v4_r001",
            "evaluator_hash": EXPECTED_EVAL_HASH,
            "taxonomy_hash": EXPECTED_TAX_HASH,
            "oracle_source_sha256": sha_bytes(ORACLE_PATH),
            "baseline_final_status": base["final_status"],
            "post_healer_final_status": post_status,
            "post_healer_primary_failure_layer": post_layer,
            "post_classifier_outcome": post_classifier_outcome,
            "gates": post_mapped.get("gates") if transformed and repaired_source else base.get("gates"),
            "mechanism_tags": (
                post_mapped.get("mechanism_tags")
                if transformed and repaired_source
                else base.get("mechanism_tags")
            ),
            "rescued": rescued,
            "regressed": regressed,
            "healer_outcome": healer_outcome,
            "llm_calls": 0,
        }
        post_scoring.append(post_row)

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
            f"[{idx + 1}/320] {cell_id} base={base['final_status']} "
            f"elig={eligibility['healer_eligibility']} "
            f"dec={healer_decision}/{healer_outcome}"
        )

    if baseline_drift:
        raise RuntimeError(f"BASELINE_RECLASSIFY_DRIFT n={len(baseline_drift)} sample={baseline_drift[:3]}")
    if fail_eligibility_done != 242:
        raise RuntimeError(f"FAIL eligibility incomplete: {fail_eligibility_done}")
    if counts["baseline_pass"] != 78:
        raise RuntimeError("baseline PASS != 78")
    if len(eligibility_inventory) != 242:
        raise RuntimeError(f"eligibility inventory != 242: {len(eligibility_inventory)}")
    if counts["fail_eligible"] != EXPECTED_ELIGIBLE:
        raise RuntimeError(
            f"ELIGIBLE_COUNT_BLOCKER: expected {EXPECTED_ELIGIBLE} got {counts['fail_eligible']}"
        )
    if counts["fail_noneligible"] != EXPECTED_NONELIGIBLE:
        raise RuntimeError(
            f"NONELIGIBLE_COUNT_BLOCKER: expected {EXPECTED_NONELIGIBLE} "
            f"got {counts['fail_noneligible']}"
        )
    if counts["fail_undetermined"] != 0:
        raise RuntimeError(f"undetermined FAIL cells: {counts['fail_undetermined']}")
    if counts["healer_ran"] != EXPECTED_ELIGIBLE:
        raise RuntimeError(f"healer_ran != {EXPECTED_ELIGIBLE}: {counts['healer_ran']}")
    if len(execution_records) != EXPECTED_ELIGIBLE:
        raise RuntimeError(f"execution_records != 10: {len(execution_records)}")
    if len(abstain_records) != EXPECTED_NONELIGIBLE:
        raise RuntimeError(f"abstain_records != 232: {len(abstain_records)}")
    if len(healer_results) != 320 or len(post_scoring) != 320:
        raise RuntimeError("incomplete 320 ledger")
    if any(r["healer_ran"] for r in healer_results if r["baseline_final_status"] == "PASSED"):
        raise RuntimeError("Healer ran on baseline PASS")
    if any(
        r["healer_ran"]
        for r in healer_results
        if (not r["healer_eligible"]) and r["baseline_final_status"] != "PASSED"
    ):
        raise RuntimeError("Healer ran on noneligible FAIL")
    if raw_sha_mismatch:
        raise RuntimeError(f"raw SHA mismatch n={len(raw_sha_mismatch)}")
    if unauthorized_rules:
        raise RuntimeError(f"unauthorized rules: {unauthorized_rules}")
    if evaluator_crash:
        raise RuntimeError(f"evaluator crashes: {evaluator_crash}")
    if protocol_errors:
        raise RuntimeError(f"protocol errors: {protocol_errors}")
    if illegal_run_attempts:
        raise RuntimeError(f"illegal run attempts: {illegal_run_attempts}")

    ids = [r["cell_id"] for r in healer_results]
    if len(set(ids)) != 320:
        raise RuntimeError("duplicate healer cell_ids")
    plan_ids = [c["cell_id"] for c in plan]
    if ids != plan_ids:
        raise RuntimeError("healer order/plan mismatch")
    elig_ids = [r["cell_id"] for r in eligibility_inventory]
    if len(set(elig_ids)) != 242:
        raise RuntimeError("duplicate eligibility cell_ids")

    audit = {
        "audit_id": f"{HEALER_ID}_completeness",
        "passed": True,
        "cell_count": 320,
        "baseline_pass": 78,
        "baseline_fail": 242,
        "fail_eligibility_records": len(eligibility_inventory),
        "fail_eligible": counts["fail_eligible"],
        "fail_noneligible": counts["fail_noneligible"],
        "eligible_execution_records": len(execution_records),
        "abstain_records": len(abstain_records),
        "healer_ran": counts["healer_ran"],
        "duplicate": [],
        "missing": [],
        "unprocessed": [],
        "unauthorized_rule": unauthorized_rules,
        "evaluator_crash": evaluator_crash,
        "protocol_error": protocol_errors,
        "raw_sha_mismatch": raw_sha_mismatch,
        "baseline_reclassify_drift": baseline_drift,
        "illegal_run_on_pass_or_noneligible": illegal_run_attempts,
        "llm_calls": 0,
        "qwen9b": False,
        "baseline_overwritten": False,
        "raw_modified": False,
        "external_eligibility_prefilter": True,
        "noneligible_direct_run": False,
    }

    overall = {
        "healer_id": HEALER_ID,
        "baseline_evaluation_id": "math16_pilot02_qwen4b_evaluation_v4_r001",
        "pins": pins,
        "counts": counts,
        "rule_applied_counts": dict(rule_applied),
        "baseline_pass_fraction": "78/320",
        "post_healer_pass_fraction": f"{counts['post_healer_pass']}/320",
        "uplift_abs": counts["post_healer_pass"] - 78,
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
            "QWEN4B_FROZEN_HEALER_EXECUTION_COMPLETED",
            "QWEN4B_HEALER_COMPLETENESS_AUDIT_PASSED",
            "QWEN4B_POST_HEALER_RESULTS_FROZEN",
            "QWEN4B_PRIMARY_HEALER_PIPELINE_COMPLETED",
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
        "# Qwen4B Pilot-02 Frozen Healer v4_r001",
        "",
        "```text",
        "QWEN4B_FROZEN_HEALER_EXECUTION_COMPLETED",
        "QWEN4B_HEALER_COMPLETENESS_AUDIT_PASSED",
        "QWEN4B_POST_HEALER_RESULTS_FROZEN",
        "QWEN4B_PRIMARY_HEALER_PIPELINE_COMPLETED",
        "```",
        "",
        "- External eligibility pre-filter: **retained** (noneligible never call `run()`)",
        f"- Baseline PASS: **78/320**",
        f"- Post-Healer PASS: **{counts['post_healer_pass']}/320**",
        f"- FAIL eligible / noneligible: **{counts['fail_eligible']} / {counts['fail_noneligible']}**",
        f"- Healer ran: **{counts['healer_ran']}**",
        f"- Rescued: **{counts['rescued']}**",
        f"- Repaired-still-fail: **{counts['repaired_still_fail']}**",
        f"- Eligible no-op: **{counts['no_op']}**",
        f"- Abstained (noneligible): **{counts['abstained']}**",
        f"- Regression: **{counts['regression']}**",
        f"- Rule applied: `{dict(rule_applied)}`",
        f"- Corpus SHA: `{EXPECTED_CLOSURE}`",
        f"- Evaluator SHA: `{EXPECTED_EVAL_HASH}`",
        f"- Healer runner SHA: `{EXPECTED_HEALER_RUNNER_HASH}`",
        f"- Healer protocol SHA: `{EXPECTED_HEALER_PROTOCOL_HASH}`",
        f"- Allowlist: `{', '.join(RULE_ALLOWLIST)}`",
        f"- LLM calls: **0**",
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
        print(json.dumps({"dry_run": True, "counts": counts}, indent=2))
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT_DIR / "eligibility_inventory.jsonl", eligibility_inventory)
    write_jsonl(OUT_DIR / "eligible_execution_records.jsonl", execution_records)
    write_jsonl(OUT_DIR / "abstain_records.jsonl", abstain_records)
    write_jsonl(OUT_DIR / "healer_results.jsonl", healer_results)
    write_jsonl(OUT_DIR / "post_healer_scoring.jsonl", post_scoring)
    write_json(OUT_DIR / "transformed_artifacts_index.json", transformed_artifacts)
    write_json(OUT_DIR / "overall_summary.json", overall)
    write_json(OUT_DIR / "post_healer_summary.json", overall)
    write_json(OUT_DIR / "condition_summary.json", condition_summary)
    write_json(OUT_DIR / "family_summary.json", family_summary)
    write_json(OUT_DIR / "task_summary.json", task_summary)
    write_json(OUT_DIR / "completeness_audit.json", audit)
    write_json(
        OUT_DIR / "execution_manifest.json",
        {
            "healer_id": HEALER_ID,
            "baseline_evaluation_id": "math16_pilot02_qwen4b_evaluation_v4_r001",
            "healer_rule_pack_source": str(
                HEALER_RUNNER_PATH.relative_to(ROOT)
            ).replace("\\", "/"),
            "healer_runner_sha256": EXPECTED_HEALER_RUNNER_HASH,
            "healer_protocol_sha256": EXPECTED_HEALER_PROTOCOL_HASH,
            "healer_allowlist": list(RULE_ALLOWLIST),
            "healer_max_passes": HEALER_MAX_PASSES,
            "external_eligibility_prefilter": True,
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
            "noneligible_direct_run": False,
        },
    )
    (OUT_DIR / "report.md").write_text(
        "\n".join(report_lines).rstrip() + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({"counts": counts, "rule_applied": dict(rule_applied)}, indent=2))
    print(f"Wrote {OUT_DIR}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    if args.preflight_only:
        pins = verify_pins()
        baseline = load_baseline()
        print(
            json.dumps(
                {
                    "preflight": "PASS",
                    "pins": pins,
                    "baseline_pass": sum(
                        1 for r in baseline.values() if r["final_status"] == "PASSED"
                    ),
                    "baseline_fail": sum(
                        1 for r in baseline.values() if r["final_status"] != "PASSED"
                    ),
                },
                indent=2,
            )
        )
        return 0
    return run(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
