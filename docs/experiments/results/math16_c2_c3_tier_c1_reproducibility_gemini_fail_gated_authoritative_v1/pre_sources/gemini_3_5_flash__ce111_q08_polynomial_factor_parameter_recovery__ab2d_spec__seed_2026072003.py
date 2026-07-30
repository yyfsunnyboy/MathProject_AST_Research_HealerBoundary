# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters
    oracle_payload = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # Factoring 39x^2 + 5x - 14 as (3x + a)(bx + c)
    # 3b = 39 => b = 13
    # ac = -14
    # 3c + 13a = 5
    # Testing factors of -14 for a:
    # If a = 2, c = -7: 3(-7) + 13(2) = -21 + 26 = 5 (Matches!)
    # Thus, a = 2, c = -7.
    # We need to find a + 2c = 2 + 2(-7) = -12.
    correct_answer = -12

    question_text = (
        "The quadratic polynomial $39x^2 + 5x - 14$ can be factored in the form "
        "$(3x + a)(bx + c)$, where $a$, $b$, and $c$ are integers. "
        "Find the value of $a + 2c$."
    )

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }