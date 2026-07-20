"""Orchestrate Math16 Phase-1 Qwen multiseed H0 blocks: generate → validate → commit → push."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = [
    ("qwen3.5:4b", 2026072001, "qwen35_4b"),
    ("qwen3.5:4b", 2026072002, "qwen35_4b"),
    ("qwen3.5:4b", 2026072003, "qwen35_4b"),
    ("qwen3.5:4b", 2026072004, "qwen35_4b"),
    ("qwen3.5:9b", 2026072001, "qwen35_9b"),
    ("qwen3.5:9b", 2026072002, "qwen35_9b"),
    ("qwen3.5:9b", 2026072003, "qwen35_9b"),
    ("qwen3.5:9b", 2026072004, "qwen35_9b"),
]


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.check_call(cmd, cwd=ROOT)


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def verify_run002_unchanged() -> None:
    snap = json.loads(
        (
            ROOT
            / "docs/experiments/results/_phase1_immutability/run_002_pre_generation_fingerprint.json"
        ).read_text(encoding="utf-8")
    )
    import hashlib

    for run, expected in snap.items():
        root = ROOT / "docs/experiments/results" / run
        arts = sorted((root / "cells").glob("*/artifact.json"))
        raws = sorted((root / "cells").glob("*/raw_response.txt"))
        ha = hashlib.sha256(b"".join(p.read_bytes() for p in arts)).hexdigest()
        hr = hashlib.sha256(b"".join(p.read_bytes() for p in raws)).hexdigest()
        if ha != expected["artifact_concat_sha256"] or hr != expected["raw_concat_sha256"]:
            raise RuntimeError(f"run_002 mutated: {run}")


def block_path(slug: str, seed: int) -> Path:
    return ROOT / "docs/experiments/results" / f"{slug}_math16_ab123_run_003_multiseed" / f"seed_{seed}"


def main() -> int:
    start_from = 0
    if len(sys.argv) > 1:
        start_from = int(sys.argv[1])

    for idx, (model, seed, slug) in enumerate(BLOCKS):
        if idx < start_from:
            continue
        print(f"\n=== BLOCK {idx+1}/8 {model} seed {seed} ===", flush=True)
        verify_run002_unchanged()
        run(
            [
                sys.executable,
                "scripts/run_math16_qwen_multiseed_h0.py",
                "--model",
                model,
                "--seed",
                str(seed),
                "--resume",
            ]
        )
        # validate
        run(
            [
                sys.executable,
                "scripts/run_math16_qwen_multiseed_h0.py",
                "--model",
                model,
                "--seed",
                str(seed),
                "--validate-only",
            ]
        )
        verify_run002_unchanged()
        path = block_path(slug, seed)
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        # Also stage fingerprint once if present
        run(["git", "add", "--", rel])
        fp = "docs/experiments/results/_phase1_immutability/run_002_pre_generation_fingerprint.json"
        if (ROOT / fp).exists():
            run(["git", "add", "--", fp])
        # scripts if not committed yet
        for script in (
            "scripts/run_math16_qwen_multiseed_h0.py",
            "scripts/orchestrate_math16_qwen_multiseed_h0.py",
            "scripts/run_math16_ab3_multiseed_phase1.py",
        ):
            if (ROOT / script).exists():
                run(["git", "add", "--", script])
        status = git_output("status", "--short")
        if not status:
            print("nothing to commit (already committed?)", flush=True)
            continue
        msg = f"Add Math16 {slug} seed {seed} H0 generations"
        run(["git", "commit", "-m", msg])
        run(["git", "push", "origin", "main"])
        print(f"COMMITTED+PUSHED block {idx+1}: {git_output('rev-parse', 'HEAD')}", flush=True)

    print("ALL_H0_BLOCKS_DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
