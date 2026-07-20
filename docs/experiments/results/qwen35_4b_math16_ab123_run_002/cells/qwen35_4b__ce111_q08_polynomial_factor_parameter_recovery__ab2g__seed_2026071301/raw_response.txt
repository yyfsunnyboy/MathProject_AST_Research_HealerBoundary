def generate(level=1, **kwargs):
    import re
    
    def latex_escape(text):
        text = str(text)
        return text.replace('_', '\\_').replace('&', '\\&')

    factor_order_policy = kwargs.get("factor_order_policy", "strict_source_template")
    
    if level == 0:
        frozen_parameters = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
        
        factor_order_policy_strict = True
        
        quadratic_coefficients_list = kwargs.get("quadratic_coefficients") or frozen_parameters["quadratic_coefficients"]
        template_left_x_coefficient_int_val = kwargs.get("template_left_x_coefficient") or frozen_parameters["template_left_x_coefficient"]
        
        a_val = 0
        b_val = -1
        
        if factor_order_policy_strict:
            left_factor_template = f"({latex_escape(template_left_x_coefficient_int_val)}x+a)"
            
            right_quadratic_polynomial_text_latex = latex(f"x^2+{quadratic_coefficients_list[1]}x+{quadratic_coefficients_list[2]}")
        else:
            left_factor_template = f"({latex_escape(template_left_x_coefficient_int_val)}x+b)"
            
            right_quadratic_polynomial_text_latex = latex(f"x^2-{a}x+a*b")

    question_text_html_content = ""

    if factor_order_policy_strict:
        # Construct the expression based on strict template (3x + a) * quadratic(x)
        left_factor_expr = f"({latex_escape(template_left_x_coefficient_int_val)}x+{a})"
        
        right_quadratic_polynomial_latex_text = latex(f"x^2+{quadratic_coefficients_list[1]}x+{quadratic_coefficients_list[2]}")

    correct_answer_str = str(a + 2 * b)

    return {
        "question_text": question_text_html_content,
        "correct_answer": correct_answer_str,
        "oracle_payload": frozen_parameters.copy() if isinstance(frozen_parameters, dict) else {}
    }