def generate(level=1, **kwargs):
    return {
        "question_text": r"Given a quadratic polynomial $P(x)$ that can be factored into $(3x + a)(bx + c)$ where the coefficients satisfy strict source template constraints with fixed left coefficient 3. If the correct answer is defined as $a + 2c$, and given frozen sampled parameters $\{ \text{"factor\_order\_policy"}: \text{"strict\_source\_template"}, \text{"quadratic\_coefficients"}: [39, 5, -14], \text{"template\_left\_x\_coefficient"}: 3 \}$ where the quadratic coefficients correspond to $[ac + ab\cdot c? No, standard form]$. Let us derive strictly from frozen params.",
        "correct_answer": None, 
        "oracle_payload": {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    }