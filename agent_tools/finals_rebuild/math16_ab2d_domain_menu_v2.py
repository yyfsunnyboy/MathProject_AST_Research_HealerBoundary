# -*- coding: utf-8 -*-
"""Math16 Ab2d+domain-menu V2: honest zero-argument runtime contract.

V1 (agent_tools/finals_rebuild/math16_ab2d_domain_menu.py) never states that the evaluator
calls `generate()` with zero arguments, and never shows a concrete skeleton demonstrating
it -- the dominant Qwen failure mode in the frozen 480-cell run was models writing
`kwargs.get("frozen_params")` and getting None (see
docs/experiments/results/Math16/math16_qwen_320cell_low_passrate_forensic_v1.md).

V2 reuses every V1 building block verbatim (SYSTEM_HEADER, domain API menu rendering,
task-specific answer contract, frozen_params block) and inserts exactly one new section
between the answer contract and the task block: a per-task zero-argument runtime skeleton
that (a) states the real contract, (b) forbids kwargs.get("frozen_params") explicitly, and
(c) shows the exact return-dict shape for this task with `...` placeholders for the parts
that require choosing which Domain API to call -- domain-menu never fills those in.

V1 module/prompt files are only ever imported, never written to.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.domain_api_ssot import validate_inventory
from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
    DOMAIN_BLOCK_BEGIN,
    DOMAIN_BLOCK_END,
    DOMAIN_OPS,
    SYSTEM_HEADER,
    build_domain_template,
    build_task_block,
    build_task_specific_answer_contract_block,
    extract_domain_api_block,
    other_domain_ops,
    validate_prompt_static as _v1_validate_prompt_static,
)
from agent_tools.finals_rebuild.math16_ab2d_v2_scaffolds import TASK_SCAFFOLDS_V2
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id

ROOT = Path(__file__).resolve().parents[2]

CONDITION = "ab2d_domain_menu_v2"
EXPERIMENT_ID = "math16_ab2d_menu_vs_full_runtime_contract_v2"

PROMPT_DIR_REL = "docs/experiments/prompts/ab2d_domain_menu_v2/prompts"
MANIFEST_REL = "docs/experiments/prompts/ab2d_domain_menu_v2/manifest.json"

RUNTIME_SKELETON_HEADER = "## Runtime binding contract (zero-argument evaluator call)"

# The one place this exact anti-pattern string is allowed to appear anywhere in a V2
# prompt -- inside this prose callout, never inside a runnable code fence.
FORBIDDEN_CALLOUT = (
    "At execution time the evaluator calls your function as `generate()` -- zero "
    "arguments. `level` defaults to 1 and `**kwargs` is always `{}`. Do NOT do this:\n"
    "    kwargs.get(\"frozen_params\")   # kwargs is empty -- this is always None, and\n"
    "                                    # any code that depends on it will fail.\n"
    "Do not read frozen values from `kwargs` in any form -- not "
    "`kwargs.get(\"frozen_params\")`, not `kwargs[\"frozen_params\"]`, not any other\n"
    "`kwargs.get(...)` lookup. The frozen values for this task are given below as plain\n"
    "Python literals; assign them to a local variable inside `generate()` and use them\n"
    "directly -- do not expect them to arrive as function arguments."
)


def _placeholder(schema: Any) -> Any:
    if schema == "int":
        return "..."
    if isinstance(schema, dict):
        return {k: _placeholder(v) for k, v in schema.items()}
    return "..."


def _render_placeholder_answer(schema: Any, indent: str = "        ") -> str:
    """Render a Python-literal-shaped placeholder (values replaced with `...`)."""
    if schema == "int":
        return "...  # int, see ## Task-specific answer contract"
    if isinstance(schema, dict):
        lines = ["{"]
        for key, value in schema.items():
            if isinstance(value, dict):
                nested = _render_placeholder_answer(value, indent + "    ")
                lines.append(f'{indent}    "{key}": {nested},')
            else:
                lines.append(f'{indent}    "{key}": ...,  # {value}')
        lines.append(f"{indent}}}")
        return "\n".join(lines)
    return "..."


def build_runtime_skeleton_block_v2(task: dict[str, Any]) -> str:
    task_id = task["task_id"]
    scaffold = TASK_SCAFFOLDS_V2[task_id]
    frozen_literal = json.dumps(scaffold["frozen_literal"], ensure_ascii=False, sort_keys=True)
    answer_repr = _render_placeholder_answer(scaffold["answer_schema"])
    code = f'''```python
def generate(level=1, **kwargs):
    # kwargs is always {{}} here -- see the Runtime binding contract above.
    frozen = {frozen_literal}
    question_text = "..."  # use ## Frozen task description below, verbatim
    correct_answer = {answer_repr}
    # ^ fill in the `...` placeholders yourself by calling Domain API methods from the
    # menu above -- domain-menu does not name which method(s) or call order to use.
    return {{
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen,
    }}
```'''
    return (
        f"{RUNTIME_SKELETON_HEADER}\n"
        f"{FORBIDDEN_CALLOUT}\n\n"
        "Zero-argument skeleton for this task's frozen_params "
        f"(`{task_id}`):\n"
        f"{code}\n"
    )


def build_domain_menu_prompt_v2(task: dict[str, Any], template_text: str | None = None) -> str:
    domain = task["domain_ops"]
    if template_text is None:
        template_text = build_domain_template(domain)
    block = extract_domain_api_block(template_text)
    wrapped = f"{DOMAIN_BLOCK_BEGIN}\n{block.rstrip()}\n{DOMAIN_BLOCK_END}"
    parts = [
        SYSTEM_HEADER.rstrip(),
        "",
        f"Domain for this task: {domain}.",
        "",
        wrapped,
        "",
        build_task_specific_answer_contract_block(task).rstrip(),
        "",
        build_runtime_skeleton_block_v2(task).rstrip(),
        "",
        build_task_block(task).rstrip(),
        "",
    ]
    return "\n".join(parts).replace("\r\n", "\n")


def validate_prompt_static_v2(prompt: str, domain_ops: str) -> list[str]:
    """V1's static checks plus a V2-specific kwargs.get('frozen_params') placement check."""
    errors = list(_v1_validate_prompt_static(prompt, domain_ops))
    if RUNTIME_SKELETON_HEADER not in prompt:
        errors.append("missing_runtime_skeleton_block")
    callout_idx = prompt.find(RUNTIME_SKELETON_HEADER)
    for idx in _find_all(prompt, 'kwargs.get("frozen_params")'):
        # Only allowed occurrence is inside the callout, before the first ```python fence
        # that follows RUNTIME_SKELETON_HEADER.
        fence_idx = prompt.find("```python", callout_idx) if callout_idx >= 0 else -1
        if callout_idx < 0 or not (callout_idx <= idx < fence_idx):
            errors.append("kwargs_get_frozen_params_outside_callout")
    return errors


def _find_all(text: str, sub: str) -> list[int]:
    out = []
    start = 0
    while True:
        idx = text.find(sub, start)
        if idx < 0:
            break
        out.append(idx)
        start = idx + 1
    return out


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
        raise RuntimeError(
            "TASK_SCAFFOLDS_V2 task set mismatch: "
            f"missing={set(pool['task_ids']) - set(TASK_SCAFFOLDS_V2)} "
            f"extra={set(TASK_SCAFFOLDS_V2) - set(pool['task_ids'])}"
        )

    prompts: dict[str, str] = {}
    task_records: list[dict[str, Any]] = []
    for tid in pool["task_ids"]:
        task = tasks[tid]
        domain = task["domain_ops"]
        prompt = build_domain_menu_prompt_v2(task, templates[domain])
        errs = validate_prompt_static_v2(prompt, domain)
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
        "manifest_id": "math16_ab2d_domain_menu_v2_freeze_v1",
        "condition": CONDITION,
        "experiment_id": EXPERIMENT_ID,
        "prompt_revision": "ab2d_domain_menu_runtime_contract_v2",
        "n_tasks": len(task_records),
        "pool_id": pool["pool_id"],
        "pool_identity_hash": pool["pool_identity_hash"],
        "task_freeze_hash": pool["task_freeze_hash"],
        "prompt_dir": PROMPT_DIR_REL,
        "v1_source_reused": [
            "agent_tools/finals_rebuild/math16_ab2d_domain_menu.py:SYSTEM_HEADER",
            "agent_tools/finals_rebuild/math16_ab2d_domain_menu.py:build_domain_template",
            "agent_tools/finals_rebuild/math16_ab2d_domain_menu.py:build_task_specific_answer_contract_block",
            "agent_tools/finals_rebuild/math16_ab2d_domain_menu.py:build_task_block",
        ],
        "v2_addition": "## Runtime binding contract (zero-argument evaluator call) + per-task zero-arg skeleton",
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
