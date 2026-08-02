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
    factors = PolynomialOps.factor_quadratic_exact(coeffs[0], coeffs[1], coeffs[2])
    
    target_x_coeff = frozen_params["template_left_x_coefficient"]
    
    factor1 = None
    factor2 = None
    
    for f in factors:
        xc = int(f["x_coefficient"])
        const = int(f["constant"])
        if xc == target_x_coeff:
            factor1 = {"x_coefficient": xc, "constant": const}
            other = [x for x in factors if x != f][0]
            factor2 = {"x_coefficient": int(other["x_coefficient"]), "constant": int(other["constant"])}
            break
        elif xc == -target_x_coeff:
            factor1 = {"x_coefficient": -xc, "constant": -const}
            other = [x for x in factors if x != f][0]
            factor2 = {"x_coefficient": -int(other["x_coefficient"]), "constant": -int(other["constant"])}
            break

    a = factor1["constant"]
    c = factor2["constant"]
    
    ans = a + 2 * c
    
    question_text = "已知\n\\[\n39x^2+5x-14=(3x+a)(bx+c),\n\\]\n其中 \\(a,b,c\\) 均為整數，求 \\(a+2c\\)。"
    
    return {
        "question_text": question_text,
        "correct_answer": ans,
        "oracle_payload": frozen_params
    }