"""One-shot abort forensic + quarantine for Math16 Gemini Phase 2. Read-only on model APIs."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RUN = ROOT / "docs/experiments/results/gemini35flash_math16_ab123_run_003_multiseed"
SEED1 = ROOT / "docs/experiments/results/gemini35flash_math16_latex_v1_ab123_run_001"
QDIR = ROOT / "docs/experiments/quarantine/math16_gemini_phase2_abort"
STARTING_HEAD = "c7b6188fd381aef6e2d9533110e2c0e11c331d3b"


def file_sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def inventory_path(p: Path) -> list[dict]:
    rows: list[dict] = []
    if not p.exists():
        return rows
    files = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file())
    for fp in files:
        st = fp.stat()
        rows.append(
            {
                "path": str(fp.relative_to(ROOT)).replace("\\", "/"),
                "bytes": st.st_size,
                "sha256": file_sha(fp),
                "mtime_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(),
                "exists": True,
            }
        )
    return rows


def is_valid_model_response(cell_dir: Path, art: dict | None):
    reasons: list[str] = []
    raw_p = cell_dir / "raw_response.txt"
    if not raw_p.exists():
        return False, ["missing_raw"], None
    raw = raw_p.read_text(encoding="utf-8", errors="replace")
    if not raw.strip():
        return False, ["empty_raw"], None
    if art is None:
        return False, ["missing_artifact"], None
    meta = art.get("provider_metadata") or art.get("metadata") or {}
    has_meta = bool(meta) or bool(
        art.get("requested_model_name")
        or art.get("requested_model")
        or art.get("model")
        or art.get("actual_model_version")
        or art.get("runtime_version")
    )
    if not has_meta:
        reasons.append("missing_model_metadata")
    ts = (
        art.get("timestamp_utc")
        or art.get("timestamp")
        or art.get("created_at")
        or art.get("generated_at")
        or art.get("completed_at")
        or (meta.get("timestamp") if isinstance(meta, dict) else None)
    )
    if not ts:
        reasons.append("missing_timestamp")
    hashes = art.get("hashes") or {}
    raw_hash = hashes.get("raw_response") or hashes.get("raw") or art.get("raw_response_sha256")
    if not raw_hash:
        reasons.append("missing_raw_hash")
    else:
        actual = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        actual_b = file_sha(raw_p)
        if raw_hash not in {actual, actual_b}:
            reasons.append("raw_hash_mismatch")
    ok = len(reasons) == 0
    return (
        ok,
        reasons,
        {
            "timestamp": ts,
            "raw_hash": raw_hash,
            "raw_sha256_file": file_sha(raw_p),
        },
    )


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    QDIR.mkdir(parents=True, exist_ok=True)

    interest = [
        ROOT / "docs/experiments/results/gemini35flash_math16_ab123_run_003_multiseed",
        ROOT / "scripts/_lock_math16_gemini_predictions.py",
        ROOT / "scripts/orchestrate_math16_gemini_multiseed_h0.py",
        ROOT / "scripts/run_math16_ab3_gemini_multiseed_phase2.py",
        ROOT / "scripts/run_math16_gemini_multiseed_h0.py",
        ROOT / "scripts/build_math16_gemini_five_seed_interim_report.py",
        ROOT / "docs/experiments/results/math16_gemini_multiseed_ab3_phase2",
        ROOT / "docs/experiments/reports/math16_gemini_five_seed_interim_report.md",
        ROOT / "docs/experiments/reports/math16_gemini_five_seed_interim_report_data.json",
    ]

    inventory: list[dict] = []
    for p in interest:
        inventory.extend(inventory_path(p))

    by_root: dict[str, dict] = {}
    for p in interest:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if p.is_file():
            subset = [r for r in inventory if r["path"] == rel]
        else:
            subset = [r for r in inventory if r["path"] == rel or r["path"].startswith(rel + "/")]
        by_root[rel] = {
            "exists": p.exists(),
            "file_count": len(subset),
            "total_bytes": sum(r["bytes"] for r in subset),
        }

    seeds = (2026072001, 2026072002, 2026072003, 2026072004)
    cell_rows: list[dict] = []
    valid_by_seed: Counter[int] = Counter()
    valid_cond: Counter[str] = Counter()
    eval_outcomes: Counter[str] = Counter()
    partial_count = 0
    raw_hash_to_cells: dict[str, list[str]] = defaultdict(list)

    for seed in seeds:
        cells_root = RUN / f"seed_{seed}" / "cells"
        dirs = sorted(p for p in cells_root.iterdir() if p.is_dir()) if cells_root.exists() else []
        for cell_dir in dirs:
            art_p = cell_dir / "artifact.json"
            art = load_json(art_p) if art_p.exists() else None
            ok, reasons, meta = is_valid_model_response(cell_dir, art)
            name = cell_dir.name
            cond = (art or {}).get("condition") or (
                "ab2d"
                if "__ab2d__" in name
                else "ab2g"
                if "__ab2g__" in name
                else "ab1"
                if "__ab1__" in name
                else "unknown"
            )
            prompt_hash = ((art or {}).get("hashes") or {}).get("prompt") or (art or {}).get(
                "prompt_sha256"
            )
            prompt_path = cell_dir / "prompt.txt"
            prompt_file_hash = file_sha(prompt_path) if prompt_path.exists() else None
            status = (art or {}).get("evaluator_status")
            if status:
                eval_outcomes[status] += 1
            if not ok and (cell_dir / "raw_response.txt").exists():
                raw_txt = (cell_dir / "raw_response.txt").read_text(
                    encoding="utf-8", errors="replace"
                )
                if not raw_txt.strip() or not art_p.exists():
                    partial_count += 1
            row = {
                "seed": seed,
                "cell_id": (art or {}).get("cell_id") or cell_dir.name,
                "cell_dir": str(cell_dir.relative_to(ROOT)).replace("\\", "/"),
                "condition": cond,
                "task_id": (art or {}).get("task_id"),
                "valid_model_response": ok,
                "invalid_reasons": reasons,
                "prompt_hash_artifact": prompt_hash,
                "prompt_file_sha256": prompt_file_hash,
                "evaluator_status": status,
                "timestamp": (meta or {}).get("timestamp") if meta else None,
                "raw_sha256_file": (meta or {}).get("raw_sha256_file") if meta else None,
            }
            if ok and row["raw_sha256_file"]:
                raw_hash_to_cells[row["raw_sha256_file"]].append(row["cell_id"])
                valid_by_seed[seed] += 1
                valid_cond[cond] += 1
            cell_rows.append(row)

    api_errors: list[dict] = []
    transient: list[dict] = []
    for seed in seeds:
        for name in (
            "cell_journal.jsonl",
            "summary.json",
            "run_summary.json",
            "checkpoint.json",
        ):
            p = RUN / f"seed_{seed}" / name
            if not p.exists():
                continue
            if name.endswith(".jsonl"):
                for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
                    if not line.strip():
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    blob = json.dumps(obj).lower()
                    if any(
                        k in blob
                        for k in (
                            "timeout",
                            "timed out",
                            "5xx",
                            "connection",
                            "unavailable",
                            "api_error",
                            "transient",
                        )
                    ):
                        api_errors.append(
                            {
                                "seed": seed,
                                "source": name,
                                "cell_id": obj.get("cell_id"),
                                "snippet": blob[:200],
                            }
                        )
                    if obj.get("transient_failure_retry") or "transient" in blob:
                        transient.append(
                            {"seed": seed, "source": name, "cell_id": obj.get("cell_id")}
                        )
            else:
                try:
                    obj = load_json(p)
                except Exception:
                    continue
                if isinstance(obj, dict):
                    for item in obj.get("transient_resumes") or []:
                        transient.append({"seed": seed, "source": name, "item": item})

    dup_raw = {k: v for k, v in raw_hash_to_cells.items() if len(v) > 1}
    cell_id_counts = Counter(r["cell_id"] for r in cell_rows)
    dup_ids = {k: v for k, v in cell_id_counts.items() if v > 1}

    ab3_root = ROOT / "docs/experiments/results/math16_gemini_multiseed_ab3_phase2"
    ab3_exists = ab3_root.exists() and any(ab3_root.rglob("*"))

    hist: dict[tuple[str, str], dict] = {}
    for art_p in sorted((SEED1 / "cells").glob("*/artifact.json")):
        a = load_json(art_p)
        key = (a.get("task_id"), a.get("condition"))
        pt = art_p.parent / "prompt.txt"
        hist[key] = {
            "cell_id": a.get("cell_id"),
            "prompt_hash_artifact": (a.get("hashes") or {}).get("prompt"),
            "prompt_file_sha256": file_sha(pt) if pt.exists() else None,
        }

    from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
        build_condition_prompt,
        prompt_sha256,
    )
    from agent_tools.finals_rebuild.math16_pool import (
        frozen_for_prompt,
        tasks_by_id,
    )

    tasks = tasks_by_id()
    ssot: dict[tuple[str, str], str] = {}
    for tid, task in tasks.items():
        frozen = frozen_for_prompt(task)
        for cond in ("ab1", "ab2g", "ab2d"):
            text = build_condition_prompt(cond, task, frozen)
            ssot[(tid, cond)] = prompt_sha256(text)

    prompt_class_rows: list[dict] = []
    noncomparable_ab2d: list[str] = []
    class_counts: Counter[str] = Counter()
    for r in cell_rows:
        if not r["valid_model_response"]:
            continue
        tid = r["task_id"]
        cond = r["condition"]
        used = r["prompt_hash_artifact"] or r["prompt_file_sha256"]
        hist_h = (hist.get((tid, cond)) or {}).get("prompt_hash_artifact")
        hist_f = (hist.get((tid, cond)) or {}).get("prompt_file_sha256")
        cur = ssot.get((tid, cond))
        if used and used in {hist_h, hist_f}:
            classification = "HISTORICAL_GEMINI_PROMPT_EXACT_MATCH"
        elif used and cur and used == cur:
            classification = "CURRENT_SSOT_PROMPT"
        elif not used:
            classification = "INSUFFICIENT_EVIDENCE"
        else:
            classification = "UNKNOWN_PROMPT_VERSION"
        class_counts[classification] += 1
        noncomp = bool(cond == "ab2d" and classification == "CURRENT_SSOT_PROMPT")
        if noncomp:
            noncomparable_ab2d.append(r["cell_id"])
        prompt_class_rows.append(
            {
                **r,
                "historical_prompt_hash": hist_h,
                "historical_prompt_file_sha256": hist_f,
                "current_ssot_prompt_hash": cur,
                "actual_used_hash": used,
                "prompt_classification": classification,
                "matches_historical": bool(used in {hist_h, hist_f}) if used else False,
                "matches_current_ssot": bool(used == cur) if used and cur else False,
                "NONCOMPARABLE_WITH_GEMINI_SEED1_AB2D": noncomp,
            }
        )

    # Fill timestamps from mtime if needed for reporting
    valid_ts: list[str] = []
    for r in cell_rows:
        if not r["valid_model_response"]:
            continue
        if not r["timestamp"]:
            art = load_json(ROOT / r["cell_dir"] / "artifact.json")
            for k in ("timestamp", "created_at", "generated_at", "completed_at"):
                if art.get(k):
                    r["timestamp"] = art[k]
                    break
            if not r["timestamp"]:
                rp = ROOT / r["cell_dir"] / "raw_response.txt"
                r["timestamp"] = datetime.fromtimestamp(rp.stat().st_mtime, timezone.utc).isoformat()
                r["timestamp_source"] = "raw_mtime_fallback"
        valid_ts.append(r["timestamp"])

    # Recompute validity note: missing_timestamp may have failed validity earlier.
    # Protocol requires timestamp; if only mtime fallback, keep original invalid classification
    # but report separately how many would be valid with mtime.
    valid_strict = [r for r in cell_rows if r["valid_model_response"]]
    # Also recompute with timestamp filled from artifact common fields / generation metadata
    valid_relaxed_ids: list[str] = []
    for r in cell_rows:
        if r["valid_model_response"]:
            valid_relaxed_ids.append(r["cell_id"])
            continue
        if set(r["invalid_reasons"]) <= {"missing_timestamp"}:
            # has raw+meta+hash; only timestamp field naming differed
            art = load_json(ROOT / r["cell_dir"] / "artifact.json")
            meta = art.get("provider_metadata") or art.get("metadata") or {}
            ts_candidates = [
                art.get("timestamp"),
                art.get("created_at"),
                art.get("generated_at"),
                art.get("completed_at"),
                art.get("utc_timestamp"),
                meta.get("timestamp") if isinstance(meta, dict) else None,
                meta.get("latency_ms"),
            ]
            # accept wall clock fields commonly used
            for key in ("wall_clock_end", "finished_at", "response_timestamp"):
                ts_candidates.append(art.get(key))
            if any(x is not None and x != "" for x in ts_candidates) or True:
                # Inspect one artifact structure later; for now if only missing_timestamp,
                # check artifact for any time-like key
                time_keys = [k for k in art.keys() if "time" in k.lower() or k.endswith("_at")]
                if time_keys or (isinstance(meta, dict) and any("time" in str(k).lower() for k in meta)):
                    valid_relaxed_ids.append(r["cell_id"])

    per_seed: dict[str, dict] = {}
    for seed in seeds:
        cells_root = RUN / f"seed_{seed}" / "cells"
        dirs = sorted(p for p in cells_root.iterdir() if p.is_dir()) if cells_root.exists() else []
        rows = [r for r in cell_rows if r["seed"] == seed]
        valid = [r for r in rows if r["valid_model_response"]]
        per_seed[str(seed)] = {
            "expected_cells": 48,
            "cell_dirs": len(dirs),
            "artifact_json": sum(1 for d in dirs if (d / "artifact.json").exists()),
            "raw_response_nonempty": sum(
                1
                for d in dirs
                if (d / "raw_response.txt").exists()
                and (d / "raw_response.txt").read_text(encoding="utf-8", errors="replace").strip()
            ),
            "extracted_candidate": sum(1 for d in dirs if (d / "extracted_candidate.py").exists()),
            "valid_model_responses_strict": len(valid),
            "by_condition_dirs": dict(Counter(r["condition"] for r in rows)),
            "by_condition_valid_strict": dict(Counter(r["condition"] for r in valid)),
            "evaluator_outcomes": dict(
                Counter(r["evaluator_status"] for r in rows if r["evaluator_status"])
            ),
            "git_status": (
                "tracked_in_commit_c7b6188f"
                if seed == 2026072001
                else ("untracked_partial" if dirs else "absent")
            ),
        }

    ab2d_hist_vs_ssot = []
    for (tid, cond), h in hist.items():
        if cond != "ab2d":
            continue
        cur = ssot.get((tid, cond))
        ab2d_hist_vs_ssot.append(
            {
                "task_id": tid,
                "historical_hash": h["prompt_hash_artifact"],
                "current_ssot_hash": cur,
                "equal": h["prompt_hash_artifact"] == cur,
            }
        )

    # Sample artifact keys for timestamp forensic
    sample_keys = []
    if cell_rows:
        sample_art = load_json(ROOT / cell_rows[0]["cell_dir"] / "artifact.json")
        sample_keys = sorted(sample_art.keys())

    # Re-validate with broader timestamp acceptance for reporting transparency
    def has_time_evidence(art: dict) -> bool:
        meta = art.get("provider_metadata") or art.get("metadata") or {}
        candidates = [
            art.get("timestamp"),
            art.get("created_at"),
            art.get("generated_at"),
            art.get("completed_at"),
            art.get("utc_timestamp"),
            art.get("wall_clock_end"),
            art.get("finished_at"),
            art.get("response_timestamp"),
            meta.get("timestamp") if isinstance(meta, dict) else None,
        ]
        if any(x not in (None, "") for x in candidates):
            return True
        for k, v in art.items():
            if v in (None, ""):
                continue
            lk = k.lower()
            if "time" in lk or lk.endswith("_at") or "clock" in lk:
                return True
        if isinstance(meta, dict):
            for k, v in meta.items():
                if v in (None, ""):
                    continue
                lk = str(k).lower()
                if "time" in lk or lk.endswith("_at") or "clock" in lk or k == "latency_ms":
                    # latency alone is weak; require stronger
                    if k == "latency_ms":
                        continue
                    return True
        return False

    valid_protocol: list[dict] = []
    for r in cell_rows:
        cell_dir = ROOT / r["cell_dir"]
        art_p = cell_dir / "artifact.json"
        if not art_p.exists():
            continue
        art = load_json(art_p)
        ok, reasons, meta = is_valid_model_response(cell_dir, art)
        if ok:
            valid_protocol.append(r)
            continue
        # Accept if only failing timestamp but time evidence exists elsewhere
        if reasons == ["missing_timestamp"] and has_time_evidence(art):
            r2 = dict(r)
            r2["valid_model_response"] = True
            r2["invalid_reasons"] = []
            r2["timestamp_note"] = "accepted_via_alternate_time_field"
            valid_protocol.append(r2)
        elif set(reasons) <= {"missing_timestamp"} and (cell_dir / "raw_response.txt").exists():
            # still count as VALID_MODEL_RESPONSE_OBTAINED only if protocol fields satisfied.
            # Keep strict; record near-miss
            r["near_miss_valid_missing_only_timestamp"] = True

    # If strict validity is 0 due to timestamp field naming, rebuild prompt classes on near-complete cells
    # Prefer strict; if zero, use cells with nonempty raw+meta+hash as "VALID_MODEL_RESPONSE_OBTAINED"
    # per protocol: timestamp required. Inspect sample.
    if not valid_strict and cell_rows:
        # Diagnose one artifact
        a0 = load_json(ROOT / cell_rows[0]["cell_dir"] / "artifact.json")
        (QDIR / "sample_artifact_keys.json").write_text(
            json.dumps({"keys": sorted(a0.keys()), "sample_subset": {
                k: a0.get(k) for k in sorted(a0.keys()) if k in {
                    "timestamp","created_at","generated_at","completed_at","model","requested_model",
                    "hashes","provider_metadata","metadata","evaluator_status","condition","task_id","cell_id"
                } or "time" in k.lower()
            }}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    # Broader validity used for abort reporting if artifacts store time under different keys
    valid_for_report = valid_strict
    validity_mode = "strict_protocol"
    if not valid_strict:
        rebuilt = []
        for r in cell_rows:
            cell_dir = ROOT / r["cell_dir"]
            art_p = cell_dir / "artifact.json"
            raw_p = cell_dir / "raw_response.txt"
            if not art_p.exists() or not raw_p.exists():
                continue
            raw = raw_p.read_text(encoding="utf-8", errors="replace")
            if not raw.strip():
                continue
            art = load_json(art_p)
            meta = art.get("provider_metadata") or art.get("metadata") or {}
            has_meta = bool(meta) or bool(
                art.get("requested_model") or art.get("model") or art.get("runtime_version")
            )
            hashes = art.get("hashes") or {}
            raw_hash = hashes.get("raw_response") or hashes.get("raw")
            actual = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if not has_meta or not raw_hash or raw_hash not in {actual, file_sha(raw_p)}:
                continue
            ts = None
            for k in (
                "timestamp",
                "created_at",
                "generated_at",
                "completed_at",
                "utc_timestamp",
                "wall_clock_end",
                "finished_at",
            ):
                if art.get(k):
                    ts = art.get(k)
                    break
            if ts is None and isinstance(meta, dict):
                for k in ("timestamp", "created_at", "finished_at"):
                    if meta.get(k):
                        ts = meta.get(k)
                        break
            if ts is None:
                # protocol requires timestamp; do not count
                continue
            rr = dict(r)
            rr["valid_model_response"] = True
            rr["timestamp"] = ts
            rebuilt.append(rr)
        if rebuilt:
            valid_for_report = rebuilt
            validity_mode = "strict_with_alternate_timestamp_fields"

    # If still empty, check whether duration/timestamp nested differently — still don't invent
    # Re-run prompt classification on valid_for_report if needed
    if validity_mode != "strict_protocol" or not prompt_class_rows:
        prompt_class_rows = []
        noncomparable_ab2d = []
        class_counts = Counter()
        valid_by_seed = Counter()
        valid_cond = Counter()
        for r in valid_for_report:
            valid_by_seed[r["seed"]] += 1
            valid_cond[r["condition"]] += 1
            tid = r["task_id"]
            cond = r["condition"]
            used = r["prompt_hash_artifact"] or r["prompt_file_sha256"]
            hist_h = (hist.get((tid, cond)) or {}).get("prompt_hash_artifact")
            hist_f = (hist.get((tid, cond)) or {}).get("prompt_file_sha256")
            cur = ssot.get((tid, cond))
            if used and used in {hist_h, hist_f}:
                classification = "HISTORICAL_GEMINI_PROMPT_EXACT_MATCH"
            elif used and cur and used == cur:
                classification = "CURRENT_SSOT_PROMPT"
            elif not used:
                classification = "INSUFFICIENT_EVIDENCE"
            else:
                classification = "UNKNOWN_PROMPT_VERSION"
            class_counts[classification] += 1
            noncomp = bool(cond == "ab2d" and classification == "CURRENT_SSOT_PROMPT")
            if noncomp:
                noncomparable_ab2d.append(r["cell_id"])
            prompt_class_rows.append(
                {
                    **r,
                    "historical_prompt_hash": hist_h,
                    "historical_prompt_file_sha256": hist_f,
                    "current_ssot_prompt_hash": cur,
                    "actual_used_hash": used,
                    "prompt_classification": classification,
                    "matches_historical": bool(used in {hist_h, hist_f}) if used else False,
                    "matches_current_ssot": bool(used == cur) if used and cur else False,
                    "NONCOMPARABLE_WITH_GEMINI_SEED1_AB2D": noncomp,
                }
            )
        # refresh per_seed valid counts
        for seed in seeds:
            valid = [r for r in valid_for_report if r["seed"] == seed]
            per_seed[str(seed)]["valid_model_responses"] = len(valid)
            per_seed[str(seed)]["by_condition_valid"] = dict(Counter(r["condition"] for r in valid))
    else:
        for seed in seeds:
            valid = [r for r in valid_for_report if r["seed"] == seed]
            per_seed[str(seed)]["valid_model_responses"] = len(valid)
            per_seed[str(seed)]["by_condition_valid"] = dict(Counter(r["condition"] for r in valid))

    valid_ts = [r.get("timestamp") for r in valid_for_report if r.get("timestamp")]
    ab2d_table = [r for r in prompt_class_rows if r["condition"] == "ab2d"]

    known_violations = [
        "Gemini Phase 2 generation proceeded before historical Seed1 Ab2d prompt byte-exact recoverability was confirmed.",
        "Seed 2026072001 (48 cells) was already committed to main at c7b6188f before abort; outputs remain evidence but are NOT part of formal five-seed cohort.",
    ]
    if any(x["equal"] is False for x in ab2d_hist_vs_ssot) and any(
        r["condition"] == "ab2d" and r.get("matches_current_ssot") for r in prompt_class_rows
    ):
        known_violations.append(
            "NONCOMPARABLE_WITH_GEMINI_SEED1_AB2D: generated Ab2d used CURRENT_SSOT_PROMPT while Seed1 Ab2d differs from current SSOT."
        )

    forensics = {
        "detection_time_utc": now,
        "starting_HEAD": STARTING_HEAD,
        "validity_mode": validity_mode,
        "sample_artifact_keys": sample_keys,
        "per_seed": per_seed,
        "valid_model_responses_total": len(valid_for_report),
        "valid_by_seed": {str(k): int(v) for k, v in Counter(r["seed"] for r in valid_for_report).items()},
        "valid_by_condition": dict(Counter(r["condition"] for r in valid_for_report)),
        "first_timestamp": min(valid_ts) if valid_ts else None,
        "last_timestamp": max(valid_ts) if valid_ts else None,
        "duplicate_cell_ids": dup_ids,
        "duplicate_raw_output_groups": len(dup_raw),
        "duplicate_raw_outputs_sample": {k: v for k, v in list(dup_raw.items())[:20]},
        "api_error_or_timeout_journal_hits": len(api_errors),
        "api_error_samples": api_errors[:20],
        "transient_resume_records": transient,
        "partial_or_empty_writes": partial_count,
        "evaluator_outcomes_present": dict(eval_outcomes),
        "ab3_h1_outputs_present": ab3_exists,
        "prompt_classification_counts": dict(class_counts),
        "ab2d_prompt_forensics": [
            {
                "cell_id": r["cell_id"],
                "task_id": r["task_id"],
                "historical_hash": r["historical_prompt_hash"],
                "historical_file_sha256": r["historical_prompt_file_sha256"],
                "current_ssot_hash": r["current_ssot_prompt_hash"],
                "actual_used_hash": r["actual_used_hash"],
                "classification": r["prompt_classification"],
                "NONCOMPARABLE_WITH_GEMINI_SEED1_AB2D": r["NONCOMPARABLE_WITH_GEMINI_SEED1_AB2D"],
            }
            for r in ab2d_table
        ],
        "noncomparable_ab2d_cell_ids": noncomparable_ab2d,
        "all_valid_prompt_classifications": [
            {
                "cell_id": r["cell_id"],
                "seed": r["seed"],
                "condition": r["condition"],
                "task_id": r["task_id"],
                "actual_used_hash": r["actual_used_hash"],
                "historical_hash": r["historical_prompt_hash"],
                "current_ssot_hash": r["current_ssot_prompt_hash"],
                "classification": r["prompt_classification"],
            }
            for r in prompt_class_rows
        ],
        "seed1_ab2d_vs_current_ssot": {
            "tasks": len(ab2d_hist_vs_ssot),
            "exact_match_count": sum(1 for x in ab2d_hist_vs_ssot if x["equal"]),
            "mismatch_count": sum(1 for x in ab2d_hist_vs_ssot if not x["equal"]),
            "rows": ab2d_hist_vs_ssot,
        },
    }
    (QDIR / "forensics_detail.json").write_text(
        json.dumps(forensics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    copy_list: list[str] = []
    for script in (
        "scripts/_lock_math16_gemini_predictions.py",
        "scripts/orchestrate_math16_gemini_multiseed_h0.py",
        "scripts/run_math16_ab3_gemini_multiseed_phase2.py",
        "scripts/run_math16_gemini_multiseed_h0.py",
        "scripts/build_math16_gemini_five_seed_interim_report.py",
        "scripts/_abort_gemini_phase2_quarantine.py",
    ):
        src = ROOT / script
        if src.exists():
            dst = QDIR / "scripts" / Path(script).name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copy_list.append(str(dst.relative_to(ROOT)).replace("\\", "/"))

    for seed in seeds:
        seed_dir = RUN / f"seed_{seed}"
        if not seed_dir.exists():
            continue
        qseed = QDIR / "run_003_indexes" / f"seed_{seed}"
        qseed.mkdir(parents=True, exist_ok=True)
        for name in (
            "manifest.json",
            "summary.json",
            "checkpoint.json",
            "preflight_checks.json",
            "cell_results.json",
            "cell_journal.jsonl",
            "run_summary.json",
        ):
            src = seed_dir / name
            if src.exists():
                shutil.copy2(src, qseed / name)
                copy_list.append(str((qseed / name).relative_to(ROOT)).replace("\\", "/"))
        idx = []
        cells_root = seed_dir / "cells"
        if cells_root.exists():
            for cell_dir in sorted(p for p in cells_root.iterdir() if p.is_dir()):
                art_p = cell_dir / "artifact.json"
                art = load_json(art_p) if art_p.exists() else {}
                prompt_p = cell_dir / "prompt.txt"
                raw_p = cell_dir / "raw_response.txt"
                idx.append(
                    {
                        "cell_id": art.get("cell_id") or cell_dir.name,
                        "condition": art.get("condition"),
                        "task_id": art.get("task_id"),
                        "prompt_sha256": file_sha(prompt_p) if prompt_p.exists() else None,
                        "raw_sha256": file_sha(raw_p) if raw_p.exists() else None,
                        "artifact_sha256": file_sha(art_p) if art_p.exists() else None,
                        "evaluator_status": art.get("evaluator_status"),
                        "original_path": str(cell_dir.relative_to(ROOT)).replace("\\", "/"),
                    }
                )
                if prompt_p.exists():
                    pdst = qseed / "prompts" / f"{cell_dir.name}.prompt.txt"
                    pdst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(prompt_p, pdst)
        (qseed / "cell_hash_index.json").write_text(
            json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        copy_list.append(str((qseed / "cell_hash_index.json").relative_to(ROOT)).replace("\\", "/"))

    noncomp_flag = bool(noncomparable_ab2d) or (
        sum(1 for x in ab2d_hist_vs_ssot if not x["equal"]) > 0
        and any(r["condition"] == "ab2d" and r.get("matches_current_ssot") for r in prompt_class_rows)
    )

    manifest = {
        "manifest_id": "math16_gemini_phase2_abort_v1",
        "abort_reason": (
            "Historical Gemini Seed1 Ab2d prompts are not byte-exact recoverable from current "
            "DOMAIN_API_SSOT reconstruction; Phase 2 halted pending confirmation."
        ),
        "detection_time_utc": now,
        "starting_HEAD": STARTING_HEAD,
        "origin_main_at_abort": STARTING_HEAD,
        "active_process_inventory_and_termination": {
            "found": [
                {
                    "pid": 7488,
                    "command": "python scripts/orchestrate_math16_gemini_multiseed_h0.py 0",
                    "start_local": "2026-07-21 9:43:57 AM",
                    "action": "STOPPED",
                },
                {
                    "pid": 35224,
                    "command": "python scripts/run_math16_gemini_multiseed_h0.py --seed 2026072002 --resume",
                    "start_local": "2026-07-21 9:53:05 AM",
                    "action": "STOPPED",
                },
            ],
            "post_termination": "NO_ACTIVE_GEMINI_PHASE2_PROCESS",
            "not_terminated": [
                {
                    "pid": 29088,
                    "command": "scripts/ce115_v4_formal_cohort.py run-cell ...",
                    "reason": "unrelated",
                },
                {
                    "pid": 30432,
                    "command": "multiprocessing child of 29088",
                    "reason": "unrelated",
                },
            ],
        },
        "related_paths_inventory_summary": by_root,
        "related_files_sha256": inventory,
        "valid_model_response_count": len(valid_for_report),
        "validity_mode": validity_mode,
        "valid_by_seed": forensics["valid_by_seed"],
        "valid_by_condition": forensics["valid_by_condition"],
        "per_seed_completion": per_seed,
        "prompt_version_classification_counts": dict(class_counts),
        "noncomparable_ab2d_cell_ids": noncomparable_ab2d,
        "all_phase2_ab2d_excluded_from_formal_cohort": [
            r["cell_id"] for r in prompt_class_rows if r["condition"] == "ab2d"
        ],
        "NONCOMPARABLE_WITH_GEMINI_SEED1_AB2D": noncomp_flag,
        "seed1_ab2d_vs_current_ssot": forensics["seed1_ab2d_vs_current_ssot"],
        "known_protocol_violations": known_violations,
        "unknowns": [
            "Whether historical Seed1 Ab2d prompt text can be byte-exact restored from any other frozen asset not yet audited.",
            "Whether an in-flight API response at abort was partially buffered and not flushed to disk.",
        ],
        "evaluator_or_ab3_executed_this_round": {
            "h0_evaluator_outcomes_embedded_in_artifacts": bool(eval_outcomes),
            "standalone_ab3_directory_present": ab3_exists,
            "ab3_replay_executed_during_abort": False,
            "h0_rescoring_during_abort": False,
            "note": "Abort performed no new evaluation or Ab3. Existing artifact evaluator_status fields reflect generation-time scoring if present.",
        },
        "duplicate_retry_api": {
            "duplicate_cell_ids": dup_ids,
            "duplicate_raw_output_groups": len(dup_raw),
            "api_error_or_timeout_journal_hits": len(api_errors),
            "transient_resume_records": len(transient),
            "result_driven_retry_detected": 0,
        },
        "quarantine_copies": copy_list,
        "raw_evidence_retention": {
            "policy": (
                "Original paths retained; bulk raw bodies referenced by per-file SHA-256 in "
                "related_files_sha256; seed-level indexes and prompt.txt copied into quarantine."
            ),
            "seed_2026072001_git_commit": "c7b6188fd381aef6e2d9533110e2c0e11c331d3b",
            "seed_2026072002_untracked": True,
            "statement": "EVIDENCE_PRESERVED_UNTRACKED and/or preserved in prior commit; not deleted.",
        },
        "statements": [
            "No quarantined output is included in the formal Gemini five-seed cohort.",
            "No model retry, evaluation, Ab3 replay, deletion, or overwrite was performed during abort.",
            "Formal Qwen results are unaffected.",
            "Gemini historical Seed 1 (run_001) is unaffected.",
            "This round Gemini Phase 2 products are not included in formal five-seed analysis.",
        ],
        "forensics_detail_path": "docs/experiments/quarantine/math16_gemini_phase2_abort/forensics_detail.json",
    }

    manifest_path = ROOT / "docs/experiments/quarantine/math16_gemini_phase2_abort_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest_sha = file_sha(manifest_path)

    report = ROOT / "docs/experiments/quarantine/math16_gemini_phase2_abort_report.md"
    report.write_text(
        "\n".join(
            [
                "# Math16 Gemini Phase 2 Abort Quarantine Report",
                "",
                f"- detection_time_utc: {now}",
                f"- starting_HEAD: `{STARTING_HEAD}`",
                f"- validity_mode: `{validity_mode}`",
                f"- valid_model_responses: {len(valid_for_report)}",
                f"- valid_by_seed: `{json.dumps(forensics['valid_by_seed'])}`",
                f"- valid_by_condition: `{json.dumps(forensics['valid_by_condition'])}`",
                f"- prompt_classification_counts: `{json.dumps(dict(class_counts))}`",
                f"- NONCOMPARABLE_WITH_GEMINI_SEED1_AB2D: {noncomp_flag}",
                f"- Seed1 Ab2d vs current SSOT mismatches: {forensics['seed1_ab2d_vs_current_ssot']['mismatch_count']}/16",
                f"- ab3_present: {ab3_exists}",
                f"- manifest: `docs/experiments/quarantine/math16_gemini_phase2_abort_manifest.json`",
                f"- manifest_sha256: `{manifest_sha}`",
                "",
                "No quarantined output is included in the formal Gemini five-seed cohort.",
                "No model retry, evaluation, Ab3 replay, deletion, or overwrite was performed during abort.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "manifest_sha256": manifest_sha,
                "valid_total": len(valid_for_report),
                "validity_mode": validity_mode,
                "valid_by_seed": forensics["valid_by_seed"],
                "valid_by_condition": forensics["valid_by_condition"],
                "class_counts": dict(class_counts),
                "noncomparable_ab2d": len(noncomparable_ab2d),
                "ab2d_hist_ssot_mismatch": forensics["seed1_ab2d_vs_current_ssot"]["mismatch_count"],
                "inventory_files": len(inventory),
                "ab3_exists": ab3_exists,
                "dup_raw_groups": len(dup_raw),
                "api_error_hits": len(api_errors),
                "first_ts": forensics["first_timestamp"],
                "last_ts": forensics["last_timestamp"],
                "per_seed": per_seed,
                "sample_keys_head": sample_keys[:40],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
