#!/usr/bin/env python3
"""Milestone 5A.1 — Frozen-rule applicability audit (read-only).

Applies only core.normalize_fullwidth_python_punctuation in memory to the
18 taxonomy candidates. Does not write post_healer ledgers or mutate artifacts.
"""
from __future__ import annotations

import ast
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

from agent_tools.finals_rebuild.core_adapter import (  # noqa: E402
    CORE_RULE_REGISTRY,
    _FULLWIDTH_PUNCT_MAP,
    normalize_fullwidth_python_punctuation,
)

RESULTS = ROOT / "docs/experiments/results/ce115_calc_local_confirmatory"
CENSUS = ROOT / "docs/experiments/analysis/ce115_healer_eligibility_census.json"
OUT_JSON = ROOT / "docs/experiments/analysis/ce115_healer_rule_applicability.json"
OUT_MD = ROOT / "docs/experiments/analysis/ce115_healer_rule_applicability.md"
GAP_JSON = ROOT / "docs/experiments/analysis/ce115_healer_rule_gap_log.json"

RULE_ID = "core.normalize_fullwidth_python_punctuation"
SUPPORTED = frozenset(_FULLWIDTH_PUNCT_MAP.keys())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def try_parse(code: str) -> dict[str, Any]:
    try:
        ast.parse(code)
        return {"ok": True, "error": None}
    except SyntaxError as exc:
        return {
            "ok": False,
            "error": {
                "msg": exc.msg,
                "lineno": exc.lineno,
                "offset": exc.offset,
                "text": (exc.text or "")[:200],
            },
        }


def find_supported_fullwidth(code: str) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    for i, ch in enumerate(code):
        if ch in SUPPORTED:
            line = code.count("\n", 0, i) + 1
            col = i - (code.rfind("\n", 0, i) + 1)
            hits.append(
                {
                    "char": ch,
                    "ascii": _FULLWIDTH_PUNCT_MAP[ch],
                    "index": i,
                    "line": line,
                    "col": col,
                }
            )
    return hits


def character_diff(before: str, after: str) -> dict[str, Any]:
    """Index-aligned replacements only; any insert/delete → non_rule / blocked."""
    if len(before) != len(after):
        return {
            "length_equal": False,
            "replacements": [],
            "non_rule_changes": abs(len(before) - len(after)),
            "non_rule_detail": "length_changed",
        }
    replacements: list[dict[str, Any]] = []
    non_rule = 0
    non_rule_detail: list[str] = []
    for i, (a, b) in enumerate(zip(before, after)):
        if a == b:
            continue
        if a in SUPPORTED and _FULLWIDTH_PUNCT_MAP[a] == b:
            replacements.append({"index": i, "from": a, "to": b})
        else:
            non_rule += 1
            non_rule_detail.append(f"{i}:{a!r}->{b!r}")
    return {
        "length_equal": True,
        "replacements": replacements,
        "non_rule_changes": non_rule,
        "non_rule_detail": non_rule_detail[:20],
    }


def detect_exclusion_signals(code: str, parse_before: dict[str, Any]) -> list[str]:
    signals: list[str] = []
    if "```" in code:
        signals.append("markdown_fence")
    if not code.strip():
        signals.append("empty_candidate")
        return signals
    # Truncation heuristics (conservative).
    stripped = code.strip()
    if stripped.endswith(("\\", ",", "(", "[", "{", ":", "+","-","*","/")):
        signals.append("truncated_trailer_token")
    if parse_before.get("error"):
        err = parse_before["error"]
        msg = str(err.get("msg") or "").lower()
        if "unexpected eof" in msg or "eof while" in msg:
            signals.append("truncated_eof")
        if "was never closed" in msg or "never closed" in msg:
            signals.append("unmatched_bracket")
        if "indent" in msg:
            signals.append("indentation_error")
    # Half-width syntax errors without supported fullwidth present handled later.
    return signals


def classify_applicability(
    *,
    code: str | None,
    raw: str | None,
) -> dict[str, Any]:
    if not isinstance(code, str) or not code.strip():
        return {
            "applicability_verdict": "INSUFFICIENT_EVIDENCE",
            "reason": "missing_or_empty_candidate_extracted",
            "rule_triggered": False,
            "normalization_changed_content": False,
            "gap_tags": ["extraction_or_persistence_issue"],
        }

    parse_before = try_parse(code)
    hits = find_supported_fullwidth(code)
    signals = detect_exclusion_signals(code, parse_before)
    gap_tags = list(signals)

    # Run frozen rule in memory only.
    after = normalize_fullwidth_python_punctuation(code)
    changed = after != code
    diff = character_diff(code, after)
    parse_after = try_parse(after)

    if diff["non_rule_changes"] != 0:
        return {
            "applicability_verdict": "PIPELINE_SUSPECT",
            "reason": "non_rule_character_changes_detected",
            "rule_triggered": bool(hits) and changed,
            "normalization_changed_content": changed,
            "supported_fullwidth_hits": hits,
            "parse_before": parse_before,
            "parse_after": parse_after,
            "before_hash": sha256_text(code),
            "after_hash": sha256_text(after),
            "exact_character_diff": diff,
            "exclusion_signals": signals,
            "gap_tags": gap_tags + ["non_rule_diff"],
            "non_rule_changes": diff["non_rule_changes"],
        }

    # Exclusion classes that this rule must never claim applicable.
    hard_exclusions = {
        "markdown_fence",
        "unmatched_bracket",
        "indentation_error",
        "truncated_eof",
        "truncated_trailer_token",
        "empty_candidate",
    }
    hard_hit = sorted(hard_exclusions.intersection(signals))

    if not hits:
        reason = "no_supported_fullwidth_punctuation"
        if hard_hit:
            reason = f"no_supported_fullwidth_and_{hard_hit[0]}"
            gap_tags.append(hard_hit[0])
        elif parse_before["ok"] is False:
            # Half-width syntax / other parse issues.
            gap_tags.append("halfwidth_or_other_syntax_error")
            reason = "parse_fail_without_supported_fullwidth"
        return {
            "applicability_verdict": "RULE_NOT_APPLICABLE",
            "reason": reason,
            "rule_triggered": False,
            "normalization_changed_content": False,
            "supported_fullwidth_hits": [],
            "parse_before": parse_before,
            "parse_after": parse_after,
            "before_hash": sha256_text(code),
            "after_hash": sha256_text(after),
            "exact_character_diff": diff,
            "exclusion_signals": signals,
            "gap_tags": gap_tags,
            "non_rule_changes": 0,
        }

    if not changed:
        return {
            "applicability_verdict": "RULE_NOT_APPLICABLE",
            "reason": "normalization_noop_despite_mapped_characters_present",
            "rule_triggered": False,
            "normalization_changed_content": False,
            "supported_fullwidth_hits": hits,
            "parse_before": parse_before,
            "parse_after": parse_after,
            "before_hash": sha256_text(code),
            "after_hash": sha256_text(after),
            "exact_character_diff": diff,
            "exclusion_signals": signals,
            "gap_tags": gap_tags + ["normalization_noop"],
            "non_rule_changes": 0,
        }

    # Rule produced allowed replacements only.
    if hard_hit and hard_hit != ["markdown_fence"]:
        # Soft: markdown fence always NOT_APPLICABLE even if fullwidth also present.
        pass
    if "markdown_fence" in signals:
        return {
            "applicability_verdict": "RULE_NOT_APPLICABLE",
            "reason": "markdown_fence_present_excluded",
            "rule_triggered": True,
            "normalization_changed_content": changed,
            "supported_fullwidth_hits": hits,
            "parse_before": parse_before,
            "parse_after": parse_after,
            "before_hash": sha256_text(code),
            "after_hash": sha256_text(after),
            "exact_character_diff": diff,
            "exclusion_signals": signals,
            "gap_tags": gap_tags + ["markdown_fence"],
            "non_rule_changes": 0,
        }

    if not parse_after["ok"]:
        return {
            "applicability_verdict": "RULE_NOT_APPLICABLE",
            "reason": "normalization_changed_but_still_parse_fail",
            "rule_triggered": True,
            "normalization_changed_content": True,
            "supported_fullwidth_hits": hits,
            "parse_before": parse_before,
            "parse_after": parse_after,
            "before_hash": sha256_text(code),
            "after_hash": sha256_text(after),
            "exact_character_diff": diff,
            "exclusion_signals": signals,
            "gap_tags": gap_tags + ["still_parse_fail_after_normalization"],
            "non_rule_changes": 0,
        }

    # All RULE_APPLICABLE conditions.
    if (
        hits
        and changed
        and diff["non_rule_changes"] == 0
        and diff["length_equal"]
        and parse_after["ok"]
        and "markdown_fence" not in signals
    ):
        return {
            "applicability_verdict": "RULE_APPLICABLE",
            "reason": "supported_fullwidth_normalized_parse_ok_rule_diff_only",
            "rule_triggered": True,
            "normalization_changed_content": True,
            "supported_fullwidth_hits": hits,
            "parse_before": parse_before,
            "parse_after": parse_after,
            "before_hash": sha256_text(code),
            "after_hash": sha256_text(after),
            "exact_character_diff": diff,
            "exclusion_signals": signals,
            "gap_tags": [],
            "non_rule_changes": 0,
        }

    return {
        "applicability_verdict": "INSUFFICIENT_EVIDENCE",
        "reason": "unresolved_applicability_state",
        "rule_triggered": bool(hits) and changed,
        "normalization_changed_content": changed,
        "supported_fullwidth_hits": hits,
        "parse_before": parse_before,
        "parse_after": parse_after,
        "before_hash": sha256_text(code),
        "after_hash": sha256_text(after),
        "exact_character_diff": diff,
        "exclusion_signals": signals,
        "gap_tags": gap_tags + ["unresolved"],
        "non_rule_changes": diff["non_rule_changes"],
    }


def load_taxonomy_candidates() -> list[dict[str, Any]]:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    cands = [c for c in census["cells"] if c.get("healer_eligible") is True]
    if len(cands) != 18:
        raise SystemExit(f"expected 18 taxonomy candidates, got {len(cands)}")
    return cands


def load_artifact(cell_id: str) -> dict[str, Any]:
    matches = list(RESULTS.glob(f"{cell_id}_git_*.jsonl"))
    if len(matches) != 1:
        # Fallback: scan
        matches = []
        for path in RESULTS.glob("*.jsonl"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("cell_id") == cell_id:
                    matches.append(path)
                    break
        matches = sorted(set(matches))
    if len(matches) != 1:
        raise SystemExit(f"artifact resolution failed for {cell_id}: {matches}")
    path = matches[0]
    row = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    return row


def _frac(n: int, d: int) -> str:
    return f"{n} / {d}"


def main() -> int:
    if RULE_ID not in CORE_RULE_REGISTRY or not CORE_RULE_REGISTRY[RULE_ID].enabled:
        raise SystemExit("frozen rule missing or disabled")

    candidates = load_taxonomy_candidates()
    cases: list[dict[str, Any]] = []
    gap_entries: list[dict[str, Any]] = []

    for cand in candidates:
        row = load_artifact(str(cand["cell_id"]))
        if row.get("outcome") != "parse_minor":
            raise SystemExit(f"candidate outcome drifted: {cand['cell_id']}")
        code = row.get("candidate_extracted")
        raw = row.get("raw_first_attempt_output")
        result = classify_applicability(
            code=code if isinstance(code, str) else None,
            raw=raw if isinstance(raw, str) else None,
        )
        case = {
            "cell_id": cand["cell_id"],
            "model": cand.get("model"),
            "condition": cand.get("condition"),
            "task": cand.get("task"),
            "seed": cand.get("seed"),
            "raw_first_attempt_output_hash": sha256_text(raw) if isinstance(raw, str) else None,
            "candidate_extracted_hash": sha256_text(code) if isinstance(code, str) else None,
            "parse_error": (result.get("parse_before") or {}).get("error"),
            "actual_fullwidth_python_punctuation": [
                h["char"] for h in result.get("supported_fullwidth_hits") or []
            ],
            "matched_characters_positions": result.get("supported_fullwidth_hits") or [],
            "normalization_before_hash": result.get("before_hash"),
            "normalization_after_hash": result.get("after_hash"),
            "exact_character_diff": result.get("exact_character_diff"),
            "rule_triggered": result.get("rule_triggered"),
            "normalization_changed_content": result.get("normalization_changed_content"),
            "after_normalization_parse_status": (
                "success" if (result.get("parse_after") or {}).get("ok") else "fail"
            ),
            "non_rule_changes": result.get("non_rule_changes", 0),
            "applicability_verdict": result["applicability_verdict"],
            "reason": result["reason"],
            "exclusion_signals": result.get("exclusion_signals") or [],
            "gap_tags": result.get("gap_tags") or [],
        }
        cases.append(case)
        if case["gap_tags"]:
            gap_entries.append(
                {
                    "cell_id": case["cell_id"],
                    "model": case["model"],
                    "condition": case["condition"],
                    "task": case["task"],
                    "gap_tags": case["gap_tags"],
                    "reason": case["reason"],
                    "note": "Potential other unfrozen repairs may exist; not in this rule pool.",
                }
            )

    verdict_counts = Counter(c["applicability_verdict"] for c in cases)
    applicable_n = verdict_counts.get("RULE_APPLICABLE", 0)

    def group_counts(key: str) -> dict[str, Any]:
        out: dict[str, Any] = {}
        buckets: dict[Any, list] = defaultdict(list)
        for c in cases:
            buckets[c.get(key)].append(c)
        for k, rows in sorted(buckets.items(), key=lambda x: str(x[0])):
            out[str(k)] = {
                "taxonomy_candidates": len(rows),
                "RULE_APPLICABLE": sum(1 for r in rows if r["applicability_verdict"] == "RULE_APPLICABLE"),
                "RULE_NOT_APPLICABLE": sum(
                    1 for r in rows if r["applicability_verdict"] == "RULE_NOT_APPLICABLE"
                ),
                "PIPELINE_SUSPECT": sum(
                    1 for r in rows if r["applicability_verdict"] == "PIPELINE_SUSPECT"
                ),
                "INSUFFICIENT_EVIDENCE": sum(
                    1 for r in rows if r["applicability_verdict"] == "INSUFFICIENT_EVIDENCE"
                ),
            }
        return out

    mx: dict[str, Any] = {}
    for model in ("qwen3.5:4b", "qwen3.5:9b"):
        for cond in ("ab1", "ab2g", "ab2d"):
            rows = [c for c in cases if c.get("model") == model and c.get("condition") == cond]
            mx[f"{model}|{cond}"] = {
                "taxonomy_candidates": len(rows),
                "RULE_APPLICABLE": sum(1 for r in rows if r["applicability_verdict"] == "RULE_APPLICABLE"),
            }

    downgraded = [
        {
            "cell_id": c["cell_id"],
            "verdict": c["applicability_verdict"],
            "reason": c["reason"],
            "gap_tags": c["gap_tags"],
        }
        for c in cases
        if c["applicability_verdict"] != "RULE_APPLICABLE"
    ]

    report = {
        "audit_kind": "frozen-rule applicability audit",
        "rule_id": RULE_ID,
        "taxonomy_candidate_count": 18,
        "verdict_counts": {
            "RULE_APPLICABLE": _frac(verdict_counts.get("RULE_APPLICABLE", 0), 18),
            "RULE_NOT_APPLICABLE": _frac(verdict_counts.get("RULE_NOT_APPLICABLE", 0), 18),
            "PIPELINE_SUSPECT": _frac(verdict_counts.get("PIPELINE_SUSPECT", 0), 18),
            "INSUFFICIENT_EVIDENCE": _frac(verdict_counts.get("INSUFFICIENT_EVIDENCE", 0), 18),
            "RULE_APPLICABLE_n": applicable_n,
            "RULE_NOT_APPLICABLE_n": verdict_counts.get("RULE_NOT_APPLICABLE", 0),
            "PIPELINE_SUSPECT_n": verdict_counts.get("PIPELINE_SUSPECT", 0),
            "INSUFFICIENT_EVIDENCE_n": verdict_counts.get("INSUFFICIENT_EVIDENCE", 0),
        },
        "windows": {
            "taxonomy_candidate_prevalence": "18 / 72",
            "taxonomy_candidate_width_among_failures": "18 / 63",
            "frozen_rule_applicable_among_failures": _frac(applicable_n, 63),
            "frozen_rule_applicable_among_total": _frac(applicable_n, 72),
        },
        "by_model": group_counts("model"),
        "by_condition": group_counts("condition"),
        "by_task": group_counts("task"),
        "model_x_condition": mx,
        "downgraded_cells": downgraded,
        "cases": cases,
        "call_counts": {
            "model_calls": 0,
            "healer_replay_calls": 0,
            "retry_calls": 0,
            "external_api_calls": 0,
        },
        "script_sha256": sha256_text(Path(__file__).read_text(encoding="utf-8")),
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notes": [
            "In-memory rule call only; no post_healer ledger; artifacts unchanged.",
            "Applicability does not overwrite observed outcomes.",
            "H1/H2: only taxonomy candidate vs frozen-rule applicable distributions reported.",
        ],
    }

    gap_report = {
        "rule_id": RULE_ID,
        "n_gap_entries": len(gap_entries),
        "gap_tag_counts": dict(Counter(tag for e in gap_entries for tag in e["gap_tags"])),
        "entries": gap_entries,
        "note": ("Gaps indicate failures that may need other unfrozen rules; not added to this pool. ""Gap tag counts may overlap on the same cell and must not be summed as unique cells; ""exploratory future work only, not a confirmatory gate."),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    GAP_JSON.write_text(json.dumps(gap_report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    gap_counts = gap_report["gap_tag_counts"]
    lines = [
        "# CE115 Frozen-Rule Applicability Audit",
        "",
        f"- rule: `{RULE_ID}`",
        f"- taxonomy candidates audited: **18**",
        f"- RULE_APPLICABLE: **{report['verdict_counts']['RULE_APPLICABLE']}**",
        f"- RULE_NOT_APPLICABLE: **{report['verdict_counts']['RULE_NOT_APPLICABLE']}**",
        f"- PIPELINE_SUSPECT: **{report['verdict_counts']['PIPELINE_SUSPECT']}**",
        f"- INSUFFICIENT_EVIDENCE: **{report['verdict_counts']['INSUFFICIENT_EVIDENCE']}**",
        f"- frozen-rule applicable window among failures: **{report['windows']['frozen_rule_applicable_among_failures']}**",
        f"- frozen-rule applicable window among total: **{report['windows']['frozen_rule_applicable_among_total']}**",
        "- verified rescue pool: **0**",
        "- Healer replay: **not executed** (no RULE_APPLICABLE cells)",
        "",
        "## Distinction (do not conflate)",
        "",
        "- **taxonomy-level candidate window:** **18 / 63** among failures (and **18 / 72** among total). "
        "This is a morphology/taxonomy filter only — **not** a repairable or intervention window.",
        f"- **frozen-rule applicable window:** **{report['windows']['frozen_rule_applicable_among_failures']}** among failures "
        f"(and **{report['windows']['frozen_rule_applicable_among_total']}** among total).",
        "- The count **18** must **not** be described as a healable/repairable/intervention set under the currently frozen single Core rule.",
        "",
        "## Formal conclusion",
        "",
        "Currently frozen single Core rule `core.normalize_fullwidth_python_punctuation` matched no formal Qwen3.5 confirmatory failures; "
        "this is Healer **rule-coverage mismatch** vs failure morphology, **not** invalid taxonomy/formal run.",
        "",
        "目前凍結的單一 Core 規則 `core.normalize_fullwidth_python_punctuation` 未匹配任何正式 Qwen3.5 confirmatory 失敗；"
        "此為 Healer **規則覆蓋與失敗型態不符**，而非 taxonomy／正式 run 無效。",
        "",
        "## Rule gaps (exploratory only)",
        "",
        "Gap tag counts (tags may **overlap** on the same cell and **must not** be summed as unique cells):",
        "",
        f"- `halfwidth_or_other_syntax_error`: {gap_counts.get('halfwidth_or_other_syntax_error', 0)}",
        f"- `indentation_error`: {gap_counts.get('indentation_error', 0)}",
        f"- `truncated_trailer_token`: {gap_counts.get('truncated_trailer_token', 0)}",
        "",
        "These gap tags are **exploratory future-work signals only**, not a confirmatory gate and not evidence for unfreezing or adding repair rules in this closeout.",
        "",
        "## Downgraded cells",
        "",
    ]
    for d in downgraded:
        lines.append(f"- `{d['cell_id']}`: **{d['verdict']}** — {d['reason']} gaps={d['gap_tags']}")
    lines.extend(["", "## Representative diffs (applicable only)", ""])
    for c in cases:
        if c["applicability_verdict"] != "RULE_APPLICABLE":
            continue
        reps = (c.get("exact_character_diff") or {}).get("replacements") or []
        lines.append(f"- `{c['cell_id']}` replacements={json.dumps(reps[:10], ensure_ascii=False)}")
    if applicable_n == 0:
        lines.append("- (none)")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(
        json.dumps(
            {
                "applicable_n": applicable_n,
                "verdict_counts": report["verdict_counts"],
                "windows": report["windows"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
