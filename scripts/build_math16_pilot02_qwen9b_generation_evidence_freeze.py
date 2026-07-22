# -*- coding: utf-8 -*-
"""Build Qwen9B Pilot-02 generation evidence freeze (zero model calls)."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/experiments/results/math16_pilot02_qwen9b"
PLAN_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json"
RUNTIME_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_runtime_manifest.json"
RUNNER_PATH = ROOT / "scripts/run_math16_pilot02_qwen9b_generation.py"
FREEZE_PATH = (
    ROOT / "docs/experiments/manifests/math16_pilot02_qwen9b_generation_evidence_freeze_v1.json"
)

FROZEN_COMMIT = "f782a55cea95af96803e0146a29985d30916468b"
EXPECTED_FP = "f45f79238bbf9400729fd00dbfaf4e33a7a7716cb9f81d4095a1fd1d52e0da5b"
EXPECTED_DIGEST = "6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7"


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_lf(path: Path) -> str:
    return hashlib.sha256(
        path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
    ).hexdigest()


def sha_json(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def main() -> int:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    runtime = json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))
    if len(plan) != 320:
        raise RuntimeError("plan not 320")
    if runtime["runtime_config_fingerprint"] != EXPECTED_FP:
        raise RuntimeError("runtime fingerprint mismatch")
    if runtime["model_digest"] != EXPECTED_DIGEST:
        raise RuntimeError("runtime digest mismatch")
    if not RUNNER_PATH.exists():
        raise RuntimeError("missing generation runner")

    missing: list[str] = []
    empty: list[str] = []
    drift: list[str] = []
    fp_mis: list[str] = []
    temp_mis: list[str] = []
    digest_mis: list[str] = []
    cell_records: list[dict[str, str]] = []
    statuses: Counter[str] = Counter()
    cond_c: Counter[str] = Counter()
    fam_c: Counter[str] = Counter()
    task_c: Counter[str] = Counter()
    seed_c: Counter[int] = Counter()

    for cell in plan:
        cid = cell["cell_id"]
        d = ROOT / "docs/experiments/results" / cell["output_relative_path"]
        ap, pp, rp = d / "artifact.json", d / "prompt.txt", d / "raw_response.txt"
        if not (ap.exists() and pp.exists() and rp.exists()):
            missing.append(cid)
            continue
        art = json.loads(ap.read_text(encoding="utf-8"))
        statuses[str(art.get("generation_status"))] += 1
        cond_c[cell["condition"]] += 1
        fam_c[cell["family"]] += 1
        task_c[cell["task_id"]] += 1
        seed_c[int(cell["seed"])] += 1
        if art.get("runtime_config_fingerprint") != EXPECTED_FP:
            fp_mis.append(cid)
        if art.get("runtime_parameters", {}).get("temperature") != 0.2:
            temp_mis.append(cid)
        if art.get("model_digest") != EXPECTED_DIGEST:
            digest_mis.append(cid)
        if art.get("prompt_sha256") != cell["prompt_sha256"]:
            drift.append(cid)
        if sha_lf(pp) != cell["prompt_sha256"]:
            drift.append(cid + ":prompt_file")
        raw = rp.read_text(encoding="utf-8")
        if art.get("generation_status") == "success" and not raw.strip():
            empty.append(cid)
        if (
            art.get("scoring") is not False
            or art.get("healer") is not False
            or art.get("ab3") is not False
        ):
            raise RuntimeError(f"scoring/healer/ab3 flag not false: {cid}")
        cell_records.append(
            {
                "cell_id": cid,
                "artifact_sha256": sha_bytes(ap),
                "prompt_sha256_file": sha_lf(pp),
                "raw_response_sha256": sha_bytes(rp),
                "plan_prompt_sha256": cell["prompt_sha256"],
                "generation_status": str(art.get("generation_status")),
            }
        )

    if missing or empty or drift or fp_mis or temp_mis or digest_mis:
        raise RuntimeError(
            json.dumps(
                {
                    "missing": missing,
                    "empty": empty,
                    "drift": drift,
                    "fp_mis": fp_mis,
                    "temp_mis": temp_mis,
                    "digest_mis": digest_mis,
                },
                ensure_ascii=False,
            )
        )

    journal_path = OUT / "cell_journal.jsonl"
    journal = [
        json.loads(line)
        for line in journal_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(journal) != 320:
        raise RuntimeError(f"journal length {len(journal)}")
    journal_ids = [r["cell_id"] for r in journal]
    plan_ids = [c["cell_id"] for c in plan]
    if journal_ids != plan_ids:
        raise RuntimeError("journal cell_id order/set mismatch vs plan")
    if any(r.get("runtime_config_fingerprint") != EXPECTED_FP for r in journal):
        raise RuntimeError("journal fingerprint mismatch")
    if any(r.get("temperature") != 0.2 for r in journal):
        raise RuntimeError("journal temperature mismatch")

    summary = json.loads((OUT / "generation_summary.json").read_text(encoding="utf-8"))
    audit = json.loads(
        (OUT / "generation_completeness_audit.json").read_text(encoding="utf-8")
    )
    run_manifest = json.loads((OUT / "run_manifest.json").read_text(encoding="utf-8"))
    if summary.get("stats", {}).get("success") != 320:
        raise RuntimeError("summary success != 320")
    if not audit.get("passed"):
        raise RuntimeError("completeness audit not passed")
    if run_manifest.get("runtime_config_fingerprint") != EXPECTED_FP:
        raise RuntimeError("run_manifest fingerprint mismatch")
    if run_manifest.get("model_digest") != EXPECTED_DIGEST:
        raise RuntimeError("run_manifest digest mismatch")
    if run_manifest.get("scoring") is not False:
        raise RuntimeError("run_manifest scoring not false")
    if run_manifest.get("healer") is not False or run_manifest.get("ab3") is not False:
        raise RuntimeError("run_manifest healer/ab3 not false")

    if cond_c != {"ab1": 80, "ab2g": 80, "ab2d": 80, "ab2d_spec_v2": 80}:
        raise RuntimeError(f"condition counts {dict(cond_c)}")
    if fam_c != {"integer": 80, "polynomial": 80, "radical": 80, "fraction": 80}:
        raise RuntimeError(f"family counts {dict(fam_c)}")
    if any(v != 20 for v in task_c.values()) or len(task_c) != 16:
        raise RuntimeError("task counts bad")
    if any(v != 64 for v in seed_c.values()) or len(seed_c) != 5:
        raise RuntimeError("seed counts bad")

    junk = []
    for p in OUT.rglob("*"):
        if not p.is_file():
            continue
        name = p.name.lower()
        if any(x in name for x in ("cache", "temp", ".lock", "partial", "debug", ".tmp")):
            junk.append(str(p.relative_to(ROOT)))
    if junk:
        raise RuntimeError(f"junk files present: {junk}")

    # Runner audit (static).
    runner_text = RUNNER_PATH.read_text(encoding="utf-8")
    for needle in (
        "EXPECTED_FINGERPRINT",
        EXPECTED_FP,
        EXPECTED_DIGEST,
        "INCOMPATIBLE_EXISTING_CELL",
        '"scoring": False',
        "ab2d_spec_v2",
    ):
        if needle not in runner_text:
            raise RuntimeError(f"runner audit missing: {needle}")
    for banned in ("evaluate_math16", "call_gemini", "MathHealerRunner", "qwen3.5:4b"):
        if banned in runner_text:
            raise RuntimeError(f"runner audit banned token present: {banned}")

    cell_records_sorted = sorted(cell_records, key=lambda r: r["cell_id"])
    corpus_sha_closure = sha_json(cell_records_sorted)

    key_files = {
        "runner": str(RUNNER_PATH.relative_to(ROOT)).replace("\\", "/"),
        "runtime_manifest": str(RUNTIME_PATH.relative_to(ROOT)).replace("\\", "/"),
        "cell_plan": str(PLAN_PATH.relative_to(ROOT)).replace("\\", "/"),
        "run_manifest": "docs/experiments/results/math16_pilot02_qwen9b/run_manifest.json",
        "cell_journal": "docs/experiments/results/math16_pilot02_qwen9b/cell_journal.jsonl",
        "generation_summary": "docs/experiments/results/math16_pilot02_qwen9b/generation_summary.json",
        "generation_completeness_audit": (
            "docs/experiments/results/math16_pilot02_qwen9b/generation_completeness_audit.json"
        ),
        "frozen_runtime_manifest_snapshot": (
            "docs/experiments/results/math16_pilot02_qwen9b/frozen_runtime_manifest.json"
        ),
        "frozen_cell_plan_snapshot": (
            "docs/experiments/results/math16_pilot02_qwen9b/frozen_cell_plan.json"
        ),
    }
    key_file_sha256 = {k: sha_bytes(ROOT / v) for k, v in key_files.items()}

    freeze = {
        "freeze_id": "math16_pilot02_qwen9b_generation_evidence_freeze_v1",
        "freeze_label": "QWEN9B_GENERATION_EVIDENCE_FROZEN",
        "frozen_preregistration_commit": FROZEN_COMMIT,
        "model_tag": "qwen3.5:9b",
        "model_digest": EXPECTED_DIGEST,
        "ollama_version": runtime["runtime_version"],
        "runtime_config_fingerprint": EXPECTED_FP,
        "temperature": 0.2,
        "top_p": 0.8,
        "top_k": 20,
        "thinking_mode": False,
        "num_ctx": 65536,
        "num_predict": 24576,
        "timeout_seconds": 1800,
        "cell_count": 320,
        "distribution": {
            "per_condition": dict(cond_c),
            "per_family": dict(fam_c),
            "per_task": {k: task_c[k] for k in sorted(task_c)},
            "per_seed": {str(k): seed_c[k] for k in sorted(seed_c)},
        },
        "generation_status_counts": dict(statuses),
        "file_counts": {
            "cell_dirs": 320,
            "artifact_json": 320,
            "prompt_txt": 320,
            "raw_response_txt": 320,
            "journal_lines": 320,
        },
        "integrity_checks": {
            "duplicate_cell_ids": 0,
            "missing": 0,
            "empty_success_raw": 0,
            "prompt_drift": 0,
            "fingerprint_mismatch": 0,
            "temperature_mismatch": 0,
            "model_digest_mismatch": 0,
        },
        "key_file_sha256": key_file_sha256,
        "corpus_sha_closure": corpus_sha_closure,
        "corpus_sha_closure_method": (
            "sha256(json.dumps(sorted_cell_records, sort_keys=True)) where each "
            "record has cell_id, artifact_sha256(raw bytes), prompt_sha256_file(LF), "
            "raw_response_sha256(raw bytes), plan_prompt_sha256, generation_status"
        ),
        "scoring": False,
        "ab3": False,
        "healer": False,
        "other_model_calls": False,
        "llm_calls_during_freeze": 0,
        "runner_audit": {
            "consumes_frozen_manifest_and_cell_plan_only": True,
            "does_not_modify_prompts_or_sampling": True,
            "resume_skips_complete_cells_fail_closed_on_mismatch": True,
            "no_scoring_ab3_healer": True,
            "model_allowlist": ["qwen3.5:9b"],
        },
        "verdicts": [
            "QWEN9B_GENERATION_EVIDENCE_FROZEN",
            "QWEN9B_RAW_CORPUS_SHA_CLOSURE_VERIFIED",
            "QWEN9B_GENERATION_GIT_CLOSEOUT_COMPLETED",
            "QWEN9B_SCORING_READY",
        ],
        "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    FREEZE_PATH.write_text(
        json.dumps(freeze, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (OUT / "generation_evidence_freeze_v1.json").write_text(
        json.dumps(freeze, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "FREEZE_BUILT",
                "corpus_sha_closure": corpus_sha_closure,
                "key_file_sha256": key_file_sha256,
                "llm_calls": 0,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
