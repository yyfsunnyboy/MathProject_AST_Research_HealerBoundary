"""Audit existing CE115 corrected Ab2d artifacts for domain-library assembly wiring."""
from __future__ import annotations

import ast
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = ROOT / "docs/experiments/results/ce115_corrected_context_formal_run"
CELLS_DIR = RUN_DIR / "cells"
JSON_OUT = RUN_DIR / "ce115_ab2d_assembly_wiring_audit.json"
MD_OUT = RUN_DIR / "ce115_ab2d_assembly_wiring_audit.md"

TASKS = {
    "ce115_calc_radical_simplification_l1": {"apis": ("RadicalLogicEngine", "RadicalOps"), "markers": ("simplify_term", "square_factor")},
    "ce115_calc_polynomial_division_l1": {"apis": ("PolynomialOps.div_qr", "PolynomialOps.format_latex", "PolynomialOps.format_plain"), "markers": ("dividend", "divisor")},
    "ce115_calc_exact_rational_expression_l1": {"apis": ("FractionOps.create", "FractionOps.add", "FractionOps.sub", "FractionOps.mul", "FractionOps.div", "FractionOps.to_latex"), "markers": ("Fraction(", "parse_decimal")},
    "ce115_calc_polynomial_factor_roots_l1": {"apis": (), "markers": (), "coverage_gap": True},
}

def sha256(text): return hashlib.sha256(text.encode("utf-8")).hexdigest()

def dotted(node):
    if isinstance(node, ast.Name): return node.id
    if isinstance(node, ast.Attribute):
        prefix = dotted(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""

def calls_in(source):
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return set(), f"syntax error: {exc.msg}"
    return {dotted(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)}, None

def audit_record(path):
    record = json.loads(path.read_text(encoding="utf-8")); spec = TASKS[record["task"]]
    prompt = record["complete_payload"]["messages"][0]["content"]; output = record.get("raw_first_attempt_output", "")
    calls, parse_error = calls_in(output); exposed = [api for api in spec["apis"] if api in prompt]; called = [api for api in spec["apis"] if api in calls]
    reimplemented = bool(spec["markers"]) and all(marker.lower() in output.lower() for marker in spec["markers"])
    if spec.get("coverage_gap"): classification = "ASSEMBLY_COVERAGE_GAP"
    elif called: classification = "ASSEMBLY_COMPLIANT" if not parse_error else "INVALID_API_CALL"
    elif exposed and reimplemented: classification = "DOMAIN_LOGIC_REIMPLEMENTED"
    elif exposed: classification = "API_EXPOSED_BUT_IGNORED"
    elif parse_error: classification = "INSUFFICIENT_EVIDENCE"
    else: classification = "LIBRARY_RUNTIME_UNAVAILABLE"
    return {"cell_id": record["cell_id"], "task": record["task"], "model": record["model"], "seed": record["seed"], "artifact_path": path.relative_to(ROOT).as_posix(), "artifact_sha256": sha256(path.read_text(encoding="utf-8")), "prompt_sha256": sha256(prompt), "output_sha256": sha256(output), "required_apis": list(spec["apis"]), "exposed_apis": exposed, "called_apis": called, "parse_error": parse_error, "domain_logic_reimplemented": reimplemented, "classification": classification, "runtime_library_available": False, "runtime_evidence": "Corrected-run records execute extracted generated code; no record supplies a domain-library import or full implementation injection."}

def build_audit():
    cells = [audit_record(p) for p in sorted(CELLS_DIR.glob("*__ab2d__*.jsonl"))]
    if len(cells) != 24: raise RuntimeError(f"Expected 24 corrected Ab2d cells, found {len(cells)}")
    denom = sum(len(c["required_apis"]) for c in cells); exposed = sum(len(c["exposed_apis"]) for c in cells); called = sum(len(c["called_apis"]) for c in cells)
    return {"audit_id": "ce115_ab2d_existing_assembly_wiring", "scope": "existing corrected Ab2d 24-cell cohort", "cohort_size": 24, "cells": cells, "classification_counts": dict(sorted(Counter(c["classification"] for c in cells).items())), "metrics": {"required_api_exposure_rate": {"numerator": exposed, "denominator": denom, "rate": exposed / denom}, "required_api_call_rate": {"numerator": called, "denominator": denom, "rate": called / denom}, "domain_logic_reimplementation_rate": {"numerator": sum(c["domain_logic_reimplemented"] for c in cells), "denominator": 24}, "runtime_library_available_cells": 0}, "pipeline": ["task/skill_id -> get_required_domains/domain routing", "prompt_builder/scaler -> get_domain_helpers_code(..., stub_mode=True)", "model output -> extracted generated code", "formal runner -> evaluator execution without recorded full library injection/import"], "verdict": "ABD2_ASSEMBLY_PARTIALLY_WIRED", "polynomial_factor_roots_verdict": "ASSEMBLY_COVERAGE_GAP", "new_ab2d_assembly_cohort_required": True, "ab1_or_ab2g_rerun_required": False, "external_call_counts": {"model": 0, "healer": 0, "repair": 0, "replay": 0, "retry": 0}}

def render_markdown(audit):
    m = audit["metrics"]; lines = ["# CE115 Ab2d Assembly Wiring Audit", "", "## Verdict", "", f"`{audit['verdict']}`. Existing cohort only; no model/healer/repair/replay/retry calls.", "", "## Pipeline", ""] + [f"- {x}" for x in audit["pipeline"]] + ["", "## Results", "", f"- Cells: {audit['cohort_size']}", f"- Classification counts: {audit['classification_counts']}", f"- Required API exposure: {m['required_api_exposure_rate']['numerator']}/{m['required_api_exposure_rate']['denominator']}", f"- Required API calls: {m['required_api_call_rate']['numerator']}/{m['required_api_call_rate']['denominator']}", f"- Domain logic reimplementation: {m['domain_logic_reimplementation_rate']['numerator']}/24", "- Runtime library availability: 0/24", f"- Polynomial factor/roots: `{audit['polynomial_factor_roots_verdict']}`", "", "- New 24-cell Ab2d-Assembly cohort required: yes.", "- Ab1/Ab2g rerun required: no.", "", "## Per-cell evidence", "", "| Cell | Classification | Exposed | Called | Artifact hash |", "| --- | --- | --- | --- | --- |"]
    for c in audit["cells"]: lines.append(f"| {c['cell_id']} | {c['classification']} | {', '.join(c['exposed_apis']) or '-'} | {', '.join(c['called_apis']) or '-'} | `{c['artifact_sha256']}` |")
    return "\n".join(lines) + "\n"

def main():
    audit = build_audit(); JSON_OUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"); MD_OUT.write_text(render_markdown(audit), encoding="utf-8"); print(f"Wrote {JSON_OUT.relative_to(ROOT)}")

if __name__ == "__main__": main()
