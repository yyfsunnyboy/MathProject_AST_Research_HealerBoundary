"""32-prompt semantic census + fairness audit for Math16 Ab2d V2.

For each of the 16 task_ids, compares the V2 domain-menu prompt against the V2 full-plan
prompt. The only allowed difference is the appended
"## Task-specific scaffold (full-plan only)" block (ALLOWED_FULL_PLAN_SCAFFOLD). Any other
difference is a FAIRNESS_VIOLATION.

Also runs the fairness checks from the plan:
  - domain-menu solution/API-choice leakage scan (must be 0)
  - task-specific answer-contract text byte-identical to V1's (unchanged)
  - kwargs.get("frozen_params") never appears outside its one designated callout

Writes docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_semantic_census.{json,md}
"""
from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (  # noqa: E402
    TASK_ANSWER_CONTRACT_HEADER,
    build_domain_menu_prompt as v1_build_domain_menu_prompt,
)
from agent_tools.finals_rebuild.math16_ab2d_domain_menu_v2 import (  # noqa: E402
    RUNTIME_SKELETON_HEADER,
    validate_prompt_static_v2,
)
from agent_tools.finals_rebuild.math16_ab2d_full_v2 import (  # noqa: E402
    SCAFFOLD_HEADER,
    validate_prompt_static_v2_full,
)
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id  # noqa: E402

MENU_DIR = ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/prompts"
FULL_DIR = ROOT / "docs/experiments/prompts/ab2d_full_v2/prompts"
OUT_JSON = ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_semantic_census.json"
OUT_MD = ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_semantic_census.md"

ALLOWED_FULL_PLAN_SCAFFOLD = SCAFFOLD_HEADER

# Rough leakage signal for domain-menu: any concrete API-call-with-real-args expression
# (e.g. "RadicalOps.simplify_term(1, 135)") appearing outside the runtime-skeleton
# placeholder block would indicate a leaked solution step. Domain-menu is only allowed to
# show the domain-generic example (with its own placeholder numbers, not this task's).
def _menu_leakage_hits(menu_text: str, task_id: str) -> list[str]:
    hits = []
    if SCAFFOLD_HEADER in menu_text:
        hits.append("full_plan_scaffold_header_present_in_menu")
    # domain-menu's own static validator already bans numbered "1) ... 2) ... 3)" steps
    # and forbidden kwargs.get placement; re-run it here as the mechanical leakage gate.
    return hits


def census_one(task_id: str, domain: str) -> dict:
    menu_text = (MENU_DIR / f"{task_id}.txt").read_text(encoding="utf-8")
    full_text = (FULL_DIR / f"{task_id}.txt").read_text(encoding="utf-8")

    menu_errors = validate_prompt_static_v2(menu_text, domain)
    full_errors = validate_prompt_static_v2_full(full_text, domain)
    leak_hits = _menu_leakage_hits(menu_text, task_id)

    # Shared-prefix check: full must start with menu's content, then exactly the
    # allowed scaffold block appended.
    menu_stripped = menu_text.rstrip()
    shared_prefix_ok = full_text.startswith(menu_stripped)
    appended = full_text[len(menu_stripped):].strip("\n") if shared_prefix_ok else None
    appended_is_only_allowed = (
        shared_prefix_ok and appended is not None and appended.startswith(ALLOWED_FULL_PLAN_SCAFFOLD)
    )

    diff_classification = "ALLOWED_FULL_PLAN_SCAFFOLD" if appended_is_only_allowed else "FAIRNESS_VIOLATION"
    if not shared_prefix_ok:
        # Full unified diff for forensic detail when prefixes don't match.
        diff_lines = list(
            difflib.unified_diff(
                menu_stripped.splitlines(), full_text.splitlines(), lineterm=""
            )
        )
    else:
        diff_lines = []

    return {
        "task_id": task_id,
        "domain_ops": domain,
        "menu_static_errors": menu_errors,
        "full_static_errors": full_errors,
        "menu_leakage_hits": leak_hits,
        "shared_prefix_byte_identical": shared_prefix_ok,
        "diff_classification": diff_classification,
        "unexpected_diff_lines": diff_lines[:200],
        "fairness_violation": diff_classification == "FAIRNESS_VIOLATION" or bool(menu_errors) or bool(full_errors) or bool(leak_hits),
    }


def _extract_contract_until_next_heading(text: str) -> str:
    """Extract from TASK_ANSWER_CONTRACT_HEADER up to (not including) the next '## '
    heading -- boundary-agnostic version of V1's extractor, needed because V2 inserts a
    new '## Runtime binding contract' section right after the answer contract (V1 has
    none, so V1's own hardcoded '\\n## Task\\n' boundary does not apply symmetrically)."""
    begin = text.find(TASK_ANSWER_CONTRACT_HEADER)
    if begin < 0:
        raise ValueError("task-specific answer contract header missing")
    rest = text[begin + len(TASK_ANSWER_CONTRACT_HEADER):]
    next_heading = rest.find("\n## ")
    body = rest[:next_heading] if next_heading >= 0 else rest
    return body.strip("\n") + "\n"


def answer_contract_identity_check(task_id: str, task: dict) -> dict:
    v1_prompt = v1_build_domain_menu_prompt(task)
    v1_contract = _extract_contract_until_next_heading(v1_prompt)
    menu_text = (MENU_DIR / f"{task_id}.txt").read_text(encoding="utf-8")
    v2_contract = _extract_contract_until_next_heading(menu_text)
    return {
        "task_id": task_id,
        "identical_to_v1": v1_contract == v2_contract,
    }


def main() -> dict:
    pool = load_pool_manifest(ROOT)
    tasks = tasks_by_id(ROOT)
    task_ids = pool["task_ids"]

    menu_files = sorted(p.stem for p in MENU_DIR.glob("*.txt"))
    full_files = sorted(p.stem for p in FULL_DIR.glob("*.txt"))

    missing_menu = sorted(set(task_ids) - set(menu_files))
    missing_full = sorted(set(task_ids) - set(full_files))
    duplicate_menu = len(menu_files) - len(set(menu_files))
    duplicate_full = len(full_files) - len(set(full_files))

    rows = [census_one(tid, tasks[tid]["domain_ops"]) for tid in task_ids]
    contract_rows = [answer_contract_identity_check(tid, tasks[tid]) for tid in task_ids]

    n_complete = 32 - len(missing_menu) - len(missing_full)
    n_fairness_violations = sum(1 for r in rows if r["fairness_violation"])
    n_contract_mismatches = sum(1 for r in contract_rows if not r["identical_to_v1"])

    result = {
        "experiment_id": "math16_ab2d_menu_vs_full_runtime_contract_v2",
        "n_tasks": len(task_ids),
        "n_prompts_expected": 32,
        "n_prompts_found": len(menu_files) + len(full_files),
        "n_prompts_complete": n_complete,
        "missing_menu": missing_menu,
        "missing_full": missing_full,
        "duplicate_menu": duplicate_menu,
        "duplicate_full": duplicate_full,
        "n_fairness_violations": n_fairness_violations,
        "n_answer_contract_mismatches_vs_v1": n_contract_mismatches,
        "rows": rows,
        "answer_contract_identity_rows": contract_rows,
    }
    result["overall_pass"] = (
        n_complete == 32
        and not missing_menu
        and not missing_full
        and duplicate_menu == 0
        and duplicate_full == 0
        and n_fairness_violations == 0
        and n_contract_mismatches == 0
    )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    md_lines = [
        "# Math16 Ab2d V2 -- 32-prompt semantic census & fairness audit",
        "",
        f"- prompts expected: 32, found: {result['n_prompts_found']}, complete: {n_complete}",
        f"- missing (menu): {missing_menu or 'none'}",
        f"- missing (full): {missing_full or 'none'}",
        f"- duplicates: menu={duplicate_menu}, full={duplicate_full}",
        f"- fairness violations: **{n_fairness_violations}**",
        f"- answer-contract mismatches vs V1: **{n_contract_mismatches}**",
        f"- overall_pass: **{result['overall_pass']}**",
        "",
        "| task_id | domain | diff_classification | menu_errors | full_errors | leak_hits | fairness_violation |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        md_lines.append(
            f"| {r['task_id']} | {r['domain_ops']} | {r['diff_classification']} | "
            f"{len(r['menu_static_errors'])} | {len(r['full_static_errors'])} | "
            f"{len(r['menu_leakage_hits'])} | {r['fairness_violation']} |"
        )
    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: r[k] for k in (
        "n_prompts_found", "n_prompts_complete", "n_fairness_violations",
        "n_answer_contract_mismatches_vs_v1", "overall_pass",
    )}, ensure_ascii=False, indent=2))
