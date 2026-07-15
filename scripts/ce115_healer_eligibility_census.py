#!/usr/bin/env python3
"""Milestone 5A — CE115 taxonomy-level Healer eligibility *candidate* census.

Read-only. No repair. This census identifies taxonomy-level candidates only;
it does NOT mean the frozen Core rule is applicable to those cells.
Actual repair pool requires a separate frozen-rule applicability audit.

Derived from docs/experiments/success_definition.md (Post-Healer + Failure
taxonomy) plus enabled Core rules in core_adapter.py. Unknown outcomes are
BLOCKED / UNCLASSIFIED rather than guessed.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RESULTS = ROOT / "docs/experiments/results/ce115_calc_local_confirmatory"
OUT_JSON = ROOT / "docs/experiments/analysis/ce115_healer_eligibility_census.json"
OUT_MD = ROOT / "docs/experiments/analysis/ce115_healer_eligibility_census.md"

TAXONOMY_SOURCE = "docs/experiments/success_definition.md"
TAXONOMY_VERSION = "success_definition.md#Post-Healer+Failure-taxonomy-mapping"
CORE_REGISTRY_REL = "agent_tools/finals_rebuild/core_adapter.py"

# Outcome → (failure_taxonomy, failure_gate) from success_definition §13 + CE115 outcomes.
# Unknown keys must not be silently guessed.
OUTCOME_TAXONOMY: dict[str, tuple[str, str]] = {
    "passed": ("none", "none"),
    "parse_minor": ("parse_failure", "G1"),
    "missing_entry_point": ("missing_entry_point", "G1"),
    "runtime_failure": ("execution_failure", "G2"),
    "schema_failure": ("contract_schema_failure", "G3"),
    "answer_incorrect": ("oracle_mismatch", "G4"),
    "empty_response": ("empty_response", "G1"),
    "extraction_failure": ("extraction_failure", "G1"),
    "infrastructure_failure": ("infrastructure_failure", "infra"),
    "intrinsic_safety": ("semantic_invariant_failure", "G4"),
    "catastrophic_truncation": ("empty_response", "G1"),
}

# Eligible iff taxonomy admits deterministic non-semantic heal AND an enabled family exists.
# Enabled Core family today: core.normalize_fullwidth_python_punctuation → syntax_or_format.
ELIGIBLE_TAXONOMY_TO_REPAIR_FAMILY: dict[str, str] = {
    "parse_failure": "tier1_core_syntax_or_format",
}

# Explicitly non-semantic-excluded taxonomies (success_definition Post-Healer / §13 G4).
NONELIGIBLE_TAXONOMY_REASONS: dict[str, str] = {
    "none": "already_passed",
    "oracle_mismatch": "g4_semantic_oracle_mismatch_excluded",
    "semantic_invariant_failure": "g4_semantic_invariant_excluded",
    "contract_schema_failure": "g3_contract_no_enabled_non_semantic_schema_repair",
    "execution_failure": "g2_runtime_no_enabled_runtime_repair",
    "missing_entry_point": "g1_missing_entry_point_no_enabled_entry_point_repair",
    "empty_response": "g1_empty_response_no_code_candidate",
    "extraction_failure": "g1_extraction_failure_no_enabled_non_semantic_recovery",
    "infrastructure_failure": "infrastructure_out_of_healer_scope",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def dataset_hash(results_dir: Path) -> str:
    """Deterministic hash over sorted relative paths + file bytes."""
    h = hashlib.sha256()
    for path in sorted(results_dir.glob("*.jsonl")):
        rel = path.relative_to(ROOT).as_posix().encode("utf-8")
        h.update(rel)
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def classify_cell(row: dict[str, Any], *, artifact_hash: str) -> dict[str, Any]:
    outcome = str(row.get("outcome") or "")
    cell_id = str(row.get("cell_id") or "")
    base = {
        "cell_id": cell_id,
        "model": row.get("model_tag"),
        "condition": row.get("prompt_condition"),
        "task": row.get("task_id"),
        "seed": row.get("seed"),
        "observed_outcome": outcome,
        "raw_artifact_hash": artifact_hash,
    }

    if outcome not in OUTCOME_TAXONOMY:
        return {
            **base,
            "failure_gate": "UNCLASSIFIED",
            "failure_taxonomy": "unknown",
            "healer_eligible": False,
            "eligibility_reason": "UNKNOWN_OUTCOME_BLOCKED",
            "applicable_deterministic_repair_family": None,
            "exclusion_reason": f"unknown_outcome:{outcome}",
            "census_status": "BLOCKED_UNCLASSIFIED",
        }

    taxonomy, gate = OUTCOME_TAXONOMY[outcome]
    if outcome == "passed" or taxonomy == "none":
        return {
            **base,
            "failure_gate": gate,
            "failure_taxonomy": taxonomy,
            "healer_eligible": False,
            "eligibility_reason": "already_passed",
            "applicable_deterministic_repair_family": None,
            "exclusion_reason": "already_passed",
            "census_status": "ALREADY_PASSED",
        }

    repair_family = ELIGIBLE_TAXONOMY_TO_REPAIR_FAMILY.get(taxonomy)
    if repair_family is not None:
        # Structural prerequisite: Healer acts on code; require candidate or raw.
        has_candidate = bool(str(row.get("candidate_extracted") or "").strip())
        has_raw = bool(str(row.get("raw_first_attempt_output") or "").strip())
        if not has_candidate and not has_raw:
            return {
                **base,
                "failure_gate": gate,
                "failure_taxonomy": taxonomy,
                "healer_eligible": False,
                "eligibility_reason": "eligible_taxonomy_but_no_code_artifact",
                "applicable_deterministic_repair_family": repair_family,
                "exclusion_reason": "missing_candidate_and_raw",
                "census_status": "NONELIGIBLE",
            }
        return {
            **base,
            "failure_gate": gate,
            "failure_taxonomy": taxonomy,
            "healer_eligible": True,
            "eligibility_reason": f"taxonomy_admits_non_semantic_repair:{taxonomy}",
            "applicable_deterministic_repair_family": repair_family,
            "exclusion_reason": None,
            "census_status": "ELIGIBLE",
        }

    exclusion = NONELIGIBLE_TAXONOMY_REASONS.get(taxonomy, f"taxonomy_not_in_eligible_map:{taxonomy}")
    return {
        **base,
        "failure_gate": gate,
        "failure_taxonomy": taxonomy,
        "healer_eligible": False,
        "eligibility_reason": exclusion,
        "applicable_deterministic_repair_family": None,
        "exclusion_reason": exclusion,
        "census_status": "NONELIGIBLE",
    }


def _frac(n: int, d: int) -> str:
    return f"{n} / {d}"


def build_stats(cells: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(cells)
    eligible = [c for c in cells if c["healer_eligible"] is True]
    passed = [c for c in cells if c["census_status"] == "ALREADY_PASSED"]
    noneligible = [c for c in cells if c["healer_eligible"] is False and c["census_status"] != "ALREADY_PASSED"]

    def subset(pred) -> list[dict[str, Any]]:
        return [c for c in cells if pred(c)]

    by_model = {}
    for model, denom in (("qwen3.5:4b", 36), ("qwen3.5:9b", 36)):
        group = subset(lambda c, m=model: c.get("model") == m)
        by_model[model] = {
            "eligible": _frac(sum(1 for c in group if c["healer_eligible"]), denom),
            "eligible_n": sum(1 for c in group if c["healer_eligible"]),
            "denominator": denom,
            "group_n": len(group),
        }

    by_condition = {}
    for cond, denom in (("ab1", 24), ("ab2g", 24), ("ab2d", 24)):
        group = subset(lambda c, k=cond: c.get("condition") == k)
        by_condition[cond] = {
            "eligible": _frac(sum(1 for c in group if c["healer_eligible"]), denom),
            "eligible_n": sum(1 for c in group if c["healer_eligible"]),
            "denominator": denom,
        }

    tasks = sorted({c.get("task") for c in cells})
    by_task = {}
    for task in tasks:
        group = subset(lambda c, t=task: c.get("task") == t)
        by_task[str(task)] = {
            "eligible": _frac(sum(1 for c in group if c["healer_eligible"]), 18),
            "eligible_n": sum(1 for c in group if c["healer_eligible"]),
            "denominator": 18,
        }

    by_outcome: dict[str, Any] = {}
    outcome_counts = Counter(c.get("observed_outcome") for c in cells)
    for outcome, count in sorted(outcome_counts.items()):
        group = subset(lambda c, o=outcome: c.get("observed_outcome") == o)
        by_outcome[str(outcome)] = {
            "n": count,
            "eligible": _frac(sum(1 for c in group if c["healer_eligible"]), count),
            "eligible_n": sum(1 for c in group if c["healer_eligible"]),
            "denominator": count,
        }

    model_x_condition: dict[str, Any] = {}
    for model in ("qwen3.5:4b", "qwen3.5:9b"):
        for cond in ("ab1", "ab2g", "ab2d"):
            key = f"{model}|{cond}"
            group = subset(lambda c, m=model, k=cond: c.get("model") == m and c.get("condition") == k)
            model_x_condition[key] = {
                "eligible": _frac(sum(1 for c in group if c["healer_eligible"]), 12),
                "eligible_n": sum(1 for c in group if c["healer_eligible"]),
                "denominator": 12,
                "group_n": len(group),
            }

    eligible_taxonomy = Counter(c["failure_taxonomy"] for c in eligible)
    noneligible_categories = Counter(
        c["exclusion_reason"] or c["eligibility_reason"] for c in cells if not c["healer_eligible"]
    )

    return {
        "overall": {
            "eligible": _frac(len(eligible), n),
            "eligible_n": len(eligible),
            "noneligible": _frac(len(noneligible), n),
            "noneligible_n": len(noneligible),
            "already_passed": _frac(len(passed), n),
            "already_passed_n": len(passed),
            "denominator": n,
        },
        "by_model": by_model,
        "by_condition": by_condition,
        "by_task": by_task,
        "by_observed_outcome": by_outcome,
        "model_x_condition": model_x_condition,
        "eligible_failure_taxonomy_composition": dict(eligible_taxonomy),
        "explicitly_noneligible_categories": dict(noneligible_categories),
    }


def main() -> int:
    from agent_tools.finals_rebuild.core_adapter import CORE_RULE_REGISTRY

    enabled_rules = {
        rid: {
            "enabled": rule.enabled,
            "safety_classification": rule.safety_classification,
            "domain_specific": rule.domain_specific,
        }
        for rid, rule in CORE_RULE_REGISTRY.items()
        if rule.enabled
    }

    cells: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in sorted(RESULTS.glob("*.jsonl")):
        text = path.read_text(encoding="utf-8")
        artifact_hash = sha256_bytes(text.encode("utf-8"))
        for line in text.splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("record_state") != "executed":
                continue
            cid = str(row.get("cell_id"))
            if cid in seen:
                raise SystemExit(f"duplicate cell_id: {cid}")
            seen.add(cid)
            cells.append(classify_cell(row, artifact_hash=artifact_hash))

    if len(cells) != 72:
        raise SystemExit(f"expected 72 executed cells, got {len(cells)}")

    script_path = Path(__file__).resolve()
    stats = build_stats(cells)
    eligible_n = int(stats["overall"]["eligible_n"])
    already_passed_n = int(stats["overall"]["already_passed_n"])
    failure_n = len(cells) - already_passed_n
    blocked = [c for c in cells if c.get("census_status") == "BLOCKED_UNCLASSIFIED"]
    report = {
        "census_kind": "taxonomy-level eligibility candidate census",
        "taxonomy_source": TAXONOMY_SOURCE,
        "taxonomy_version": TAXONOMY_VERSION,
        "core_registry": CORE_REGISTRY_REL,
        "enabled_core_rules": enabled_rules,
        "eligible_taxonomy_to_repair_family": dict(ELIGIBLE_TAXONOMY_TO_REPAIR_FAMILY),
        "observed_dataset_hash": dataset_hash(RESULTS),
        "script_sha256": sha256_file(script_path),
        "success_definition_sha256": sha256_file(ROOT / TAXONOMY_SOURCE),
        "core_adapter_sha256": sha256_file(ROOT / CORE_REGISTRY_REL),
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "call_counts": {"model": 0, "healer": 0, "retry": 0, "external_api": 0},
        "n_cells": len(cells),
        "unique_cell_ids": len(seen),
        "blocked_unclassified_count": len(blocked),
        "blocked_unclassified_cell_ids": [c["cell_id"] for c in blocked],
        "window_metrics": {
            "taxonomy_candidate_prevalence": f"{eligible_n} / {len(cells)}",
            "taxonomy_candidate_width_among_failures": f"{eligible_n} / {failure_n}",
            "rule_applicable_window": "PENDING_FROZEN_RULE_APPLICABILITY_AUDIT",
        },
        "stats": stats,
        "cells": cells,
        "notes": [
            "This is a taxonomy-level eligibility candidate census only.",
            "The 18 taxonomy candidates are NOT confirmed rule-applicable.",
            "Actual Healer replay pool requires frozen-rule applicability audit.",
            "Read-only; no Healer repair executed.",
            "answer_incorrect / oracle_mismatch are excluded (G4 semantic).",
            "Only parse_failure currently maps to an enabled Core non-semantic family.",
            "Unknown outcomes are BLOCKED_UNCLASSIFIED.",
        ],
    }

    # Deterministic body (exclude generated_at from hash of stats content by sorting keys).
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    stats = report["stats"]
    lines = [
        "# CE115 Taxonomy-Level Healer Eligibility Candidate Census (read-only)",
        "",
        "This document reports a **taxonomy-level eligibility candidate census**.",
        "Candidates are **not** confirmed frozen-rule applicable.",
        "Actual repair window remains pending the frozen-rule applicability audit.",
        "",
        f"- taxonomy: `{TAXONOMY_SOURCE}` (`{TAXONOMY_VERSION}`)",
        f"- observed_dataset_hash: `{report['observed_dataset_hash']}`",
        f"- script_sha256: `{report['script_sha256']}`",
        f"- enabled Core rules: `{list(enabled_rules)}`",
        f"- BLOCKED_UNCLASSIFIED: **{report['blocked_unclassified_count']}** `{report['blocked_unclassified_cell_ids']}`",
        f"- taxonomy candidate prevalence: **{report['window_metrics']['taxonomy_candidate_prevalence']}**",
        f"- candidate window width among failures: **{report['window_metrics']['taxonomy_candidate_width_among_failures']}**",
        f"- rule-applicable window: **{report['window_metrics']['rule_applicable_window']}**",
        f"- call_counts: model/healer/retry/API = 0/0/0/0",
        "",
        "## Overall (taxonomy candidates)",
        "",
        f"- taxonomy-level eligible candidates: **{stats['overall']['eligible']}**",
        f"- noneligible: **{stats['overall']['noneligible']}**",
        f"- already_passed: **{stats['overall']['already_passed']}**",
        "",
        "## By model",
        "",
    ]
    for model, row in stats["by_model"].items():
        lines.append(f"- {model}: taxonomy candidates **{row['eligible']}**")
    lines.extend(["", "## By condition", ""])
    for cond, row in stats["by_condition"].items():
        lines.append(f"- {cond}: taxonomy candidates **{row['eligible']}**")
    lines.extend(["", "## By task", ""])
    for task, row in stats["by_task"].items():
        lines.append(f"- {task}: taxonomy candidates **{row['eligible']}**")
    lines.extend(["", "## By observed outcome", ""])
    for outcome, row in stats["by_observed_outcome"].items():
        lines.append(f"- {outcome}: n={row['n']}, taxonomy candidates **{row['eligible']}**")
    lines.extend(["", "## Model × condition (taxonomy candidates / 12)", ""])
    for key, row in stats["model_x_condition"].items():
        lines.append(f"- {key}: **{row['eligible']}**")
    lines.extend(
        [
            "",
            "## Taxonomy candidate composition",
            "",
            f"`{stats['eligible_failure_taxonomy_composition']}`",
            "",
            "## Explicitly noneligible categories",
            "",
            f"`{stats['explicitly_noneligible_categories']}`",
            "",
            "## Boundary notes",
            "",
            "- Taxonomy candidate window = G1 `parse_failure` / observed `parse_minor` only.",
            "- These candidates are **not** yet confirmed applicable to frozen Core rule.",
            "- All 16 `answer_incorrect` cells are G4 `oracle_mismatch` → excluded.",
            "- G2 runtime / G3 schema / missing_entry_point have no enabled non-semantic repair family → excluded.",
            "- No Healer repair was executed in this census.",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "json": str(OUT_JSON.relative_to(ROOT)).replace("\\", "/"),
                "md": str(OUT_MD.relative_to(ROOT)).replace("\\", "/"),
                "overall": stats["overall"],
                "eligible_taxonomy": stats["eligible_failure_taxonomy_composition"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
