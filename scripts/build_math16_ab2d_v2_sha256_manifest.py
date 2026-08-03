"""SHA-256 manifest for all Math16 Ab2d V2 deliverables (LF-normalized, matches the
sha256_text/sha256_file convention used throughout math16_ab2d_domain_menu.py,
math16_ab2d_gemini_topk_qualification.py, math16_ab2d_formal_execution.py)."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


OUT = ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_sha256.json"

TARGETS = (
    sorted((ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/prompts").glob("*.txt"))
    + sorted((ROOT / "docs/experiments/prompts/ab2d_full_v2/prompts").glob("*.txt"))
    + sorted((ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2/domain_api_coverage").glob("*.json"))
    + sorted((ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2/domain_api_coverage").glob("*.md"))
    + [ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/manifest.json",
       ROOT / "docs/experiments/prompts/ab2d_full_v2/manifest.json",
       ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_semantic_census.json",
       ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_zero_model_preflight.json",
       ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_notes.md"]
)


def main() -> dict:
    entries = []
    for path in TARGETS:
        if not path.exists():
            entries.append({"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": None, "missing": True})
            continue
        entries.append({
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_file(path),
            "missing": False,
        })
    result = {
        "experiment_id": "math16_ab2d_menu_vs_full_runtime_contract_v2",
        "hash_convention": "sha256(bytes with CRLF normalized to LF)",
        "n_files": len(entries),
        "n_missing": sum(1 for e in entries if e["missing"]),
        "entries": entries,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    r = main()
    print(json.dumps({"n_files": r["n_files"], "n_missing": r["n_missing"]}, ensure_ascii=False))
