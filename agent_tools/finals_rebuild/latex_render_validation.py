"""G6 split: notation lint (G6a), browser render (G6b), human visual review (G6c).

Report-side overlays only. Does not mutate formal artifacts or replace G1–G5.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from agent_tools.finals_rebuild.generator_success import (
    FAIL,
    NOT_ASSESSED,
    NOT_OBSERVED,
    PASS,
    evaluate_math_notation,
)

ISSUE_TAGS = frozenset({
    "raw_latex_visible",
    "broken_delimiter",
    "missing_symbol",
    "unsupported_command",
    "clipping",
    "overlap",
    "bad_line_break",
    "mixed_text_math",
    "answer_render_error",
    "other",
})
VISUAL_SCORES = frozenset({0, 1, 2})

RendererFn = Callable[..., dict[str, Any]]


def _status_gate(status: str, reason: str, **evidence: Any) -> dict[str, Any]:
    return {"status": status, "reason": reason, **evidence}


def evaluate_notation_lint(text: Any, *, side: str) -> dict[str, Any]:
    """G6a: reuse formal delimiter/brace/malformed lint (regex-assisted)."""
    if text is None or (isinstance(text, str) and not text.strip()):
        return _status_gate(
            NOT_OBSERVED,
            f"{side}_text_unavailable",
            side=side,
            uses_latex=False,
        )
    if not isinstance(text, str):
        text = str(text)
    gate = evaluate_math_notation(text)
    gate = dict(gate)
    gate["side"] = side
    gate["gate"] = "report_g6a_notation_lint"
    return gate


def evaluate_renderer_side(side_result: Mapping[str, Any] | None, *, side: str) -> dict[str, Any]:
    """Map browser probe evidence to report_g6b_renderer_parse PASS/FAIL/NOT_OBSERVED."""
    if side_result is None:
        return _status_gate(NOT_ASSESSED, "renderer_result_missing", side=side, gate="report_g6b_renderer_parse")
    if side_result.get("blocked"):
        return _status_gate(
            FAIL,
            side_result.get("reason") or "browser_unavailable",
            side=side,
            gate="report_g6b_renderer_parse",
            blocked=True,
            evidence=dict(side_result),
        )
    status = side_result.get("status")
    if status == NOT_OBSERVED:
        return _status_gate(
            NOT_OBSERVED,
            side_result.get("reason") or f"{side}_text_unavailable",
            side=side,
            gate="report_g6b_renderer_parse",
            evidence=dict(side_result),
        )
    if status == PASS:
        return _status_gate(
            PASS,
            "renderer_checks_passed",
            side=side,
            gate="report_g6b_renderer_parse",
            evidence=dict(side_result),
            overlap_warning=bool(side_result.get("overlap")),
        )
    reasons = []
    if side_result.get("renderer_errors"):
        reasons.append("renderer_error")
    if side_result.get("leftover_latex_commands"):
        reasons.append("raw_latex_visible")
    if side_result.get("clipping"):
        reasons.append("clipping")
    # Overlap is warning/evidence only — do not FAIL aggregate G6b on overlap alone.
    return _status_gate(
        FAIL,
        ",".join(reasons) if reasons else "renderer_validation_failed",
        side=side,
        gate="report_g6b_renderer_parse",
        evidence=dict(side_result),
        overlap_warning=bool(side_result.get("overlap")),
    )


def load_human_reviews(
    path: Path | str | None,
    *,
    known_cell_ids: set[str] | None = None,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Load independent human review JSON or CSV.

    Returns (reviews_by_cell_id, unknown_cell_ids). Unknown IDs are tracked and
    never silently dropped. Malformed review JSON raises ValueError.
    """
    if path is None:
        return {}, []
    path = Path(path)
    if not path.is_file():
        return {}, []
    try:
        if path.suffix.lower() == ".csv":
            out = _load_reviews_csv(path)
        else:
            raw = path.read_text(encoding="utf-8")
            if not raw.strip():
                raise ValueError(f"malformed review JSON (empty): {path}")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"malformed review JSON: {path}: {exc}") from exc
            rows = data.get("reviews", data) if isinstance(data, dict) else data
            if not isinstance(rows, list):
                raise ValueError("human review JSON must be a list or {reviews: [...]}")
            out = {}
            for row in rows:
                validated = validate_human_review(row)
                out[validated["cell_id"]] = validated
    except ValueError:
        raise
    unknown: list[str] = []
    if known_cell_ids is not None:
        unknown = sorted(cid for cid in out if cid not in known_cell_ids)
    return out, unknown


def _load_reviews_csv(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            tags = [t.strip() for t in (row.get("issue_tags") or "").split("|") if t.strip()]
            payload = {
                "cell_id": row["cell_id"],
                "question_visual_score": int(row["question_visual_score"]),
                "answer_visual_score": int(row["answer_visual_score"]),
                "issue_tags": tags,
                "reviewer": row.get("reviewer") or "",
                "reviewed_at": row.get("reviewed_at") or "",
                "note": row.get("note") or "",
                "adjudication": row.get("adjudication") or None,
            }
            validated = validate_human_review(payload)
            out[validated["cell_id"]] = validated
    return out


def validate_human_review(row: Mapping[str, Any]) -> dict[str, Any]:
    cell_id = row.get("cell_id")
    if not isinstance(cell_id, str) or not cell_id.strip():
        raise ValueError("human review requires cell_id")
    q = row.get("question_visual_score")
    a = row.get("answer_visual_score")
    if q not in VISUAL_SCORES or a not in VISUAL_SCORES:
        raise ValueError(f"visual scores must be 0/1/2 for {cell_id}")
    tags = list(row.get("issue_tags") or [])
    unknown = [t for t in tags if t not in ISSUE_TAGS]
    if unknown:
        raise ValueError(f"unknown issue_tags for {cell_id}: {unknown}")
    return {
        "cell_id": cell_id,
        "question_visual_score": int(q),
        "answer_visual_score": int(a),
        "issue_tags": tags,
        "reviewer": row.get("reviewer") or "",
        "reviewed_at": row.get("reviewed_at") or "",
        "note": row.get("note") or "",
        "adjudication": row.get("adjudication"),
    }


def save_human_reviews(path: Path | str, reviews: Mapping[str, Mapping[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "reviews": [validate_human_review(v) for _, v in sorted(reviews.items())],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def evaluate_human_side(review: Mapping[str, Any] | None, *, side: str) -> dict[str, Any]:
    """report_g6c_human_visual: score 2 => PASS, score 0/1 => FAIL, missing => NOT_ASSESSED."""
    if review is None:
        return _status_gate(NOT_ASSESSED, "human_review_incomplete", side=side, gate="report_g6c_human_visual")
    key = "question_visual_score" if side == "question" else "answer_visual_score"
    score = review.get(key)
    if score not in VISUAL_SCORES:
        return _status_gate(NOT_ASSESSED, "human_review_incomplete", side=side, gate="report_g6c_human_visual")
    if score == 2:
        return _status_gate(
            PASS, "visual_score_2", side=side, gate="report_g6c_human_visual", score=score, review=dict(review)
        )
    return _status_gate(
        FAIL,
        f"visual_score_{score}",
        side=side,
        gate="report_g6c_human_visual",
        score=score,
        review=dict(review),
    )


def combine_g6_triple(g6a: Mapping[str, Any], g6b: Mapping[str, Any], g6c: Mapping[str, Any]) -> str:
    statuses = [g6a["status"], g6b["status"], g6c["status"]]
    if NOT_ASSESSED in statuses or NOT_OBSERVED in statuses:
        # Incomplete human review or missing evidence must not become PASS/FAIL for aggregate G6.
        if FAIL in statuses and NOT_ASSESSED not in statuses and NOT_OBSERVED not in statuses:
            return FAIL
        if NOT_ASSESSED in statuses:
            return NOT_ASSESSED
        if FAIL in statuses:
            return FAIL
        return NOT_OBSERVED
    if FAIL in statuses:
        return FAIL
    return PASS


def g6_pass_requires_all_sides(question: Mapping[str, str], answer: Mapping[str, str]) -> str:
    """G6 PASS only when Q/A each have G6a/G6b PASS and G6c score 2."""
    needed = (
        question.get("g6a"), question.get("g6b"), question.get("g6c"),
        answer.get("g6a"), answer.get("g6b"), answer.get("g6c"),
    )
    # Incomplete human review must not resolve to PASS or FAIL.
    if any(s == NOT_ASSESSED for s in needed):
        return NOT_ASSESSED
    if any(s in {None, NOT_OBSERVED} for s in needed):
        return NOT_OBSERVED if any(s == NOT_OBSERVED for s in needed) else NOT_ASSESSED
    if all(s == PASS for s in needed):
        return PASS
    return FAIL


def combine_presentation(g5: str | None, g6: str) -> str:
    if g6 == NOT_ASSESSED:
        return NOT_ASSESSED
    values = [g5 or NOT_OBSERVED, g6]
    if FAIL in values:
        return FAIL
    if NOT_OBSERVED in values or NOT_ASSESSED in values:
        return NOT_OBSERVED if NOT_OBSERVED in values else NOT_ASSESSED
    return PASS


def combine_full(technical: str | None, presentation: str) -> str:
    if presentation == NOT_ASSESSED:
        return NOT_ASSESSED
    values = [technical or NOT_OBSERVED, presentation]
    if FAIL in values:
        return FAIL
    if NOT_OBSERVED in values or NOT_ASSESSED in values:
        return NOT_OBSERVED if NOT_OBSERVED in values else NOT_ASSESSED
    return PASS


def extract_answer_text(record: Mapping[str, Any]) -> str | None:
    for key in ("correct_answer", "oracle_expected", "answer"):
        value = record.get(key)
        if isinstance(value, (str, int, float)) and str(value).strip():
            return str(value)
    # Nested returned payload sometimes only lives in forensic fields.
    detail = record.get("failure_detail")
    if isinstance(detail, dict):
        value = detail.get("correct_answer")
        if isinstance(value, (str, int, float)) and str(value).strip():
            return str(value)
    return None


def sanitize_renderer_public(render: Mapping[str, Any]) -> dict[str, Any]:
    """Strip absolute machine paths / temp URLs from persisted report evidence."""
    browser = render.get("browser")
    public_browser = None
    if isinstance(browser, dict):
        public_browser = {
            "name": browser.get("name"),
            "version": browser.get("version"),
            "path": "(local-browser)",
        }
    network = dict(render.get("network") or {})
    network = {
        "network_calls": int(network.get("network_calls") or 0),
        "remote_url_count": len(network.get("remote_urls") or []),
        "local_request_count": len(network.get("local_urls") or []),
        "total_requests_observed": int(network.get("total_requests_observed") or 0),
    }
    return {
        "browser": public_browser,
        "mathjax_version": render.get("mathjax_version"),
        "mathjax_vendor": "agent_tools/finals_rebuild/vendor/mathjax/tex-svg.js",
        "network": network,
        "model_calls": int(render.get("model_calls") or 0),
        "healer_calls": int(render.get("healer_calls") or 0),
        "blocked": bool(render.get("blocked")),
        "status": render.get("status"),
        "question_evidence": render.get("question"),
        "answer_evidence": render.get("answer"),
    }


def assess_cell_g6(
    record: Mapping[str, Any],
    *,
    review: Mapping[str, Any] | None,
    renderer_fn: RendererFn | None = None,
    render_cache: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build report-side G6 overlays without rewriting formal artifact gates."""
    from agent_tools.finals_rebuild.browser_mathjax_renderer import render_texts_with_mathjax

    question_text = record.get("actual_question_text")
    if question_text is not None and not isinstance(question_text, str):
        question_text = str(question_text)
    answer_text = extract_answer_text(record)

    q_g6a = evaluate_notation_lint(question_text, side="question")
    a_g6a = evaluate_notation_lint(answer_text, side="answer")

    cache_key = json.dumps(
        {"q": question_text, "a": answer_text},
        ensure_ascii=False,
        sort_keys=True,
    )
    if render_cache is not None and cache_key in render_cache:
        render = render_cache[cache_key]
    else:
        fn = renderer_fn or render_texts_with_mathjax
        render = fn(question_text=question_text, answer_text=answer_text)
        if render_cache is not None:
            render_cache[cache_key] = render

    q_g6b = evaluate_renderer_side(render.get("question"), side="question")
    a_g6b = evaluate_renderer_side(render.get("answer"), side="answer")
    q_g6c = evaluate_human_side(review, side="question")
    a_g6c = evaluate_human_side(review, side="answer")

    question_statuses = {
        "g6a": q_g6a["status"],
        "g6b": q_g6b["status"],
        "g6c": q_g6c["status"],
    }
    answer_statuses = {
        "g6a": a_g6a["status"],
        "g6b": a_g6b["status"],
        "g6c": a_g6c["status"],
    }
    overall = g6_pass_requires_all_sides(question_statuses, answer_statuses)

    formal_gates = record.get("evaluation_gates") or {}
    formal_composites = record.get("composite_outcomes") or {}
    g5 = (formal_gates.get("g5_problem_presentation") or {}).get("status")
    technical = formal_composites.get("technical_pass")
    presentation = combine_presentation(g5, overall)
    full = combine_full(technical, presentation)
    artifact_g6 = (formal_gates.get("g6_math_notation") or {}).get("status")

    return {
        "artifact_g6_legacy_lint": artifact_g6 if artifact_g6 is not None else NOT_ASSESSED,
        "report_g6_overall": overall,
        "presentation_pass": presentation,
        "full_pass": full,
        "technical_pass": technical if technical is not None else NOT_ASSESSED,
        "question": {
            "report_g6a_notation_lint": q_g6a,
            "report_g6b_renderer_parse": q_g6b,
            "report_g6c_human_visual": q_g6c,
        },
        "answer": {
            "report_g6a_notation_lint": a_g6a,
            "report_g6b_renderer_parse": a_g6b,
            "report_g6c_human_visual": a_g6c,
        },
        "renderer": sanitize_renderer_public(render),
        "human_review": dict(review) if review else None,
        "human_review_complete": review is not None,
    }


def na(value: Any, *, default: str = "NOT_AVAILABLE") -> Any:
    if value is None or value == "":
        return default
    return value
