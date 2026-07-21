# -*- coding: utf-8 -*-
"""Score frozen Qwen4B Pilot-02 320-cell corpus with Math16 v4 evaluator rules.

Offline only. Zero LLM calls. Does not run Ab3/Healer. Does not modify raw.
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

from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _empty_layer_counter,
    _hash_file,
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)

PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json"
RUNTIME_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_runtime_manifest.json"
EVIDENCE_FREEZE = (
    ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_generation_evidence_freeze_v1.json"
)
CORPUS_ROOT = ROOT / "docs/experiments/results/math16_pilot02_qwen4b"
OUT_DIR = ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001"
EVALUATOR_PATH = ROOT / "scripts/evaluate_math16_pilot02_full_v4.py"
TAXONOMY_PATH = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
ORACLE_PATH = ROOT / "agent_tools/finals_rebuild/math16_oracles.py"

EXPECTED_HEAD = "d074303cd7f11bb91631a7181131cfd9588b349e"
EXPECTED_FP = "33fd7603f58cdc47843bb048456d6d167dd71dc891b636377baf33dea30358f7"
EXPECTED_CLOSURE = "7dd3ba5f7e7a38e7ad20142e8c5c5b2e84c20df1b7f5abcf5701c23d24172a22"
EXPECTED_EVAL_HASH = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
EXPECTED_TAX_HASH = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"

EVAL_ID = "math16_pilot02_qwen4b_evaluation_v4_r001"
EVAL_REVISION = "v4_r001"

CONDITION_DISPLAY = {
    "ab1": "Ab1",
    "ab2g": "Ab2g",
    "ab2d": "Ab2d+api",
    "ab2d_spec_v2": "Ab2d+spec-v2",
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


def verify_corpus_immutable() -> dict[str, Any]:
    freeze = json.loads(EVIDENCE_FREEZE.read_text(encoding="utf-8"))
    if freeze["corpus_sha_closure"] != EXPECTED_CLOSURE:
        raise RuntimeError(
            f"CORPUS_SHA_CLOSURE_MISMATCH: expected {EXPECTED_CLOSURE} "
            f"got {freeze['corpus_sha_closure']}"
        )
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    if len(plan) != 320:
        raise RuntimeError("plan not 320")

    records = []
    missing = []
    for cell in plan:
        d = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        ap, pp, rp = d / "artifact.json", d / "prompt.txt", d / "raw_response.txt"
        if not (ap.exists() and pp.exists() and rp.exists()):
            missing.append(cell["cell_id"])
            continue
        art = json.loads(ap.read_text(encoding="utf-8"))
        records.append(
            {
                "cell_id": cell["cell_id"],
                "artifact_sha256": sha_bytes(ap),
                "prompt_sha256_file": sha_lf(pp),
                "raw_response_sha256": sha_bytes(rp),
                "plan_prompt_sha256": cell["prompt_sha256"],
                "generation_status": str(art.get("generation_status")),
            }
        )
    if missing:
        raise RuntimeError(f"missing cell files: {missing[:5]}")
    recomputed = sha_json(sorted(records, key=lambda r: r["cell_id"]))
    if recomputed != EXPECTED_CLOSURE:
        raise RuntimeError(
            f"CORPUS_SHA_RECOMPUTE_MISMATCH: expected {EXPECTED_CLOSURE} got {recomputed}"
        )

    journal = [
        json.loads(l)
        for l in (CORPUS_ROOT / "cell_journal.jsonl").read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]
    if len(journal) != 320:
        raise RuntimeError(f"journal lines={len(journal)}")

    file_count = sum(1 for _ in (CORPUS_ROOT / "cells").rglob("*") if _.is_file())
    # 320 * 3 minimum; may include error.json etc — require at least 960
    if file_count < 960:
        raise RuntimeError(f"cell files under 960: {file_count}")

    runtime = json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))
    if runtime["runtime_config_fingerprint"] != EXPECTED_FP:
        raise RuntimeError("runtime fingerprint drift")

    eval_hash = _hash_file(EVALUATOR_PATH)
    tax_hash = _hash_file(TAXONOMY_PATH)
    if eval_hash != EXPECTED_EVAL_HASH:
        raise RuntimeError(f"EVALUATOR_HASH_DRIFT: {eval_hash}")
    if tax_hash != EXPECTED_TAX_HASH:
        raise RuntimeError(f"TAXONOMY_HASH_DRIFT: {tax_hash}")

    return {
        "corpus_sha_closure": recomputed,
        "cells": 320,
        "journal_lines": 320,
        "min_cell_files": 960,
        "cell_files_observed": file_count,
        "evaluator_hash": eval_hash,
        "taxonomy_hash": tax_hash,
        "runtime_fingerprint": EXPECTED_FP,
        "llm_calls": 0,
    }


def slice_summary(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        groups[r[key]].append(r)
    out: dict[str, Any] = {}
    for k, items in sorted(groups.items(), key=lambda x: str(x[0])):
        passed = sum(1 for i in items if i["final_status"] == "PASSED")
        failed = len(items) - passed
        layers = _empty_layer_counter()
        for i in items:
            layer = i.get("primary_failure_layer")
            if layer in layers:
                layers[layer] += 1
        out[str(k)] = {
            "total": len(items),
            "passed": passed,
            "failed": failed,
            "pass_fraction": f"{passed}/{len(items)}",
            "failure_layer_distribution": layers,
        }
    return out


def run_scoring() -> dict[str, Any]:
    from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id
    from scripts.run_math16_latex_v1_gemini_live import classify_math16_response, extract_code

    pre = verify_corpus_immutable()
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    family_map, api_policy_map = _load_family_and_api_policy()
    # Use ab2d_spec (v1 freeze) task api_policy map identically to Gemini Pilot-02 v4.
    # Condition id ab2d_spec_v2 is bookkeeping only; classifier rules are unchanged.

    tasks = tasks_by_id()
    eval_hash = pre["evaluator_hash"]
    tax_hash = pre["taxonomy_hash"]
    oracle_hash = _hash_file(ORACLE_PATH)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    crashes: list[dict[str, Any]] = []
    raw_sha_mismatch: list[str] = []
    unknown_identity: list[str] = []

    for cell in plan:
        cid = cell["cell_id"]
        tid = cell["task_id"]
        cond = cell["condition"]
        seed = int(cell["seed"])
        if tid not in tasks:
            unknown_identity.append(cid)
            continue
        cell_dir = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        raw_path = cell_dir / "raw_response.txt"
        art_path = cell_dir / "artifact.json"
        raw = raw_path.read_text(encoding="utf-8")
        raw_sha = sha_bytes(raw_path)
        art = json.loads(art_path.read_text(encoding="utf-8"))
        # recompute artifact sha for record; verify raw bytes unchanged via closure already
        artifact_sha = sha_bytes(art_path)
        if art.get("prompt_sha256") != cell["prompt_sha256"]:
            raw_sha_mismatch.append(cid + ":prompt_meta")

        family = cell.get("family") or family_map[tid]
        api_policy = api_policy_map[tid]
        task = tasks[tid]
        frozen = frozen_for_prompt(task)

        try:
            outcome, source, details = classify_math16_response(
                raw,
                frozen_params=frozen["oracle_payload"],
                audit_oracle_payload=task["oracle_payload"],
                task=task,
            )
            mapped = classify_outcome_to_v3(outcome, details, api_policy=api_policy)
        except Exception as exc:  # noqa: BLE001
            crashes.append(
                {
                    "cell_id": cid,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                }
            )
            continue

        extracted = extract_code(raw)
        cand_code = extracted.extracted_code or ""
        candidate_hash = (
            hashlib.sha256(cand_code.encode("utf-8")).hexdigest() if cand_code else None
        )
        row = {
            "dataset": "CE115_Math16",
            "evaluation_id": EVAL_ID,
            "evaluation_revision": EVAL_REVISION,
            "cell_id": cid,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "condition_display": CONDITION_DISPLAY.get(cond, cond),
            "seed": seed,
            "model": "qwen3.5:4b",
            "model_tag": "qwen3.5:4b",
            "prompt_hash": cell["prompt_sha256"],
            "prompt_sha256": cell["prompt_sha256"],
            "raw_artifact_sha256": artifact_sha,
            "raw_response_sha256": raw_sha,
            "candidate_hash": candidate_hash,
            "runtime_fingerprint": EXPECTED_FP,
            "runtime_config_fingerprint": art.get("runtime_config_fingerprint"),
            "evaluator_hash": eval_hash,
            "taxonomy_hash": tax_hash,
            "oracle_source_sha256": oracle_hash,
            "api_policy": api_policy,
            "gates": mapped["gates"],
            "g1_parse": mapped["gates"].get("g1_parse"),
            "g2_execution": mapped["gates"].get("g2_execution"),
            "g3_contract": mapped["gates"].get("g3_contract"),
            "g4_correctness": mapped["gates"].get("g4_correctness"),
            "final_status": mapped["final_status"],
            "primary_failure_layer": mapped["primary_failure_layer"],
            "failure_subtype": mapped.get("failure_subtype"),
            "mechanism_tags": mapped.get("mechanism_tags") or [],
            "classifier_outcome": mapped.get("classifier_outcome") or outcome,
            "classifier_source": source,
            "exception_class": mapped.get("exception_class"),
            "exception_message": mapped.get("exception_message"),
            "outcome_validity": mapped.get("outcome_validity"),
            "failure_chain": mapped.get("failure_chain"),
            "evaluator_diagnostics": {
                "details_keys": sorted(details.keys()) if isinstance(details, dict) else [],
                "first_failure_location": mapped.get("first_failure_location"),
                "classification_status": mapped.get("classification_status"),
            },
            # Healer not run this round
            "healer_stage": "not_run",
            "post_healer_status": "not_run",
            "rescued": "not_run",
            "regression": "not_run",
            "baseline_only": True,
            "llm_calls": 0,
            "ab3": False,
            "healer": False,
        }
        rows.append(row)

    if unknown_identity:
        raise RuntimeError(f"unknown cell identity: {unknown_identity}")
    if crashes:
        # record but do not regenerate; fail audit if any
        write_json(OUT_DIR / "evaluator_crashes.json", crashes)
    if len(rows) != 320:
        raise RuntimeError(f"scored rows={len(rows)} expected 320 (crashes={len(crashes)})")

    # write cell jsonl
    cell_jsonl = OUT_DIR / "cell_level_baseline.jsonl"
    cell_jsonl.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    passed = sum(1 for r in rows if r["final_status"] == "PASSED")
    failed = 320 - passed
    layers = _empty_layer_counter()
    mechanisms: Counter[str] = Counter()
    exceptions: Counter[str] = Counter()
    validity: Counter[str] = Counter()
    gate_stats = Counter()
    for r in rows:
        layer = r.get("primary_failure_layer")
        if layer in layers:
            layers[layer] += 1
        for tag in r.get("mechanism_tags") or []:
            mechanisms[tag] += 1
        if r.get("exception_class"):
            exceptions[str(r["exception_class"])] += 1
        validity[str(r.get("outcome_validity") or "UNKNOWN")] += 1
        for gname, gkey in (
            ("G1", "g1_parse"),
            ("G2", "g2_execution"),
            ("G3", "g3_contract"),
            ("G4", "g4_correctness"),
        ):
            val = (r.get("gates") or {}).get(gkey)
            if val == "FAIL":
                gate_stats[f"{gname}_FAIL"] += 1
            elif val == "PASS":
                gate_stats[f"{gname}_PASS"] += 1

    baseline_summary = {
        "evaluation_id": EVAL_ID,
        "evaluation_revision": EVAL_REVISION,
        "evaluator_hash": eval_hash,
        "taxonomy_hash": tax_hash,
        "oracle_source_sha256": oracle_hash,
        "runtime_config_fingerprint": EXPECTED_FP,
        "corpus_sha_closure": EXPECTED_CLOSURE,
        "source_generation_commit": EXPECTED_HEAD,
        "model_tag": "qwen3.5:4b",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total": 320,
        "passed": passed,
        "failed": failed,
        "pass_fraction": f"{passed}/320",
        "pass_rate": passed / 320,
        "outcome_validity_distribution": dict(validity),
        "failure_layer_distribution": layers,
        "mechanism_tags_distribution": dict(mechanisms),
        "exception_class_distribution": dict(exceptions),
        "gate_stats": dict(gate_stats),
        "healer": {
            "executed": False,
            "rescued": "not_run",
            "regression": "not_run",
            "post_healer": "not_run",
        },
        "ab3": False,
        "llm_calls": 0,
        "other_model_calls": False,
        "qwen9b": False,
    }
    write_json(OUT_DIR / "baseline_summary.json", baseline_summary)
    write_json(OUT_DIR / "overall_summary.json", baseline_summary)
    write_json(OUT_DIR / "condition_summary.json", slice_summary(rows, "condition"))
    write_json(OUT_DIR / "family_summary.json", slice_summary(rows, "family"))
    write_json(OUT_DIR / "task_summary.json", slice_summary(rows, "task_id"))
    write_json(OUT_DIR / "seed_summary.json", slice_summary(rows, "seed"))
    write_json(
        OUT_DIR / "failure_taxonomy_summary.json",
        {
            "failure_layer_distribution": layers,
            "mechanism_tags_distribution": dict(mechanisms),
            "exception_class_distribution": dict(exceptions),
            "failed_cells": failed,
        },
    )

    # completeness audit
    scored_ids = {r["cell_id"] for r in rows}
    plan_ids = {c["cell_id"] for c in plan}
    missing_score = sorted(plan_ids - scored_ids)
    dup = [cid for cid, n in Counter(r["cell_id"] for r in rows).items() if n != 1]
    audit = {
        "audit": "qwen4b_scoring_completeness",
        "scored": len(rows),
        "expected": 320,
        "duplicate": dup,
        "missing": missing_score,
        "unscored": missing_score,
        "raw_sha_mismatch": raw_sha_mismatch,
        "unknown_cell_identity": unknown_identity,
        "evaluator_crash": crashes,
        "corpus_sha_closure_verified": EXPECTED_CLOSURE,
        "evaluator_hash": eval_hash,
        "taxonomy_hash": tax_hash,
        "passed": (
            len(rows) == 320
            and not dup
            and not missing_score
            and not raw_sha_mismatch
            and not unknown_identity
            and not crashes
        ),
        "baseline_only": True,
        "healer_executed": False,
        "ab3_executed": False,
        "llm_calls": 0,
    }
    write_json(OUT_DIR / "scoring_completeness_audit.json", audit)

    scoring_manifest = {
        "evaluation_id": EVAL_ID,
        "evaluation_revision": EVAL_REVISION,
        "evaluator_source": "scripts/evaluate_math16_pilot02_full_v4.py",
        "evaluator_hash": eval_hash,
        "taxonomy_source": str(TAXONOMY_PATH.relative_to(ROOT)).replace("\\", "/"),
        "taxonomy_hash": tax_hash,
        "oracle_source": "agent_tools/finals_rebuild/math16_oracles.py",
        "oracle_source_sha256": oracle_hash,
        "classifier": "scripts/run_math16_latex_v1_gemini_live.py::classify_math16_response",
        "outcome_mapper": "scripts/evaluate_math16_pilot02_full_v4.py::classify_outcome_to_v3",
        "input_corpus": "docs/experiments/results/math16_pilot02_qwen4b",
        "input_cell_plan": "docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json",
        "corpus_sha_closure": EXPECTED_CLOSURE,
        "runtime_config_fingerprint": EXPECTED_FP,
        "source_generation_commit": EXPECTED_HEAD,
        "cell_count": 320,
        "llm_calls": 0,
        "ab3": False,
        "healer": False,
        "qwen9b": False,
        "baseline_pass_fraction": f"{passed}/320",
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    write_json(OUT_DIR / "scoring_manifest.json", scoring_manifest)

    # human report
    cond = slice_summary(rows, "condition")
    fam = slice_summary(rows, "family")
    md = [
        "# Math16 Pilot-02 Qwen 3.5 4B Evaluation v4_r001 (baseline only)",
        "",
        f"- Evaluation ID: `{EVAL_ID}`",
        f"- Evaluator hash: `{eval_hash}`",
        f"- Taxonomy hash: `{tax_hash}`",
        f"- Corpus SHA closure: `{EXPECTED_CLOSURE}`",
        f"- Runtime fingerprint: `{EXPECTED_FP}`",
        f"- LLM calls: `0`",
        f"- Healer / Ab3: **not run**",
        "",
        "## Overall",
        f"- Baseline pass: `{passed}/320`",
        f"- Baseline fail: `{failed}/320`",
        "",
        "## By condition",
        "| Condition | Pass |",
        "| :--- | ---: |",
    ]
    for k, v in cond.items():
        md.append(f"| {CONDITION_DISPLAY.get(k, k)} (`{k}`) | {v['pass_fraction']} |")
    md.extend(["", "## By family", "| Family | Pass |", "| :--- | ---: |"])
    for k, v in fam.items():
        md.append(f"| {k} | {v['pass_fraction']} |")
    md.extend(
        [
            "",
            "## Failure layers (baseline failures)",
            json.dumps(layers, ensure_ascii=False),
            "",
            "QWEN4B_320CELL_SCORING_COMPLETED",
            "",
        ]
    )
    (OUT_DIR / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")

    if not audit["passed"]:
        raise RuntimeError(f"SCORING_COMPLETENESS_AUDIT_FAILED: {audit}")

    print(json.dumps(baseline_summary, ensure_ascii=False, indent=2))
    print("QWEN4B_320CELL_SCORING_COMPLETED")
    print("QWEN4B_SCORING_COMPLETENESS_AUDIT_PASSED")
    return baseline_summary


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    pre = verify_corpus_immutable()
    print(json.dumps({"preflight": "PASS", **pre}, indent=2))
    if args.preflight_only:
        return 0
    run_scoring()
    print("QWEN4B_BASELINE_RESULTS_FROZEN")
    print("QWEN4B_AB3_HEALER_READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
