from core.prompts.domain_function_library import PolynomialOps
from agent_tools.finals_rebuild.ce115_ab2d_assembly import stub_for_task
def test_flat_remainder_contract_positive_and_negative_shapes():
 q,r=PolynomialOps.div_qr([-6,-4,3],[1,-2]);assert q==[-6,-16] and r==[-29]
 assert r!=[r] and not isinstance(r[0],(list,float))
def test_prompt_example_requires_direct_unpacking():
 s=stub_for_task('ce115_calc_polynomial_division_l1');assert 'quotient_coefficients, remainder_coefficients' in s and 'without wrapping' in s
