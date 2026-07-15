"""Write the frozen CE115 Ab2d-Assembly manifests; never calls a model."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from agent_tools.finals_rebuild.ce115_ab2d_assembly import REPO_ROOT, TASK_API_MAPPING, build_protocol

OUT = REPO_ROOT / "docs/experiments/manifests"
def main():
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    protocol = build_protocol(commit); OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ce115_ab2d_task_api_mapping.json").write_text(json.dumps(TASK_API_MAPPING, indent=2) + "\n", encoding="utf-8")
    (OUT / "ce115_ab2d_assembly_protocol.json").write_text(json.dumps(protocol, indent=2) + "\n", encoding="utf-8")
    (OUT / "ce115_ab2d_assembly_protocol.md").write_text(f"# CE115 Ab2d-Assembly Protocol\n\n- Planned cells: {protocol['planned_cell_count']}\n- Condition: `ab2d_assembly` only\n- Model/Healer/repair/replay/retry calls: 0\n- Protocol hash: `{protocol['hashes']['protocol_manifest']}`\n", encoding="utf-8")
    (REPO_ROOT / "docs/experiments/results/ce115_corrected_context_formal_run/ce115_ab2d_condition_semantics.md").write_text("# Ab2d condition semantics\n\n`ab2d_spec` is legacy specification-only evidence. `ab2d_assembly` is a distinct, frozen 24-cell protocol requiring canonical runtime imports and required API calls. The existing corrected artifacts are unchanged.\n", encoding="utf-8")
if __name__ == "__main__": main()
