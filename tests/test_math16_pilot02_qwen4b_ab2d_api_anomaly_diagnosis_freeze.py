# -*- coding: utf-8 -*-
"""Freeze / closeout tests for Qwen4B Ab2d+api anomaly diagnosis v1."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = (
    ROOT
    / "docs/experiments/audits/math16_pilot02_qwen4b_ab2d_api_anomaly_diagnosis_v1.md"
)
JS = (
    ROOT
    / "docs/experiments/audits/math16_pilot02_qwen4b_ab2d_api_anomaly_diagnosis_v1.json"
)
EVAL = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl"
)
SCORING_MANIFEST = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/scoring_manifest.json"
)

CORPUS_SHA = "7dd3ba5f7e7a38e7ad20142e8c5c5b2e84c20df1b7f5abcf5701c23d24172a22"
EVALUATOR_HASH = "2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc"
TAXONOMY_HASH = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
SOURCE_COMMIT = "9bfbd30bdc965c5f26003043606ca02d8096314c"

EXPECTED_MD_BODY_SHA = "a308f73daebf72ee2574fc474fdf22fe3e4305c25d37f6705ffd97e3ba348c6c"
EXPECTED_JSON_CONTENT_SHA = (
    "ae7303f5526841b0475f27f2d69fdb139985329f7455aaaf0c86b74bc0478b99"
)
EXPECTED_JSON_FILE_SHA = "b82f4f99881a5cb220d1a1b248c07865fccd34fcb6ffc8d6afcbdd4739135393"
EXPECTED_MD_FILE_SHA = "c9d479c18ed104ee15504383c800f2e51d7cd127414eff84c2f41d308058a989"


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_sha_rows(md: str) -> str:
    out = []
    for line in md.splitlines(keepends=True):
        if line.startswith("| MD SHA-256 |") or line.startswith("| JSON SHA-256 |"):
            continue
        out.append(line)
    return "".join(out)


def parse_md_cell_rows(md: str) -> list[tuple[str, int, str]]:
    out: list[tuple[str, int, str]] = []
    in_cell_table = False
    for line in md.splitlines():
        if line.startswith("## 1. Per-cell table"):
            in_cell_table = True
            continue
        if in_cell_table and line.startswith("## "):
            break
        if not in_cell_table or not line.startswith("| `ce"):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        assert len(parts) >= 8, line
        out.append(
            (parts[0].strip("`"), int(parts[1]), parts[7].replace("**", "").strip())
        )
    return out


def baseline_subset_ids() -> list[str]:
    rows = [
        json.loads(l)
        for l in EVAL.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]
    ids = []
    for r in rows:
        if r["condition"] != "ab2d":
            continue
        layer = r.get("primary_failure_layer")
        tags = r.get("mechanism_tags") or []
        if layer in {"L1", "L2", "L3"} or "format_contamination" in tags:
            ids.append(r["cell_id"])
    return sorted(ids)


def test_files_exist_and_file_shas_frozen():
    assert MD.exists()
    assert JS.exists()
    assert sha_file(MD) == EXPECTED_MD_FILE_SHA
    assert sha_file(JS) == EXPECTED_JSON_FILE_SHA


def test_freeze_block_and_policy_flags():
    payload = json.loads(JS.read_text(encoding="utf-8"))
    freeze = payload["freeze"]
    assert freeze["freeze_label"] == "QWEN4B_AB2D_API_ANOMALY_DIAGNOSIS_FROZEN"
    assert freeze["corpus_sha_closure"] == CORPUS_SHA
    assert freeze["evaluator_hash"] == EVALUATOR_HASH
    assert freeze["taxonomy_hash"] == TAXONOMY_HASH
    assert freeze["source_scoring_commit"] == SOURCE_COMMIT
    assert freeze["subset_n"] == 27
    assert freeze["label_counts_frozen"] == {
        "TRUE_LOGIC_ERROR": 1,
        "PARSER_UNFRIENDLY": 5,
        "OTHER": 21,
    }
    assert freeze["llm_calls"] == 0
    assert freeze["rescored"] is False
    assert freeze["evaluator_modified"] is False
    assert freeze["raw_modified"] is False
    assert freeze["ab3"] is False
    assert freeze["healer"] is False
    assert freeze["qwen9b"] is False
    assert freeze["md_body_sha256"] == EXPECTED_MD_BODY_SHA
    assert freeze["json_content_sha256"] == EXPECTED_JSON_CONTENT_SHA

    scope = payload["scope"]
    assert scope["condition"] == "ab2d"
    assert scope["subset_n"] == 27
    assert scope["llm_calls"] == 0
    assert scope["rescored"] is False
    assert scope["corpus_sha_closure"] == CORPUS_SHA

    sm = json.loads(SCORING_MANIFEST.read_text(encoding="utf-8"))
    assert sm["corpus_sha_closure"] == CORPUS_SHA
    assert sm["evaluator_hash"] == EVALUATOR_HASH
    assert sm["taxonomy_hash"] == TAXONOMY_HASH


def test_stable_content_hashes_recompute():
    md = MD.read_text(encoding="utf-8")
    body_sha = hashlib.sha256(strip_sha_rows(md).encode("utf-8")).hexdigest()
    assert body_sha == EXPECTED_MD_BODY_SHA

    payload = json.loads(JS.read_text(encoding="utf-8"))
    freeze = dict(payload["freeze"])
    freeze.pop("md_body_sha256", None)
    freeze.pop("json_content_sha256", None)
    payload_for_hash = dict(payload)
    payload_for_hash["freeze"] = freeze
    content_sha = hashlib.sha256(
        json.dumps(payload_for_hash, ensure_ascii=False, indent=2).encode("utf-8")
        + b"\n"
    ).hexdigest()
    assert content_sha == EXPECTED_JSON_CONTENT_SHA


def test_twenty_seven_cells_unique_and_match_baseline_filter():
    payload = json.loads(JS.read_text(encoding="utf-8"))
    cells = payload["cells"]
    assert len(cells) == 27
    ids = [c["cell_id"] for c in cells]
    assert len(set(ids)) == 27
    assert sorted(ids) == baseline_subset_ids()
    labels = Counter(c["root_cause"] for c in cells)
    assert labels == Counter(
        {"OTHER": 21, "PARSER_UNFRIENDLY": 5, "TRUE_LOGIC_ERROR": 1}
    )
    assert payload["label_counts"] == {
        "OTHER": 21,
        "PARSER_UNFRIENDLY": 5,
        "TRUE_LOGIC_ERROR": 1,
    }


def test_md_json_per_cell_consistency_and_required_text():
    md = MD.read_text(encoding="utf-8")
    payload = json.loads(JS.read_text(encoding="utf-8"))
    md_rows = parse_md_cell_rows(md)
    js_rows = [(c["task_id"], c["seed"], c["root_cause"]) for c in payload["cells"]]
    assert len(md_rows) == 27
    assert md_rows == js_rows

    assert "| PARSER_UNFRIENDLY | 5 |" in md
    assert "| TRUE_LOGIC_ERROR | 1 |" in md
    assert "| OTHER | 21 |" in md
    assert "SyntaxError inside an already-extracted candidate" in md
    assert "not the primary cause" in md
    assert "not recommended" in md
    assert "L5 algorithmic_error" in md
    assert "must not" in md.lower()
    assert "overwrite baseline" in md
    assert CORPUS_SHA in md
    assert EVALUATOR_HASH in md
    assert TAXONOMY_HASH in md
    assert EXPECTED_MD_BODY_SHA in md
    assert EXPECTED_JSON_FILE_SHA in md
    assert "QWEN4B_AB2D_API_ANOMALY_DIAGNOSIS_FROZEN" in md
    assert "QWEN4B_PARSER_VS_LOGIC_EVIDENCE_VERIFIED" in md
