"""Build docs/experiments/results/v2_unified_relabel_map.json (read-only over artifacts).

Translates existing forensic / revision / run labels into v2 taxonomy.
Does NOT mutate artifacts, call models, or re-score.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.failure_classification_v2 import (  # noqa: E402
    classify_cell,
)

RESULTS = ROOT / "docs/experiments/results"
OUT_PATH = RESULTS / "v2_unified_relabel_map.json"
STANDARD_BLOB = "2c0ce7bdd935fa5664c877babf892c816be4c256"

GEMINI_RUN = "gemini35flash_math16_latex_v1_ab123_run_001"
QWEN_4B_002 = "qwen35_4b_math16_ab123_run_002"
QWEN_9B_002 = "qwen35_9b_math16_ab123_run_002"
QWEN_4B_001 = "qwen35_4b_math16_ab123_run_001"
QWEN_9B_001 = "qwen35_9b_math16_ab123_run_001"

# Gemini forensic overrides (translate; do not re-judge)
GEMINI_INVALID_EVALUATOR = {
    "gemini_3_5_flash__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301",
    "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301",
    "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301",
}
GEMINI_INVALID_CONTRACT = {
    # factor_roots ab2d — API doc mismatch / return-shape hallucination
    "gemini_3_5_flash__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301": {
        "layer": "L3",
        "tags": ["prompt_api_mismatch", "return_shape_hallucination"],
        "basis": "v2.md L3 + ab2d_v2 adjudication; API returns-tuple docs mismatch",
    },
    # q10 ab2d — Fraction JSON serialization channel
    "gemini_3_5_flash__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026071301": {
        "layer": "L4",
        "tags": [],
        "basis": "v2.md L4 + revision_003 official_q10_ab2d; INVALID_CONTRACT serialization",
    },
}
GEMINI_Q02_TASK = "ce111_q02_polynomial_division_remainder"


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _gate_status(gate: Any) -> str:
    if not isinstance(gate, dict):
        return "NOT_ASSESSED"
    status = str(gate.get("status") or "NOT_ASSESSED").upper()
    if status == "PASSED":
        return "PASS"
    if status == "FAILED":
        return "FAIL"
    return status


def _gates_from_artifact(art: dict[str, Any]) -> dict[str, str]:
    gates = art.get("gates") or (art.get("evaluator_details") or {}).get("evaluation_gates") or {}
    return {
        "g1_parse": _gate_status(gates.get("g1_evaluability") or gates.get("g1_parse")),
        "g2_execution": _gate_status(gates.get("g2_executability") or gates.get("g2_execution")),
        "g3_contract": _gate_status(
            gates.get("g3_contract_compliance") or gates.get("g3_contract")
        ),
        "g3a_required_api": "NOT_APPLICABLE",
        "g3c_canonical_form": "NOT_APPLICABLE",
        "g4_correctness": _gate_status(
            gates.get("g4_semantic_correctness") or gates.get("g4_correctness")
        ),
    }


def _layer_from_evaluator_status(status: str | None) -> str | None:
    if not status:
        return None
    s = status.upper()
    if s == "PASSED":
        return "PASSED"
    if s in {
        "PARSE_MINOR",
        "EXTRACTION_FAILURE",
        "MISSING_ENTRY_POINT",
        "CATASTROPHIC_TRUNCATION",
        "EMPTY_RESPONSE",
    }:
        return "L1"
    if s in {"SCHEMA_FAILURE", "STRUCTURAL_MISMATCH", "LATEX_MISMATCH"}:
        # v2: packaging / canonical form → L2
        return "L2"
    if s in {"EXECUTION_FAILURE", "RUNTIME_FAILURE"}:
        return "L4"
    if s in {"ANSWER_INCORRECT", "INTRINSIC_SAFETY"}:
        return "L5"
    if s in {
        "INFRASTRUCTURE_FAILURE",
        "API_FAILURE",
        "API_FATAL_STOP",
        "L0_INVALID_INFRASTRUCTURE",
    }:
        return "L0"
    return None


def _is_degenerate(text: str) -> bool:
    if len(text) < 2000:
        return False
    sample = text[-20000:] if len(text) > 20000 else text
    lines = [ln for ln in sample.splitlines() if len(ln.strip()) > 5]
    if lines:
        from collections import Counter

        _top, top_c = Counter(lines).most_common(1)[0]
        if top_c >= 10:
            return True
    from collections import Counter

    for n in (40, 80):
        counts = Counter(sample[i : i + n] for i in range(0, len(sample) - n, n))
        if counts:
            chunk, c = counts.most_common(1)[0]
            if c >= 8 and chunk.strip():
                return True
    return False


def _original_label(art: dict[str, Any]) -> dict[str, Any]:
    fl = art.get("failure_layer") if isinstance(art.get("failure_layer"), dict) else {}
    return {
        "evaluator_status": art.get("evaluator_status"),
        "failure_category": art.get("failure_category") or art.get("failure_class"),
        "failure_layer_primary": fl.get("primary_layer"),
        "validity": art.get("validity"),
        "outcome_validity": art.get("outcome_validity"),
        "suspected_invalid": art.get("suspected_invalid"),
        "suspected_invalid_reason": art.get("suspected_invalid_reason"),
    }


def _row(
    *,
    run_id: str,
    model: str,
    art: dict[str, Any],
    v2_layer: str | None,
    v2_validity: str,
    mechanism: list[str],
    gates: dict[str, str],
    basis: list[str],
    needs_review: bool = False,
    suspected_invalid: bool | None = None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "cell_id": art.get("cell_id"),
        "task_id": art.get("task_id"),
        "model": model,
        "condition": art.get("condition") or art.get("treatment"),
        "original_labels": _original_label(art),
        "v2": {
            "primary_failure_layer": v2_layer,
            "outcome_validity": v2_validity,
            "mechanism_tags": mechanism,
            "gates": gates,
            "needs_human_review": needs_review,
            "suspected_invalid": suspected_invalid,
        },
        "translation_basis": basis,
    }


def translate_gemini() -> tuple[list[dict[str, Any]], list[str]]:
    run_dir = RESULTS / GEMINI_RUN
    validity_report = _load(run_dir / "validity_report.json")
    full_table = {r["cell_id"]: r for r in _load(run_dir / "full_cell_table.json")}
    rev003 = {
        r["cell_id"]: r
        for r in _load(run_dir / "evaluation_revision_003" / "cell_outcomes.json")
    }
    rev_summary = _load(run_dir / "evaluation_revision_003" / "summary.json")

    rows: list[dict[str, Any]] = []
    needs_review: list[str] = []

    for cell_dir in sorted((run_dir / "cells").iterdir()):
        art_path = cell_dir / "artifact.json"
        if not art_path.exists():
            continue
        art = _load(art_path)
        cell_id = art["cell_id"]
        task_id = art.get("task_id")
        gates = _gates_from_artifact(art)
        table = full_table.get(cell_id) or {}
        rev = rev003.get(cell_id) or {}
        basis = [
            f"validity_report.json production_bugs / valid_model_failures",
            f"full_cell_table.json validity={table.get('validity')}",
            f"evaluation_revision_003 status={rev.get('revised_evaluator_status')}",
        ]

        mechanism: list[str] = []
        needs = False
        suspected = None

        if cell_id in GEMINI_INVALID_EVALUATOR:
            layer = "L5"
            validity = "INVALID_EVALUATOR"
            basis.append(
                "validity_report.json MATH16_LATEX_EXACT_STRING_FALSE_NEGATIVE "
                "(評分冤案 → L5+INVALID_EVALUATOR)"
            )
        elif cell_id in GEMINI_INVALID_CONTRACT:
            meta = GEMINI_INVALID_CONTRACT[cell_id]
            layer = meta["layer"]
            validity = "INVALID_CONTRACT"
            mechanism = list(meta["tags"])
            basis.append(meta["basis"])
        elif task_id == GEMINI_Q02_TASK:
            # Forensic: content correct, packaging wrong; schema explicit in prompt
            layer = "L2"
            validity = "VALID_MODEL_OUTCOME"
            mechanism = ["output_packaging"]
            basis.append(
                "validity_report.json valid_model_failures q02 + v2.md L2 anchor"
            )
        else:
            # Translate historical evaluator_status; validity from full_cell_table
            hist_status = art.get("evaluator_status") or table.get("evaluator_status")
            layer = _layer_from_evaluator_status(hist_status)
            table_validity = table.get("validity") or "VALID_MODEL_OUTCOME"
            if table_validity == "NEEDS_REVIEW":
                validity = "PENDING_REVIEW"
                needs = True
                mechanism.append("needs_human_review")
                needs_review.append(cell_id)
            elif table_validity in {
                "VALID_MODEL_OUTCOME",
                "INVALID_EVALUATOR",
                "INVALID_CONTRACT",
                "INVALID_INFRASTRUCTURE",
                "PENDING_REVIEW",
            }:
                validity = table_validity
            else:
                validity = "PENDING_REVIEW"
                needs = True
                mechanism.append("needs_human_review")
                needs_review.append(cell_id)

            if layer is None:
                needs = True
                if "needs_human_review" not in mechanism:
                    mechanism.append("needs_human_review")
                if cell_id not in needs_review:
                    needs_review.append(cell_id)
                basis.append(f"unmapped evaluator_status={hist_status}")

            # Align LATEX/STRUCTURAL to L2 already via helper; note G3c
            if (hist_status or "").upper() in {"STRUCTURAL_MISMATCH", "LATEX_MISMATCH"}:
                basis.append("v2 G3c: structural/latex → L2 symptom")

        rows.append(
            _row(
                run_id=GEMINI_RUN,
                model="gemini-3.5-flash",
                art=art,
                v2_layer=layer,
                v2_validity=validity,
                mechanism=mechanism,
                gates=gates,
                basis=basis
                + [
                    f"revision_003 confirmatory hashes "
                    f"orig={rev_summary.get('original_evaluator_hash')} "
                    f"rev={rev_summary.get('revised_evaluator_hash')}"
                ],
                needs_review=needs,
                suspected_invalid=suspected,
            )
        )

    # sanity: also note revision flipped cells in basis already via rev status
    _ = validity_report
    return rows, needs_review


def translate_qwen_run002(run_id: str, model: str) -> tuple[list[dict[str, Any]], list[str]]:
    run_dir = RESULTS / run_id
    rows: list[dict[str, Any]] = []
    needs_review: list[str] = []

    for cell_dir in sorted((run_dir / "cells").iterdir()):
        art_path = cell_dir / "artifact.json"
        if not art_path.exists():
            continue
        art = _load(art_path)
        cell_id = art["cell_id"]
        gates = _gates_from_artifact(art)
        fl = art.get("failure_layer") if isinstance(art.get("failure_layer"), dict) else {}
        layer = fl.get("primary_layer")
        status = art.get("evaluator_status")
        if status == "PASSED":
            layer = "PASSED"
        elif layer is None:
            layer = _layer_from_evaluator_status(status)

        mechanism: list[str] = []
        basis = [
            f"{run_id}/cells/.../artifact.json failure_layer + evaluator_status",
        ]
        needs = False
        suspected = bool(art.get("suspected_invalid"))
        validity = "VALID_MODEL_OUTCOME"

        if suspected:
            # Keep SUSPECTED mark; map formal validity to PENDING_REVIEW
            validity = "PENDING_REVIEW"
            needs = True
            mechanism.append("needs_human_review")
            basis.append(
                "artifact.suspected_invalid + summary.think_tag_residue_note "
                "(maintain SUSPECTED; no rerun)"
            )
            needs_review.append(cell_id)

        raw_path = cell_dir / "raw_response.txt"
        raw = raw_path.read_text(encoding="utf-8", errors="replace") if raw_path.exists() else ""
        if _is_degenerate(raw):
            if "degenerate_repetition" not in mechanism:
                mechanism.append("degenerate_repetition")
            basis.append("raw_response degenerate_repetition heuristic")
            if layer is None:
                layer = "L1"

        # STRUCTURAL/LATEX already L3 in some qwen preliminary labels — keep existing
        # primary_layer from artifact when present (do not re-judge).
        if fl.get("primary_layer") is not None and status != "PASSED":
            layer = fl.get("primary_layer")
            basis.append("kept artifact.failure_layer.primary_layer (no re-judge)")

        if layer is None:
            needs = True
            if "needs_human_review" not in mechanism:
                mechanism.append("needs_human_review")
            if cell_id not in needs_review:
                needs_review.append(cell_id)
            validity = "PENDING_REVIEW"

        rows.append(
            _row(
                run_id=run_id,
                model=model,
                art=art,
                v2_layer=layer,
                v2_validity=validity,
                mechanism=mechanism,
                gates=gates,
                basis=basis,
                needs_review=needs,
                suspected_invalid=suspected or None,
            )
        )
    return rows, needs_review


def translate_qwen_run001(run_id: str, model: str) -> tuple[list[dict[str, Any]], list[str]]:
    run_dir = RESULTS / run_id
    marker = _load(run_dir / "OUTCOME_VALIDITY.json")
    rows: list[dict[str, Any]] = []
    for cell_dir in sorted((run_dir / "cells").iterdir()):
        art_path = cell_dir / "artifact.json"
        if not art_path.exists():
            continue
        art = _load(art_path)
        gates = _gates_from_artifact(art)
        fl = art.get("failure_layer") if isinstance(art.get("failure_layer"), dict) else {}
        layer = fl.get("primary_layer") or _layer_from_evaluator_status(art.get("evaluator_status"))
        # Batch infrastructure invalidation; symptom layer retained from original labels
        rows.append(
            _row(
                run_id=run_id,
                model=model,
                art=art,
                v2_layer=layer if art.get("evaluator_status") != "PASSED" else "PASSED",
                v2_validity="INVALID_INFRASTRUCTURE",
                mechanism=["infrastructure_failure"],
                gates=gates,
                basis=[
                    f"{run_id}/OUTCOME_VALIDITY.json",
                    "artifact.outcome_validity=INVALID_INFRASTRUCTURE (batch)",
                    marker.get("outcome_validity_annotation", {}).get("reason_summary")
                    or "run_001 call-layer defects",
                ],
                needs_review=False,
            )
        )
    return rows, []


def _cross_tab(rows: list[dict[str, Any]]) -> dict[str, Any]:
    # model × condition × L × validity
    ctr: Counter[tuple[str, str, str, str]] = Counter()
    by_run: Counter[tuple[str, str, str, str, str]] = Counter()
    for r in rows:
        model = r["model"]
        cond = r["condition"] or "?"
        layer = str(r["v2"]["primary_failure_layer"])
        validity = r["v2"]["outcome_validity"]
        run_id = r["run_id"]
        ctr[(model, cond, layer, validity)] += 1
        by_run[(run_id, model, cond, layer, validity)] += 1

    nested: dict[str, Any] = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for (model, cond, layer, validity), n in sorted(ctr.items()):
        nested[model][cond][layer][validity] = n

    nested_by_run: dict[str, Any] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    )
    for (run_id, model, cond, layer, validity), n in sorted(by_run.items()):
        nested_by_run[run_id][model][cond][layer][validity] = n

    # model × condition × L (summed over validity) — overall
    layer_only: Counter[tuple[str, str, str]] = Counter()
    for (model, cond, layer, _v), n in ctr.items():
        layer_only[(model, cond, layer)] += n
    layer_table: dict[str, Any] = defaultdict(lambda: defaultdict(dict))
    for (model, cond, layer), n in sorted(layer_only.items()):
        layer_table[model][cond][layer] = n

    # Prefer formal capability runs for the compact layer table
    formal_runs = {
        GEMINI_RUN,
        QWEN_4B_002,
        QWEN_9B_002,
    }
    layer_formal: Counter[tuple[str, str, str]] = Counter()
    for (run_id, model, cond, layer, _v), n in by_run.items():
        if run_id in formal_runs:
            layer_formal[(model, cond, layer)] += n
    layer_table_formal: dict[str, Any] = defaultdict(lambda: defaultdict(dict))
    for (model, cond, layer), n in sorted(layer_formal.items()):
        layer_table_formal[model][cond][layer] = n

    return {
        "model_x_condition_x_layer_x_validity": nested,
        "model_x_condition_x_layer_x_validity_by_run": nested_by_run,
        "model_x_condition_x_layer": layer_table,
        "model_x_condition_x_layer_formal_runs_only": layer_table_formal,
        "formal_runs": sorted(formal_runs),
    }


def main() -> int:
    all_rows: list[dict[str, Any]] = []
    all_needs: list[dict[str, str]] = []

    g_rows, g_needs = translate_gemini()
    all_rows.extend(g_rows)
    all_needs.extend({"run_id": GEMINI_RUN, "cell_id": c} for c in g_needs)

    for run_id, model in (
        (QWEN_4B_002, "qwen3.5:4b"),
        (QWEN_9B_002, "qwen3.5:9b"),
    ):
        rows, needs = translate_qwen_run002(run_id, model)
        all_rows.extend(rows)
        all_needs.extend({"run_id": run_id, "cell_id": c} for c in needs)

    for run_id, model in (
        (QWEN_4B_001, "qwen3.5:4b"),
        (QWEN_9B_001, "qwen3.5:9b"),
    ):
        rows, needs = translate_qwen_run001(run_id, model)
        all_rows.extend(rows)
        all_needs.extend({"run_id": run_id, "cell_id": c} for c in needs)

    validity_by_run: dict[str, Counter[str]] = defaultdict(Counter)
    for r in all_rows:
        validity_by_run[r["run_id"]][r["v2"]["outcome_validity"]] += 1

    payload = {
        "standard": "failure_classification_standard_v2",
        "standard_path": "docs/standards/failure_classification_standard_v2.md",
        "standard_git_blob_hash": STANDARD_BLOB,
        "policy": {
            "artifacts_mutated": False,
            "model_calls": 0,
            "rescoring": False,
            "translation_only": True,
        },
        "runs_included": [
            GEMINI_RUN,
            QWEN_4B_002,
            QWEN_9B_002,
            QWEN_4B_001,
            QWEN_9B_001,
        ],
        "cell_count": len(all_rows),
        "needs_human_review_count": len(all_needs),
        "needs_human_review": all_needs,
        "validity_distribution_by_run": {
            run: dict(counter) for run, counter in sorted(validity_by_run.items())
        },
        "cross_tab": _cross_tab(all_rows),
        "cells": all_rows,
    }

    OUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "output": str(OUT_PATH),
                "cell_count": len(all_rows),
                "needs_human_review_count": len(all_needs),
                "validity_distribution_by_run": payload["validity_distribution_by_run"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    # classify_cell import retained for future runner wiring smoke
    _ = classify_cell
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
