"""Math16 Phase 1 Ab3 replay for Qwen multiseed H0 cells (H0 immutable; H1 separate).

Does not modify RULE_ALLOWLIST, Healer rules, prompts, or evaluator.
Does not write into H0 cell directories.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    MathHealerRunner,
    RULE_ALLOWLIST,
    RULE_REGISTRY,
)
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response

RESULTS = ROOT / "docs/experiments/results"
OUT_ROOT = RESULTS / "math16_qwen_multiseed_ab3_phase1"
H1_ROOT = OUT_ROOT / "h1_cells"
REPORT_JSON = OUT_ROOT / "ab3_report_data.json"
REPORT_MD = OUT_ROOT / "ab3_report.md"

MODELS = ("qwen35_4b", "qwen35_9b")
NEW_SEEDS = (2026072001, 2026072002, 2026072003, 2026072004)
EXPECTED_ALLOWLIST = {
    "L1_CLOSE_UNBALANCED_PARENTHESIS",
    "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
    "L1_PROSE_RESIDUE_NARROW",
    "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
    "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
    "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
}
OUTCOMES = {
    "no_trigger",
    "guarded_abstain",
    "layer_exposure",
    "rescue_to_pass",
    "regression",
    "excluded_no_program_structure",
    "evaluator_failure",
    "identity_reuse",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def context_for(artifact: dict[str, Any]) -> dict[str, Any]:
    task = dict(artifact.get("audit_oracle_payload") or {})
    task.update({"skill_id": artifact["task_id"], "oracle_type": artifact["family"]})
    return {"task": task, "frozen": artifact.get("frozen_parameters") or {}}


def source_for(cell_dir: Path) -> tuple[str, str]:
    candidate = cell_dir / "extracted_candidate.py"
    raw = cell_dir / "raw_response.txt"
    if candidate.exists():
        text = candidate.read_text(encoding="utf-8")
        return text, "extracted_candidate"
    if raw.exists():
        text = raw.read_text(encoding="utf-8")
        return text, "raw_response"
    raise FileNotFoundError(f"no H0 source for {cell_dir.name}")


def iter_phase1_cells() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for model in MODELS:
        run = RESULTS / f"{model}_math16_ab123_run_003_multiseed"
        for seed in NEW_SEEDS:
            seed_dir = run / f"seed_{seed}"
            cells_root = seed_dir / "cells"
            if not cells_root.exists():
                raise RuntimeError(f"missing cells for {model} seed {seed}")
            cell_dirs = sorted(p for p in cells_root.iterdir() if p.is_dir())
            if len(cell_dirs) != 48:
                raise RuntimeError(f"expected 48 cells for {model} seed {seed}, got {len(cell_dirs)}")
            for cell_dir in cell_dirs:
                artifact_path = cell_dir / "artifact.json"
                artifact = load_json(artifact_path)
                rows.append(
                    {
                        "model": model,
                        "seed": seed,
                        "run": f"{model}_math16_ab123_run_003_multiseed",
                        "cell_dir": cell_dir,
                        "artifact_path": artifact_path,
                        "artifact": artifact,
                        "cell_id": artifact["cell_id"],
                        "h0_status": artifact["evaluator_status"],
                        "h0_artifact_sha256": sha256_bytes(artifact_path),
                    }
                )
    if len(rows) != 384:
        raise RuntimeError(f"expected 384 cells, got {len(rows)}")
    return rows


def map_outcome(
    *,
    h0_pass: bool,
    changed: bool,
    rolled_back: bool,
    reevaluation: str | None,
    no_program: bool,
    eval_failed: bool,
    guarded: bool,
) -> str:
    if h0_pass:
        return "identity_reuse"
    if no_program:
        return "excluded_no_program_structure"
    if eval_failed:
        return "evaluator_failure"
    if guarded and not changed:
        return "guarded_abstain"
    if not changed:
        return "no_trigger"
    if rolled_back:
        # Protocol fixed set does not include triggered_rolled_back; map conservatively.
        return "guarded_abstain"
    if reevaluation == "PASSED":
        return "rescue_to_pass"
    # triggered_changed_still_fail -> layer_exposure
    return "layer_exposure"


def execute_ab3() -> dict[str, Any]:
    if len(RULE_ALLOWLIST) != 6 or set(RULE_ALLOWLIST) != EXPECTED_ALLOWLIST:
        raise RuntimeError(f"frozen allowlist mismatch: {RULE_ALLOWLIST}")

    rows = iter_phase1_cells()
    runner = MathHealerRunner(max_passes=3)
    results: list[dict[str, Any]] = []
    H1_ROOT.mkdir(parents=True, exist_ok=True)

    for row in rows:
        artifact = row["artifact"]
        cell_dir: Path = row["cell_dir"]
        artifact_before = cell_dir / "artifact.json"
        before_sha = sha256_bytes(artifact_before)
        h0_pass = row["h0_status"] == "PASSED"

        if h0_pass:
            # Negative control: must not mutate source.
            source, source_kind = source_for(cell_dir)
            source_before = source
            # Do not run healer on PASS cells for mutation; identity reuse only.
            actual = "identity_reuse"
            h1 = {
                "schema_version": 1,
                "cell_id": row["cell_id"],
                "model": row["model"],
                "seed": row["seed"],
                "h0_status": row["h0_status"],
                "h0_artifact_path": str(row["artifact_path"].relative_to(ROOT)).replace("\\", "/"),
                "h0_artifact_sha256": before_sha,
                "h0_source_sha256": sha256_text(source_before),
                "source_kind": source_kind,
                "actual_outcome": actual,
                "triggered_rule": None,
                "changed": False,
                "healer_ran": False,
                "note": "H0 PASS identity reuse / negative control; healer not applied",
            }
            after_sha = sha256_bytes(artifact_before)
            if after_sha != before_sha:
                raise RuntimeError(f"PROTOCOL_VIOLATION_PASS_CELL_MUTATED: artifact changed for {row['cell_id']}")
            # Also ensure source files unchanged
            source_after, _ = source_for(cell_dir)
            if source_after != source_before:
                raise RuntimeError(f"PROTOCOL_VIOLATION_PASS_CELL_MUTATED: source changed for {row['cell_id']}")
        else:
            source, source_kind = source_for(cell_dir)
            h0_source_sha = sha256_text(source)
            no_program = False
            if not source.strip():
                no_program = True
                actual = "excluded_no_program_structure"
                h1 = {
                    "schema_version": 1,
                    "cell_id": row["cell_id"],
                    "model": row["model"],
                    "seed": row["seed"],
                    "h0_status": row["h0_status"],
                    "h0_artifact_path": str(row["artifact_path"].relative_to(ROOT)).replace("\\", "/"),
                    "h0_artifact_sha256": before_sha,
                    "h0_source_sha256": h0_source_sha,
                    "source_kind": source_kind,
                    "actual_outcome": actual,
                    "triggered_rule": None,
                    "changed": False,
                    "healer_ran": False,
                }
            else:
                result = runner.run(source, context=context_for(artifact))
                provenance = [
                    dataclasses.asdict(p) if dataclasses.is_dataclass(p) else dict(p)
                    for p in result.provenance
                ]
                changed = any(p.get("changed") for p in provenance)
                triggered_rules = [
                    p.get("selected_rule_id") or p.get("rule_id")
                    for p in provenance
                    if p.get("changed") or p.get("triggered")
                ]
                triggered_rules = [r for r in triggered_rules if r]
                guarded = any(
                    (p.get("final_status") in {"no_op", "validation_failed"})
                    and p.get("triggered")
                    for p in provenance
                )
                rolled_back = bool(result.rolled_back)
                reevaluation = None
                evaluator_details: dict[str, Any] | None = None
                repaired = result.output_source if changed and not rolled_back else None
                eval_failed = False
                if changed and not rolled_back and repaired is not None:
                    try:
                        outcome, _, evaluator_details = classify_response(
                            repaired,
                            {"oracle_payload": dict(artifact.get("frozen_parameters") or {})},
                            dict(context_for(artifact)["task"]),
                        )
                        reevaluation = "PASSED" if outcome == "passed" else outcome.upper()
                        if outcome == "passed":
                            reevaluation = "PASSED"
                        else:
                            # normalize
                            reevaluation = "FAIL"
                    except Exception as exc:  # noqa: BLE001
                        eval_failed = True
                        reevaluation = "EVALUATOR_EXCEPTION"
                        evaluator_details = {
                            "exception_type": type(exc).__name__,
                            "message": str(exc),
                        }

                if h0_pass and changed:
                    raise RuntimeError(f"PROTOCOL_VIOLATION_PASS_CELL_MUTATED: {row['cell_id']}")

                actual = map_outcome(
                    h0_pass=False,
                    changed=changed,
                    rolled_back=rolled_back,
                    reevaluation=reevaluation,
                    no_program=False,
                    eval_failed=eval_failed,
                    guarded=guarded and not changed,
                )
                if actual == "rescue_to_pass" and row["h0_status"] == "PASSED":
                    actual = "regression"  # should not happen on FAIL path
                # Regression: H0 PASS mutated to FAIL — handled on PASS path above.
                # For FAIL->changed->still fail: layer_exposure already.

                h1 = {
                    "schema_version": 1,
                    "cell_id": row["cell_id"],
                    "model": row["model"],
                    "seed": row["seed"],
                    "h0_status": row["h0_status"],
                    "h0_artifact_path": str(row["artifact_path"].relative_to(ROOT)).replace("\\", "/"),
                    "h0_artifact_sha256": before_sha,
                    "h0_source_sha256": h0_source_sha,
                    "source_kind": source_kind,
                    "actual_outcome": actual,
                    "triggered_rule": triggered_rules[0] if triggered_rules else None,
                    "triggered_rules": triggered_rules,
                    "changed": changed,
                    "rolled_back": rolled_back,
                    "healer_ran": True,
                    "max_passes": 3,
                    "allowlist": list(RULE_ALLOWLIST),
                    "final_status": result.final_status,
                    "provenance": provenance,
                    "reevaluation_status": reevaluation,
                    "reevaluation_details": evaluator_details,
                    "repaired_source_sha256": sha256_text(repaired) if repaired else None,
                }
                if repaired is not None:
                    h1_dir = H1_ROOT / row["cell_id"]
                    h1_dir.mkdir(parents=True, exist_ok=True)
                    (h1_dir / "repaired_candidate.py").write_text(repaired, encoding="utf-8")

            after_sha = sha256_bytes(artifact_before)
            if after_sha != before_sha:
                raise RuntimeError(f"H0_ARTIFACT_MUTATED: {row['cell_id']}")

        # Always write H1 sidecar outside H0 tree
        h1_dir = H1_ROOT / row["cell_id"]
        h1_dir.mkdir(parents=True, exist_ok=True)
        dump_json(h1_dir / "artifact_h1.json", h1)

        results.append(
            {
                "model": row["model"],
                "seed": row["seed"],
                "cell_id": row["cell_id"],
                "h0_status": row["h0_status"],
                "actual": actual,
                "triggered_rule": h1.get("triggered_rule"),
                "changed": h1.get("changed", False),
            }
        )

    # Closure checks
    by_outcome = Counter(r["actual"] for r in results)
    if sum(by_outcome.values()) != 384:
        raise RuntimeError("outcome count != 384")
    unknown = [r for r in results if r["actual"] not in OUTCOMES]
    if unknown:
        raise RuntimeError(f"unknown outcomes: {unknown[:3]}")

    # trigger = changed or triggered_rule present among FAIL path (not identity_reuse)
    triggers = [
        r
        for r in results
        if r["actual"] in {"layer_exposure", "rescue_to_pass", "guarded_abstain", "regression"}
        and r.get("changed")
        or (r.get("triggered_rule") and r["actual"] != "identity_reuse" and r["actual"] != "no_trigger")
    ]
    # cleaner trigger definition: healer changed source OR selected a triggered rule that abstained
    trigger_rows = []
    for r in results:
        if r["actual"] == "identity_reuse":
            continue
        if r["actual"] in {"layer_exposure", "rescue_to_pass"}:
            trigger_rows.append(r)
        elif r["actual"] == "guarded_abstain" and r.get("triggered_rule"):
            trigger_rows.append(r)
        elif r.get("changed"):
            trigger_rows.append(r)

    summary = {
        "cells": 384,
        "by_outcome": dict(by_outcome),
        "by_model": {},
        "by_model_seed": {},
        "trigger_count": len(trigger_rows),
        "layer_exposure": by_outcome.get("layer_exposure", 0),
        "rescue_to_pass": by_outcome.get("rescue_to_pass", 0),
        "regression": by_outcome.get("regression", 0),
        "guarded_abstain": by_outcome.get("guarded_abstain", 0),
        "no_trigger": by_outcome.get("no_trigger", 0),
        "identity_reuse": by_outcome.get("identity_reuse", 0),
        "excluded_no_program_structure": by_outcome.get("excluded_no_program_structure", 0),
        "evaluator_failure": by_outcome.get("evaluator_failure", 0),
        "allowlist": list(RULE_ALLOWLIST),
        "max_passes": 3,
        "h0_immutable": True,
        "h1_root": str(H1_ROOT.relative_to(ROOT)).replace("\\", "/"),
    }
    for model in MODELS:
        subset = [r for r in results if r["model"] == model]
        summary["by_model"][model] = {
            "cells": len(subset),
            "by_outcome": dict(Counter(r["actual"] for r in subset)),
            "trigger": sum(1 for r in trigger_rows if r["model"] == model),
            "layer_exposure": sum(1 for r in subset if r["actual"] == "layer_exposure"),
            "rescue_to_pass": sum(1 for r in subset if r["actual"] == "rescue_to_pass"),
            "regression": sum(1 for r in subset if r["actual"] == "regression"),
        }
        for seed in NEW_SEEDS:
            ss = [r for r in subset if r["seed"] == seed]
            summary["by_model_seed"][f"{model}__{seed}"] = {
                "cells": len(ss),
                "by_outcome": dict(Counter(r["actual"] for r in ss)),
            }

    payload = {"summary": summary, "results": results}
    dump_json(REPORT_JSON, payload)

    lines = [
        "# Math16 Qwen Phase 1 Ab3 report",
        "",
        f"- cells: {summary['cells']}",
        f"- identity_reuse: {summary['identity_reuse']}",
        f"- no_trigger: {summary['no_trigger']}",
        f"- guarded_abstain: {summary['guarded_abstain']}",
        f"- layer_exposure: {summary['layer_exposure']}",
        f"- rescue_to_pass: {summary['rescue_to_pass']}",
        f"- regression: {summary['regression']}",
        f"- trigger_count: {summary['trigger_count']}",
        f"- H1 root: `{summary['h1_root']}`",
        "",
        "H0 artifacts were not modified.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if not args.execute:
        print("pass --execute")
        return 2
    summary = execute_ab3()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
