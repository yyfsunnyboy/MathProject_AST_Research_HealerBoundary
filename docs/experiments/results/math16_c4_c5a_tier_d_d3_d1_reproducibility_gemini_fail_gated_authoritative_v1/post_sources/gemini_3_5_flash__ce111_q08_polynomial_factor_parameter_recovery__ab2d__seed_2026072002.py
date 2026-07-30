def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps, FractionOps

    # Frozen parameters
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    A, B, C = quadratic_coefficients
    k = template_left_x_coefficient
    
    # Compute b using FractionOps
    b = int(FractionOps.create(A) / FractionOps.create(k))
    
    # Find a and c such that a * c = C and k * c + a * b = B
    a_found, c_found = None, None
    for a in range(-abs(C), abs(C) + 1):
        if a == 0:
            continue
        if C % a == 0:
            c = C // a
            if k * c + a * b == B:
                # Verify with PolynomialOps.mul
                if PolynomialOps.mul([k, a], [b, c]) == quadratic_coefficients:
                    a_found, c_found = a, c
                    break
                    
    if a_found is None:
        raise ValueError("No solution found")
        
    correct_answer = a_found + 2 * c_found
    
    poly_str = "39x^2 + 5x - 14"
    question_text = (
        f"The polynomial ${poly_str}$ can be factored into the form "
        f"$(3x + a)(bx + c)$ where $a, b, c$ are integers. "
        f"Find the value of $a + 2c$."
    )
    
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