from agent_tools.finals_rebuild.ce115_ab2d_assembly import resolve_task_operations, scan_toolbox

def test_fraction_resolver_uses_structure_not_unused_operations():
 assert resolve_task_operations("ce115_calc_exact_rational_expression_l1", {"operations":["sub","div"]})["required"] == ["FractionOps.create","FractionOps.sub","FractionOps.div"]

def test_alias_result_must_reach_output():
 s="def generate():\n f=PolynomialOps.div_qr\n q,r=f([1,0],[1])\n return {\"correct_answer\":(q,r)}\n"
 assert scan_toolbox(s,"ce115_calc_polynomial_division_l1")["classification"] == "ASSEMBLY_COMPLIANT"
 s=s.replace("(q,r)", "0")
 assert scan_toolbox(s,"ce115_calc_polynomial_division_l1")["called_but_result_unused"]
