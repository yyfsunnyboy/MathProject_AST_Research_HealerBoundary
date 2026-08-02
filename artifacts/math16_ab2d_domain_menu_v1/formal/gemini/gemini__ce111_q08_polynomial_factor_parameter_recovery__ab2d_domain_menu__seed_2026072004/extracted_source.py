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
    target_left_x_coeff = frozen_params["template_left_x_coefficient"]
    
    factors = PolynomialOps.factor_quadratic_exact(coeffs[0], coeffs[1], coeffs[2])
    
    parsed_factors = []
    for f in factors:
        x_coeff = int(f['x_coefficient']) if isinstance(f['x_coefficient'], int) else int(f['x_coefficient'])
        constant = int(f['constant']) if isinstance(f['constant'], int) else int(f['constant'])
        parsed_factors.append({'x_coefficient': x_coeff, 'constant': constant})
        
    f1, f2 = parsed_factors
    
    if abs(f1['x_coefficient']) == target_left_x_coeff:
        first_factor = f1
        second_factor = f2
    elif abs(f2['x_coefficient']) == target_left_x_coeff:
        first_factor = f2
        second_factor = f1
    else:
        raise ValueError("Could not find factor with matching x_coefficient")
        
    if first_factor['x_coefficient'] < 0:
        a = -first_factor['constant']
        b = -second_factor['x_coefficient']
        c = -second_factor['constant']
    else:
        a = first_factor['constant']
        b = second_factor['x_coefficient']
        c = second_factor['constant']
        
    correct_answer = a + 2 * c
    
    question_text = "已知\n\\[\n39x^2+5x-14=(3x+a)(bx+c),\n\\]\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }