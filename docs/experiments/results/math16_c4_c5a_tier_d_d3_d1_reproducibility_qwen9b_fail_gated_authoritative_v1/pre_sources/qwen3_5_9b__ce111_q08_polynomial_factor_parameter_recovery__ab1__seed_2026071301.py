def generate(level=1, **kwargs):
    return {
        "question_text": r"Given that $3x^2 + 47x - 56$ factors as $(3x+a)(bx+c)$ with integers $a,b,c$, find the value of $a+2c$.",
        "correct_answer": 1,
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }