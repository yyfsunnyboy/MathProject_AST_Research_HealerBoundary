from scripts.audit_ce115_ab2d_assembly_wiring import build_audit

def test_ab2d_assembly_audit_is_24_cell_and_evidence_backed():
    audit = build_audit()
    assert audit["cohort_size"] == 24
    assert all(cell["artifact_sha256"] and cell["prompt_sha256"] for cell in audit["cells"])
    assert audit["verdict"] == "ABD2_ASSEMBLY_PARTIALLY_WIRED"
    assert audit["polynomial_factor_roots_verdict"] == "ASSEMBLY_COVERAGE_GAP"

def test_ab2d_assembly_audit_covers_tasks_and_makes_no_calls():
    audit = build_audit()
    assert len({cell["task"] for cell in audit["cells"]}) == 4
    assert audit["metrics"]["required_api_call_rate"]["numerator"] == 0
    assert audit["external_call_counts"] == {"model": 0, "healer": 0, "repair": 0, "replay": 0, "retry": 0}
