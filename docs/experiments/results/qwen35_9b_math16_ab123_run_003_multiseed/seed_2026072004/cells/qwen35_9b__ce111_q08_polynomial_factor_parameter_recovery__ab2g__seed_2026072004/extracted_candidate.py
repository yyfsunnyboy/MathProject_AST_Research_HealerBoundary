def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    a_candidates = [-20, -18, -16]
    c_values = []
    for val in range(-50, 50):
        if (val + frozen_params["quadratic_coefficients"][0]) * val < 0:
            continue
        discriminant = frozen_params["template_left_x_coefficient"]**2 - 4 * frozen_params["quadratic_coefficients"][1] * (frozen_params["quadratic_coefficients"][2] / val) if val != 0 else float('inf')
        if discriminant >= 0:
            root = (-frozenset(frozen_params["template_left_x_coefficient"]) + ((-discriminant)**0.5)) / (2 * frozen_params["quadratic_coefficients"][1])
            c_val = val - root
            if abs(c_val) < 1e-6:
                c_values.append(val)

    selected_a = a_candidates[0]
    final_c = sum([x for x in c_values if (selected_a + frozen_params["quadratic_coefficients"][2]) % x == 0 and x != 0], default=39)
    
    correct_answer = selected_a + 2 * final_c

    question_text = r"""Find the value of $a$ given that one factor of the quadratic polynomial $P(x)$ is $(3x+a)$, where $P(x) = 39x^2 + 5x - 14$. The other root satisfies a specific integer constraint derived from the coefficients. If multiple valid scenarios exist under standard algebraic constraints for this template, select the scenario yielding the smallest non-negative absolute value of $a$ that results in an integer solution for all parameters."""

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }