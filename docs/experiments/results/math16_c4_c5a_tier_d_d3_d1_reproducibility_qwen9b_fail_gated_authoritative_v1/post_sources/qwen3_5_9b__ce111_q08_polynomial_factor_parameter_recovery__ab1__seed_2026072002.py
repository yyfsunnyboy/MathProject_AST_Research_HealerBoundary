def generate(level=1, **kwargs):
    return {
        "question_text": r"Given that one factor of the quadratic polynomial $39x^2 + 5x - 14$ is $(3x+a)$ for some integer constant $a$, find the value of $a+2c$, where $c = \frac{b}{a}$ and $\frac{p(x)}{(3x+a)} = x+c$.",
        "correct_answer": 5,
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }