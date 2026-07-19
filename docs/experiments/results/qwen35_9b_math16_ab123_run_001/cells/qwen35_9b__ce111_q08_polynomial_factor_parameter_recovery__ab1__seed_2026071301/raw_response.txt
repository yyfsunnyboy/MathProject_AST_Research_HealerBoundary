def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the polynomial $P(x) = (3x + a)(bx^2 + cx + d)$ where one factor is fixed as $(3x+a)$ and the quadratic coefficients are known to be in the frozen set $\{b, c, d\} = \{5, -14, 0\}$ with $c=-14$ from strict_source_template constraints on sorted or implied ordering if not fully explicit, calculate $a+2c$. The correct answer is derived directly from the hidden parameters.",
        "correct_answer": None, 
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }