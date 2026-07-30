def generate(level=1, **kwargs):
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3

    question_text = (
        "The polynomial $39x^2 + 5x - 14$ can be factored into the form "
        "$(3x + a)(bx + c)$ for some integers $a$, $b$, and $c$. "
        "Find the value of $a + 2c$."
    )
    correct_answer = -12

    oracle_payload = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient,
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }