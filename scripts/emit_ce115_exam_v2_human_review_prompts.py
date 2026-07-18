"""Emit contract-aligned v2 prompts + API cards for human review only.

real_model_calls=0. Does not call Gemini/Qwen. Does not overwrite v1 artifacts.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_contract_aligned_ablation_v2 import (
    LINEAGE_ID,
    TASK_DOMAIN_APIS,
    assert_v2_ablation_invariants,
    build_condition_prompt_v2,
    canonical_prompt_hash,
    verify_generic_body_frozen_vs_v1,
)
from agent_tools.finals_rebuild.ce115_exam_external_validation import (
    FROZEN_PAYLOADS,
    PROVENANCE,
    TASK_IDS,
)
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

SEED = 2026071301
MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
OUT = ROOT / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/human_review_prompts_02"
TASK_114_02 = "ce115_ext_114_02_polynomial_simplify_l1"

# Adoption policy is sourced from TASK_DOMAIN_APIS[*]["adoption"] at emit time.
ADOPTION: dict[str, dict[str, str]] = {
    tid: {api["name"]: api.get("adoption", "required") for api in apis}
    for tid, apis in TASK_DOMAIN_APIS.items()
}


def load_tasks() -> dict[str, dict]:
    rows = [
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by = {r["task_id"]: r for r in rows}
    return {tid: by[tid] for tid in TASK_IDS}


def main() -> None:
    verify_generic_body_frozen_vs_v1()
    if OUT.exists():
        raise SystemExit(f"REFUSE: output exists {OUT}")
    OUT.mkdir(parents=True)
    prompts_dir = OUT / "prompts"
    prompts_dir.mkdir()
    tasks = load_tasks()
    hashes: dict[str, dict[str, str]] = {}
    cards: dict[str, object] = {}

    for tid in TASK_IDS:
        task = tasks[tid]
        sampled = sample_task_parameters(task, SEED)
        frozen = {
            "task_id": tid,
            "oracle_type": task["oracle_type"],
            "oracle_payload": sampled["oracle_payload"],
            "repeat_seed": SEED,
        }
        assert frozen["oracle_payload"] == FROZEN_PAYLOADS[tid]
        prompts = assert_v2_ablation_invariants(task, frozen)
        hashes[tid] = {}
        # Always emit Ab2d-v2
        for cond in ("ab2d",):
            text = prompts[cond]
            assert text == build_condition_prompt_v2(cond, task, frozen)
            h = canonical_prompt_hash(text)
            hashes[tid][cond] = h
            stem = f"{tid}__{cond}-v2"
            (prompts_dir / f"{stem}.txt").write_text(text, encoding="utf-8")
            (prompts_dir / f"{stem}.meta.json").write_text(
                json.dumps(
                    {
                        "task_id": tid,
                        "condition": f"{cond}-v2",
                        "canonical_prompt_hash": h,
                        "lineage_id": LINEAGE_ID,
                        "seed": SEED,
                        "chars": len(text),
                        "provenance": PROVENANCE[tid],
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
        # 114-02 also Ab1/Ab2g
        if tid == TASK_114_02:
            for cond in ("ab1", "ab2g"):
                text = prompts[cond]
                h = canonical_prompt_hash(text)
                hashes[tid][cond] = h
                stem = f"{tid}__{cond}-v2"
                (prompts_dir / f"{stem}.txt").write_text(text, encoding="utf-8")
                (prompts_dir / f"{stem}.meta.json").write_text(
                    json.dumps(
                        {
                            "task_id": tid,
                            "condition": f"{cond}-v2",
                            "canonical_prompt_hash": h,
                            "lineage_id": LINEAGE_ID,
                            "seed": SEED,
                            "chars": len(text),
                            "provenance": PROVENANCE[tid],
                        },
                        indent=2,
                        ensure_ascii=False,
                    )
                    + "\n",
                    encoding="utf-8",
                )

        api_rows = []
        for api in TASK_DOMAIN_APIS[tid]:
            api_rows.append(
                {
                    "name": api["name"],
                    "import": api["import"],
                    "signature": api["signature"],
                    "returns": api["returns"],
                    "legal_input_grammar_notes": api.get("notes", ""),
                    "necessity": api.get("necessity", ""),
                    "adoption": ADOPTION[tid].get(api["name"], "required"),
                    "json_serialization": (
                        "via FractionOps.to_exact / to_degree_map / normalize_term_list "
                        "when return is Fraction or non-JSON leaf; otherwise JSON-native"
                    ),
                }
            )
        cards[tid] = {
            "exam": PROVENANCE[tid],
            "required_operations": [],  # filled from coverage matrix below
            "selected_apis": api_rows,
        }

    coverage = json.loads(
        (ROOT / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/operation_to_api_coverage_matrix.json").read_text(
            encoding="utf-8"
        )
    )
    by_cov = {row["task_id"]: row for row in coverage["matrix"]}
    for tid, card in cards.items():
        card["required_operations"] = by_cov[tid]["required_operations"]
        card["coverage"] = by_cov[tid]["coverage"]
        card["notes"] = by_cov[tid]["notes"]

    (OUT / "per_task_api_cards.json").write_text(
        json.dumps(cards, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (OUT / "canonical_prompt_hashes.json").write_text(
        json.dumps({"lineage_id": LINEAGE_ID, "seed": SEED, "hashes": hashes}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    # Sync analysis freeze
    freeze = ROOT / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/canonical_prompt_hashes.json"
    freeze.write_text(
        json.dumps({"lineage_id": LINEAGE_ID, "seed": SEED, "hashes": hashes}, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    index = {
        "lineage_id": LINEAGE_ID,
        "purpose": "human_review_only",
        "real_model_calls": 0,
        "prompts": sorted(p.name for p in prompts_dir.glob("*.txt")),
        "hashes": hashes,
        "files": {
            "prompts_dir": str(prompts_dir.relative_to(ROOT)),
            "api_cards": str((OUT / "per_task_api_cards.json").relative_to(ROOT)),
            "inventory": "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/production_api_inventory.json",
            "coverage": "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/operation_to_api_coverage_matrix.json",
            "mismatches": "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/api_mismatches_found_fixed.json",
        },
    }
    (OUT / "INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"emitted": len(index["prompts"]), "out": str(OUT), "real_model_calls": 0}, indent=2))


if __name__ == "__main__":
    main()
