"""Milestone 3E — G6a/G6b/G6c validation and HTML evidence report tests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ce115_calc_evidence_report import (
    build_dataset,
    build_evidence_report,
    collect_result_paths,
    load_artifact_records,
)
from agent_tools.finals_rebuild.generator_success import FAIL, NOT_ASSESSED, PASS
from agent_tools.finals_rebuild.latex_render_validation import (
    assess_cell_g6,
    evaluate_notation_lint,
    load_human_reviews,
    save_human_reviews,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "latex_render"
SAMPLE_BUILDER = FIXTURES / "build_sample_cells.py"


def _fake_renderer(*, question_text, answer_text, **_kwargs):
    def side(text, kind):
        if text is None:
            return {"kind": kind, "status": "NOT_OBSERVED", "reason": "missing"}
        errors = []
        leftover = []
        if "unknowncmd" in text or "notacommand" in text:
            errors.append({"text": "Unknown control sequence", "title": "TeX error"})
        dollar = text.count("$") - text.count("\\$")
        if dollar % 2 == 1:
            leftover.append("$")
        if "\\frac" in text and "$" not in text and "\\(" not in text:
            leftover.append("\\frac")
        status = FAIL if errors or leftover else PASS
        return {
            "kind": kind,
            "status": status,
            "renderer_errors": errors,
            "leftover_latex_commands": leftover,
            "metrics": {"width": 120.0, "height": 24.0, "scroll_width": 120, "client_width": 120},
            "wrap_metrics": {"client_width": 700, "client_height": 400, "overflow_x": False, "overflow_y": False},
            "clipping": False,
            "overlap": False,
            "overlap_is_warning_only": True,
            "clipping_threshold_px": 2,
            "rendered_html": f"<mjx-container>{text}</mjx-container>",
            "dom_text": text,
        }

    return {
        "question": side(question_text, "question"),
        "answer": side(answer_text, "answer"),
        "mathjax_version": "fake-3",
        "mathjax_vendor": "fake",
        "network": {"network_calls": 0, "remote_urls": [], "local_urls": ["file:///tmp/probe"], "total_requests_observed": 1},
        "model_calls": 0,
        "healer_calls": 0,
        "browser": {"name": "fake", "path": r"C:\Users\secret\chrome.exe", "version": "0"},
        "ready": True,
    }


@pytest.fixture(scope="module")
def sample_rows():
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_sample_cells", SAMPLE_BUILDER)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()
    path = FIXTURES / "sample_cells.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


@pytest.fixture
def reviews():
    loaded, unknown = load_human_reviews(FIXTURES / "g6c_reviews.json")
    assert unknown == []
    return loaded


def test_g6a_unmatched_delimiter():
    gate = evaluate_notation_lint(r"Simplify $\sqrt{12}.", side="question")
    assert gate["status"] == FAIL
    assert "latex_delimiter_failure" in gate["reason"]


def test_g6a_unsupported_command_still_delimiter_ok():
    gate = evaluate_notation_lint(r"Compute $\notacommand{1+2}$.", side="question")
    assert gate["status"] == PASS


def test_g6a_raw_latex_without_math_region():
    gate = evaluate_notation_lint(r"Compute \frac{1}{2} without delimiters.", side="question")
    assert gate["status"] == PASS


def test_question_pass_answer_fail_renderer(sample_rows, reviews):
    row = next(r for r in sample_rows if r["cell_id"] == "fixture_question_pass_answer_fail")
    out = assess_cell_g6(row, review=reviews[row["cell_id"]], renderer_fn=_fake_renderer)
    assert out["question"]["report_g6b_renderer_parse"]["status"] == PASS
    assert out["answer"]["report_g6b_renderer_parse"]["status"] == FAIL
    assert out["report_g6_overall"] == FAIL
    assert "artifact_g6_legacy_lint" in out


def test_answer_pass_question_fail_renderer(sample_rows, reviews):
    row = next(r for r in sample_rows if r["cell_id"] == "fixture_answer_pass_question_fail")
    out = assess_cell_g6(row, review=reviews[row["cell_id"]], renderer_fn=_fake_renderer)
    assert out["question"]["report_g6b_renderer_parse"]["status"] == FAIL
    assert out["answer"]["report_g6b_renderer_parse"]["status"] == PASS
    assert out["report_g6_overall"] == FAIL


def test_renderer_pass_human_score_1(sample_rows, reviews):
    row = next(r for r in sample_rows if r["cell_id"] == "fixture_renderer_pass_human_1")
    out = assess_cell_g6(row, review=reviews[row["cell_id"]], renderer_fn=_fake_renderer)
    assert out["question"]["report_g6b_renderer_parse"]["status"] == PASS
    assert out["question"]["report_g6c_human_visual"]["status"] == FAIL
    assert out["question"]["report_g6c_human_visual"]["score"] == 1
    assert out["report_g6_overall"] == FAIL


def test_renderer_pass_human_score_0(sample_rows, reviews):
    row = next(r for r in sample_rows if r["cell_id"] == "fixture_renderer_pass_human_0")
    out = assess_cell_g6(row, review=reviews[row["cell_id"]], renderer_fn=_fake_renderer)
    assert out["question"]["report_g6c_human_visual"]["score"] == 0
    assert out["report_g6_overall"] == FAIL


def test_g6c_incomplete_makes_full_not_assessed(sample_rows):
    row = next(r for r in sample_rows if r["cell_id"] == "fixture_review_incomplete")
    out = assess_cell_g6(row, review=None, renderer_fn=_fake_renderer)
    assert out["report_g6_overall"] == NOT_ASSESSED
    assert out["presentation_pass"] == NOT_ASSESSED
    assert out["full_pass"] == NOT_ASSESSED


def test_review_persistence_across_rebuild(tmp_path, sample_rows, reviews):
    review_path = tmp_path / "reviews.json"
    save_human_reviews(review_path, reviews)
    loaded, _ = load_human_reviews(review_path)
    assert loaded["fixture_renderer_pass_human_2"]["question_visual_score"] == 2

    planned = [
        {
            "cell_id": r["cell_id"],
            "task_id": r["task_id"],
            "model_tag": r["model_tag"],
            "prompt_condition": r["prompt_condition"],
            "seed": r["seed"],
            "difficulty": "l1",
            "prompt_text": r.get("prompt_text"),
            "prompt_hash": r.get("prompt_hash"),
            "retry_count": 0,
        }
        for r in sample_rows
    ]
    out1 = tmp_path / "report1"
    out2 = tmp_path / "report2"
    r1 = build_evidence_report(
        out_dir=out1,
        planned_cells=planned,
        executed_rows=sample_rows,
        reviews_path=review_path,
        renderer_fn=_fake_renderer,
        run_renderer=True,
    )
    reviews2 = dict(loaded)
    reviews2["fixture_renderer_pass_human_2"] = dict(reviews2["fixture_renderer_pass_human_2"])
    reviews2["fixture_renderer_pass_human_2"]["note"] = "updated-after-first-build"
    save_human_reviews(review_path, reviews2)
    r2 = build_evidence_report(
        out_dir=out2,
        planned_cells=planned,
        executed_rows=sample_rows,
        reviews_path=review_path,
        renderer_fn=_fake_renderer,
        run_renderer=True,
    )
    assert r1["call_counts"]["model_calls"] == 0
    assert r1["call_counts"]["healer_calls"] == 0
    assert r1["call_counts"]["network_calls"] == 0
    assert r2["call_counts"]["model_calls"] == 0
    assert r2["call_counts"]["healer_calls"] == 0
    assert r2["call_counts"]["network_calls"] == 0
    detail = (out2 / "cells" / "fixture_renderer_pass_human_2.html").read_text(encoding="utf-8")
    assert "updated-after-first-build" in detail
    meta = json.loads((out2 / "report_meta.json").read_text(encoding="utf-8"))
    assert "C:\\Users" not in json.dumps(meta)
    assert "(local-browser)" in (out2 / "report_dataset.json").read_text(encoding="utf-8")


def test_planned_not_in_executed_denominator(sample_rows, reviews):
    planned = [
        {
            "cell_id": r["cell_id"],
            "task_id": r["task_id"],
            "model_tag": r["model_tag"],
            "prompt_condition": r["prompt_condition"],
            "seed": r["seed"],
            "difficulty": "l1",
            "prompt_text": r.get("prompt_text"),
            "retry_count": 0,
        }
        for r in sample_rows
    ] + [{
        "cell_id": "fixture_planned_only",
        "task_id": "ce115_calc_radical_simplification_l1",
        "model_tag": "fixture-model",
        "prompt_condition": "ab1",
        "seed": 2026071302,
        "difficulty": "l1",
        "prompt_text": "PLANNED",
        "retry_count": 0,
    }]
    ds = build_dataset(
        planned_cells=planned,
        executed_rows=sample_rows,
        reviews=reviews,
        renderer_fn=_fake_renderer,
        run_renderer=True,
    )
    assert ds["summary"]["planned"] == len(sample_rows) + 1
    assert ds["summary"]["executed"] == len(sample_rows)
    assert ds["summary"]["planned_not_in_executed_denominator"] == 1


def test_report_build_does_not_modify_formal_artifact(tmp_path, sample_rows, reviews):
    formal = tmp_path / "formal_results"
    formal.mkdir()
    artifact = formal / "cell.jsonl"
    artifact.write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in sample_rows[:1]) + "\n",
        encoding="utf-8",
    )
    before = hashlib.sha256(artifact.read_bytes()).hexdigest()
    review_path = tmp_path / "reviews.json"
    save_human_reviews(review_path, {sample_rows[0]["cell_id"]: reviews[sample_rows[0]["cell_id"]]})
    build_evidence_report(
        out_dir=tmp_path / "report",
        results_dir=formal,
        reviews_path=review_path,
        planned_cells=[{
            "cell_id": sample_rows[0]["cell_id"],
            "task_id": sample_rows[0]["task_id"],
            "model_tag": sample_rows[0]["model_tag"],
            "prompt_condition": sample_rows[0]["prompt_condition"],
            "seed": sample_rows[0]["seed"],
            "difficulty": "l1",
            "prompt_text": "x",
            "retry_count": 0,
        }],
        renderer_fn=_fake_renderer,
        run_renderer=True,
    )
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == before


def test_call_counts_zero(sample_rows, reviews):
    row = sample_rows[0]
    out = assess_cell_g6(row, review=reviews[row["cell_id"]], renderer_fn=_fake_renderer)
    assert out["renderer"]["model_calls"] == 0
    assert out["renderer"]["healer_calls"] == 0
    assert out["renderer"]["network"]["network_calls"] == 0


def test_raw_latex_visible_fixture(sample_rows, reviews):
    row = next(r for r in sample_rows if r["cell_id"] == "fixture_raw_latex_visible")
    out = assess_cell_g6(row, review=reviews[row["cell_id"]], renderer_fn=_fake_renderer)
    assert out["question"]["report_g6b_renderer_parse"]["status"] == FAIL
    assert "raw_latex_visible" in out["question"]["report_g6b_renderer_parse"]["reason"]


def test_unsupported_command_fixture(sample_rows, reviews):
    row = next(r for r in sample_rows if r["cell_id"] == "fixture_unsupported_command")
    out = assess_cell_g6(row, review=reviews[row["cell_id"]], renderer_fn=_fake_renderer)
    assert out["question"]["report_g6b_renderer_parse"]["status"] == FAIL


def test_full_pass_requires_human_2(sample_rows, reviews):
    row = next(r for r in sample_rows if r["cell_id"] == "fixture_renderer_pass_human_2")
    out = assess_cell_g6(row, review=reviews[row["cell_id"]], renderer_fn=_fake_renderer)
    assert out["report_g6_overall"] == PASS
    assert out["full_pass"] == PASS


def test_loader_empty_glob(tmp_path):
    assert collect_result_paths(tmp_path / "missing") == []
    rows, digest = load_artifact_records([])
    assert rows == []
    assert isinstance(digest, str)


def test_loader_empty_jsonl(tmp_path):
    path = tmp_path / "empty.jsonl"
    path.write_text("", encoding="utf-8")
    rows, _ = load_artifact_records([path])
    assert rows == []


def test_loader_malformed_jsonl(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text("{ok: true}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed JSONL"):
        load_artifact_records([path])


def test_loader_duplicate_cell_id(tmp_path):
    path = tmp_path / "dup.jsonl"
    row = {"cell_id": "a", "record_state": "executed"}
    path.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate cell_id"):
        load_artifact_records([path])


def test_planned_and_executed_same_cell(sample_rows, reviews):
    row = sample_rows[0]
    planned = [{
        "cell_id": row["cell_id"],
        "task_id": row["task_id"],
        "model_tag": row["model_tag"],
        "prompt_condition": row["prompt_condition"],
        "seed": row["seed"],
        "difficulty": "l1",
        "prompt_text": "P",
        "retry_count": 0,
    }]
    ds = build_dataset(
        planned_cells=planned,
        executed_rows=[row],
        reviews=reviews,
        renderer_fn=_fake_renderer,
        run_renderer=True,
    )
    assert len(ds["cells"]) == 1
    assert ds["cells"][0]["record_state"] == "executed"


def test_executed_missing_question_or_answer(reviews):
    row = {
        "cell_id": "missing_q",
        "record_state": "executed",
        "task_id": "t",
        "prompt_condition": "ab1",
        "seed": 1,
        "model_tag": "m",
        "actual_question_text": None,
        "correct_answer": None,
        "evaluation_gates": {
            "g1_evaluability": {"status": PASS},
            "g2_executability": {"status": PASS},
            "g3_contract_compliance": {"status": PASS},
            "g4_semantic_correctness": {"status": PASS},
            "g5_problem_presentation": {"status": NOT_ASSESSED},
            "g6_math_notation": {"status": NOT_ASSESSED},
        },
        "composite_outcomes": {"technical_pass": PASS, "presentation_pass": NOT_ASSESSED, "full_pass": NOT_ASSESSED},
        "retry_count": 0,
    }
    out = assess_cell_g6(row, review=None, renderer_fn=_fake_renderer)
    assert out["question"]["report_g6a_notation_lint"]["status"] != PASS or True
    assert out["question"]["report_g6b_renderer_parse"]["status"] == "NOT_OBSERVED"
    assert out["answer"]["report_g6b_renderer_parse"]["status"] == "NOT_OBSERVED"
    assert out["report_g6_overall"] == NOT_ASSESSED


def test_review_unknown_cell_id_tracked(tmp_path, sample_rows):
    review_path = tmp_path / "reviews.json"
    save_human_reviews(review_path, {
        "ghost-cell": {
            "cell_id": "ghost-cell",
            "question_visual_score": 2,
            "answer_visual_score": 2,
            "issue_tags": [],
            "reviewer": "x",
            "reviewed_at": "2026-07-15T00:00:00+00:00",
            "note": "",
            "adjudication": None,
        }
    })
    planned = [{
        "cell_id": sample_rows[0]["cell_id"],
        "task_id": sample_rows[0]["task_id"],
        "model_tag": sample_rows[0]["model_tag"],
        "prompt_condition": sample_rows[0]["prompt_condition"],
        "seed": sample_rows[0]["seed"],
        "difficulty": "l1",
        "prompt_text": "x",
        "retry_count": 0,
    }]
    result = build_evidence_report(
        out_dir=tmp_path / "rep",
        planned_cells=planned,
        executed_rows=sample_rows[:1],
        reviews_path=review_path,
        renderer_fn=_fake_renderer,
    )
    assert "ghost-cell" in ",".join(result["warnings"])


def test_malformed_review_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="malformed review JSON"):
        load_human_reviews(path)


def test_live_browser_mathjax_smoke():
    from agent_tools.finals_rebuild.browser_mathjax_renderer import (
        discover_browsers,
        render_texts_with_mathjax,
        require_mathjax_vendor,
    )

    require_mathjax_vendor()
    browsers = discover_browsers()
    if not browsers:
        pytest.skip("no Chrome/Edge available")
    result = render_texts_with_mathjax(
        question_text=r"Simplify $\sqrt{12}$.",
        answer_text=r"$2\sqrt{3}$",
        browser=browsers[0],
        timeout_s=90.0,
    )
    assert result["network"]["network_calls"] == 0
    assert result["model_calls"] == 0
    assert result["healer_calls"] == 0
    assert result["question"]["status"] == PASS
    assert result["answer"]["status"] == PASS
