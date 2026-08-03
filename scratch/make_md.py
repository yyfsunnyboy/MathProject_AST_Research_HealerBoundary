import json
from pathlib import Path

json_path = Path("docs/experiments/results/Math16/math16_ab2d_480cell_system_prompt_defect_audit_v1.json")
data = json.loads(json_path.read_text(encoding="utf-8"))

lines = []
lines.append("# Math16 Ab2d menu-vs-full 480-cell System & Prompt Defect Audit Report (v1)")
lines.append("")
lines.append("**Commit**: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`  ")
lines.append("**Date**: 2026-08-03  ")
lines.append("**Scope**: All 480 formal evaluation cells (Gemini 3.5 Flash: 160, Qwen 3.5 9B: 160, Qwen 3.5 4B: 160)  ")
lines.append("**Auditor**: Antigravity AI Agent  ")
lines.append("**Overall Verdict**: **SYSTEM_AND_PROMPT_DEFECT_FREE**  ")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 1. Executive Summary & Verdict")
lines.append("")
lines.append("This audit evaluated all 480 formal execution cells for the Math16 Ab2d experiment (domain-menu vs full-plan) to rule out system bugs, prompt defects, runner misconfigurations, cache contamination, or evaluator errors before interpreting model performance differences.")
lines.append("")
lines.append("### Key Audit Findings:")
lines.append("1. **Prompt Provenance**: **0 / 480** prompt SHAs mismatched against frozen prompt manifests (when LF-normalized). Across all 480 cells, Gemini, Qwen 9B, and Qwen 4B received **100% byte-identical prompts** for the same task_id, condition, seed. Task-specific answer contracts were present in **480 / 480** prompts.")
lines.append("2. **Runner & Request Provenance**: All 6 runner scripts strictly adhered to preregistered settings (model_settings.json). Recorded model calls = **480 / 480**; skipped/cached cells = **0**.")
lines.append("3. **Schema Failure Forensics (15 cells)**: All 15 schema failure cells (Qwen 9B: 5, Qwen 4B: 10, Gemini: 0) were classified as `MODEL_NONCOMPLIANCE` (100%). In every case, prompt contracts were present, but the model produced non-compliant code.")
lines.append("4. **Gemini 5 Execution Failures**: All 5 execution failures in Gemini occurred under `ab2d_full` condition for a single task: `ce113_q11_rationalize_denominator`. The cause was model misinterpretation of the 3-tuple return signature of `RadicalOps.rationalize_linear_denominator(num, a, b, r)`.")
lines.append("5. **System/Prompt/Runner Bugs**: **0 bugs found**.")
lines.append("6. **Usability & Rerun Recommendation**: All 3 models dataset (Gemini: 160 cells, Qwen 9B: 160 cells, Qwen 4B: 160 cells) are rated `VALID_AS_MODEL_RESULT`. **No rerun is required (0 cells)**.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 2. Prompt Provenance Audit")
lines.append("")
lines.append("| Metric | Result | Target / Expected | Pass/Fail |")
lines.append("|---|---|---|---|")
lines.append("| Total Formal Cells Audited | 480 | 480 | PASS |")
lines.append("| LF-Normalized Prompt SHA Mismatches | 0 / 480 | 0 | PASS |")
lines.append("| Cross-Model Prompt Mismatches (Same Task/Cond/Seed) | 0 / 480 | 0 | PASS |")
lines.append("| Answer Contract Missing Count | 0 / 480 | 0 | PASS |")
lines.append("| Line-Ending Normalization Check | CRLF on disk (Windows git), LF-normalized matches 100% | LF-normalized match | PASS |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 3. Runner & Request Provenance Audit")
lines.append("")
lines.append("- **Runner Entrypoints Audited**:")
lines.append("  1. `scripts/run_math16_ab2d_domain_menu_gemini_formal.py` ")
lines.append("  2. `scripts/run_math16_ab2d_domain_menu_qwen9b_formal.py` ")
lines.append("  3. `scripts/run_math16_ab2d_domain_menu_qwen4b_formal.py` ")
lines.append("  4. `scripts/run_math16_ab2d_full_gemini_formal.py` ")
lines.append("  5. `scripts/run_math16_ab2d_full_qwen9b_formal.py` ")
lines.append("  6. `scripts/run_math16_ab2d_full_qwen4b_formal.py` ")
lines.append("- **Parameter Authority**: `artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/model_settings.json`")
lines.append("- **Model Calls**: 480 recorded calls (Gemini: 160, Qwen 9B: 160, Qwen 4B: 160).")
lines.append("- **Skipped / Cached Cells**: 0.")
lines.append("- **Request Configurations**:")
lines.append("  - Gemini 3.5 Flash: `temperature=0.0`, `top_p=1.0`, `top_k=1`, `max_output_tokens=24576`, `timeout=600s`.")
lines.append("  - Qwen 3.5 9B: `temperature=0.2`, `top_p=0.8`, `top_k=20`, `num_ctx=65536`, `num_predict=24576`, `seed=cell_seed`.")
lines.append("  - Qwen 3.5 4B: `temperature=0.2`, `top_p=0.8`, `top_k=20`, `num_ctx=65536`, `num_predict=24576`, `seed=cell_seed`.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 4. Schema Failure Forensic (15 Cells Itemized)")
lines.append("")

for idx, sf in enumerate(data["schema_failures_forensic_ledger"], 1):
    lines.append(f"### [{idx:02d}] Cell: `{sf['cell_id']}`")
    lines.append(f"- **Model**: `{sf['model']}`")
    lines.append(f"- **Condition**: `{sf['condition']}`")
    lines.append(f"- **Task ID**: `{sf['task_id']}` | **Seed**: `{sf['seed']}`")
    lines.append(f"- **Prompt Contract Present**: `{sf['answer_contract_present']}`")
    lines.append(f"- **Returned Value**: `{sf['returned_value']}`")
    lines.append(f"- **Oracle Payload Equals Frozen**: `{sf['oracle_payload_equals_frozen_params']}`")
    lines.append(f"- **Final Classification**: `{sf['classification']}`")
    lines.append(f"- **Forensic Explanation**: {sf['root_cause_explanation']}")
    lines.append("")

lines.extend([
    "### Classification Statistics:",
    "1. `MODEL_NONCOMPLIANCE`: **15 / 15** (100%)",
    "2. `PROMPT_DEFECT`: **0 / 15**",
    "3. `RUNNER_DEFECT`: **0 / 15**",
    "4. `EVALUATOR_DEFECT`: **0 / 15**",
    "5. `ARTIFACT_DEFECT`: **0 / 15**",
    "6. `UNRESOLVED`: **0 / 15**",
    "",
    "---",
    "",
    "## 5. Other FAIL Forensic (Gemini & Qwen Failure Analysis)",
    "",
    "### Gemini 5 Execution Failures Forensic:",
    "All 5 execution failures in Gemini occurred under `ab2d_full` condition in task `ce113_q11_rationalize_denominator`:",
    "- Seeds: `2026071301`, `2026072001`, `2026072002`, `2026072003`, `2026072004`.",
    "- Error: `ValueError: exact_integer requires an integral Fraction (got 4/7)`.",
    "- Cause: The generated code misread the 3-tuple return signature of `RadicalOps.rationalize_linear_denominator(num, a, b, r)` (which returns simplified coefficients `(a_out, b_out, r)`). Gemini attempted an extra division by `r`, resulting in `Fraction(4, 7)`, which failed `RadicalOps.exact_integer`.",
    "- Note: Under `ab2d_domain_menu` without scaffold instructions, Gemini wrote clean code and passed 5/5.",
    "",
    "### Qwen FAIL Failure Breakdown:",
    "- **Qwen 9B (160 cells)**: Passed 96/160 (60.0%). Failures: `runtime_failure` (22), `parse_minor` (20), `answer_incorrect` (8), `schema_failure` (5), `missing_entry_point` (4), `structural_mismatch` (5).",
    "- **Qwen 4B (160 cells)**: Passed 60/160 (37.5%). Failures: `runtime_failure` (51), `parse_minor` (15), `schema_failure` (10), `catastrophic_truncation` (9), `missing_entry_point` (9), `answer_incorrect` (4), `structural_mismatch` (1), `extraction_failure` (1).",
    "",
    "---",
    "",
    "## 6. Usability Determination & Recommendations",
    "",
    "| Model | Audited Cells | Usability Determination | Rerun Required? |",
    "|---|---|---|---|",
    "| **Gemini 3.5 Flash** | 160 | `VALID_AS_MODEL_RESULT` | NO (0 cells) |",
    "| **Qwen 3.5 9B** | 160 | `VALID_AS_MODEL_RESULT` | NO (0 cells) |",
    "| **Qwen 3.5 4B** | 160 | `VALID_AS_MODEL_RESULT` | NO (0 cells) |",
    "",
    "- **Rerun Recommendation**: **None (0 cells to rerun)**.",
    "- **Unresolved Evidence Gaps**: **None (0 evidence gaps)**."
])

out_md = Path("docs/experiments/results/Math16/math16_ab2d_480cell_system_prompt_defect_audit_v1.md")
out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Wrote:", out_md)
