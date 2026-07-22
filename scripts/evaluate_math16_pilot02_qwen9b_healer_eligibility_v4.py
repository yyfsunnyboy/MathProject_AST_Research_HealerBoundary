# -*- coding: utf-8 -*-
"""Freeze external Healer eligibility for Qwen9B Pilot-02 baseline FAIL cells.

Offline only. Uses frozen decide_healer_eligibility() unchanged.
Does NOT execute Healer transforms. Does NOT modify raw / scores / rules.
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

from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _hash_file,
    _load_family_and_api_policy,
    decide_healer_eligibility,
)
from agent_tools.finals_rebuild.extraction import extract_code  # noqa: E402
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json"
EVIDENCE_FREEZE = (
    ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_generation_evidence_freeze_v1.json"
)
BASELINE_DIR = ROOT / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001"
CORPUS_ROOT = ROOT / "docs/experiments/results/math16_pilot02_qwen9b"
OUT_DIR = ROOT / "docs/experiments/results/math16_pilot02_qwen9b_healer_eligibility_v4_r001"
EVALUATOR_PATH = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
HEALER_RUNNER_PATH = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_runner.py"
HEALER_PROTOCOL_PATH = ROOT / "agent_tools/finals_rebuild/ce115_research_healer_protocol.py"
TAXONOMY_PATH = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"

EXPECTED_HEAD = "4b923fe768a7248e964965d47d3f2327d5dbc6d6"
EXPECTED_CLOSURE = "dedac60aceb5d285a86d3b5cc35ce8064a317c2b52ecc66a673f48632fb6cccf"
EXPECTED_FP = "f45f79238bbf9400729fd00dbfaf4e33a7a7716cb9f81d4095a1fd1d52e0da5b"
EXPECTED_DIGEST = "6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7"
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
EXPECTED_FAIL = 219
EXPECTED_PASS = 101
RUN_ID = "math16_pilot02_qwen9b_healer_eligibility_v4_r001"

# Frozen decide_healer_eligibility() reasons → ledger disposition labels.
# Mapping only; policy logic remains in evaluate_math16_pilot02_full_v4.py.
DISPOSITION_BY_REASON = {
    "No frozen allowlist rule triggered.": "noneligible_no_rule_triggered",
    "No extractable candidate source for frozen healer.": "abstain_no_extractable_source",
    "Ambiguous entry point; frozen healer abstains.": "abstain_ambiguous_entry_point",
    "Pending review; healer abstains.": "pending_review",
}
ALLOWED_DISPOSITIONS = {
    "eligible",
    "noneligible_no_rule_triggered",
    "abstain_no_extractable_source",
    "abstain_ambiguous_entry_point",
    "pending_review",
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
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def map_disposition(eligibility: dict[str, Any]) -> str:
    if eligibility.get("healer_eligible") is True:
        return "eligible"
    reason = str(eligibility.get("eligibility_reason") or "")
    if reason in DISPOSITION_BY_REASON:
        return DISPOSITION_BY_REASON[reason]
    raise RuntimeError(f"UNMAPPED_ELIGIBILITY_REASON: {reason!r}")


def verify_pins() -> dict[str, Any]:
    freeze = json.loads(EVIDENCE_FREEZE.read_text(encoding="utf-8"))
    if freeze["corpus_sha_closure"] != EXPECTED_CLOSURE:
        raise RuntimeError("corpus SHA closure drift")
    if freeze.get("runtime_config_fingerprint") != EXPECTED_FP:
        raise RuntimeError("runtime fingerprint drift")
    if freeze.get("model_digest") != EXPECTED_DIGEST:
        raise RuntimeError("model digest drift")

    eval_hash = _hash_file(EVALUATOR_PATH)
    tax_hash = _hash_file(TAXONOMY_PATH)
    runner_hash = sha_bytes(HEALER_RUNNER_PATH)
    proto_hash = sha_bytes(HEALER_PROTOCOL_PATH)
    if eval_hash != EXPECTED_EVAL_HASH:
        raise RuntimeError(f"EVALUATOR_HASH_DRIFT: {eval_hash}")
    if tax_hash != EXPECTED_TAX_HASH:
        raise RuntimeError(f"TAXONOMY_HASH_DRIFT: {tax_hash}")
    if runner_hash != EXPECTED_HEALER_RUNNER_HASH:
        raise RuntimeError(f"HEALER_RUNNER_HASH_DRIFT: {runner_hash}")
    if proto_hash != EXPECTED_HEALER_PROTOCOL_HASH:
        raise RuntimeError(f"HEALER_PROTOCOL_HASH_DRIFT: {proto_hash}")

    from agent_tools.finals_rebuild.ce115_research_healer_runner import RULE_ALLOWLIST

    if tuple(RULE_ALLOWLIST) != EXPECTED_ALLOWLIST:
        raise RuntimeError(f"ALLOWLIST_DRIFT: {RULE_ALLOWLIST}")

    self_text = Path(__file__).read_text(encoding="utf-8")
    # Forbid importing/constructing the runner class (string split avoids self-match).
    banned = "MathHealer" + "Runner"
    if banned in self_text:
        raise RuntimeError("eligibility script must not reference " + banned)

    return {
        "corpus_sha_closure": EXPECTED_CLOSURE,
        "evaluator_hash": eval_hash,
        "taxonomy_hash": tax_hash,
        "healer_runner_sha256": runner_hash,
        "healer_protocol_sha256": proto_hash,
        "allowlist": list(RULE_ALLOWLIST),
        "llm_calls": 0,
    }


def slice_summary(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    groups: dict[Any, list] = defaultdict(list)
    for r in rows:
        groups[r[key]].append(r)
    out: dict[str, Any] = {}
    for k, items in sorted(groups.items(), key=lambda x: str(x[0])):
        disp = Counter(i["eligibility_disposition"] for i in items)
        out[str(k)] = {
            "total": len(items),
            "eligible": disp.get("eligible", 0),
            "noneligible_no_rule_triggered": disp.get("noneligible_no_rule_triggered", 0),
            "abstain_no_extractable_source": disp.get("abstain_no_extractable_source", 0),
            "abstain_ambiguous_entry_point": disp.get("abstain_ambiguous_entry_point", 0),
            "pending_review": disp.get("pending_review", 0),
            "disposition_distribution": dict(disp),
        }
    return out


def run_eligibility() -> dict[str, Any]:
    pins = verify_pins()
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    if len(plan) != 320:
        raise RuntimeError("plan not 320")

    baseline_rows = [
        json.loads(l)
        for l in (BASELINE_DIR / "cell_level_baseline.jsonl").read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]
    if len(baseline_rows) != 320:
        raise RuntimeError(f"baseline rows={len(baseline_rows)}")
    baseline = {r["cell_id"]: r for r in baseline_rows}
    if len(baseline) != 320:
        raise RuntimeError("duplicate baseline cell_ids")

    fails = [r for r in baseline_rows if r["final_status"] != "PASSED"]
    passes = [r for r in baseline_rows if r["final_status"] == "PASSED"]
    if len(fails) != EXPECTED_FAIL or len(passes) != EXPECTED_PASS:
        raise RuntimeError(
            f"FAIL/PASS set mismatch: fail={len(fails)} pass={len(passes)} "
            f"expected {EXPECTED_FAIL}/{EXPECTED_PASS}"
        )

    family_map, _api = _load_family_and_api_policy()
    tasks = tasks_by_id()
    plan_by_id = {c["cell_id"]: c for c in plan}

    ledger: list[dict[str, Any]] = []
    raw_sha_mismatch: list[str] = []
    unknown_disposition: list[str] = []
    pass_included: list[str] = []

    for base in sorted(fails, key=lambda r: r["cell_id"]):
        cell_id = base["cell_id"]
        if base["final_status"] == "PASSED":
            pass_included.append(cell_id)
            continue
        cell = plan_by_id[cell_id]
        tid = cell["task_id"]
        cond = cell["condition"]
        seed = int(cell["seed"])
        family = cell.get("family") or family_map[tid]
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        raw_path = cell_dir / "raw_response.txt"
        raw = raw_path.read_text(encoding="utf-8")
        raw_sha = sha_bytes(raw_path)
        if raw_sha != base.get("raw_response_sha256"):
            raw_sha_mismatch.append(cell_id)

        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        frozen_params = frozen["oracle_payload"]

        # Offline extract/classify for source only — not a rescore writeback.
        _outcome, source, details = classify_math16_response(
            raw,
            frozen_params=frozen_params,
            audit_oracle_payload=task["oracle_payload"],
            task=task,
        )
        if not source:
            extracted = extract_code(raw)
            source = extracted.extracted_code or None

        classification_status = str(
            (base.get("evaluator_diagnostics") or {}).get("classification_status")
            or details.get("classification_status")
            or "ADJUDICATED"
        )
        mechanism_tags = list(base.get("mechanism_tags") or [])

        eligibility = decide_healer_eligibility(
            baseline_passed=False,
            source=source,
            context={"task": task, "frozen": frozen_params},
            mechanism_tags=mechanism_tags,
            classification_status=classification_status,
        )
        disposition = map_disposition(eligibility)
        if disposition not in ALLOWED_DISPOSITIONS:
            unknown_disposition.append(f"{cell_id}:{disposition}")
            raise RuntimeError(f"unknown disposition {disposition} for {cell_id}")

        row = {
            "run_id": RUN_ID,
            "cell_id": cell_id,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "seed": seed,
            "baseline_final_status": base["final_status"],
            "baseline_primary_failure_layer": base.get("primary_failure_layer"),
            "baseline_mechanism_tags": mechanism_tags,
            "baseline_classifier_outcome": base.get("classifier_outcome"),
            "raw_response_sha256": raw_sha,
            "raw_artifact_sha256": base.get("raw_artifact_sha256"),
            "extracted_source_present": bool(source and str(source).strip()),
            "probe_hits": eligibility.get("probe_hits") or [],
            "matched_rule_probe": eligibility.get("matched_rule"),
            "eligible_rule_id": eligibility.get("matched_rule")
            if eligibility.get("healer_eligible")
            else None,
            "healer_eligible": eligibility["healer_eligible"],
            "healer_eligibility": eligibility["healer_eligibility"],
            "eligibility_disposition": disposition,
            "eligibility_reason": eligibility["eligibility_reason"],
            "healer_execution": False,
            "rescued": "not_run",
            "regression": "not_run",
            "llm_calls": 0,
            "ab3": False,
            "healer": False,
        }
        ledger.append(row)

    if pass_included:
        raise RuntimeError(f"baseline PASS incorrectly included: {pass_included[:5]}")
    if len(ledger) != EXPECTED_FAIL:
        raise RuntimeError(f"ledger size {len(ledger)} != {EXPECTED_FAIL}")
    if raw_sha_mismatch:
        raise RuntimeError(f"raw SHA mismatch: {raw_sha_mismatch[:5]}")
    if unknown_disposition:
        raise RuntimeError(f"unknown disposition: {unknown_disposition[:5]}")

    ids = [r["cell_id"] for r in ledger]
    dup = [cid for cid, n in Counter(ids).items() if n != 1]
    missing = sorted(set(r["cell_id"] for r in fails) - set(ids))
    unprocessed = missing
    disp_counts = Counter(r["eligibility_disposition"] for r in ledger)
    rule_counts = Counter(
        r["eligible_rule_id"] for r in ledger if r.get("eligible_rule_id")
    )
    layer_counts = Counter(r.get("baseline_primary_failure_layer") for r in ledger)
    mech_counts: Counter[str] = Counter()
    for r in ledger:
        for t in r.get("baseline_mechanism_tags") or []:
            mech_counts[t] += 1

    eligible_rows = [r for r in ledger if r["eligibility_disposition"] == "eligible"]
    abstain_rows = [
        r
        for r in ledger
        if r["eligibility_disposition"]
        in {
            "abstain_no_extractable_source",
            "abstain_ambiguous_entry_point",
            "pending_review",
        }
    ]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT_DIR / "eligibility_ledger.jsonl", ledger)
    write_jsonl(OUT_DIR / "eligibility_inventory.jsonl", ledger)
    write_jsonl(OUT_DIR / "eligible_cells.jsonl", eligible_rows)
    write_jsonl(
        OUT_DIR / "noneligible_and_abstain_cells.jsonl",
        [r for r in ledger if r["eligibility_disposition"] != "eligible"],
    )
    write_jsonl(OUT_DIR / "abstain_cells.jsonl", abstain_rows)

    summary = {
        "run_id": RUN_ID,
        "source_baseline_commit": EXPECTED_HEAD,
        "corpus_sha_closure": EXPECTED_CLOSURE,
        "runtime_config_fingerprint": EXPECTED_FP,
        "model_digest": EXPECTED_DIGEST,
        "model_tag": "qwen3.5:9b",
        "evaluator_hash": pins["evaluator_hash"],
        "taxonomy_hash": pins["taxonomy_hash"],
        "healer_runner_sha256": pins["healer_runner_sha256"],
        "healer_protocol_sha256": pins["healer_protocol_sha256"],
        "eligibility_policy_source": (
            "scripts/evaluate_math16_pilot02_full_v4.py::decide_healer_eligibility"
        ),
        "external_eligibility_prefilter": True,
        "baseline_pass": EXPECTED_PASS,
        "baseline_fail": EXPECTED_FAIL,
        "records": len(ledger),
        "disposition_counts": dict(disp_counts),
        "eligible": disp_counts.get("eligible", 0),
        "noneligible_no_rule_triggered": disp_counts.get("noneligible_no_rule_triggered", 0),
        "abstain_no_extractable_source": disp_counts.get("abstain_no_extractable_source", 0),
        "abstain_ambiguous_entry_point": disp_counts.get("abstain_ambiguous_entry_point", 0),
        "pending_review": disp_counts.get("pending_review", 0),
        "eligible_rule_distribution": dict(rule_counts),
        "layer_distribution": {str(k): v for k, v in layer_counts.items()},
        "mechanism_tags_distribution": dict(mech_counts),
        "healer_execution": False,
        "rescued": "not_run",
        "regression": "not_run",
        "ab3": False,
        "llm_calls": 0,
        "other_model_calls": False,
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    write_json(OUT_DIR / "eligibility_summary.json", summary)
    write_json(OUT_DIR / "condition_summary.json", slice_summary(ledger, "condition"))
    write_json(OUT_DIR / "family_summary.json", slice_summary(ledger, "family"))
    write_json(OUT_DIR / "task_summary.json", slice_summary(ledger, "task_id"))
    write_json(
        OUT_DIR / "layer_summary.json",
        slice_summary(ledger, "baseline_primary_failure_layer"),
    )
    write_json(
        OUT_DIR / "rule_hit_distribution.json",
        {
            "eligible_rule_distribution": dict(rule_counts),
            "probe_hit_counter": dict(
                Counter(h for r in ledger for h in (r.get("probe_hits") or []))
            ),
        },
    )

    audit = {
        "audit": "qwen9b_healer_eligibility_completeness",
        "records": len(ledger),
        "expected": EXPECTED_FAIL,
        "duplicate": dup,
        "missing": missing,
        "unprocessed": unprocessed,
        "unknown_disposition": unknown_disposition,
        "baseline_pass_included": pass_included,
        "raw_sha_mismatch": raw_sha_mismatch,
        "healer_execution": False,
        "math_healer_runner_run_calls": 0,
        "llm_calls": 0,
        "ab3": False,
        "passed": (
            len(ledger) == EXPECTED_FAIL
            and not dup
            and not missing
            and not unprocessed
            and not unknown_disposition
            and not pass_included
            and not raw_sha_mismatch
        ),
    }
    write_json(OUT_DIR / "eligibility_completeness_audit.json", audit)

    manifest = {
        "run_id": RUN_ID,
        "eligibility_only": True,
        "healer_execution": False,
        "external_eligibility_prefilter": True,
        "noneligible_direct_run": False,
        "eligibility_policy_source": summary["eligibility_policy_source"],
        "input_baseline": str(BASELINE_DIR.relative_to(ROOT)).replace("\\", "/"),
        "input_corpus": str(CORPUS_ROOT.relative_to(ROOT)).replace("\\", "/"),
        "corpus_sha_closure": EXPECTED_CLOSURE,
        "evaluator_hash": pins["evaluator_hash"],
        "taxonomy_hash": pins["taxonomy_hash"],
        "healer_runner_sha256": pins["healer_runner_sha256"],
        "healer_protocol_sha256": pins["healer_protocol_sha256"],
        "allowlist": pins["allowlist"],
        "baseline_fail": EXPECTED_FAIL,
        "eligible": summary["eligible"],
        "rescued": "not_run",
        "regression": "not_run",
        "llm_calls": 0,
        "ab3": False,
        "qwen9b": True,
        "created_at_utc": summary["created_at_utc"],
    }
    write_json(OUT_DIR / "eligibility_manifest.json", manifest)

    md = [
        "# Math16 Pilot-02 Qwen 3.5 9B Healer Eligibility v4_r001",
        "",
        f"- Run ID: `{RUN_ID}`",
        "- Policy: `decide_healer_eligibility` (frozen, same as Qwen4B/Gemini)",
        f"- Baseline FAIL: `{EXPECTED_FAIL}`",
        f"- Eligible: `{summary['eligible']}`",
        "- Healer execution: **false**",
        "- LLM calls: `0`",
        "",
        "## Disposition counts",
        json.dumps(dict(disp_counts), ensure_ascii=False, indent=2),
        "",
        "## Eligible rule distribution",
        json.dumps(dict(rule_counts), ensure_ascii=False, indent=2),
        "",
        "QWEN9B_HEALER_ELIGIBILITY_COMPLETED",
        "QWEN9B_HEALER_ELIGIBILITY_AUDIT_PASSED",
        "QWEN9B_ELIGIBLE_CELL_SET_FROZEN",
        "QWEN9B_CORRECTED_CHAIN_HEALER_READY",
    ]
    (OUT_DIR / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")

    if not audit["passed"]:
        raise RuntimeError(f"ELIGIBILITY_AUDIT_FAILED: {audit}")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("QWEN9B_HEALER_ELIGIBILITY_COMPLETED")
    print("QWEN9B_HEALER_ELIGIBILITY_AUDIT_PASSED")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    pins = verify_pins()
    baseline_rows = [
        json.loads(l)
        for l in (BASELINE_DIR / "cell_level_baseline.jsonl").read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]
    n_fail = sum(1 for r in baseline_rows if r["final_status"] != "PASSED")
    print(
        json.dumps(
            {
                "preflight": "PASS",
                **pins,
                "baseline_fail": n_fail,
                "expected_fail": EXPECTED_FAIL,
                "healer_execution": False,
            },
            indent=2,
        )
    )
    if n_fail != EXPECTED_FAIL:
        raise RuntimeError(f"baseline FAIL count {n_fail} != {EXPECTED_FAIL}")
    if args.preflight_only:
        return 0
    run_eligibility()
    print("QWEN9B_ELIGIBLE_CELL_SET_FROZEN")
    print("QWEN9B_CORRECTED_CHAIN_HEALER_READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
