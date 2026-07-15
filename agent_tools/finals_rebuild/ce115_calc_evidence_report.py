"""Offline HTML experiment evidence report builder for CE115 calc confirmatory runs.

Read-only over formal artifacts. Recomputes G6a/G6b/G6c overlays for the report
without mutating source JSONL or G1–G5 evaluator results.
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from typing import Any, Mapping

from agent_tools.finals_rebuild.ce115_calc_formal_runner import (
    RECORD_STATE_EXECUTED,
    RECORD_STATE_PLANNED,
    build_local_confirmatory_plan,
)
from agent_tools.finals_rebuild.generator_success import FAIL, NOT_ASSESSED, NOT_OBSERVED, PASS
from agent_tools.finals_rebuild.latex_render_validation import (
    assess_cell_g6,
    load_human_reviews,
    na,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS_DIR = REPO_ROOT / "docs" / "experiments" / "results" / "ce115_calc_local_confirmatory"
DEFAULT_REVIEWS = REPO_ROOT / "docs" / "experiments" / "human_reviews" / "ce115_calc_g6c_reviews.json"
DEFAULT_MANIFEST = REPO_ROOT / "docs" / "experiments" / "manifests" / "ce115_calc_main_experiment_manifest.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _ratio(num: int, den: int) -> str:
    return f"{num} / {den}"


def _gate_status(record: Mapping[str, Any], key: str) -> str:
    gates = record.get("evaluation_gates")
    if not isinstance(gates, dict):
        return NOT_ASSESSED
    gate = gates.get(key)
    if not isinstance(gate, dict):
        return NOT_ASSESSED
    return str(gate.get("status") or NOT_ASSESSED)


def _healer_block(record: Mapping[str, Any]) -> dict[str, Any]:
    healer = record.get("healer")
    if not isinstance(healer, dict):
        return {
            "eligible": NOT_ASSESSED,
            "attempted": NOT_ASSESSED,
            "rescued": NOT_ASSESSED,
            "regressed": NOT_ASSESSED,
        }
    return {
        "eligible": healer.get("eligible"),
        "attempted": healer.get("attempted"),
        "rescued": healer.get("rescued"),
        "regressed": healer.get("regression"),
    }


def _diagnostics(record: Mapping[str, Any]) -> dict[str, Any]:
    diag = record.get("token_duration_diagnostics")
    if not isinstance(diag, dict):
        return {
            "prompt_tokens": NOT_ASSESSED,
            "completion_tokens": NOT_ASSESSED,
            "latency_ns": NOT_ASSESSED,
            "model_calls": NOT_ASSESSED,
            "repair_cpu_seconds": NOT_ASSESSED,
        }
    return {
        "prompt_tokens": na(diag.get("prompt_eval_count"), default=NOT_ASSESSED),
        "completion_tokens": na(diag.get("eval_count"), default=NOT_ASSESSED),
        "latency_ns": na(diag.get("total_duration"), default=NOT_ASSESSED),
        "model_calls": record.get("request_count", NOT_ASSESSED),
        "repair_cpu_seconds": na(record.get("repair_cpu_seconds"), default=NOT_ASSESSED),
    }


def load_artifact_records(paths: list[Path]) -> tuple[list[dict[str, Any]], str]:
    """Load JSONL artifacts. Empty path list / empty files are valid.

    Malformed lines and duplicate cell_id values raise ValueError (never silent).
    """
    rows: list[dict[str, Any]] = []
    hasher = hashlib.sha256()
    seen_ids: dict[str, str] = {}
    for path in sorted(paths):
        raw = path.read_bytes()
        hasher.update(raw)
        hasher.update(b"\n")
        text = raw.decode("utf-8")
        if not text.strip():
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"malformed JSONL {path}:{line_no}: {exc}") from exc
            cell_id = row.get("cell_id")
            if cell_id is not None:
                cid = str(cell_id)
                if cid in seen_ids:
                    raise ValueError(
                        f"duplicate cell_id {cid!r} in {path} "
                        f"(also seen in {seen_ids[cid]})"
                    )
                seen_ids[cid] = f"{path}:{line_no}"
            rows.append(row)
    return rows, hasher.hexdigest()


def collect_result_paths(results_dir: Path) -> list[Path]:
    """Glob formal result JSONL files. Missing directory → empty list (tracked)."""
    if not results_dir.is_dir():
        return []
    return sorted(p for p in results_dir.glob("*.jsonl") if p.is_file())


def _relpath_public(path: Path | str | None, *, repo_root: Path) -> str:
    if path is None:
        return "NOT_AVAILABLE"
    try:
        return Path(path).resolve().relative_to(repo_root.resolve()).as_posix()
    except Exception:  # noqa: BLE001
        # Keep basename only — never embed absolute machine paths in committed reports.
        return Path(path).name


def build_dataset(
    *,
    planned_cells: list[Mapping[str, Any]],
    executed_rows: list[Mapping[str, Any]],
    reviews: Mapping[str, Mapping[str, Any]],
    renderer_fn=None,
    run_renderer: bool = True,
    unknown_review_cell_ids: list[str] | None = None,
) -> dict[str, Any]:
    # Detect duplicate executed cell_ids before indexing.
    seen_exec: set[str] = set()
    for row in executed_rows:
        if not row.get("cell_id"):
            continue
        cid = str(row["cell_id"])
        if cid in seen_exec:
            raise ValueError(f"duplicate cell_id in executed rows: {cid}")
        seen_exec.add(cid)

    executed_by_id = {
        str(row["cell_id"]): dict(row)
        for row in executed_rows
        if row.get("cell_id")
    }
    render_cache: dict[str, Any] = {}
    cells: list[dict[str, Any]] = []
    model_calls = 0
    healer_calls = 0
    network_calls = 0
    warnings: list[str] = []
    if unknown_review_cell_ids:
        warnings.append(
            "unknown_review_cell_ids:" + ",".join(unknown_review_cell_ids)
        )

    planned_ids = [str(c["cell_id"]) for c in planned_cells]
    for cell in planned_cells:
        cell_id = str(cell["cell_id"])
        executed = executed_by_id.get(cell_id)
        if executed is None:
            row = {
                "cell_id": cell_id,
                "record_state": RECORD_STATE_PLANNED,
                "task_id": cell.get("task_id"),
                "model_tag": cell.get("model_tag"),
                "prompt_condition": cell.get("prompt_condition"),
                "seed": cell.get("seed"),
                "difficulty": cell.get("difficulty") or "l1",
                "prompt_text": cell.get("prompt_text"),
                "prompt_hash": cell.get("prompt_hash"),
                "output_path": cell.get("output_path"),
                "raw_first_attempt_output": None,
                "candidate_extracted": None,
                "actual_question_text": None,
                "correct_answer": None,
                "evaluation_gates": None,
                "composite_outcomes": None,
                "healer": None,
                "retry_count": cell.get("retry_count", 0),
                "failed": False,
                "g6_overlay": None,
            }
        else:
            review = reviews.get(cell_id)
            if run_renderer:
                overlay = assess_cell_g6(
                    executed,
                    review=review,
                    renderer_fn=renderer_fn,
                    render_cache=render_cache,
                )
                net = (overlay.get("renderer") or {}).get("network") or {}
                network_calls += int(net.get("network_calls") or 0)
                model_calls += int((overlay.get("renderer") or {}).get("model_calls") or 0)
                healer_calls += int((overlay.get("renderer") or {}).get("healer_calls") or 0)
            else:
                overlay = {
                    "artifact_g6_legacy_lint": _gate_status(executed, "g6_math_notation"),
                    "report_g6_overall": NOT_ASSESSED,
                    "presentation_pass": NOT_ASSESSED,
                    "full_pass": NOT_ASSESSED,
                    "technical_pass": (executed.get("composite_outcomes") or {}).get("technical_pass", NOT_ASSESSED),
                    "question": {},
                    "answer": {},
                    "human_review": dict(review) if review else None,
                    "human_review_complete": review is not None,
                    "renderer": {"network": {"network_calls": 0}, "model_calls": 0, "healer_calls": 0},
                }
            row = {
                "cell_id": cell_id,
                "record_state": executed.get("record_state", RECORD_STATE_EXECUTED),
                "task_id": executed.get("task_id") or cell.get("task_id"),
                "model_tag": executed.get("model_tag") or cell.get("model_tag"),
                "prompt_condition": executed.get("prompt_condition") or cell.get("prompt_condition"),
                "seed": executed.get("seed", cell.get("seed")),
                "difficulty": executed.get("difficulty") or cell.get("difficulty") or "l1",
                "prompt_text": cell.get("prompt_text"),
                "prompt_hash": executed.get("prompt_hash") or cell.get("prompt_hash"),
                "output_path": executed.get("output_path") or cell.get("output_path"),
                "raw_first_attempt_output": executed.get("raw_first_attempt_output"),
                "candidate_extracted": executed.get("candidate_extracted"),
                "actual_question_text": executed.get("actual_question_text"),
                "correct_answer": executed.get("correct_answer") or executed.get("oracle_expected"),
                "evaluation_gates": executed.get("evaluation_gates"),
                "composite_outcomes": executed.get("composite_outcomes"),
                "healer": _healer_block(executed),
                "retry_count": executed.get("retry_count", 0),
                "token_duration_diagnostics": _diagnostics(executed),
                "failed": executed.get("observation_status") not in {None, "observed_success"}
                and executed.get("record_state") == RECORD_STATE_EXECUTED
                and executed.get("outcome") not in {None, "passed"},
                "outcome": executed.get("outcome"),
                "ledger_stage": executed.get("ledger_stage"),
                "manifest_hash": executed.get("manifest_hash"),
                "git_commit": executed.get("git_commit"),
                "run_id": executed.get("run_id"),
                "g6_overlay": overlay,
                "source_record": executed,
            }
        cells.append(row)

    # Orphan executed rows not in plan (still show, not in planned denominator).
    for cell_id, executed in executed_by_id.items():
        if cell_id in planned_ids:
            continue
        review = reviews.get(cell_id)
        overlay = (
            assess_cell_g6(executed, review=review, renderer_fn=renderer_fn, render_cache=render_cache)
            if run_renderer
            else None
        )
        cells.append({
            "cell_id": cell_id,
            "record_state": executed.get("record_state", RECORD_STATE_EXECUTED),
            "task_id": executed.get("task_id"),
            "model_tag": executed.get("model_tag"),
            "prompt_condition": executed.get("prompt_condition"),
            "seed": executed.get("seed"),
            "difficulty": executed.get("difficulty") or "l1",
            "prompt_text": None,
            "orphan_executed": True,
            "raw_first_attempt_output": executed.get("raw_first_attempt_output"),
            "candidate_extracted": executed.get("candidate_extracted"),
            "actual_question_text": executed.get("actual_question_text"),
            "correct_answer": executed.get("correct_answer") or executed.get("oracle_expected"),
            "evaluation_gates": executed.get("evaluation_gates"),
            "composite_outcomes": executed.get("composite_outcomes"),
            "healer": _healer_block(executed),
            "retry_count": executed.get("retry_count", 0),
            "token_duration_diagnostics": _diagnostics(executed),
            "failed": True,
            "g6_overlay": overlay,
            "source_record": executed,
        })

    executed_cells = [c for c in cells if c.get("record_state") == RECORD_STATE_EXECUTED]
    planned_only = [c for c in cells if c.get("record_state") == RECORD_STATE_PLANNED]
    failed_cells = [c for c in executed_cells if c.get("failed")]

    def count_status(rows: list[dict[str, Any]], getter) -> dict[str, int]:
        out = {PASS: 0, FAIL: 0, NOT_ASSESSED: 0, NOT_OBSERVED: 0}
        for row in rows:
            status = getter(row) or NOT_ASSESSED
            out[status] = out.get(status, 0) + 1
        return out

    den = len(executed_cells)
    summary = {
        "planned": len(planned_cells),
        "executed": den,
        "failed": len(failed_cells),
        "planned_not_in_executed_denominator": len(planned_only),
        "g1": count_status(executed_cells, lambda r: _gate_status(r, "g1_evaluability")),
        "g2": count_status(executed_cells, lambda r: _gate_status(r, "g2_executability")),
        "g3": count_status(executed_cells, lambda r: _gate_status(r, "g3_contract_compliance")),
        "g4": count_status(executed_cells, lambda r: _gate_status(r, "g4_semantic_correctness")),
        "g5": count_status(executed_cells, lambda r: _gate_status(r, "g5_problem_presentation")),
        "g6": count_status(executed_cells, lambda r: (r.get("g6_overlay") or {}).get("report_g6_overall")),
        "artifact_g6_legacy_lint": count_status(
            executed_cells, lambda r: (r.get("g6_overlay") or {}).get("artifact_g6_legacy_lint")
            or _gate_status(r, "g6_math_notation"),
        ),
        "g6a_question": count_status(
            executed_cells,
            lambda r: ((r.get("g6_overlay") or {}).get("question") or {}).get(
                "report_g6a_notation_lint", {}
            ).get("status"),
        ),
        "g6b_question": count_status(
            executed_cells,
            lambda r: ((r.get("g6_overlay") or {}).get("question") or {}).get(
                "report_g6b_renderer_parse", {}
            ).get("status"),
        ),
        "g6c_question": count_status(
            executed_cells,
            lambda r: ((r.get("g6_overlay") or {}).get("question") or {}).get(
                "report_g6c_human_visual", {}
            ).get("status"),
        ),
        "technical": count_status(
            executed_cells,
            lambda r: (r.get("composite_outcomes") or {}).get("technical_pass")
            or (r.get("g6_overlay") or {}).get("technical_pass"),
        ),
        "presentation": count_status(
            executed_cells, lambda r: (r.get("g6_overlay") or {}).get("presentation_pass"),
        ),
        "full": count_status(executed_cells, lambda r: (r.get("g6_overlay") or {}).get("full_pass")),
        "healer_eligible": sum(
            1 for r in executed_cells if (r.get("healer") or {}).get("eligible") is True
        ),
        "healer_attempted": sum(
            1 for r in executed_cells if (r.get("healer") or {}).get("attempted") is True
        ),
        "healer_rescued": sum(
            1 for r in executed_cells if (r.get("healer") or {}).get("rescued") is True
        ),
        "healer_regressed": sum(
            1 for r in executed_cells if (r.get("healer") or {}).get("regressed") is True
        ),
        "retry_once": sum(1 for r in executed_cells if int(r.get("retry_count") or 0) == 1),
        "model_calls": model_calls,
        "healer_calls": healer_calls,
        "network_calls": network_calls,
        "executed_denominator": den,
        "warnings": warnings,
        "unknown_review_cell_ids": list(unknown_review_cell_ids or []),
    }

    return {
        "cells": cells,
        "summary": summary,
        "call_counts": {
            "model_calls": model_calls,
            "healer_calls": healer_calls,
            "network_calls": network_calls,
        },
        "warnings": warnings,
    }


def _esc(value: Any) -> str:
    if value is None:
        return "NOT_AVAILABLE"
    return html.escape(str(value), quote=True)


def _pre(value: Any) -> str:
    if value is None or value == "":
        return "<pre class=\"raw\">NOT_AVAILABLE</pre>"
    return f"<pre class=\"raw\">{html.escape(str(value))}</pre>"


def _status_badge(status: Any) -> str:
    label = NOT_ASSESSED if status is None else str(status)
    cls = {
        PASS: "ok",
        FAIL: "bad",
        NOT_ASSESSED: "na",
        NOT_OBSERVED: "na",
    }.get(label, "na")
    return f'<span class="badge {cls}">{_esc(label)}</span>'


CSS = """
:root { --bg:#f7f8fa; --card:#fff; --ink:#1a1a1a; --muted:#5b616a; --line:#d8dde6;
  --ok:#0f7b3a; --bad:#a12027; --na:#6b7280; }
* { box-sizing: border-box; }
body { margin:0; font-family:"Segoe UI","Noto Sans TC",sans-serif; background:var(--bg); color:var(--ink); }
header, main { max-width: 1200px; margin: 0 auto; padding: 16px; }
h1,h2,h3 { margin: 0.4em 0; }
.card { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px 14px; margin:12px 0; }
.grid { display:grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap:8px; }
.metric { background:#f3f5f8; border-radius:6px; padding:8px; }
.metric .label { color:var(--muted); font-size:12px; }
.metric .value { font-size:18px; font-weight:600; }
.badge { display:inline-block; padding:2px 8px; border-radius:999px; font-size:12px; border:1px solid var(--line); }
.badge.ok { color:var(--ok); background:#e8f7ee; }
.badge.bad { color:var(--bad); background:#fdecec; }
.badge.na { color:var(--na); background:#eef0f3; }
table { width:100%; border-collapse: collapse; font-size:13px; }
th, td { border-bottom:1px solid var(--line); padding:6px 8px; text-align:left; vertical-align:top; }
th { position:sticky; top:0; background:#eef2f7; }
.filters { display:flex; flex-wrap:wrap; gap:8px; margin:8px 0; }
.filters input, .filters select { padding:4px 6px; }
pre.raw { white-space:pre-wrap; word-break:break-word; background:#f4f5f7; border:1px solid var(--line);
  padding:8px; border-radius:6px; font-size:12px; }
.render-box { border:1px solid var(--line); padding:10px; background:#fff; min-height:2em; }
.muted { color:var(--muted); }
a { color:#0b57d0; }
"""


INDEX_JS = r"""
function applyFilters() {
  const q = (id) => document.getElementById(id);
  const val = (id) => (q(id).value || '').trim().toLowerCase();
  const rows = Array.from(document.querySelectorAll('tbody tr[data-cell]'));
  const want = {
    model: val('f-model'),
    task: val('f-task'),
    difficulty: val('f-difficulty'),
    condition: val('f-condition'),
    seed: val('f-seed'),
    g1: val('f-g1'),
    g2: val('f-g2'),
    g3: val('f-g3'),
    g4: val('f-g4'),
    g5: val('f-g5'),
    g6: val('f-g6'),
    special: val('f-special'),
  };
  let shown = 0;
  for (const row of rows) {
    const d = row.dataset;
    let ok = true;
    if (want.model && d.model !== want.model) ok = false;
    if (want.task && !(d.task || '').includes(want.task)) ok = false;
    if (want.difficulty && d.difficulty !== want.difficulty) ok = false;
    if (want.condition && d.condition !== want.condition) ok = false;
    if (want.seed && d.seed !== want.seed) ok = false;
    for (const g of ['g1','g2','g3','g4','g5','g6']) {
      if (want[g] && (d[g] || '').toLowerCase() !== want[g]) ok = false;
    }
    if (want.special === 'g6ab_pass_g6c_fail') {
      if (!(d.g6a === 'pass' && d.g6b === 'pass' && d.g6c === 'fail')) ok = false;
    } else if (want.special === 'healer_eligible' && d.healerEligible !== 'true') ok = false;
    else if (want.special === 'rescued' && d.rescued !== 'true') ok = false;
    else if (want.special === 'regressed' && d.regressed !== 'true') ok = false;
    else if (want.special === 'review_incomplete' && d.reviewComplete !== 'false') ok = false;
    row.style.display = ok ? '' : 'none';
    if (ok) shown += 1;
  }
  q('filter-count').textContent = shown + ' rows';
}
document.addEventListener('DOMContentLoaded', () => {
  for (const id of ['f-model','f-task','f-difficulty','f-condition','f-seed','f-g1','f-g2','f-g3','f-g4','f-g5','f-g6','f-special']) {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', applyFilters);
    if (el) el.addEventListener('change', applyFilters);
  }
  applyFilters();
});
"""


def _summary_metric(label: str, num: int, den: int) -> str:
    return (
        f'<div class="metric"><div class="label">{_esc(label)}</div>'
        f'<div class="value">{_esc(_ratio(num, den))}</div></div>'
    )


def render_index_html(dataset: Mapping[str, Any], meta: Mapping[str, Any]) -> str:
    summary = dataset["summary"]
    den = summary["executed_denominator"] or 0
    rows_html: list[str] = []
    for cell in dataset["cells"]:
        overlay = cell.get("g6_overlay") or {}
        q = overlay.get("question") or {}
        healer = cell.get("healer") or {}
        g6a = (q.get("report_g6a_notation_lint") or {}).get("status")
        g6b = (q.get("report_g6b_renderer_parse") or {}).get("status")
        g6c = (q.get("report_g6c_human_visual") or {}).get("status")
        overall = overlay.get("report_g6_overall")
        legacy = overlay.get("artifact_g6_legacy_lint")
        rows_html.append(
            f"<tr data-cell=\"{_esc(cell['cell_id'])}\" "
            f"data-model=\"{_esc(str(cell.get('model_tag') or '').lower())}\" "
            f"data-task=\"{_esc(str(cell.get('task_id') or '').lower())}\" "
            f"data-difficulty=\"{_esc(str(cell.get('difficulty') or '').lower())}\" "
            f"data-condition=\"{_esc(str(cell.get('prompt_condition') or '').lower())}\" "
            f"data-seed=\"{_esc(cell.get('seed'))}\" "
            f"data-g1=\"{_esc(str(_gate_status(cell, 'g1_evaluability')).lower())}\" "
            f"data-g2=\"{_esc(str(_gate_status(cell, 'g2_executability')).lower())}\" "
            f"data-g3=\"{_esc(str(_gate_status(cell, 'g3_contract_compliance')).lower())}\" "
            f"data-g4=\"{_esc(str(_gate_status(cell, 'g4_semantic_correctness')).lower())}\" "
            f"data-g5=\"{_esc(str(_gate_status(cell, 'g5_problem_presentation')).lower())}\" "
            f"data-g6=\"{_esc(str(overall or NOT_ASSESSED).lower())}\" "
            f"data-g6a=\"{_esc(str(g6a or NOT_ASSESSED).lower())}\" "
            f"data-g6b=\"{_esc(str(g6b or NOT_ASSESSED).lower())}\" "
            f"data-g6c=\"{_esc(str(g6c or NOT_ASSESSED).lower())}\" "
            f"data-healer-eligible=\"{str(healer.get('eligible') is True).lower()}\" "
            f"data-rescued=\"{str(healer.get('rescued') is True).lower()}\" "
            f"data-regressed=\"{str(healer.get('regressed') is True).lower()}\" "
            f"data-review-complete=\"{str(bool(overlay.get('human_review_complete'))).lower()}\">"
            f"<td><a href=\"cells/{_esc(cell['cell_id'])}.html\">{_esc(cell['cell_id'])}</a></td>"
            f"<td>{_esc(cell.get('record_state'))}</td>"
            f"<td>{_esc(cell.get('model_tag'))}</td>"
            f"<td>{_esc(cell.get('task_id'))}</td>"
            f"<td>{_esc(cell.get('prompt_condition'))}</td>"
            f"<td>{_esc(cell.get('seed'))}</td>"
            f"<td>{_status_badge(_gate_status(cell, 'g1_evaluability'))}</td>"
            f"<td>{_status_badge(_gate_status(cell, 'g2_executability'))}</td>"
            f"<td>{_status_badge(_gate_status(cell, 'g3_contract_compliance'))}</td>"
            f"<td>{_status_badge(_gate_status(cell, 'g4_semantic_correctness'))}</td>"
            f"<td>{_status_badge(_gate_status(cell, 'g5_problem_presentation'))}</td>"
            f"<td title=\"artifact_g6_legacy_lint\">{_status_badge(legacy)}</td>"
            f"<td title=\"report_g6_overall\">{_status_badge(overall)}</td>"
            f"<td>{_status_badge(overlay.get('technical_pass') or (cell.get('composite_outcomes') or {}).get('technical_pass'))}</td>"
            f"<td>{_status_badge(overlay.get('presentation_pass'))}</td>"
            f"<td>{_status_badge(overlay.get('full_pass'))}</td>"
            "</tr>"
        )

    metrics = [
        _summary_metric("planned", summary["planned"], summary["planned"] or 0),
        _summary_metric("executed", summary["executed"], summary["planned"] or summary["executed"] or 0),
        _summary_metric("failed", summary["failed"], den or 0),
        _summary_metric("G1 PASS", summary["g1"].get(PASS, 0), den),
        _summary_metric("G2 PASS", summary["g2"].get(PASS, 0), den),
        _summary_metric("G3 PASS", summary["g3"].get(PASS, 0), den),
        _summary_metric("G4 PASS", summary["g4"].get(PASS, 0), den),
        _summary_metric("G5 PASS", summary["g5"].get(PASS, 0), den),
        _summary_metric("artifact G6 legacy lint PASS", summary["artifact_g6_legacy_lint"].get(PASS, 0), den),
        _summary_metric("report_g6_overall PASS", summary["g6"].get(PASS, 0), den),
        _summary_metric("report_g6_overall NOT_ASSESSED", summary["g6"].get(NOT_ASSESSED, 0), den),
        _summary_metric("Technical PASS", summary["technical"].get(PASS, 0), den),
        _summary_metric("Presentation PASS", summary["presentation"].get(PASS, 0), den),
        _summary_metric("Full PASS", summary["full"].get(PASS, 0), den),
        _summary_metric("Healer eligible", summary["healer_eligible"], den),
        _summary_metric("Healer attempted", summary["healer_attempted"], den),
        _summary_metric("rescued", summary["healer_rescued"], den),
        _summary_metric("regressed", summary["healer_regressed"], den),
        _summary_metric("retry-once", summary["retry_once"], den),
    ]

    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8"/>
<title>CE115 Calc Evidence Report</title>
<style>{CSS}</style></head><body>
<header>
  <h1>CE115 Calc Evidence Report</h1>
  <p class="muted">Offline rebuildable experiment evidence. Formal artifacts are read-only.</p>
  <div class="card">
    <div class="grid">
      <div class="metric"><div class="label">artifact hash</div><div class="value" style="font-size:12px">{_esc(meta.get('artifact_hash'))}</div></div>
      <div class="metric"><div class="label">dataset hash</div><div class="value" style="font-size:12px">{_esc(meta.get('report_dataset_hash'))}</div></div>
      <div class="metric"><div class="label">build hash</div><div class="value" style="font-size:12px">{_esc(meta.get('report_build_hash'))}</div></div>
      <div class="metric"><div class="label">model_calls</div><div class="value">{_esc(summary['model_calls'])}</div></div>
      <div class="metric"><div class="label">healer_calls</div><div class="value">{_esc(summary['healer_calls'])}</div></div>
      <div class="metric"><div class="label">network_calls</div><div class="value">{_esc(summary['network_calls'])}</div></div>
      <div class="metric"><div class="label">renderer</div><div class="value" style="font-size:12px">{_esc(meta.get('browser_summary'))}</div></div>
    </div>
  </div>
</header>
<main>
  <section class="card"><h2>Summary (numerator / denominator)</h2>
    <p class="muted">Executed denominators exclude planned-only cells ({summary['planned_not_in_executed_denominator']} planned-only).</p>
    <div class="grid">{''.join(metrics)}</div>
  </section>
  <section class="card"><h2>Cells</h2>
    <div class="filters">
      <input id="f-model" placeholder="model"/>
      <input id="f-task" placeholder="task"/>
      <input id="f-difficulty" placeholder="difficulty"/>
      <input id="f-condition" placeholder="condition"/>
      <input id="f-seed" placeholder="seed"/>
      <select id="f-g1"><option value="">G1</option><option>PASS</option><option>FAIL</option><option>NOT_ASSESSED</option><option>NOT_OBSERVED</option></select>
      <select id="f-g2"><option value="">G2</option><option>PASS</option><option>FAIL</option><option>NOT_ASSESSED</option><option>NOT_OBSERVED</option></select>
      <select id="f-g3"><option value="">G3</option><option>PASS</option><option>FAIL</option><option>NOT_ASSESSED</option><option>NOT_OBSERVED</option></select>
      <select id="f-g4"><option value="">G4</option><option>PASS</option><option>FAIL</option><option>NOT_ASSESSED</option><option>NOT_OBSERVED</option></select>
      <select id="f-g5"><option value="">G5</option><option>PASS</option><option>FAIL</option><option>NOT_ASSESSED</option><option>NOT_OBSERVED</option></select>
      <select id="f-g6"><option value="">G6</option><option>PASS</option><option>FAIL</option><option>NOT_ASSESSED</option><option>NOT_OBSERVED</option></select>
      <select id="f-special">
        <option value="">special</option>
        <option value="g6ab_pass_g6c_fail">G6a PASS + G6b PASS + G6c FAIL</option>
        <option value="healer_eligible">Healer eligible</option>
        <option value="rescued">rescued</option>
        <option value="regressed">regressed</option>
        <option value="review_incomplete">human review incomplete</option>
      </select>
      <span id="filter-count" class="muted"></span>
    </div>
    <div style="overflow:auto; max-height:70vh;">
      <table><thead><tr>
        <th>cell</th><th>state</th><th>model</th><th>task</th><th>condition</th><th>seed</th>
        <th>G1</th><th>G2</th><th>G3</th><th>G4</th><th>G5</th>
        <th>artifact_g6_legacy_lint</th><th>report_g6_overall</th>
        <th>Technical</th><th>Presentation</th><th>Full</th>
      </tr></thead><tbody>
      {''.join(rows_html)}
      </tbody></table>
    </div>
  </section>
</main>
<script>{INDEX_JS}</script>
</body></html>
"""


def render_cell_html(cell: Mapping[str, Any], meta: Mapping[str, Any]) -> str:
    overlay = cell.get("g6_overlay") or {}
    q = overlay.get("question") or {}
    a = overlay.get("answer") or {}
    renderer = overlay.get("renderer") or {}
    q_ev = renderer.get("question_evidence") or {}
    a_ev = renderer.get("answer_evidence") or {}
    healer = cell.get("healer") or {}
    diag = cell.get("token_duration_diagnostics") or {}
    review = overlay.get("human_review")

    def side_block(title: str, side: Mapping[str, Any], evidence: Mapping[str, Any], raw_text: Any) -> str:
        return f"""
        <div class="card">
          <h3>{_esc(title)}</h3>
          <p>report_g6a_notation_lint {_status_badge((side.get('report_g6a_notation_lint') or {}).get('status'))}
             report_g6b_renderer_parse {_status_badge((side.get('report_g6b_renderer_parse') or {}).get('status'))}
             report_g6c_human_visual {_status_badge((side.get('report_g6c_human_visual') or {}).get('status'))}</p>
          <h4>Raw (escaped)</h4>{_pre(raw_text)}
          <h4>Rendered DOM evidence</h4>
          <div class="render-box">{(evidence.get('rendered_html') or 'NOT_AVAILABLE')}</div>
          <h4>Metrics / errors</h4>
          {_pre(json.dumps({
              'metrics': evidence.get('metrics'),
              'clipping': evidence.get('clipping'),
              'clipping_threshold_px': evidence.get('clipping_threshold_px'),
              'overlap': evidence.get('overlap'),
              'overlap_is_warning_only': evidence.get('overlap_is_warning_only', True),
              'renderer_errors': evidence.get('renderer_errors'),
              'leftover_latex_commands': evidence.get('leftover_latex_commands'),
          }, ensure_ascii=False, indent=2) if evidence else 'NOT_AVAILABLE')}
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="UTF-8"/>
<title>{_esc(cell.get('cell_id'))}</title>
<style>{CSS}</style>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    macros: {{ dfrac: ['{{\\\\displaystyle\\\\frac{{#1}}{{#2}}}}', 2] }}
  }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script src="../../../../agent_tools/finals_rebuild/vendor/mathjax/tex-svg.js"></script>
</head><body>
<header>
  <p><a href="../index.html">← index</a></p>
  <h1>{_esc(cell.get('cell_id'))}</h1>
  <p class="muted">state={_esc(cell.get('record_state'))} ·
     artifact_g6_legacy_lint {_status_badge(overlay.get('artifact_g6_legacy_lint'))} ·
     report_g6_overall {_status_badge(overlay.get('report_g6_overall'))} ·
     Presentation {_status_badge(overlay.get('presentation_pass'))} ·
     Full {_status_badge(overlay.get('full_pass'))}</p>
</header>
<main>
  <section class="card"><h2>Provenance</h2>
    {_pre(json.dumps({
        'task_id': cell.get('task_id'),
        'model_tag': cell.get('model_tag'),
        'prompt_condition': cell.get('prompt_condition'),
        'seed': cell.get('seed'),
        'difficulty': cell.get('difficulty'),
        'prompt_hash': cell.get('prompt_hash'),
        'output_path': cell.get('output_path'),
        'run_id': cell.get('run_id'),
        'manifest_hash': cell.get('manifest_hash'),
        'git_commit': cell.get('git_commit'),
        'ledger_stage': cell.get('ledger_stage'),
        'outcome': cell.get('outcome'),
        'artifact_hash': meta.get('artifact_hash'),
        'report_dataset_hash': meta.get('report_dataset_hash'),
        'report_build_hash': meta.get('report_build_hash'),
        'browser': renderer.get('browser'),
        'mathjax_version': renderer.get('mathjax_version'),
        'mathjax_vendor': renderer.get('mathjax_vendor'),
        'renderer_equivalence_note': 'docs/experiments/ce115_calc_g6_renderer_equivalence.md',
    }, ensure_ascii=False, indent=2))}
  </section>
  <section class="card"><h2>Prompt</h2>{_pre(cell.get('prompt_text'))}</section>
  <section class="card"><h2>Raw output</h2>{_pre(cell.get('raw_first_attempt_output'))}</section>
  <section class="card"><h2>Extracted candidate</h2>{_pre(cell.get('candidate_extracted'))}</section>
  <section class="card"><h2>actual_question_text</h2>{_pre(cell.get('actual_question_text'))}</section>
  <section class="card"><h2>answer</h2>{_pre(cell.get('correct_answer'))}</section>
  {side_block('Question render / G6', q, q_ev, cell.get('actual_question_text'))}
  {side_block('Answer render / G6', a, a_ev, cell.get('correct_answer'))}
  <section class="card"><h2>Formal G1–G6</h2>{_pre(json.dumps(cell.get('evaluation_gates'), ensure_ascii=False, indent=2))}</section>
  <section class="card"><h2>Human review</h2>{_pre(json.dumps(review, ensure_ascii=False, indent=2) if review else 'NOT_ASSESSED')}</section>
  <section class="card"><h2>Healer before/after</h2>{_pre(json.dumps(healer, ensure_ascii=False, indent=2) if healer else 'NOT_AVAILABLE')}</section>
  <section class="card"><h2>Retry comparator</h2>{_pre(json.dumps({'retry_count': cell.get('retry_count')}, ensure_ascii=False, indent=2))}</section>
  <section class="card"><h2>Cost diagnostics</h2>{_pre(json.dumps(diag, ensure_ascii=False, indent=2))}</section>
</main>
<script>
document.addEventListener('DOMContentLoaded', () => {{
  if (window.MathJax && MathJax.typesetPromise) {{
    MathJax.typesetPromise().catch(err => console.error(err));
  }}
}});
</script>
</body></html>
"""


def write_report(
    out_dir: Path,
    dataset: Mapping[str, Any],
    meta: Mapping[str, Any],
    *,
    copy_mathjax: bool = False,
) -> dict[str, Any]:
    out_dir = Path(out_dir)
    cells_dir = out_dir / "cells"
    cells_dir.mkdir(parents=True, exist_ok=True)
    if copy_mathjax:
        vendor_src = REPO_ROOT / "agent_tools" / "finals_rebuild" / "vendor" / "mathjax" / "tex-svg.js"
        vendor_dst = out_dir / "vendor" / "mathjax"
        vendor_dst.mkdir(parents=True, exist_ok=True)
        (vendor_dst / "tex-svg.js").write_bytes(vendor_src.read_bytes())

    index = render_index_html(dataset, meta)
    (out_dir / "index.html").write_text(index, encoding="utf-8")
    for cell in dataset["cells"]:
        page = render_cell_html(cell, meta)
        (cells_dir / f"{cell['cell_id']}.html").write_text(page, encoding="utf-8")

    dataset_path = out_dir / "report_dataset.json"
    slim_cells = []
    for cell in dataset["cells"]:
        slim = {k: v for k, v in cell.items() if k != "source_record"}
        slim_cells.append(slim)
    slim_dataset = {
        "cells": slim_cells,
        "summary": dataset["summary"],
        "call_counts": dataset["call_counts"],
        "warnings": dataset.get("warnings") or [],
    }
    payload = json.dumps(slim_dataset, ensure_ascii=False, sort_keys=True, indent=2)
    dataset_path.write_text(payload + "\n", encoding="utf-8")
    meta_out = dict(meta)
    meta_out["report_dataset_hash"] = sha256_text(payload)
    build_material = json.dumps(
        {"meta": meta_out, "index_sha256": sha256_text(index), "n_cells": len(slim_cells)},
        sort_keys=True,
    )
    meta_out["report_build_hash"] = sha256_text(build_material)
    (out_dir / "report_meta.json").write_text(
        json.dumps(meta_out, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "README.md").write_text(
        "# CE115 evidence report (offline)\n\n"
        "Open `index.html` from the repo checkout. MathJax is loaded from\n"
        "`agent_tools/finals_rebuild/vendor/mathjax/tex-svg.js` via relative path "
        "(no CDN). See `docs/experiments/ce115_calc_g6_renderer_equivalence.md`.\n",
        encoding="utf-8",
    )
    return meta_out


def build_evidence_report(
    *,
    out_dir: Path,
    results_dir: Path | None = None,
    reviews_path: Path | None = None,
    manifest_path: Path | None = None,
    planned_cells: list[Mapping[str, Any]] | None = None,
    executed_rows: list[Mapping[str, Any]] | None = None,
    renderer_fn=None,
    run_renderer: bool = True,
    repo_root: Path | None = None,
    copy_mathjax: bool = False,
) -> dict[str, Any]:
    root = repo_root or REPO_ROOT
    manifest_path = Path(manifest_path) if manifest_path else DEFAULT_MANIFEST
    results_dir = Path(results_dir) if results_dir else DEFAULT_RESULTS_DIR
    reviews_path = Path(reviews_path) if reviews_path else DEFAULT_REVIEWS

    artifact_paths: list[Path] = []
    if executed_rows is None:
        artifact_paths = collect_result_paths(results_dir)
        executed_rows, artifact_hash = (
            load_artifact_records(artifact_paths) if artifact_paths else ([], sha256_text(""))
        )
    else:
        blob = "\n".join(json.dumps(r, sort_keys=True, ensure_ascii=False) for r in executed_rows)
        artifact_hash = sha256_text(blob)

    if planned_cells is None:
        plan = build_local_confirmatory_plan(manifest_path, repo_root=root)
        planned_cells = plan["cells"]
        manifest_hash = plan["manifest_hash"]
    else:
        manifest_hash = "fixture"

    out_dir = Path(out_dir)
    if results_dir.exists() and out_dir.resolve() == results_dir.resolve():
        raise ValueError("refusing to write report into formal results directory")

    before_hashes = {str(p): sha256_file(p) for p in artifact_paths}

    known_ids = {
        str(c["cell_id"]) for c in planned_cells if c.get("cell_id")
    } | {
        str(r["cell_id"]) for r in executed_rows if r.get("cell_id")
    }
    reviews, unknown_reviews = load_human_reviews(
        reviews_path if reviews_path.is_file() else None,
        known_cell_ids=known_ids,
    )
    dataset = build_dataset(
        planned_cells=list(planned_cells),
        executed_rows=list(executed_rows),
        reviews=reviews,
        renderer_fn=renderer_fn,
        run_renderer=run_renderer,
        unknown_review_cell_ids=unknown_reviews,
    )
    browser_summary = "NOT_AVAILABLE"
    for cell in dataset["cells"]:
        browser = ((cell.get("g6_overlay") or {}).get("renderer") or {}).get("browser")
        if browser:
            browser_summary = f"{browser.get('name')} {browser.get('version')} @ {browser.get('path')}"
            break

    meta = {
        "artifact_hash": artifact_hash,
        "manifest_hash": manifest_hash,
        "reviews_path": _relpath_public(reviews_path, repo_root=root),
        "results_dir": _relpath_public(results_dir, repo_root=root),
        "browser_summary": browser_summary,
        "model_calls": dataset["call_counts"]["model_calls"],
        "healer_calls": dataset["call_counts"]["healer_calls"],
        "network_calls": dataset["call_counts"]["network_calls"],
        "warnings": dataset.get("warnings") or [],
        "renderer_equivalence_doc": "docs/experiments/ce115_calc_g6_renderer_equivalence.md",
        "g6_naming": {
            "artifact_g6_legacy_lint": "formal evaluation_gates.g6_math_notation lint",
            "report_g6a_notation_lint": "report notation lint",
            "report_g6b_renderer_parse": "report browser MathJax validation",
            "report_g6c_human_visual": "report human visual score",
            "report_g6_overall": "report overall G6 (a∧b∧c for Q and A)",
        },
    }
    meta_out = write_report(out_dir, dataset, meta, copy_mathjax=copy_mathjax)

    after_hashes = {str(p): sha256_file(p) for p in artifact_paths}
    if before_hashes != after_hashes:
        raise RuntimeError("formal artifacts were modified during report build")

    meta_out["formal_artifacts_unchanged"] = True
    return {
        "meta": meta_out,
        "summary": dataset["summary"],
        "call_counts": dataset["call_counts"],
        "out_dir": str(out_dir),
        "cell_count": len(dataset["cells"]),
        "warnings": dataset.get("warnings") or [],
    }
