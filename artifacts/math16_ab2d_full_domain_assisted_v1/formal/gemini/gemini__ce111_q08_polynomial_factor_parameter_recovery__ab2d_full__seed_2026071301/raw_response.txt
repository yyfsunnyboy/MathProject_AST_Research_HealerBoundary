from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # frozen_params
    frozen = {
      "factor_order_policy": "strict_source_template",
      "quadratic_coefficients": [
        39,
        5,
        -14
      ],
      "template_left_x_coefficient": 3
    }
    
    coeffs = frozen["quadratic_coefficients"]
    factors = PolynomialOps.factor_quadratic_exact(coeffs[0], coeffs[1], coeffs[2])
    
    target_x_coeff = frozen["template_left_x_coefficient"]
    
    f1, f2 = factors
    p1, q1 = int(f1['x_coefficient']), int(f1['constant'])
    p2, q2 = int(f2['x_coefficient']), int(f2['constant'])
    
    if p1 == target_x_coeff:
        a, b, c = q1, p2, q2
    elif p1 == -target_x_coeff:
        a, b, c = -q1, -p2, -q2
    elif p2 == target_x_coeff:
        a, b, c = q2, p1, q1
    elif p2 == -target_x_coeff:
        a, b, c = -q2, -p1, -q1
    else:
        a, b, c = 0, 0, 0
        
    ans = a + 2 * c
    
    question_text = "已知\n\\[\n39x^2+5x-14=(3x+a)(bx+c),\n\\]\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。"
    
    return {
        "question_text": question_text,
        "correct_answer": ans,
        "oracle_payload": frozen
    }