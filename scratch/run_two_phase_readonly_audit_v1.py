"""Two-phase read-only Prompt–Healer coverage audit + domain-menu FAIL census.

Produces audit artifacts under docs/experiments/audits/math16_ab2d_v2_prompt_healer_audit_v1/
Does NOT modify prompts, healers, runners, evaluators, or formal results.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.domain_api_ssot import DOMAIN_API_SSOT, SUPPORTED_PUBLIC
from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
    DOMAIN_OPS,
    SHARED_OUTPUT_CONTRACT,
    SYSTEM_HEADER,
    supported_apis_for_domain,
)
from agent_tools.finals_rebuild.math16_ab2d_domain_menu_v2 import (
    FORBIDDEN_CALLOUT,
    RUNTIME_SKELETON_HEADER,
)
from agent_tools.finals_rebuild.math16_ab2d_full_v2 import SCAFFOLD_HEADER
from agent_tools.finals_rebuild.math16_ab2d_v2_scaffolds import TASK_SCAFFOLDS_V2
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id
from agent_tools.finals_rebuild.extraction import extract_code

OUT_DIR = ROOT / "docs/experiments/audits/math16_ab2d_v2_prompt_healer_audit_v1"
MENU_DIR = ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/prompts"
FULL_DIR = ROOT / "docs/experiments/prompts/ab2d_full_v2/prompts"
BASE_COMMIT = "f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4"

# Frozen Math16 research healer allowlist (read-only reference)
RESEARCH_HEALER_RULES: dict[str, dict[str, str]] = {
    "L1_CLOSE_UNBALANCED_PARENTHESIS": {
        "file": "agent_tools/finals_rebuild/ce115_research_healer_rules_l1_paren_close.py",
        "scope": "general_syntax",
    },
    "L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED": {
        "file": "agent_tools/finals_rebuild/ce115_research_healer_rules_l1_delimiter_extended.py",
        "scope": "general_syntax",
    },
    "L1_PROSE_RESIDUE_NARROW": {
        "file": "agent_tools/finals_rebuild/ce115_research_healer_rules_l1_prose_narrow.py",
        "scope": "general_syntax",
    },
    "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP": {
        "file": "agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py",
        "scope": "oracle_payload_shape",
    },
    "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM": {
        "file": "agent_tools/finals_rebuild/ce115_research_healer_rules_l2_kwargs_bag_inline.py",
        "scope": "kwargs_frozen_binding",
    },
    "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP": {
        "file": "agent_tools/finals_rebuild/ce115_research_healer_rules_l2_json_dumps_unwrap.py",
        "scope": "correct_answer_shape",
    },
}

CORE_HEALER_FILES = {
    "ast_healer": "core/healers/ast_healer.py",
    "regex_healer": "core/healers/regex_healer.py",
    "unified_cleanup_healer": "core/healers/unified_cleanup_healer.py",
    "anti_duplication_healer": "core/healers/anti_duplication_healer.py",
    "math_healer_runner": "agent_tools/finals_rebuild/math_healer_runner.py",
    "research_healer_runner": "agent_tools/finals_rebuild/ce115_research_healer_runner.py",
}

GENERAL_SAFETY_CHECKS = [
    {
        "contract_id": "GEN_EVAL_EXEC",
        "contract_category": "forbidden_runtime_operations",
        "description": "Block eval()/exec() misuse",
        "healer_detection": "full",
        "healer_repair": "deterministic",
        "existing_rule_or_file": "core/healers/ast_healer.py::visit_Call (eval/exec → safe_eval)",
        "gap_class": "keep",
        "recommended_action": "keep",
    },
    {
        "contract_id": "GEN_INPUT",
        "contract_category": "forbidden_runtime_operations",
        "description": "Block input() blocking calls",
        "healer_detection": "full",
        "healer_repair": "deterministic",
        "existing_rule_or_file": "core/healers/ast_healer.py, core/healers/regex_healer.py",
        "gap_class": "keep",
        "recommended_action": "keep",
    },
    {
        "contract_id": "GEN_ILLEGAL_IMPORT",
        "contract_category": "illegal_imports",
        "description": "Strip non-safe imports",
        "healer_detection": "partial",
        "healer_repair": "deterministic",
        "existing_rule_or_file": "core/healers/ast_healer.py::visit_Import/visit_ImportFrom",
        "gap_class": "keep",
        "recommended_action": "keep",
    },
    {
        "contract_id": "GEN_UNSAFE_LOOP",
        "contract_category": "unsafe_loops",
        "description": "while True → bounded for (legacy AST healer)",
        "healer_detection": "partial",
        "healer_repair": "unsafe",
        "existing_rule_or_file": "core/healers/ast_healer.py (legacy; frozen research healer forbids legacy pipelines)",
        "gap_class": "out_of_scope",
        "recommended_action": "out_of_scope",
    },
    {
        "contract_id": "GEN_SYNTAX_PAREN",
        "contract_category": "generic_syntax_ast_repair",
        "description": "Unbalanced parentheses/delimiters",
        "healer_detection": "partial",
        "healer_repair": "deterministic",
        "existing_rule_or_file": "L1_CLOSE_UNBALANCED_PARENTHESIS, L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED",
        "gap_class": "keep",
        "recommended_action": "keep",
    },
    {
        "contract_id": "GEN_PROSE_RESIDUE",
        "contract_category": "generic_syntax_ast_repair",
        "description": "Prose residue outside Python",
        "healer_detection": "partial",
        "healer_repair": "deterministic",
        "existing_rule_or_file": "L1_PROSE_RESIDUE_NARROW",
        "gap_class": "keep",
        "recommended_action": "keep",
    },
    {
        "contract_id": "GEN_MARKDOWN_FENCE",
        "contract_category": "generic_syntax_ast_repair",
        "description": "Markdown fence removal pre-parse",
        "healer_detection": "full",
        "healer_repair": "deterministic",
        "existing_rule_or_file": "core/healers/regex_healer.py, agent_tools/finals_rebuild/extraction.py",
        "gap_class": "keep",
        "recommended_action": "keep",
    },
    {
        "contract_id": "GEN_HALLUCINATED_FUNC",
        "contract_category": "forbidden_runtime_operations",
        "description": "Replace hallucinated polynomial formatters",
        "healer_detection": "partial",
        "healer_repair": "unsafe",
        "existing_rule_or_file": "core/healers/ast_healer.py (legacy; not in frozen research allowlist)",
        "gap_class": "out_of_scope",
        "recommended_action": "abstain_only",
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _api_calls_in_source(source: str) -> list[str]:
    calls: list[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return calls
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id in DOMAIN_OPS:
                calls.append(f"{node.func.value.id}.{node.func.attr}")
    return calls


def _required_apis_from_scaffold(task_id: str) -> list[str]:
    body = TASK_SCAFFOLDS_V2[task_id]["full_plan_body"]
    found = re.findall(r"(IntegerOps|FractionOps|RadicalOps|PolynomialOps)\.(\w+)", body)
    return [f"{a}.{m}" for a, m in found]


def _has_kwargs_frozen_pattern(source: str) -> bool:
    patterns = [
        r'kwargs\.get\s*\(\s*["\']frozen_params',
        r'kwargs\s*\[\s*["\']frozen_params',
        r'kwargs\.get\s*\(\s*["\']oracle_payload',
    ]
    return any(re.search(p, source) for p in patterns)


def _has_local_reimplementation(source: str) -> bool:
    hints = [
        r"def _simplify",
        r"def _format",
        r"class RadicalOps",
        r"class FractionOps",
        r"class IntegerOps",
        r"class PolynomialOps",
        r"math\.sqrt",
    ]
    return any(re.search(p, source) for p in hints)


def _extract_source_from_cell_dir(cell_dir: Path, artifact: dict[str, Any]) -> tuple[str | None, str]:
    for name in ("extracted_candidate.py", "candidate.py"):
        fp = cell_dir / name
        if fp.exists():
            return fp.read_text(encoding="utf-8"), str(fp.relative_to(ROOT))
    raw = artifact.get("raw_response") or ""
    if raw:
        ext = extract_code(raw)
        if ext.extraction_status == "extracted" and ext.extracted_code:
            return ext.extracted_code, "extracted_from_raw_response"
    return None, "missing"


def classify_fail_cell(
    task_id: str,
    source: str | None,
    original_failure: str,
) -> dict[str, Any]:
    required = _required_apis_from_scaffold(task_id)
    if not source:
        return {
            "used_APIs": [],
            "full_plan_required_APIs": required,
            "call_order_relation": "UNPARSEABLE",
            "parameter_binding_relation": "UNPARSEABLE",
            "return_binding_relation": "UNPARSEABLE",
            "answer_provenance_relation": "UNPARSEABLE",
            "structural_similarity_class": "UNPARSEABLE_OR_INSUFFICIENT_EVIDENCE",
            "unique_local_repair_possible": "no",
            "estimated_AST_nodes_changed": None,
            "algorithm_change_required": "ambiguous",
            "eligibility_for_future_cross_contract_test": False,
            "evidence": f"no_parseable_source; original_failure={original_failure}",
        }

    used = _api_calls_in_source(source)
    used_set = set(used)
    req_set = set(required)
    kwargs_bad = _has_kwargs_frozen_pattern(source)
    local_reimpl = _has_local_reimplementation(source)

    if local_reimpl and not used_set:
        sim = "STRUCTURALLY_DIVERGENT"
        repair = "no"
        algo = "yes"
        elig = False
    elif kwargs_bad and used_set & req_set:
        sim = "ALIGNED_LOCAL_DEVIATION"
        repair = "yes"
        algo = "no"
        elig = True
    elif kwargs_bad and not used_set:
        sim = "WRONG_API_OR_BINDING"
        repair = "yes" if "frozen" in source else "ambiguous"
        algo = "no"
        elig = True
    elif used_set == req_set:
        sim = "ALIGNED_LOCAL_DEVIATION"
        repair = "ambiguous"
        algo = "no"
        elig = True
    elif used_set and not (used_set & req_set):
        sim = "LEGAL_ALTERNATIVE_METHOD" if not kwargs_bad else "WRONG_API_OR_BINDING"
        repair = "ambiguous" if sim == "LEGAL_ALTERNATIVE_METHOD" else "yes"
        algo = "ambiguous" if sim == "LEGAL_ALTERNATIVE_METHOD" else "no"
        elig = sim != "LEGAL_ALTERNATIVE_METHOD"
    elif used_set & req_set and used_set != req_set:
        sim = "ALIGNED_LOCAL_DEVIATION" if len(used_set - req_set) <= 2 else "STRUCTURALLY_DIVERGENT"
        repair = "yes" if sim == "ALIGNED_LOCAL_DEVIATION" else "no"
        algo = "ambiguous" if sim == "ALIGNED_LOCAL_DEVIATION" else "yes"
        elig = sim == "ALIGNED_LOCAL_DEVIATION"
    else:
        sim = "UNPARSEABLE_OR_INSUFFICIENT_EVIDENCE"
        repair = "ambiguous"
        algo = "ambiguous"
        elig = False

    order_rel = "MATCH" if used == required else ("PARTIAL_OVERLAP" if used_set & req_set else "DIVERGENT")
    if kwargs_bad:
        bind_rel = "kwargs_instead_of_frozen_literal"
    elif 'frozen = {' in source or 'frozen={' in source:
        bind_rel = "local_frozen_literal"
    else:
        bind_rel = "ambiguous"

    return {
        "used_APIs": used,
        "full_plan_required_APIs": required,
        "call_order_relation": order_rel,
        "parameter_binding_relation": bind_rel,
        "return_binding_relation": "requires_manual_provenance_trace",
        "answer_provenance_relation": "LOCAL_REIMPL" if local_reimpl else ("API_DERIVED" if used else "UNKNOWN"),
        "structural_similarity_class": sim,
        "unique_local_repair_possible": repair,
        "estimated_AST_nodes_changed": "1-5" if repair == "yes" else ("6-20" if repair == "ambiguous" else ">20"),
        "algorithm_change_required": algo,
        "eligibility_for_future_cross_contract_test": elig,
        "evidence": f"used={used}; required={required}; kwargs_misuse={kwargs_bad}; local_reimpl={local_reimpl}",
    }


def build_prompt_contracts() -> list[dict[str, Any]]:
    pool = load_pool_manifest(ROOT)
    tasks = tasks_by_id(ROOT)
    rows: list[dict[str, Any]] = []

    def add_row(
        task_id: str,
        condition: str,
        contract_id: str,
        category: str,
        excerpt: str,
        machine: str,
        detection: str,
        repair: str,
        rule_file: str,
        gap: str,
        action: str,
        notes: str = "",
    ) -> None:
        rows.append(
            {
                "task_id": task_id,
                "condition": condition,
                "contract_id": contract_id,
                "contract_category": category,
                "source_prompt_excerpt_or_location": excerpt,
                "machine_checkable": machine,
                "current_healer_detection": detection,
                "current_healer_repair": repair,
                "existing_rule_or_file": rule_file,
                "gap_class": gap,
                "recommended_action": action,
                "notes": notes,
            }
        )

    for tid in pool["task_ids"]:
        task = tasks[tid]
        domain = task["domain_ops"]
        menu_text = (MENU_DIR / f"{tid}.txt").read_text(encoding="utf-8")
        full_text = (FULL_DIR / f"{tid}.txt").read_text(encoding="utf-8")
        scaffold = TASK_SCAFFOLDS_V2[tid]
        allowed = supported_apis_for_domain(domain)
        required = _required_apis_from_scaffold(tid)

        # --- Shared / domain-menu contracts ---
        for cond, text in (("ab2d_domain_menu_v2", menu_text), ("ab2d_full_v2", full_text)):
            add_row(
                tid,
                cond,
                "PC_ALLOWED_DOMAIN_APIS",
                "allowed_apis",
                f"Domain API menu lists {len(allowed)} SUPPORTED_PUBLIC APIs for {domain}",
                "yes",
                "none",
                "none",
                "N/A (prompt menu only; no runtime enforcement healer)",
                "not_covered",
                "detection_only",
                "Domain-menu grants API choice; Healer does not verify allowed set at runtime.",
            )
            add_row(
                tid,
                cond,
                "PC_FORBIDDEN_CROSS_DOMAIN",
                "forbidden_alternative_apis",
                SYSTEM_HEADER.split("\n")[6],
                "yes",
                "none",
                "none",
                "N/A",
                "not_covered",
                "abstain_only",
            )
            add_row(
                tid,
                cond,
                "PC_GENERATE_SIGNATURE",
                "generate_signature",
                "def generate(level=1, **kwargs):",
                "yes",
                "none",
                "none",
                "agent_tools/finals_rebuild/extraction.py (entry-point gate only)",
                "partial",
                "detection_only",
            )
            add_row(
                tid,
                cond,
                "PC_ZERO_ARG_RUNTIME",
                "zero_argument_runtime_contract",
                RUNTIME_SKELETON_HEADER,
                "yes",
                "partial",
                "deterministic",
                "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM (narrow: empty-bag + unique frozen only)",
                "narrow_rule",
                "deterministic_repair_candidate",
                "Detects empty kwargs bag inline; does not cover all kwargs.get('frozen_params') forms.",
            )
            add_row(
                tid,
                cond,
                "PC_PROHIBIT_KWARGS_FROZEN",
                "prohibited_nonexistent_runtime_kwargs",
                FORBIDDEN_CALLOUT[:120] + "...",
                "partial",
                "partial",
                "deterministic",
                "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM; L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
                "narrow_rule",
                "deterministic_repair_candidate",
            )
            add_row(
                tid,
                cond,
                "PC_FROZEN_LITERAL_BINDING",
                "frozen_parameter_binding",
                json.dumps(scaffold["frozen_literal"], ensure_ascii=False),
                "yes",
                "partial",
                "deterministic",
                "L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM",
                "narrow_rule",
                "deterministic_repair_candidate",
                "Requires evaluation context frozen bag; not prompt-only.",
            )
            add_row(
                tid,
                cond,
                "PC_OUTPUT_DICT_KEYS",
                "output_dictionary_keys",
                "question_text, correct_answer, oracle_payload",
                "yes",
                "partial",
                "none",
                "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP (oracle_payload scalar only)",
                "partial",
                "detection_only",
            )
            add_row(
                tid,
                cond,
                "PC_ORACLE_PAYLOAD_SOURCE",
                "correct_answer_source_provenance",
                "oracle_payload must equal frozen_params object",
                "yes",
                "partial",
                "deterministic",
                "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
                "narrow_rule",
                "deterministic_repair_candidate",
                "Scalar-wrap only; dict frozen_params not covered.",
            )
            schema = scaffold["answer_schema"]
            add_row(
                tid,
                cond,
                "PC_CORRECT_ANSWER_SHAPE",
                "correct_answer_shape",
                str(schema),
                "yes",
                "partial",
                "deterministic",
                "L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP",
                "partial",
                "detection_only",
                "Unwrap rule is narrow; shape validation is evaluator-side.",
            )

        # --- domain-menu only ---
        add_row(
            tid,
            "ab2d_domain_menu_v2",
            "PC_DOMAIN_MENU_NO_REQUIRED_API",
            "required_api",
            "domain-menu does not name which method(s) or call order to use",
            "yes",
            "none",
            "none",
            "N/A",
            "not_applicable_by_design",
            "out_of_scope",
            "By design: model chooses APIs; must not enforce full-plan API.",
        )
        add_row(
            tid,
            "ab2d_domain_menu_v2",
            "PC_FORBID_PRESCRIBED_ORDER",
            "api_call_order",
            "Forbidden: prescribed per-item API sequences (none are provided)",
            "yes",
            "none",
            "none",
            "N/A",
            "not_applicable_by_design",
            "out_of_scope",
        )

        # --- full-plan only ---
        steps = "\n".join(scaffold["full_plan_steps"])
        add_row(
            tid,
            "ab2d_full_v2",
            "PC_FULL_REQUIRED_APIS",
            "required_api",
            ", ".join(required),
            "yes",
            "none",
            "none",
            "N/A",
            "not_covered",
            "detection_only",
            f"Scaffold: {SCAFFOLD_HEADER}",
        )
        add_row(
            tid,
            "ab2d_full_v2",
            "PC_FULL_API_CALL_ORDER",
            "api_call_order",
            steps[:200],
            "partial",
            "none",
            "none",
            "N/A",
            "not_covered",
            "abstain_only",
        )
        add_row(
            tid,
            "ab2d_full_v2",
            "PC_FULL_RETURN_BINDING",
            "return_value_binding",
            scaffold["full_plan_body"][:200],
            "partial",
            "none",
            "none",
            "N/A",
            "not_covered",
            "abstain_only",
        )
        add_row(
            tid,
            "ab2d_full_v2",
            "PC_FULL_ANSWER_PROVENANCE",
            "answer_assembly_provenance",
            "correct_answer values must trace to specified API returns + allowed assembly",
            "partial",
            "none",
            "none",
            "N/A",
            "not_covered",
            "abstain_only",
            "No Healer performs def-use provenance to API returns.",
        )

    return rows


def collect_fail_cells() -> list[dict[str, Any]]:
    cells: dict[str, dict[str, Any]] = {}

    # Source A: ab123 run_002 with evaluator FAIL
    for root_rel in (
        "docs/experiments/results/qwen35_4b_math16_ab123_run_002/cells",
        "docs/experiments/results/qwen35_9b_math16_ab123_run_002/cells",
    ):
        root = ROOT / root_rel
        if not root.exists():
            continue
        for artifact_path in root.glob("*/artifact.json"):
            art = json.loads(artifact_path.read_text(encoding="utf-8"))
            if art.get("condition") != "ab2d":
                continue
            ev = art.get("evaluator_details") or {}
            fp = (ev.get("composite_outcomes") or {}).get("full_pass")
            if fp != "FAIL":
                continue
            src, src_path = _extract_source_from_cell_dir(artifact_path.parent, art)
            cid = art["cell_id"]
            cells[cid] = {
                "cell_id": cid,
                "task_id": art["task_id"],
                "seed": art.get("seed"),
                "original_failure": art.get("evaluator_status") or fp,
                "source_path": src_path,
                "source": src,
                "evidence_source": root_rel,
            }

    # Source B: 480-cell audit domain-menu schema failures
    audit480 = ROOT / "docs/experiments/results/Math16/math16_ab2d_480cell_system_prompt_defect_audit_v1.json"
    if audit480.exists():
        audit = json.loads(audit480.read_text(encoding="utf-8"))
        for row in audit.get("schema_failures_forensic_ledger", []):
            if row.get("condition") != "ab2d_domain_menu":
                continue
            cid = row["cell_id"]
            snippet = row.get("extracted_source_snippet") or row.get("raw_response_snippet") or ""
            ext = extract_code(snippet) if snippet else None
            src = ext.extracted_code if ext and ext.extraction_status == "extracted" else snippet
            cells[cid] = {
                "cell_id": cid,
                "task_id": row["task_id"],
                "seed": row.get("seed"),
                "original_failure": row.get("classification", "MODEL_NONCOMPLIANCE"),
                "source_path": "480cell_audit_snippet",
                "source": src,
                "evidence_source": str(audit480.relative_to(ROOT)),
            }

    out = []
    for cid, base in cells.items():
        classified = classify_fail_cell(base["task_id"], base.get("source"), base["original_failure"])
        out.append({**base, **classified, "source": None})  # omit bulky source from jsonl
    return out


def render_prompt_coverage_md(rows: list[dict[str, Any]], title: str) -> str:
    prompt_rows = [r for r in rows if r["contract_id"].startswith("PC_")]
    lines = [
        f"# {title}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Baseline commit: `{BASE_COMMIT}`",
        "",
        "## Prompt-derived contract coverage matrix",
        "",
        "| task_id | condition | contract_id | machine | detection | repair | gap | action |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in prompt_rows:
        lines.append(
            f"| {r['task_id']} | {r['condition']} | {r['contract_id']} | {r['machine_checkable']} | "
            f"{r['current_healer_detection']} | {r['current_healer_repair']} | {r['gap_class']} | {r['recommended_action']} |"
        )

    # Healer summary buckets
    buckets = {
        "fully_covered": [],
        "narrow": [],
        "detection_only": [],
        "missing": [],
        "no_auto_repair": [],
    }
    for r in prompt_rows:
        if r["recommended_action"] == "out_of_scope":
            buckets["no_auto_repair"].append(r["contract_id"])
        elif r["current_healer_detection"] == "none":
            buckets["missing"].append(r["contract_id"])
        elif r["current_healer_repair"] in ("none", "unsafe") and r["current_healer_detection"] != "none":
            buckets["detection_only"].append(r["contract_id"])
        elif r["gap_class"] == "narrow_rule":
            buckets["narrow"].append(r["contract_id"])
        elif r["current_healer_detection"] == "full" and r["current_healer_repair"] == "deterministic":
            buckets["fully_covered"].append(r["contract_id"])

    lines += [
        "",
        "## Healer coverage summary (Prompt-derived only)",
        "",
        f"- Fully covered (deterministic): **{len(set(buckets['fully_covered']))}** distinct contract types",
        f"- Narrow / conditional: **{len(set(buckets['narrow']))}**",
        f"- Detection-only or partial: **{len(set(buckets['detection_only']))}**",
        f"- Missing: **{len(set(buckets['missing']))}**",
        f"- Out of scope / abstain: **{len(set(buckets['no_auto_repair']))}**",
        "",
        "## Domain-menu vs full-plan contract diff (per task)",
        "",
    ]
    pool = load_pool_manifest(ROOT)
    for tid in pool["task_ids"]:
        menu_ids = {r["contract_id"] for r in prompt_rows if r["task_id"] == tid and r["condition"] == "ab2d_domain_menu_v2"}
        full_ids = {r["contract_id"] for r in prompt_rows if r["task_id"] == tid and r["condition"] == "ab2d_full_v2"}
        only_full = sorted(full_ids - menu_ids)
        lines.append(f"### `{tid}`")
        lines.append(f"- Shared contracts: **{len(menu_ids & full_ids)}**")
        lines.append(f"- Full-plan-only: **{', '.join(only_full) or '(none beyond shared set)'}**")
        lines.append("")

    return "\n".join(lines) + "\n"


def render_general_safety_md() -> str:
    lines = [
        "# General safety Healer coverage (NOT Prompt contract coverage)",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Baseline commit: `{BASE_COMMIT}`",
        "",
        "These checks are **General safety** — independent of V2 prompt contract text.",
        "",
        "## General safety coverage matrix",
        "",
        "| contract_id | category | detection | repair | rule/file | action |",
        "|---|---|---|---|---|---|",
    ]
    for r in GENERAL_SAFETY_CHECKS:
        lines.append(
            f"| {r['contract_id']} | {r['contract_category']} | {r['healer_detection']} | "
            f"{r['healer_repair']} | {r['existing_rule_or_file']} | {r['recommended_action']} |"
        )
    lines += [
        "",
        "## Frozen Math16 research Healer vs legacy core/healers",
        "",
        "| Layer | Research healer (frozen) | Legacy core/healers |",
        "|---|---|---|",
        "| Production path | ce115_research_healer_runner.py allowlist L1+L2 | math_healer_runner unified cleanup (legacy) |",
        "| Legacy AST/Regex | **Forbidden** in frozen research protocol | ast_healer.py, regex_healer.py still present read-only |",
        "",
        "**Verdict:** General syntax/dangerous-call coverage exists in legacy healers but is **out of scope** for frozen Math16 research Healer production path.",
        "",
    ]
    return "\n".join(lines) + "\n"


def render_provenance_md(rows: list[dict[str, Any]]) -> str:
    prov = [r for r in rows if r["contract_id"] == "PC_FULL_ANSWER_PROVENANCE"]
    lines = [
        "# Answer assembly provenance audit",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Baseline commit: `{BASE_COMMIT}`",
        "",
        "## Definition (applied)",
        "",
        "Provenance is limited to def-use chains from:",
        "1. full-plan specified API return values;",
        "2. prompt-allowed indexing/unpacking/sorting/normalization;",
        "3. frozen fields explicitly allowed in correct_answer.",
        "",
        "Violations: unsourced literals, wrong API fields, alternative algorithms, nonexistent kwargs, broken chains.",
        "Ambiguous multi-source paths marked AMBIGUOUS (not guessed).",
        "",
        "## Answer assembly provenance feasibility table",
        "",
        "| task_id | condition | machine_checkable | healer_detection | healer_repair | feasibility |",
        "|---|---|---|---|---|---|",
    ]
    for r in prov:
        feas = "NOT_FEASIBLE_IN_CURRENT_HEALER" if r["condition"] == "ab2d_full_v2" else "N/A_domain_menu_has_choice"
        lines.append(
            f"| {r['task_id']} | {r['condition']} | {r['machine_checkable']} | "
            f"{r['current_healer_detection']} | {r['current_healer_repair']} | {feas} |"
        )
    lines += [
        "",
        "## Verdict",
        "",
        "- **No existing Healer** performs AST def-use provenance tracing for `correct_answer` assembly.",
        "- **L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP** addresses JSON double-encoding only — not provenance.",
        "- Full-plan provenance enforcement would require new **detection-only or abstain** machinery (Prompt-Contract Healer v2 candidate scope).",
        "",
    ]
    return "\n".join(lines) + "\n"


def render_census_summary(census: list[dict[str, Any]]) -> str:
    from collections import Counter

    cls = Counter(c["structural_similarity_class"] for c in census)
    elig = sum(1 for c in census if c["eligibility_for_future_cross_contract_test"])
    abstain = sum(1 for c in census if c["structural_similarity_class"] == "UNPARSEABLE_OR_INSUFFICIENT_EVIDENCE")
    rewrite = sum(1 for c in census if c["algorithm_change_required"] == "yes")

    lines = [
        "# Domain-menu FAIL vs full-plan contract relation census",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Baseline commit: `{BASE_COMMIT}`",
        "",
        "## Evidence scope",
        "",
        "- Primary: `qwen35_*_math16_ab123_run_002` cells with `condition=ab2d` and `full_pass=FAIL`",
        "- Secondary: `math16_ab2d_480cell_system_prompt_defect_audit_v1.json` `ab2d_domain_menu` schema failures",
        "- **Not included:** per-cell pilot02 qwen4b/9b evaluation baseline (cell_level_baseline.jsonl not present in repo); aggregate FAIL rates cited from existing condition_summary only.",
        "",
        f"**Total census rows:** {len(census)}",
        "",
        "## Classification counts",
        "",
    ]
    for k, v in sorted(cls.items()):
        lines.append(f"- {k}: **{v}**")
    lines += [
        "",
        "## Summary",
        "",
        f"- Eligible for small cross-contract repair test: **{elig}**",
        f"- Must abstain (unparseable/insufficient): **{abstain}**",
        f"- Rewrite-level (algorithm change required): **{rewrite}**",
        "",
        "## Prompt-Contract Healer v2 worth designing?",
        "",
        "**Conditional yes.** Kwargs→frozen literal and narrow L2 rules cover a subset of domain-menu FAILs, but API-order/provenance/return-semantics gaps dominate. A v2 Healer should prioritize **detection + abstention** for full-plan-only contracts and **narrow deterministic repair** for zero-arg/kwargs misuse — not cross-condition algorithm rewrites.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    starting_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    pool = load_pool_manifest(ROOT)
    menu_files = sorted(MENU_DIR.glob("*.txt"))
    full_files = sorted(FULL_DIR.glob("*.txt"))
    prompts_complete = len(menu_files) == 16 and len(full_files) == 16

    contract_rows = build_prompt_contracts()
    manifest = {
        "audit_id": "math16_ab2d_v2_prompt_healer_readonly_audit_v1",
        "baseline_commit": BASE_COMMIT,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "experiment_id": "math16_ab2d_menu_vs_full_runtime_contract_v2",
        "n_tasks": 16,
        "n_prompts_expected": 32,
        "n_prompts_found": len(menu_files) + len(full_files),
        "prompts_complete": prompts_complete,
        "prompt_contract_entries": len(contract_rows),
        "general_safety_entries": len(GENERAL_SAFETY_CHECKS),
        "contracts": contract_rows,
        "general_safety": GENERAL_SAFETY_CHECKS,
        "research_healer_allowlist": list(RESEARCH_HEALER_RULES.keys()),
        "core_healer_files_readonly": CORE_HEALER_FILES,
        "scanned_files": {
            "prompts_domain_menu_v2": [str(p.relative_to(ROOT)) for p in menu_files],
            "prompts_full_v2": [str(p.relative_to(ROOT)) for p in full_files],
            "scaffolds": "agent_tools/finals_rebuild/math16_ab2d_v2_scaffolds.py",
            "healers_readonly": list(CORE_HEALER_FILES.values()) + list(r["file"] for r in RESEARCH_HEALER_RULES.values()),
        },
    }

    manifest_path = OUT_DIR / "prompt_contract_manifest_v2.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (OUT_DIR / "prompt_healer_coverage_audit_v1.md").write_text(
        render_prompt_coverage_md(contract_rows, "Prompt–Healer Coverage Audit (Prompt-derived contracts)"),
        encoding="utf-8",
    )
    (OUT_DIR / "general_safety_healer_coverage_v1.md").write_text(render_general_safety_md(), encoding="utf-8")
    (OUT_DIR / "answer_assembly_provenance_audit_v1.md").write_text(
        render_provenance_md(contract_rows), encoding="utf-8"
    )

    census = collect_fail_cells()
    jsonl_path = OUT_DIR / "domain_menu_fail_full_plan_relation_census_v1.jsonl"
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as f:
        for row in census:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    (OUT_DIR / "domain_menu_fail_full_plan_relation_summary_v1.md").write_text(
        render_census_summary(census), encoding="utf-8"
    )

    artifact_files = sorted(OUT_DIR.glob("*"))
    sha_lines = []
    for p in artifact_files:
        if p.is_file():
            sha_lines.append(f"{sha256_file(p)}  {p.relative_to(ROOT).as_posix()}")
    sha_path = OUT_DIR / "audit_manifest_sha256.txt"
    sha_path.write_text("\n".join(sha_lines) + "\n", encoding="utf-8")

    ending_head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    prompt_cov = [r for r in contract_rows if r["contract_id"].startswith("PC_")]
    coverage_counts = {
        "prompt_derived_contract_rows": len(prompt_cov),
        "general_safety_rows": len(GENERAL_SAFETY_CHECKS),
        "full_healer_detection": sum(1 for r in prompt_cov if r["current_healer_detection"] == "full"),
        "partial_healer_detection": sum(1 for r in prompt_cov if r["current_healer_detection"] == "partial"),
        "none_healer_detection": sum(1 for r in prompt_cov if r["current_healer_detection"] == "none"),
        "deterministic_repair": sum(1 for r in prompt_cov if r["current_healer_repair"] == "deterministic"),
        "detection_only_recommended": sum(1 for r in prompt_cov if r["recommended_action"] == "detection_only"),
        "abstain_recommended": sum(1 for r in prompt_cov if r["recommended_action"] == "abstain_only"),
    }
    census_counts = {
        "total_fail_cells_census": len(census),
        "by_class": {k: sum(1 for c in census if c["structural_similarity_class"] == k) for k in sorted({c["structural_similarity_class"] for c in census})},
        "cross_contract_eligible": sum(1 for c in census if c["eligibility_for_future_cross_contract_test"]),
    }

    return {
        "starting_head": starting_head,
        "ending_head": ending_head,
        "prompts_complete": prompts_complete,
        "coverage_counts": coverage_counts,
        "census_counts": census_counts,
        "artifact_dir": str(OUT_DIR.relative_to(ROOT)),
        "sha256_manifest": str(sha_path.relative_to(ROOT)),
    }


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
