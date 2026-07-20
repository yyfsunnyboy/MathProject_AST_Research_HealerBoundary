def generate(level=1, **kwargs):
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a = kwargs.get("a", 7)
    c = quadratic_coefficients[2]
    
    question_text = r"The polynomial $P(x)$ has factors $(3x + a)(bx + c)$. Given that the coefficient of $x^2$ in the expansion is $\frac{1}{4}bc$, find the value of $a+2c$."

    correct_answer = a + 2 * c
    oracle_payload = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }