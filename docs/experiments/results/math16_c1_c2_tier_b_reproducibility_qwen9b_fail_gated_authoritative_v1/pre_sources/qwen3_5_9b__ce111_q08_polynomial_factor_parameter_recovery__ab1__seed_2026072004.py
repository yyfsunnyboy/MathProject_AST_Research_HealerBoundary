def generate(level=1, **kwargs):
    return {
        "question_text": r"Given that $3x^2 + 5x - 14$ can be factored as $(3x+a)(bx+c)$ where $a,b,c$ are integers and the factors are ordered such that the first factor is $(3x+a)$, find the value of $a+2c$.",
        "correct_answer": 7,
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }