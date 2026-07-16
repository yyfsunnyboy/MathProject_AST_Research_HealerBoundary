from agent_tools.finals_rebuild.ce115_ab2d_assembly import resolve_task_operations,scan_toolbox
def test_fraction_resolver_does_not_require_unused_operations():
 assert resolve_task_operations('ce115_calc_exact_rational_expression_l1',{'products':[{}]})['required']==['FractionOps.create','FractionOps.mul']
def test_toolbox_scanner_requires_polydiv_but_not_formatter():
 s='def generate(level=1,**k):\n q,r=PolynomialOps.div_qr([1,0,-1],[1,-1]);return {}\n'
 assert scan_toolbox(s,'ce115_calc_polynomial_division_l1')['classification']=='ASSEMBLY_COMPLIANT'
