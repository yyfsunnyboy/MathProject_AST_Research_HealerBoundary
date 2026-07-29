def generate(level=1, **kwargs):
    return {
        "question_text": r"Let $P(x) = (3x+a)(bx+c)$ be a polynomial with integer coefficients. Given that the product of the constant terms is 5 and the sum of the linear coefficients minus twice the first factor's leading coefficient equals -14, find the value of $(a+2c)$.",
        "correct_answer": 73,
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }