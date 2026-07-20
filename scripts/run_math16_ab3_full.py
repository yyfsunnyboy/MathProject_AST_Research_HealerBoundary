"""Math16 full Ab3 formal run for three frozen 48-cell cohorts.

The ``predict`` phase writes the 144-cell prediction lock only.  The ``execute``
phase refuses to run unless that file is already committed and the worktree is
clean, preserving the prediction-before-execution evidence chain.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    MathHealerRunner,
    RULE_ALLOWLIST,
    RULE_REGISTRY,
)
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "docs" / "experiments" / "results"
PREDICTIONS = RESULTS / "math16_ab3_full_predictions.json"
REPORT_JSON = RESULTS / "math16_ab3_full_report_data.json"
REPORT_MD = RESULTS / "math16_ab3_full_report.md"
BASELINE = "b3eced2b698e0751783bda39fa39c08439b0e3ef"
RUNS = (
    "gemini35flash_math16_latex_v1_ab123_run_001",
    "qwen35_4b_math16_ab123_run_002",
    "qwen35_9b_math16_ab123_run_002",
)
KNOWN_LAYER_EXPOSURE = {
    "qwen35_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301",
    "qwen35_4b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def context_for(artifact: dict[str, Any]) -> dict[str, Any]:
    task = dict(artifact.get("audit_oracle_payload") or {})
    task.update({"skill_id": artifact["task_id"], "oracle_type": artifact["family"]})
    return {"task": task, "frozen": artifact.get("frozen_parameters") or {}}


def source_for(cell_dir: Path) -> str:
    candidate = cell_dir / "extracted_candidate.py"
    raw = cell_dir / "raw_response.txt"
    if candidate.exists():
        return candidate.read_text(encoding="utf-8")
    if raw.exists():
        return raw.read_text(encoding="utf-8")
    raise FileNotFoundError(f"no H0 source for {cell_dir.name}")


def cells() -> list[dict[str, Any]]:
    revised = {
        row["cell_id"]: row["revised_evaluator_status"]
        for row in load_json(
            RESULTS / RUNS[0] / "evaluation_revision_003" / "cell_outcomes.json"
        )
    }
    rows: list[dict[str, Any]] = []
    for run_name in RUNS:
        for cell_dir in sorted((RESULTS / run_name / "cells").iterdir()):
            artifact_path = cell_dir / "artifact.json"
            artifact = load_json(artifact_path)
            status = revised.get(artifact["cell_id"], artifact["evaluator_status"])
            rows.append(
                {
                    "run": run_name,
                    "cell_dir": cell_dir,
                    "artifact_path": artifact_path,
                    "artifact": artifact,
                    "cell_id": artifact["cell_id"],
                    "h0_status": status,
                }
            )
    counts = Counter(row["run"] for row in rows)
    if len(rows) != 144 or any(counts[name] != 48 for name in RUNS):
        raise RuntimeError(f"expected 48x3 cells, got {dict(counts)}")
    return rows


def predicted_for(row: dict[str, Any]) -> tuple[str, str | None]:
    if row["h0_status"] == "PASSED":
        return "predicted_identity_reuse", None
    if row["run"].startswith("qwen"):
        if row["cell_id"] in KNOWN_LAYER_EXPOSURE:
            return "predicted_layer_exposure", None
        return "predicted_no_trigger", None

    artifact = row["artifact"]
    source = source_for(row["cell_dir"])
    context = context_for(artifact)
    hits: list[str] = []
    for rule_id in RULE_ALLOWLIST:
        rule = RULE_REGISTRY[rule_id]
        applicable, _, _ = rule.is_applicable(source, context)
        if applicable:
            triggered, _ = rule.is_triggered(source, context)
            if triggered:
                hits.append(rule_id)
    if hits:
        return "predicted_trigger_uncertain", "Frozen precondition symptom matched: " + ", ".join(hits)
    return "predicted_no_trigger", None


def predict() -> None:
    if git("rev-parse", "HEAD") != BASELINE or git("rev-parse", "origin/main") != BASELINE:
        raise RuntimeError("HEAD/origin baseline mismatch")
    if git("status", "--short") not in ("", "?? scripts/run_math16_ab3_full.py"):
        raise RuntimeError("unexpected dirty worktree before prediction lock")
    expected = {
        "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
        "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
        "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
        "L1_CLOSE_UNBALANCED_PARENTHESIS",
        "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
        "L1_PROSE_RESIDUE_NARROW",
    }
    if len(RULE_ALLOWLIST) != 6 or set(RULE_ALLOWLIST) != expected:
        raise RuntimeError(f"frozen allowlist mismatch: {RULE_ALLOWLIST}")
    predictions = []
    for row in cells():
        predicted, reason = predicted_for(row)
        item = {
            "cell_id": row["cell_id"],
            "h0_status": row["h0_status"],
            "predicted_outcome": predicted,
        }
        if reason:
            item["reason"] = reason
        predictions.append(item)
    dump_json(PREDICTIONS, predictions)
    print(json.dumps({"count": len(predictions), "sha256": sha256_bytes(PREDICTIONS),
                      "outcomes": Counter(x["predicted_outcome"] for x in predictions)},
                     ensure_ascii=False, default=dict, indent=2))


def provenance_dict(item: Any) -> dict[str, Any]:
    return dataclasses.asdict(item) if dataclasses.is_dataclass(item) else dict(item)


def prediction_matches(predicted: str, actual: str) -> bool:
    if predicted == "predicted_identity_reuse":
        return actual == "identity_reuse"
    if predicted == "predicted_no_trigger":
        return actual == "no_trigger"
    if predicted == "predicted_layer_exposure":
        return actual == "layer_exposure"
    if predicted == "predicted_trigger_uncertain":
        return actual in {"triggered_rolled_back", "layer_exposure", "rescue_to_pass"}
    return False


def execute() -> None:
    if git("status", "--short"):
        raise RuntimeError("execute requires a clean worktree")
    prediction_commit = git("log", "-1", "--format=%H", "--", str(PREDICTIONS.relative_to(ROOT)))
    if prediction_commit == BASELINE:
        raise RuntimeError("prediction file was not committed after the evidence baseline")
    predictions = {x["cell_id"]: x for x in load_json(PREDICTIONS)}
    if len(predictions) != 144:
        raise RuntimeError("prediction lock is not 144 cells")
    pred_hash = sha256_bytes(PREDICTIONS)
    runner = MathHealerRunner(max_passes=3)
    results: list[dict[str, Any]] = []

    for row in cells():
        pred = predictions[row["cell_id"]]["predicted_outcome"]
        artifact = row["artifact"]
        if row["h0_status"] == "PASSED":
            actual = "identity_reuse"
            provenance: list[dict[str, Any]] = []
        else:
            source = source_for(row["cell_dir"])
            result = runner.run(source, context=context_for(artifact))
            provenance = [provenance_dict(p) for p in result.provenance]
            changed = any(p.get("changed") for p in provenance)
            if not changed:
                actual = "no_trigger"
            elif result.rolled_back:
                actual = "triggered_rolled_back"
            else:
                repaired = result.output_source
                try:
                    outcome, _, evaluator_details = classify_response(
                        repaired,
                        {"oracle_payload": dict(artifact.get("frozen_parameters") or {})},
                        dict(context_for(artifact)["task"]),
                    )
                except Exception as exc:  # evaluation remains FAIL, but preserve exact error
                    outcome = "EVALUATOR_EXCEPTION"
                    evaluator_details = {"exception_type": type(exc).__name__, "message": str(exc)}
                actual = "rescue_to_pass" if outcome == "PASSED" else "layer_exposure"
                repaired_path = row["cell_dir"] / "repaired_candidate.py"
                repaired_path.write_text(repaired, encoding="utf-8")
                artifact.setdefault("hashes", {})["repaired_candidate"] = sha256_bytes(repaired_path)
                artifact["healer"] = {
                    "attempted": True,
                    "enabled": True,
                    "max_passes": 3,
                    "allowlist": list(RULE_ALLOWLIST),
                    "actual_outcome": actual,
                    "final_status": result.final_status,
                    "rolled_back": result.rolled_back,
                    "provenance": provenance,
                    "reevaluation_status": outcome,
                    "reevaluation_details": evaluator_details,
                }
                dump_json(row["artifact_path"], artifact)
            if not changed or result.rolled_back:
                artifact["healer"] = {
                    "attempted": True,
                    "enabled": True,
                    "max_passes": 3,
                    "allowlist": list(RULE_ALLOWLIST),
                    "actual_outcome": actual,
                    "final_status": result.final_status,
                    "rolled_back": result.rolled_back,
                    "provenance": provenance,
                }
                dump_json(row["artifact_path"], artifact)
        results.append(
            {
                "run": row["run"], "cell_id": row["cell_id"],
                "h0_status": row["h0_status"], "predicted": pred,
                "actual": actual, "match": prediction_matches(pred, actual),
            }
        )

    report = {
        "baseline_commit": BASELINE,
        "prediction_commit": prediction_commit,
        "prediction_sha256": pred_hash,
        "allowlist": list(RULE_ALLOWLIST),
        "max_passes": 3,
        "results": results,
    }
    dump_json(REPORT_JSON, report)
    lines = ["# Math16 full Ab3 formal report", "",
             f"- Baseline commit: `{BASELINE}`", f"- Prediction commit: `{prediction_commit}`",
             f"- Prediction SHA-256: `{pred_hash}`", ""]
    summary_rows = []
    for run_name in RUNS:
        subset = [x for x in results if x["run"] == run_name]
        lines += [f"## {run_name}", "", "| cell_id | h0_status | predicted | actual | match |",
                  "|---|---|---|---|---|"]
        lines += [f"| {x['cell_id']} | {x['h0_status']} | {x['predicted']} | {x['actual']} | {str(x['match']).lower()} |" for x in subset]
        lines.append("")
        identity = [x for x in subset if x["h0_status"] == "PASSED"]
        summary_rows.append((run_name, "not applicable (identity reuse skipped Healer)",
                             sum(x["actual"] == "layer_exposure" for x in subset),
                             sum(x["actual"] == "rescue_to_pass" for x in subset),
                             f"{sum(x['match'] for x in subset)}/{len(subset)} ({sum(x['match'] for x in subset)/len(subset):.2%})",
                             len(identity)))
    lines += ["## Summary", "", "| model | false positive | layer_exposure | rescue_to_pass | match rate | identity reuse |",
              "|---|---|---:|---:|---:|---:|"]
    lines += [f"| {r} | {fp} | {le} | {rescue} | {rate} | {identity} |" for r, fp, le, rescue, rate, identity in summary_rows]
    lines += ["", "## git status --short", "", "Recorded immediately before the final result commit; see commit diff for the generated H1 and report files.", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"results": len(results), "prediction_sha256": pred_hash,
                      "actual": Counter(x["actual"] for x in results)}, ensure_ascii=False,
                     default=dict, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("predict", "execute"))
    args = parser.parse_args()
    predict() if args.phase == "predict" else execute()
