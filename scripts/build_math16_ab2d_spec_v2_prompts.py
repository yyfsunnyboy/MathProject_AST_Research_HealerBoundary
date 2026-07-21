# -*- coding: utf-8 -*-
"""Freeze Ab2d+spec-v2 exact prompts for the 4 API-gap tasks only.

Parallel to ab2d_spec (v1); never overwrites v1 prompts or manifest.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import build_condition_prompt
from agent_tools.finals_rebuild.math16_pool import build_pool_tasks, frozen_for_prompt

# Exact user scope (4 tasks). Note: q08 is native-only and already 5/5 under v1;
# format_latex card is added per request. Residual q02 L3 to_latex is out of scope.
V2_TASKS = [
    {
        "task_id": "ce111_q05_exact_fraction_expression",
        "family": "fraction",
        "domain": "FractionOps",
        "api_policy": "API-only",
        "scaffold": "fraction_domain_scaffold_compact.py",
        "signature_card": "fraction_api_signature_card.md",
        "guardrail_subdir": "fraction",
        "is_api": True,
        "assessment_timing": "PRE_RUN",
        "result_known": False,
        "evidence_basis": "HISTORICAL_FROZEN_ONLY",
        "difficulty": "MEDIUM",
        "discrimination": "HIGH",
        "ceiling_risk": "LOW",
    },
    {
        "task_id": "ce112_q12_independent_probability_fraction",
        "family": "fraction",
        "domain": "FractionOps",
        "api_policy": "API-only",
        "scaffold": "fraction_domain_scaffold_compact.py",
        "signature_card": "fraction_api_signature_card.md",
        "guardrail_subdir": "fraction",
        "is_api": True,
        "assessment_timing": "PRE_RUN",
        "result_known": False,
        "evidence_basis": "HISTORICAL_FROZEN_ONLY",
        "difficulty": "MEDIUM",
        "discrimination": "MEDIUM",
        "ceiling_risk": "MODERATE",
    },
    {
        "task_id": "ce113_q01_negative_fraction_subtraction",
        "family": "fraction",
        "domain": "FractionOps",
        "api_policy": "API-only",
        "scaffold": "fraction_domain_scaffold_compact.py",
        "signature_card": "fraction_api_signature_card.md",
        "guardrail_subdir": "fraction",
        "is_api": True,
        "assessment_timing": "PRE_RUN",
        "result_known": False,
        "evidence_basis": "HISTORICAL_FROZEN_ONLY",
        "difficulty": "LOW",
        "discrimination": "MEDIUM",
        "ceiling_risk": "HIGH",
    },
    {
        "task_id": "ce111_q08_polynomial_factor_parameter_recovery",
        "family": "polynomial",
        "domain": "PolynomialOps",
        "api_policy": "native-only",
        "scaffold": "integer_domain_scaffold_compact.py",
        "signature_card": "polynomial_api_signature_card.md",
        "guardrail_subdir": "polynomial",
        "is_api": False,
        "assessment_timing": "PRE_RUN",
        "result_known": False,
        "evidence_basis": "HISTORICAL_FROZEN_ONLY",
        "difficulty": "HIGH",
        "discrimination": "HIGH",
        "ceiling_risk": "LOW",
    },
]

OUTPUT_DIR = ROOT / "docs/experiments/prompts/ab2d_spec_v2"
PROMPTS_OUT_DIR = OUTPUT_DIR / "prompts"
TEMPLATES_DIR = ROOT / "docs/experiments/templates/ab2d_spec_v2"
V1_PROMPT_DIR = ROOT / "docs/experiments/prompts/ab2d_spec/prompts"
V1_MANIFEST = ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"


def get_rel_path_str(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def get_file_sha256(path: Path) -> str:
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def main() -> None:
    PROMPTS_OUT_DIR.mkdir(parents=True, exist_ok=True)

    v1_prompt_hashes = {p.name: get_file_sha256(p) for p in sorted(V1_PROMPT_DIR.glob("*.txt"))}
    v1_manifest_sha = get_file_sha256(V1_MANIFEST)

    pool_manifest_path = ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json"
    ab2g_prefix_path = ROOT / "agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py"
    pool_manifest_sha = get_file_sha256(pool_manifest_path)
    ab2g_prefix_sha = get_file_sha256(ab2g_prefix_path)

    tasks_dict = {t["task_id"]: t for t in build_pool_tasks()}
    manifest_records = []

    final_check_api = (
        "Final check before output:\n"
        "- Output one complete Python source only.\n"
        "- Define the required generate() entry point.\n"
        "- Use the frozen parameters exactly.\n"
        "- Return the exact required keys and answer schema.\n"
        "- Only import the specified Domain API.\n"
        "- Obey the API Signature Cards exactly (no invented helpers / wrong arity)."
    )
    final_check_native = (
        "Final check before output:\n"
        "- Output one complete Python source only.\n"
        "- Define the required generate() entry point.\n"
        "- Use the frozen parameters exactly.\n"
        "- Return the exact required keys and answer schema.\n"
        "- Do not use domain APIs or invented APIs.\n"
        "- If any polynomial latex helper name is referenced, the only valid name is "
        "PolynomialOps.format_latex (never to_latex)."
    )

    for item in V2_TASKS:
        tid = item["task_id"]
        task = tasks_dict[tid]
        frozen = frozen_for_prompt(task)
        ab2g_prompt = build_condition_prompt("ab2g", task, frozen)

        scaffold_path = TEMPLATES_DIR / item["scaffold"]
        scaffold_content = scaffold_path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        scaffold_sha = get_file_sha256(scaffold_path)

        signature_path = TEMPLATES_DIR / item["signature_card"]
        signature_content = signature_path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        signature_sha = get_file_sha256(signature_path)

        v1_guardrail = (
            ROOT
            / "docs/experiments/prompts/ab2d_spec/task_guardrails"
            / item["guardrail_subdir"]
            / f"{tid}.md"
        )
        guardrail_path = (
            OUTPUT_DIR / "task_guardrails" / item["guardrail_subdir"] / f"{tid}.md"
        )
        guardrail_content = v1_guardrail.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        guardrail_path.parent.mkdir(parents=True, exist_ok=True)
        guardrail_path.write_text(guardrail_content + "\n", encoding="utf-8", newline="\n")
        if get_file_sha256(guardrail_path) != get_file_sha256(v1_guardrail):
            raise RuntimeError(f"Guardrail drift vs v1 for {tid}")
        guardrail_sha = get_file_sha256(guardrail_path)

        final_check = final_check_api if item["is_api"] else final_check_native

        exact_prompt = (
            f"{ab2g_prompt.strip()}\n\n"
            f"## Compact Domain Scaffold\n{scaffold_content}\n\n"
            f"## API Signature Cards\n{signature_content}\n\n"
            f"## Task Guardrails\n{guardrail_content}\n\n"
            f"## Final Check\n{final_check}\n"
        ).replace("\r\n", "\n")

        prompt_txt_path = PROMPTS_OUT_DIR / f"{tid}.txt"
        prompt_txt_path.write_text(exact_prompt, encoding="utf-8", newline="\n")
        prompt_sha = hashlib.sha256(exact_prompt.encode("utf-8")).hexdigest()

        v1_sha = get_file_sha256(V1_PROMPT_DIR / f"{tid}.txt")
        if prompt_sha == v1_sha:
            raise RuntimeError(f"v2 prompt unexpectedly identical to v1 for {tid}")

        # Signature cards must include required APIs
        if item["family"] == "fraction":
            if "FractionOps.create" not in exact_prompt or "FractionOps.from_parts" not in exact_prompt:
                raise RuntimeError(f"Missing FractionOps signatures in {tid}")
            if "(value)" not in exact_prompt or "(numerator, denominator)" not in exact_prompt:
                raise RuntimeError(f"Incomplete FractionOps signature text in {tid}")
        else:
            if "PolynomialOps.format_latex" not in exact_prompt:
                raise RuntimeError(f"Missing format_latex in {tid}")
            if "to_latex" not in exact_prompt.lower():
                raise RuntimeError(f"Missing explicit to_latex prohibition in {tid}")

        manifest_records.append(
            {
                "condition": "ab2d_spec_v2",
                "task_id": tid,
                "family": item["family"],
                "domain": item["domain"],
                "api_policy": item["api_policy"],
                "assessment": {
                    "assessment_timing": item["assessment_timing"],
                    "result_known": item["result_known"],
                    "evidence_basis": item["evidence_basis"],
                    "difficulty": item["difficulty"],
                    "discrimination": item["discrimination"],
                    "ceiling_risk": item["ceiling_risk"],
                },
                "prompt_revision": "ab2d_spec_v2",
                "prior_prompt_revision": "ab2d_spec_v1",
                "prior_exact_prompt_sha256": v1_sha,
                "task_contract_source": get_rel_path_str(pool_manifest_path),
                "task_contract_sha256": pool_manifest_sha,
                "ab2g_prefix_source": get_rel_path_str(ab2g_prefix_path),
                "ab2g_prefix_sha256": ab2g_prefix_sha,
                "domain_scaffold_source": get_rel_path_str(scaffold_path),
                "domain_scaffold_sha256": scaffold_sha,
                "api_signature_card_source": get_rel_path_str(signature_path),
                "api_signature_card_sha256": signature_sha,
                "task_guardrail_source": get_rel_path_str(guardrail_path),
                "task_guardrail_sha256": guardrail_sha,
                "exact_prompt_sha256": prompt_sha,
                "prompt_path": get_rel_path_str(prompt_txt_path),
                "char_count": len(exact_prompt),
                "utf8_byte_count": len(exact_prompt.encode("utf-8")),
                "estimated_token_count": int(len(exact_prompt) / 4),
                "prompt_frozen": True,
                "model_called": False,
            }
        )

    manifest_out = {
        "manifest_id": "math16_ab2d_spec_pilot02_freeze_v2",
        "prompt_revision": "ab2d_spec_v2",
        "prior_manifest_id": "math16_ab2d_spec_pilot02_freeze_v1",
        "prior_manifest_sha256": v1_manifest_sha,
        "prior_v1_prompt_sha256_snapshot": v1_prompt_hashes,
        "tasks": manifest_records,
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "llm_policy": "freeze_only; zero model calls",
        "overwrite_policy": "never overwrite docs/experiments/prompts/ab2d_spec/ (v1)",
        "residual_note": (
            "ce111_q02 ab2d_spec v1 still has residual L3 to_latex failures (2/5) "
            "outside this v2 scope per user instruction."
        ),
    }

    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps(manifest_out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    for name, sha in v1_prompt_hashes.items():
        if get_file_sha256(V1_PROMPT_DIR / name) != sha:
            raise RuntimeError(f"v1 prompt mutated during v2 freeze: {name}")
    if get_file_sha256(V1_MANIFEST) != v1_manifest_sha:
        raise RuntimeError("v1 manifest mutated during v2 freeze")

    print(f"Frozen {len(manifest_records)} ab2d_spec_v2 prompts")
    for rec in manifest_records:
        print(f"  {rec['task_id']}: {rec['exact_prompt_sha256']}")


if __name__ == "__main__":
    main()
