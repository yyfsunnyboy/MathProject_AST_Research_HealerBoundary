def generate(level=1, **kwargs):
    return {
        "question_text": r"Given a quadratic polynomial $P(x)$ that can be factored as $(3x + a)(bx + c)$ where the coefficient of $x$ in the first factor is fixed at 3. The expanded form of this polynomial has coefficients for $x^2$, $x$, and the constant term equal to 39, 5, and -14 respectively. If we define the 'recovery value' as $a + 2c$, calculate its integer value.",
        "correct_answer": 7,
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }