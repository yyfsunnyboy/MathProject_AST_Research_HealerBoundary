def generate(level=1, **kwargs):
    return {
        "question_text": r"Given that $3x^2 + bx - 42$ factors as $(3x+a)(x+c)$ where $a,b,c$ are integers and the factor order is strict (first factor fixed as $3x+a$), find the value of $a+2c$. Note: The quadratic coefficients for this specific instance are $[39, 5, -14]$.",
        "correct_answer": 70,
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }