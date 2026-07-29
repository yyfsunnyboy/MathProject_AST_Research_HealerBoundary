def generate(level=1, **kwargs):
    polynomials = []
    
    # Frozen sampled parameters from task specification
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a = 2 * level + 7
    c = 6 * level - 3
    
    # Construct the polynomial based on parameters
    # Factors are (x+a) and (3x+c) per strict_source_template policy with fixed left coefficient 3
    factor1 = f"({template_left_x_coefficient}x+{a})"
    factor2 = f"(x-{c})" if c > 0 else f"(x+{-c})"
    
    # Generate question text using formal LaTeX delimiters
    latex_factorization = f"{factor1}\\cdot{x}-{c}" if c > 0 else "{factor1}\\\\cdot x+{{-{c}}}"
    
    polynomial_str = r"\text{(3x+$a$)} \cdot (\text{$x$-$c$})"
    question_text = rf"""Find the integer value of $a$. The given quadratic expression is a product of two linear factors. One factor is fixed as $(3x+a)$ and the other has an x-coefficient of 1. Given that the expanded form matches $\{polynomial_str}$, determine $a$."""
    
    # Correct answer calculation: integer a + 2c
    correct_answer = int(a) + (int(2 * c)) if isinstance(c, float) else int(a) + int(2 * c)
    
    oracle_payload = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }