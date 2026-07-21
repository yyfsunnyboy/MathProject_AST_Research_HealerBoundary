# -*- coding: utf-8 -*-
"""Append ce111_q02 to ab2d_spec_v2 without rewriting the existing 4 frozen prompts."""
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

OUTPUT_DIR = ROOT / "docs/experiments/prompts/ab2d_spec_v2"
PROMPTS_OUT_DIR = OUTPUT_DIR / "prompts"
TEMPLATES_DIR = ROOT / "docs/experiments/templates/ab2d_spec_v2"
V1_PROMPT_DIR = ROOT / "docs/experiments/prompts/ab2d_spec/prompts"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"

# Frozen SHAs of the first 4 v2 tasks — must remain unchanged.
FROZEN_EXISTING = {
    "ce111_q05_exact_fraction_expression": "927977168ad6a72c644641fed7ef653495e55279689dc0beb06253033242926d",
    "ce112_q12_independent_probability_fraction": "183c3a708e2a1361e9ccd41de1cb33c51bb169b1f6b7cd99d874f98aa23ada51",
    "ce113_q01_negative_fraction_subtraction": "319926943ccbc9ca260979e04cf024cc1d896f00bc3e6be23e7b9632170ca54a",
    "ce111_q08_polynomial_factor_parameter_recovery": "4e8f345ad99e87317c2bb38ce741268ce4f57d9e2ca98518eea4f37fb36fb477",
}

Q02 = {
    "task_id": "ce111_q02_polynomial_division_remainder",
    "family": "polynomial",
    "domain": "PolynomialOps",
    "api_policy": "API-only",
    "scaffold": "polynomial_domain_scaffold_compact.py",
    "signature_card": "polynomial_api_signature_card.md",
    "guardrail_subdir": "polynomial",
    "is_api": True,
    "assessment_timing": "PRE_RUN",
    "result_known": False,
    "evidence_basis": "HISTORICAL_FROZEN_ONLY",
    "difficulty": "MEDIUM",
    "discrimination": "HIGH",
    "ceiling_risk": "LOW",
}


def sha_lf(path: Path) -> str:
    return hashlib.sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    # 1) Verify existing 4 prompts untouched on disk vs frozen SHAs
    by_id = {t["task_id"]: t for t in manifest["tasks"]}
    for tid, expected in FROZEN_EXISTING.items():
        path = ROOT / by_id[tid]["prompt_path"]
        actual = sha_lf(path)
        if actual != expected:
            raise RuntimeError(f"Existing v2 prompt mutated before q02 extend: {tid}")
        if by_id[tid]["exact_prompt_sha256"] != expected:
            raise RuntimeError(f"Manifest SHA drift for {tid}")

    if "ce111_q02_polynomial_division_remainder" in by_id:
        # Idempotent: allow rebuild of q02 only if we intentionally overwrite q02 file
        print("q02 already in manifest; rebuilding q02 prompt only")

    tasks_dict = {t["task_id"]: t for t in build_pool_tasks()}
    tid = Q02["task_id"]
    task = tasks_dict[tid]
    frozen = frozen_for_prompt(task)
    ab2g_prompt = build_condition_prompt("ab2g", task, frozen)

    scaffold_path = TEMPLATES_DIR / Q02["scaffold"]
    signature_path = TEMPLATES_DIR / Q02["signature_card"]
    if "format_latex" not in scaffold_path.read_text(encoding="utf-8"):
        raise RuntimeError("polynomial scaffold missing format_latex example")
    if "format_latex" not in signature_path.read_text(encoding="utf-8"):
        raise RuntimeError("signature card missing format_latex")
    if "to_latex" not in signature_path.read_text(encoding="utf-8").lower():
        raise RuntimeError("signature card missing to_latex prohibition")

    scaffold_content = scaffold_path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    signature_content = signature_path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()

    v1_guardrail = (
        ROOT
        / "docs/experiments/prompts/ab2d_spec/task_guardrails/polynomial"
        / f"{tid}.md"
    )
    guardrail_path = OUTPUT_DIR / "task_guardrails/polynomial" / f"{tid}.md"
    guardrail_content = v1_guardrail.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    guardrail_path.parent.mkdir(parents=True, exist_ok=True)
    guardrail_path.write_text(guardrail_content + "\n", encoding="utf-8", newline="\n")
    if sha_lf(guardrail_path) != sha_lf(v1_guardrail):
        raise RuntimeError("q02 guardrail drifted from v1")

    final_check = (
        "Final check before output:\n"
        "- Output one complete Python source only.\n"
        "- Define the required generate() entry point.\n"
        "- Use the frozen parameters exactly.\n"
        "- Return the exact required keys and answer schema.\n"
        "- Only import the specified Domain API.\n"
        "- Obey the API Signature Cards exactly (no invented helpers / wrong arity).\n"
        "- Use PolynomialOps.format_latex for latex; never to_latex."
    )

    exact_prompt = (
        f"{ab2g_prompt.strip()}\n\n"
        f"## Compact Domain Scaffold\n{scaffold_content}\n\n"
        f"## API Signature Cards\n{signature_content}\n\n"
        f"## Task Guardrails\n{guardrail_content}\n\n"
        f"## Final Check\n{final_check}\n"
    ).replace("\r\n", "\n")

    prompt_path = PROMPTS_OUT_DIR / f"{tid}.txt"
    prompt_path.write_text(exact_prompt, encoding="utf-8", newline="\n")
    prompt_sha = hashlib.sha256(exact_prompt.encode("utf-8")).hexdigest()
    v1_sha = sha_lf(V1_PROMPT_DIR / f"{tid}.txt")
    if prompt_sha == v1_sha:
        raise RuntimeError("q02 v2 prompt identical to v1")

    pool_manifest_path = ROOT / "docs/experiments/manifests/math16_latex_v1_pool_manifest.json"
    ab2g_prefix_path = ROOT / "agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py"

    record = {
        "condition": "ab2d_spec_v2",
        "task_id": tid,
        "family": Q02["family"],
        "domain": Q02["domain"],
        "api_policy": Q02["api_policy"],
        "assessment": {
            "assessment_timing": Q02["assessment_timing"],
            "result_known": Q02["result_known"],
            "evidence_basis": Q02["evidence_basis"],
            "difficulty": Q02["difficulty"],
            "discrimination": Q02["discrimination"],
            "ceiling_risk": Q02["ceiling_risk"],
        },
        "prompt_revision": "ab2d_spec_v2",
        "prior_prompt_revision": "ab2d_spec_v1",
        "prior_exact_prompt_sha256": v1_sha,
        "task_contract_source": rel(pool_manifest_path),
        "task_contract_sha256": sha_lf(pool_manifest_path),
        "ab2g_prefix_source": rel(ab2g_prefix_path),
        "ab2g_prefix_sha256": sha_lf(ab2g_prefix_path),
        "domain_scaffold_source": rel(scaffold_path),
        "domain_scaffold_sha256": sha_lf(scaffold_path),
        "api_signature_card_source": rel(signature_path),
        "api_signature_card_sha256": sha_lf(signature_path),
        "task_guardrail_source": rel(guardrail_path),
        "task_guardrail_sha256": sha_lf(guardrail_path),
        "exact_prompt_sha256": prompt_sha,
        "prompt_path": rel(prompt_path),
        "char_count": len(exact_prompt),
        "utf8_byte_count": len(exact_prompt.encode("utf-8")),
        "estimated_token_count": int(len(exact_prompt) / 4),
        "prompt_frozen": True,
        "model_called": False,
        "patch_reason": "residual_l3_to_latex_AttributeError_seeds_1301_2003",
    }

    # Keep existing 4 records byte-identical; append/replace only q02
    new_tasks = []
    for t in manifest["tasks"]:
        if t["task_id"] == tid:
            continue
        new_tasks.append(t)
    new_tasks.append(record)
    manifest["tasks"] = new_tasks
    manifest["q02_extension_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest["residual_note"] = (
        "ce111_q02 residual L3 to_latex patched into ab2d_spec_v2; "
        "existing Fraction×3 + q08 prompts unchanged."
    )
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    # Re-verify existing 4 unchanged
    for tid_e, expected in FROZEN_EXISTING.items():
        path = ROOT / "docs/experiments/prompts/ab2d_spec_v2/prompts" / f"{tid_e}.txt"
        if sha_lf(path) != expected:
            raise RuntimeError(f"Accidental overwrite of {tid_e}")

    print(f"Appended q02 prompt sha={prompt_sha}")
    print("Existing 4 prompts unchanged: OK")


if __name__ == "__main__":
    main()
