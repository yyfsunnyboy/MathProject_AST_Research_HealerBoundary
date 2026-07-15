from fractions import Fraction
from core.prompts.domain_function_library import PolynomialOps,FractionOps,RadicalOps
def test_polydiv_contract_is_flat_exact_and_rejects_zero_divisor():
 q,r=PolynomialOps.div_qr([1,0,-1],[1,-1]);assert q==[1,1] and r==[0]
 assert PolynomialOps.div_qr([1],[2])[0]==['1/2']
 try: PolynomialOps.div_qr([1],[0])
 except ValueError: pass
 else: assert False
def test_fraction_and_radical_canonical_edges():
 assert FractionOps.div(FractionOps.create('1/2'),FractionOps.create('1/3'))==Fraction(3,2)
 assert RadicalOps.simplify_term(1,12)==(2,3)
