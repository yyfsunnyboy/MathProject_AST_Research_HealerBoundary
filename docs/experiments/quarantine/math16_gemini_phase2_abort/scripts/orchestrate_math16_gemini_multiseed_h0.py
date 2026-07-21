"""Orchestrate Gemini Phase-2 multiseed H0: generate → validate → commit → push."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (2026072001, 2026072002, 2026072003, 2026072004)
RUN = "gemini35flash_math16_ab123_run_003_multiseed"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.check_call(cmd, cwd=ROOT)


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def verify_seed1_unchanged() -> None:
    snap = json.loads(
        (
            ROOT
            / "docs/experiments/results/_phase1_immutability/gemini_run_001_pre_phase2_fingerprint.json"
        ).read_text(encoding="utf-8")
    )
    root = ROOT / "docs/experiments/results/gemini35flash_math16_latex_v1_ab123_run_001"
    arts = sorted((root / "cells").glob("*/artifact.json"))
    raws = sorted((root / "cells").glob("*/raw_response.txt"))
    ha = hashlib.sha256(b"".join(p.read_bytes() for p in arts)).hexdigest()
    hr = hashlib.sha256(b"".join(p.read_bytes() for p in raws)).hexdigest()
    if ha != snap["artifact_concat_sha256"] or hr != snap["raw_concat_sha256"]:
        raise RuntimeError("gemini Seed1/run_001 mutated")


def main() -> int:
    start_from = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    for idx, seed in enumerate(SEEDS):
        if idx < start_from:
            continue
        print(f"\n=== BLOCK {idx+1}/4 Gemini seed {seed} ===", flush=True)
        verify_seed1_unchanged()
        run([sys.executable, "scripts/run_math16_gemini_multiseed_h0.py", "--seed", str(seed), "--resume"])
        run(
            [
                sys.executable,
                "scripts/run_math16_gemini_multiseed_h0.py",
                "--seed",
                str(seed),
                "--validate-only",
            ]
        )
        verify_seed1_unchanged()
        rel = f"docs/experiments/results/{RUN}/seed_{seed}"
        run(["git", "add", "--", rel])
        fp = "docs/experiments/results/_phase1_immutability/gemini_run_001_pre_phase2_fingerprint.json"
        run(["git", "add", "--", fp])
        for script in (
            "scripts/run_math16_gemini_multiseed_h0.py",
            "scripts/orchestrate_math16_gemini_multiseed_h0.py",
        ):
            if (ROOT / script).exists():
                run(["git", "add", "--", script])
        if not git_output("status", "--short"):
            print("nothing to commit", flush=True)
            continue
        run(["git", "commit", "-m", f"Add Math16 Gemini seed {seed} H0 generations"])
        run(["git", "push", "origin", "main"])
        print(f"COMMITTED+PUSHED block {idx+1}: {git_output('rev-parse', 'HEAD')}", flush=True)
    print("ALL_GEMINI_H0_BLOCKS_DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
