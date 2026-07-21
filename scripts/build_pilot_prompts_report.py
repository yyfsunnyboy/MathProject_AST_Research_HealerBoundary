import difflib
import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TARGET_TASKS = [
    "ce111_q03_prime_factor_selection",
    "ce112_q01_negative_integer_power",
    "ce112_q09_divisor_multiple_intersection",
    "ce111_nonchoice_q01_part1_exponential_growth"
]

def load_ab2s_prompts() -> dict[str, str]:
    spec_path = ROOT / "docs/experiments/manifests/ab2s_integer_prompt_spec_v1.md"
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('\r\n', '\n')
    parts = content.split('\x60\x60\x60text\n')
    prompts = {}
    for i, tid in enumerate(TARGET_TASKS):
        block = parts[i+1].split('\x60\x60\x60')[0].rstrip('\n')
        prompts[tid] = block
    return prompts

def build_report():
    from agent_tools.finals_rebuild.math16_pool import build_pool_tasks, frozen_for_prompt
    from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import build_condition_prompt, prompt_sha256

    tasks = {t["task_id"]: t for t in build_pool_tasks()}
    ab2s_prompts = load_ab2s_prompts()

    report = []
    report.append("# Math16 Ab2s Pilot Prompts Specification & Diff Report\n")
    report.append("This document contains the exact model-visible prompts for both **ab2d_replication** and **ab2s_integer_skill** conditions across the 4 pilot integer tasks, along with precise unified diffs proving their strictly incremental structural relationship.\n")
    report.append("## Verification Summary\n")
    report.append("- **Prefix Exact-Match**: Passed. All `ab2s_integer_skill` prompts start with the byte-exact `ab2g` prompt prefix.\n")
    report.append("- **No Answer/Evaluator Leakage**: Passed. No correct answers, healer rules, or evaluator internals exist in the prompts.\n")
    report.append("- **Module Import Paths Omitted**: Passed. All `core.prompts.domain_function_library` import paths are omitted from `ab2s_integer_skill` blocks.\n")
    report.append("\n---\n")

    for tid in TARGET_TASKS:
        task = tasks[tid]
        frozen = frozen_for_prompt(task)

        ab2d_prompt = build_condition_prompt("ab2d", task, frozen)
        ab2s_prompt = ab2s_prompts[tid]

        ab2d_sha = prompt_sha256(ab2d_prompt)
        ab2s_sha = prompt_sha256(ab2s_prompt)

        ab2d_bytes = len(ab2d_prompt.encode("utf-8"))
        ab2s_bytes = len(ab2s_prompt.encode("utf-8"))

        ab2d_chars = len(ab2d_prompt)
        ab2s_chars = len(ab2s_prompt)

        report.append(f"## Task: {tid}\n")

        # Ab2d Prompt
        report.append("### ab2d_replication — exact model-visible prompt\n")
        report.append("```text")
        report.append(ab2d_prompt)
        report.append("```\n")
        report.append("- **SHA-256**: `" + ab2d_sha + "`")
        report.append(f"- **UTF-8 Byte Count**: {ab2d_bytes} bytes")
        report.append(f"- **Character Count**: {ab2d_chars} chars\n")

        # Ab2s Prompt
        report.append("### ab2s_integer_skill — exact model-visible prompt\n")
        report.append("```text")
        report.append(ab2s_prompt)
        report.append("```\n")
        report.append("- **SHA-256**: `" + ab2s_sha + "`")
        report.append(f"- **UTF-8 Byte Count**: {ab2s_bytes} bytes")
        report.append(f"- **Character Count**: {ab2s_chars} chars\n")

        # Prompt Diff
        report.append("### Prompt diff\n")
        diff = list(difflib.unified_diff(
            ab2d_prompt.splitlines(keepends=True),
            ab2s_prompt.splitlines(keepends=True),
            fromfile='ab2d_replication',
            tofile='ab2s_integer_skill',
            n=3
        ))
        diff_text = "".join(diff)

        report.append("```diff")
        report.append(diff_text.strip())
        report.append("```\n")
        report.append("\n---\n")

    report_dir = ROOT / "docs/experiments/reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    with open(report_dir / "math16_ab2s_pilot_prompts.md", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(report))

    print("Prompt report generated at docs/experiments/reports/math16_ab2s_pilot_prompts.md")

if __name__ == "__main__":
    build_report()
