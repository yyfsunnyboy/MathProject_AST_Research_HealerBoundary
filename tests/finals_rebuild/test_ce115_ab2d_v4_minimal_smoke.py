from scripts.run_ce115_ab2d_v4_minimal_smoke import preflight

def test_v4_smoke_preflight_contract():
 assert preflight()["passed"]
