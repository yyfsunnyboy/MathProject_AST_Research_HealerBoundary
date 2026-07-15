from agent_tools.finals_rebuild.ce115_ab2d_assembly import build_protocol, runtime_smoke, scan_assembly, stub_for_task

TASK = "ce115_calc_polynomial_division_l1"
GOOD = "def generate(level=1, **kwargs):\n q,r=PolynomialOps.div_qr([1,0,-1],[1,-1])\n return {'question_text':'q','correct_answer':{},'oracle_payload':{}}\n"

def test_stubs_are_contracts_not_implementations():
    stub = stub_for_task(TASK)
    assert "MUST_CALL" in stub and "DO_NOT_REIMPLEMENT_DOMAIN_LOGIC" in stub
    assert "class PolynomialOps" not in stub

def test_scanner_rejects_missing_and_redefined_helpers_and_accepts_wrapper():
    assert scan_assembly("def generate(): return {}", TASK)["classification"] == "REQUIRED_API_NOT_CALLED"
    assert scan_assembly("class PolynomialOps: pass\n" + GOOD, TASK)["classification"] == "FORBIDDEN_HELPER_REDEFINED"
    assert runtime_smoke(GOOD, TASK)["classification"] == "ASSEMBLY_COMPLIANT"

def test_factor_roots_is_explicitly_unavailable_and_protocol_is_24_cells():
    assert scan_assembly("def generate(): return {}", "ce115_calc_polynomial_factor_roots_l1")["classification"] == "ASSEMBLY_COVERAGE_UNAVAILABLE"
    protocol = build_protocol("c37eaba4")
    assert protocol["planned_cell_count"] == 24
    assert {c["condition"] for c in protocol["cells"]} == {"ab2d_assembly"}
    assert protocol["generation"]["healer"] == protocol["generation"]["retry"] == 0

def test_scanner_rejects_reimplementation_and_invalid_api_call():
    assert scan_assembly("def long_division(): pass\n" + GOOD, TASK)["classification"] == "DOMAIN_LOGIC_REIMPLEMENTED"
    bad = "def generate(level=1, **kwargs):\n PolynomialOps.div_qr([1])\n return {}\n"
    assert scan_assembly(bad, TASK)["classification"] == "INVALID_API_CALL"
