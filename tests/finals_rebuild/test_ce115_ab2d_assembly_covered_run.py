import json
from pathlib import Path
from agent_tools.finals_rebuild.ce115_ab2d_assembly import build_protocol

def test_covered_geometry_is_18_with_six_structural_exclusions():
    p=build_protocol("b1a3e2d2")
    covered=[c for c in p["cells"] if c["task"] != "ce115_calc_polynomial_factor_roots_l1"]
    assert len(covered)==18 and len(p["cells"])-len(covered)==6
    assert all(c["condition"]=="ab2d_assembly" for c in covered)
