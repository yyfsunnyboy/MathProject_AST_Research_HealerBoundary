# -*- coding: utf-8 -*-
"""Math16 Ab2d+full V2: same runtime contract as ab2d_domain_menu_v2, plus a
task-specific solving scaffold.

The ONLY allowed difference from ab2d_domain_menu_v2 for the same task_id is the block
appended by this module (`full_plan_scaffold_block`) -- everything before it (system
header, Domain API menu, shared output contract, task-specific answer contract, the
zero-argument runtime skeleton, frozen_params) is byte-identical, because it is literally
produced by calling `math16_ab2d_domain_menu_v2.build_domain_menu_prompt_v2()`.

The appended scaffold gives the concrete API selection, call order, parameter binding,
return-value destructuring, JSON-safe conversion, and correct_answer assembly for this
task, computed via genuine Domain API composition (never a hardcoded literal standing in
for the answer) -- sourced from `math16_ab2d_v2_scaffolds.TASK_SCAFFOLDS_V2`, which was
itself mined from an already-passing V1 cell and independently re-verified against the
real oracle evaluator (see scripts/preflight_math16_ab2d_v2.py).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import re

from agent_tools.finals_rebuild.domain_api_ssot import validate_inventory
from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
    DOMAIN_BLOCK_BEGIN,
    DOMAIN_BLOCK_END,
    DOMAIN_OPS,
    TASK_ANSWER_CONTRACT_HEADER,
    build_domain_template,
    other_domain_ops,
)
from agent_tools.finals_rebuild.math16_ab2d_domain_menu_v2 import (
    RUNTIME_SKELETON_HEADER,
    build_domain_menu_prompt_v2,
)
from agent_tools.finals_rebuild.math16_ab2d_v2_scaffolds import TASK_SCAFFOLDS_V2
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id

ROOT = Path(__file__).resolve().parents[2]

CONDITION = "ab2d_full_v2"
EXPERIMENT_ID = "math16_ab2d_menu_vs_full_runtime_contract_v2"

PROMPT_DIR_REL = "docs/experiments/prompts/ab2d_full_v2/prompts"
MANIFEST_REL = "docs/experiments/prompts/ab2d_full_v2/manifest.json"

SCAFFOLD_HEADER = "## Task-specific scaffold (full-plan only)"


def _extra_imports_block(scaffold: dict[str, Any]) -> str:
    extra = scaffold.get("extra_imports") or []
    if not extra:
        return ""
    return "\n".join(extra) + "\n"


def full_plan_scaffold_block(task: dict[str, Any]) -> str:
    task_id = task["task_id"]
    scaffold = TASK_SCAFFOLDS_V2[task_id]
    domain = task["domain_ops"]
    steps = "\n".join(scaffold["full_plan_steps"])
    extra_imports = _extra_imports_block(scaffold)
    frozen_literal = json.dumps(scaffold["frozen_literal"], ensure_ascii=False, sort_keys=True)
    code = f'''```python
from core.prompts.domain_function_library import {domain}
{extra_imports}
def generate(level=1, **kwargs):
    # kwargs is always {{}} here -- see the Runtime binding contract above.
    frozen = {frozen_literal}
    question_text = "..."  # use ## Frozen task description above, verbatim
{scaffold["full_plan_body"]}
    return {{
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen,
    }}
```'''
    return (
        f"{SCAFFOLD_HEADER}\n"
        f"Concrete API selection, call order, and assembly for `{task_id}` "
        "(computed via genuine Domain API composition; not a hardcoded ground-truth value):\n"
        f"{steps}\n\n"
        f"{code}\n"
    )


def build_ab2d_full_prompt_v2(task: dict[str, Any], template_text: str | None = None) -> str:
    menu_prompt = build_domain_menu_prompt_v2(task, template_text)
    scaffold = full_plan_scaffold_block(task).rstrip()
    return (menu_prompt.rstrip() + "\n\n" + scaffold + "\n").replace("\r\n", "\n")


def validate_prompt_static_v2_full(prompt: str, domain_ops: str) -> list[str]:
    """Full-plan checks: everything domain-menu-v2 checks EXCEPT the numbered-steps ban
    (V1's SOLUTION_PLAN_PATTERNS), since full-plan is deliberately allowed -- and required
    -- to contain a numbered task-specific scaffold. See validate_prompt_static_v2_menu_only
    in math16_ab2d_domain_menu_v2.py for the domain-menu-side ban.
    """
    errors: list[str] = []
    if DOMAIN_BLOCK_BEGIN not in prompt or DOMAIN_BLOCK_END not in prompt:
        errors.append("missing_domain_block_markers")
    if TASK_ANSWER_CONTRACT_HEADER not in prompt:
        errors.append("missing_task_specific_answer_contract")
    if RUNTIME_SKELETON_HEADER not in prompt:
        errors.append("missing_runtime_skeleton_block")
    if SCAFFOLD_HEADER not in prompt:
        errors.append("missing_task_specific_scaffold")
    for other in other_domain_ops(domain_ops):
        if other in prompt:
            errors.append(f"cross_domain_exposure:{other}")
    if re.search(r"(?i)expected[_ ]answer\s*[:=]", prompt):
        errors.append("expected_answer_label")
    if "task_id →" in prompt or "task_id->" in prompt:
        errors.append("task_id_lookup_arrow")
    callout_idx = prompt.find(RUNTIME_SKELETON_HEADER)
    fence_idx = prompt.find("```python", callout_idx) if callout_idx >= 0 else -1
    start = 0
    while True:
        idx = prompt.find('kwargs.get("frozen_params")', start)
        if idx < 0:
            break
        if callout_idx < 0 or not (callout_idx <= idx < fence_idx):
            errors.append("kwargs_get_frozen_params_outside_callout")
        start = idx + 1
    return errors


def build_all_prompts_v2(root: Path | None = None) -> dict[str, Any]:
    root = root or ROOT
    inv_errors = validate_inventory()
    if inv_errors:
        raise RuntimeError(f"SSOT inventory invalid: {inv_errors}")

    templates = {d: build_domain_template(d) for d in DOMAIN_OPS}
    prompt_dir = root / PROMPT_DIR_REL
    prompt_dir.mkdir(parents=True, exist_ok=True)

    pool = load_pool_manifest(root)
    tasks = tasks_by_id(root)
    if set(TASK_SCAFFOLDS_V2) != set(pool["task_ids"]):
        raise RuntimeError("TASK_SCAFFOLDS_V2 task set mismatch vs pool")

    prompts: dict[str, str] = {}
    task_records: list[dict[str, Any]] = []
    for tid in pool["task_ids"]:
        task = tasks[tid]
        domain = task["domain_ops"]
        prompt = build_ab2d_full_prompt_v2(task, templates[domain])
        errs = validate_prompt_static_v2_full(prompt, domain)
        if errs:
            raise RuntimeError(f"static validation failed for {tid}: {errs}")
        path = prompt_dir / f"{tid}.txt"
        path.write_text(prompt, encoding="utf-8", newline="\n")
        prompts[tid] = prompt
        task_records.append(
            {
                "condition": CONDITION,
                "task_id": tid,
                "domain_ops": domain,
                "oracle_type": task["oracle_type"],
                "prompt_path": f"{PROMPT_DIR_REL}/{tid}.txt".replace("\\", "/"),
                "char_count": len(prompt),
            }
        )

    manifest = {
        "manifest_id": "math16_ab2d_full_v2_freeze_v1",
        "condition": CONDITION,
        "experiment_id": EXPERIMENT_ID,
        "prompt_revision": "ab2d_full_runtime_contract_v2",
        "n_tasks": len(task_records),
        "pool_id": pool["pool_id"],
        "pool_identity_hash": pool["pool_identity_hash"],
        "task_freeze_hash": pool["task_freeze_hash"],
        "prompt_dir": PROMPT_DIR_REL,
        "shared_prefix_source": "agent_tools/finals_rebuild/math16_ab2d_domain_menu_v2.py:build_domain_menu_prompt_v2",
        "v2_addition": f"{SCAFFOLD_HEADER} (task-specific API scaffold, from math16_ab2d_v2_scaffolds.TASK_SCAFFOLDS_V2)",
        "tasks": task_records,
    }
    manifest_path = root / MANIFEST_REL
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return {"manifest": manifest, "prompts": prompts}


if __name__ == "__main__":
    result = build_all_prompts_v2()
    print(json.dumps({"n_tasks": result["manifest"]["n_tasks"]}, ensure_ascii=False))
