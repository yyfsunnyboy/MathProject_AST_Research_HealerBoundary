def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps

    # Frozen sampled parameters
    oracle_payload = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # The polynomial is 39x^2 + 5x - 14
    # We factor it as (3x + a)(dx + c)
    # Since 3 * d = 39, d = 13.
    # We have (3x + a)(13x + c) = 39x^2 + (3c + 13a)x + ac
    # ac = -14 and 3c + 13a = 5
    # Solving this gives a = 2, c = -7.
    # Let's verify using PolynomialOps.mul
    # [2, 3] represents 2 + 3x, [-7, 13] represents -7 + 13x
    prod = PolynomialOps.mul([2, 3], [-7, 13])
    # prod should be [-14, 5, 39], which corresponds to 39x^2 + 5x - 14

    a = 2
    c = -7
    correct_answer = a + 2 * c

    question_text = (
        "The quadratic polynomial $39x^2 + 5x - 14$ can be factored in the form "
        "$(3x + a)(dx + c)$ for some integers $a, c, d$. Find the value of $a + 2c$."
    )

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }