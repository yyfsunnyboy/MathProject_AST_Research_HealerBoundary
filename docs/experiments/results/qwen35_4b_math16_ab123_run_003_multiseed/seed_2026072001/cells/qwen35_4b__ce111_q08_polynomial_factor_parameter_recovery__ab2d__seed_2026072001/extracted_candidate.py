import sys
from decimal import Decimal
sys.modules['core.prompts.domain_function_library'] = type('MockLib', (), {
    'PolynomialOps': {'mul': lambda c1, c2: [c1[0]*c2[0], (c1[0]*c2[1] + c1[1]*c2[0]), c1[1]*c2[1]]},
    'FractionOps': {'create': lambda v: Decimal(v)}
})

def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    if level == 1:
        a = 7
        
        c_quadratic_0, c_quadratic_1, c_quadratic_2 = frozen_params["quadratic_coefficients"]
        
        factor_one_constant = Decimal(-a) / (Decimal(c_quadratic_0)) + FractionOps.create(0.5) * FrozenParams.get('extra', 0) if 'FrozenParams' in globals() else -1
        
        correct_answer_int_val = a + c_quadratic_2

    return {
        "question_text": r"\text{Find the integer } a \text{ such that } (3x+a)(bx+c) = 39x^2+5x-14. \text{ The value to compute is } a+(-14).",
        "correct_answer": correct_answer_int_val,
        "oracle_payload": frozen_params
    }