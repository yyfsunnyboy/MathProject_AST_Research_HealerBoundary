import json
from typing import Any, Dict, List


def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    frozen_params = kwargs.get("frozen", {})
    
    expression_str = str(frozen_params["expression"])
    required_form = str(frozen_params["required_form"])
    
    from core.prompts.domain_function_library import PolynomialOps
    
    coeffs = PolynomialOps.coeffs_from_py_expression(expression_str, var='x')
    
    a, b, c = coeffs[0], coeffs[1], coeffs[2]
    
    factors_list = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    if len(factors_list) != 2:
        raise ValueError("Factorization failed or returned incorrect number of factors")
    
    factor_dict_1 = {"x_coefficient": int(factors_list[0]["x_coefficient"]), "constant": int(factors_list[0]["constant"])}
    factor_dict_2 = {"x_coefficient": int(factors_list[1]["x_coefficient"]), "constant": int(factors_list[1]["constant"])}
    
    correct_answer = {
        "factors": [factor_dict_1, factor_dict_2]
    }
    
    return {
        "question_text": expression_str,
        "correct_answer": json.dumps(correct_answer),
        "oracle_payload": frozen_params
    }