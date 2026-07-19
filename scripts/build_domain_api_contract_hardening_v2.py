"""Build deterministic no-model Domain API Contract Hardening v2 artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (  # noqa: E402
    TASK_DOMAIN_APIS, build_condition_prompt, prompt_sha256,
)
from agent_tools.finals_rebuild.domain_answer_assembly import TASK_OUTPUT_ASSEMBLY  # noqa: E402
from agent_tools.finals_rebuild.domain_api_ssot import (  # noqa: E402
    API_CLASSIFICATION, DOMAIN_API_SSOT, render_supported_api_reference,
    runtime_public_inventory, validate_inventory,
)
from agent_tools.finals_rebuild.git_blob_hash import sha256_git_blob_lf  # noqa: E402
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, load_pool_manifest  # noqa: E402

OUT = ROOT / "docs/experiments/results/domain_api_contract_hardening_v2"
OLD_DIFF = ROOT / "docs/experiments/results/math16_domain_api_ssot_prompt_hash_diff.json"
FREEZE = ROOT / "docs/experiments/results/math16_latex_v1_freeze_closeout_report.json"
SKILL_DOC = ROOT / "agent_skills/domain_api_contract_v2/SKILL.md"


def sha(path: Path) -> str:
    """SHA-256 of git blob content (LF). Never hash raw CRLF working-tree bytes."""
    return sha256_git_blob_lf(path, repo_root=ROOT)


def main() -> int:
    errors = validate_inventory()
    if errors:
        raise SystemExit(f"inventory errors: {errors}")
    OUT.mkdir(parents=True, exist_ok=True)
    SKILL_DOC.parent.mkdir(parents=True, exist_ok=True)
    SKILL_DOC.write_text(
        "---\nname: domain-api-contract-v2\ndescription: Generated typed Domain API reference for formal Ab2d/Qwen prompts.\n---\n\n"
        + render_supported_api_reference(), encoding="utf-8"
    )
    inventory = {
        "inventory_count": len(runtime_public_inventory()),
        "classification_counts": {c: list(API_CLASSIFICATION.values()).count(c) for c in sorted(set(API_CLASSIFICATION.values()))},
        "apis": [{"name": n, "classification": API_CLASSIFICATION[n]} for n in runtime_public_inventory()],
    }
    (OUT / "api_inventory.json").write_text(json.dumps(inventory, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    (OUT / "typed_contracts.json").write_text(json.dumps(DOMAIN_API_SSOT, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    (OUT / "task_output_assembly.json").write_text(json.dumps(TASK_OUTPUT_ASSEMBLY, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

    prior = json.loads(OLD_DIFF.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    old = {(r["task_id"], r["condition"]): r["prompt_sha256"] for r in freeze["prompt_hashes_48"]}
    # The committed SSOT validation diff records the six cells changed after
    # the original freeze; those new hashes are the aa33a6e1 baseline.
    for r in prior["changed_cells"]:
        old[(r["task_id"], r["condition"])] = r["new_prompt_hash"]
    tasks = {t["task_id"]: t for t in load_pool_manifest()["tasks"]}
    changed, unchanged = [], []
    for tid, task in sorted(tasks.items()):
        for condition in ("ab1", "ab2g", "ab2d"):
            new_hash = prompt_sha256(build_condition_prompt(condition, task, frozen_for_prompt(task)))
            old_hash = old[(tid, condition)]
            routed = [a["name"] for a in TASK_DOMAIN_APIS[tid]] if condition == "ab2d" else []
            row = {"task_id":tid,"condition":condition,"old_prompt_hash":old_hash,"new_prompt_hash":new_hash,"changed":old_hash != new_hash,"routed_apis":routed}
            if row["changed"]:
                row["hash_change_reason"] = "typed SSOT return contract and/or radical presentation API routing"
                changed.append(row)
            else:
                unchanged.append(row)
    unexpected = [r for r in changed if r["condition"] != "ab2d"]
    diff = {"baseline_head":"aa33a6e1e24f423c62526c4c02d7019d6b778fb1","cells":48,"changed_count":len(changed),"unchanged_count":len(unchanged),"changed_cells":changed,"unchanged_cells":unchanged,"unexpected_changes":unexpected,"stop":bool(unexpected)}
    (OUT / "prompt_hash_diff_48.json").write_text(json.dumps(diff, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

    components = {
        "toolbox": sha(ROOT / "core/prompts/domain_function_library.py"),
        "ssot": sha(ROOT / "agent_tools/finals_rebuild/domain_api_ssot.py"),
        "skill": sha(SKILL_DOC),
        "answer_assembly": sha(ROOT / "agent_tools/finals_rebuild/domain_answer_assembly.py"),
        "answer_contract": sha(ROOT / "agent_tools/finals_rebuild/math_answer_contracts.py"),
        "evaluator": sha(ROOT / "agent_tools/finals_rebuild/math16_oracles.py"),
    }
    summary = {
        "version": "Ab2d-v2-candidate",
        "no_model": True,
        "hash_basis": "git_blob_lf",
        "inventory": inventory["classification_counts"],
        "supported_count": len(DOMAIN_API_SSOT),
        "prompt_diff": {"changed": len(changed), "unchanged": len(unchanged)},
        "component_sha256": components,
        "preflight_requirements": [
            "runtime inventory == classification",
            "all routed APIs SUPPORTED_PUBLIC",
            "runtime probes == typed SSOT",
            "prompt and generated SKILL lines from SSOT",
            "task assembly covers 16/16",
            "JSON round-trip",
            "Math16 preflight",
        ],
        "stop": bool(unexpected),
    }
    (OUT / "preflight_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return int(summary["stop"])


if __name__ == "__main__":
    raise SystemExit(main())
