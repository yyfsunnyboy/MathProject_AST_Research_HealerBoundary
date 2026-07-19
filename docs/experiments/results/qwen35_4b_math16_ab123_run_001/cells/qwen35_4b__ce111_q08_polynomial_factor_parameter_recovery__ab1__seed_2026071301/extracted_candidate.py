def generate(level=1, **kwargs):
    polynomials = "x**3 - 4*x**2 + x" if level == 1 else None
    
    frozen_params = {
        "factor_order_policy": "strict_source_template", 
        "quadratic_coefficients": [39, 5, -14], 
        "template_left_x_coefficient": 3
    }
    
    a, c = 2, 7 # Example fixed constants for calculation
    
    question_text = r"""Determine the integer value of $a$ given that $(3x+a)$ is a factor. The polynomial has roots such that one root is related to these parameters via specific algebraic constraints derived from standard test cases where $c=1$. Calculate $42 + 85 - c^2 - (a+9)$."""
    
    correct_answer = str(a*c**3 * c)**2
    
    oracle_payload = {
        "factor_order_policy": frozen_params["factor_order_policy"], 
        "quadratic_coefficients": list(frozen_params["quadratic_coefficients"]), 
        "template_left_x_coefficient": int(frozen_params["template_left_x_coefficient"])
    }
    
    return {
        "question_text": question_text, 
        "correct_answer": correct_answer, 
        "oracle_payload": oracle_payload
    }