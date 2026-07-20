def generate(level=1, **kwargs):
    factor_order_policy = kwargs.get("factor_order_policy", "strict_source_template")
    quadratic_coefficients = kwargs.get("quadratic_coefficient_list", [39, 5, -14])
    template_left_x_coefficient = kwargs.get("template_left_x_coefficient", 3)

    a, b, c = quadratic_coefficients[0], quadratic_coefficients[1], quadratic_coefficients[2]

    question_text = f"Given the polynomial $P(x) = {c}x^2 + {b}x + {a}$ and its factorization starting with $(\\{{{template_left_x_coefficient}\\}x+{y})$ where ${y}=0$, find the integer value of $a + 2c$."

    correct_answer = a + 2 * c
    oracle_payload = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }