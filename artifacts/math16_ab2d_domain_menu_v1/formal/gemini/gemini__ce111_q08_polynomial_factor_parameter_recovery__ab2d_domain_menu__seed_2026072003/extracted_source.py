from fractions import Fraction
from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
      "factor_order_policy": "strict_source_template",
      "quadratic_coefficients": [
        39,
        5,
        -14
      ],
      "template_left_x_coefficient": 3
    }
    
    coeffs = frozen_params["quadratic_coefficients"]
    target_left_x = frozen_params["template_left_x_coefficient"]
    
    factors = PolynomialOps.factor_quadratic_exact(coeffs[0], coeffs[1], coeffs[2])
    
    parsed_factors = []
    for f in factors:
        x_coeff = int(Fraction(str(f["x_coefficient"])))
        constant = int(Fraction(str(f["constant"])))
        parsed_factors.append({"x_coefficient": x_coeff, "constant": constant})
        
    f1, f2 = None, None
    if abs(parsed_factors[0]["x_coefficient"]) == target_left_x:
        f1, f2 = parsed_factors[0], parsed_factors[1]
    elif abs(parsed_factors[1]["x_coefficient"]) == target_left_x:
        f1, f2 = parsed_factors[1], parsed_factors[0]
        
    if f1["x_coefficient"] == target_left_x:
        a = f1["constant"]
        c = f2["constant"]
    else:
        a = -f1["constant"]
        c = -f2["constant"]
        
    ans = a + 2 * c
    
    question_text = "已知\n\\[\n39x^2+5x-14=(3x+a)(bx+c),\n\\]\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。"
    
    return {
        "question_text": question_text,
        "correct_answer": ans,
        "oracle_payload": frozen_params
    }