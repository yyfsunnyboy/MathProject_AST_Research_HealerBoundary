"""Production allowlist chained repair on Qwen4B v2 113-10 Ab2d.

Does NOT call generation models. Does NOT modify raw artifacts.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_research_healer_protocol import (  # noqa: E402
    provenance_to_dict,
    research_result_to_dict,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (  # noqa: E402
    RECOMMENDED_CHAIN_MAX_PASSES,
    RULE_ALLOWLIST,
    MathHealerRunner,
)
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response  # noqa: E402

OUT = (
    ROOT
    / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2"
    / "qwen4b_v2_113_10_production_chain_01"
)
CELL = (
    ROOT
    / "docs/experiments/results/ce115_exam_ext_contract_aligned_v2_qwen4b_01/cells"
    / "qwen3_5_4b__ce115_ext_113_10_factorization_l1__ab2d__seed_2026071301"
)
TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
PROMOTION_AUDIT = (
    ROOT
    / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2"
    / "rule_promotion_audit_01.json"
)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    art = json.loads((CELL / "artifact.json").read_text(encoding="utf-8"))
    source = (CELL / "extracted_candidate.py").read_text(encoding="utf-8").replace(
        "\r\n", "\n"
    )
    frozen = dict(art["frozen_parameters"])
    task = None
    for line in TASK_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("task_id") == art["task_id"]:
            task = row
            break
    if task is None:
        raise KeyError(art["task_id"])

    before, _, before_details = classify_response(
        source, {"oracle_payload": frozen}, task
    )
    result = MathHealerRunner(max_passes=RECOMMENDED_CHAIN_MAX_PASSES).run(
        source,
        context={"frozen": frozen, "task": task},
    )
    after, _, after_details = classify_response(
        result.output_source, {"oracle_payload": frozen}, task
    )

    (OUT / "repaired_candidate.py").write_text(
        result.output_source, encoding="utf-8", newline="\n"
    )
    summary = {
        "real_model_calls": 0,
        "cell_id": art.get("cell_id"),
        "production_allowlist": list(RULE_ALLOWLIST),
        "max_passes": RECOMMENDED_CHAIN_MAX_PASSES,
        "before_outcome": before,
        "after_outcome": after,
        "rescue_to_pass": after == "passed",
        "healer": research_result_to_dict(result),
        "provenance": [provenance_to_dict(p) for p in result.provenance],
        "changed_chain": [
            {
                "chain_position": p.chain_position,
                "rule_id": p.selected_rule_id,
                "pass_index": p.pass_index,
            }
            for p in result.provenance
            if p.changed
        ],
        "before_gates": (before_details or {}).get("evaluation_gates"),
        "after_gates": (after_details or {}).get("evaluation_gates"),
        "raw_artifact_unmodified": True,
        "promotion_audit": str(PROMOTION_AUDIT.relative_to(ROOT)).replace("\\", "/"),
    }
    (OUT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "out": str(OUT),
                "before": before,
                "after": after,
                "rescue_to_pass": after == "passed",
                "changed_chain": summary["changed_chain"],
                "real_model_calls": 0,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
