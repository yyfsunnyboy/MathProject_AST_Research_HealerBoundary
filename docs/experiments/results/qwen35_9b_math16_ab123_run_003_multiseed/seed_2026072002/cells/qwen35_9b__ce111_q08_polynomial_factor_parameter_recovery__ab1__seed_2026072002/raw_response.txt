def generate(level=1, **kwargs):
    return {
        "question_text": r"Given that $(3x + a)$ is a factor of $f(x) = 39x^2 + bx - 42$, where the quadratic coefficients are $\{39, b, c\}$ with $c=-14$ and the linear coefficient satisfies $b=5$. If we assume the standard form for this difficulty level implies finding a specific integer parameter recovery based on the constant term relationship in such factorization problems, determine the value of $a+2c$. Note: The problem setup fixes one root-related constraint.",
        "correct_answer": 149,
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }