def generate(level=1, **kwargs):
    # Frozen parameters
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3

    A, B, C = quadratic_coefficients
    k = template_left_x_coefficient

    # Solve for d, a, c
    # A = k * d => d = A // k
    d = A // k
    
    # Find a and c such that a * c = C and k * c + a * d = B
    found = False
    for a in range(-abs(C), abs(C) + 1):
        if a == 0:
            continue
        if C % a == 0:
            c = C // a
            if k * c + a * d == B:
                found = True
                break
    
    if not found:
        raise ValueError("No solution found")

    correct_answer = a + 2 * c

    # Format polynomial string
    poly_str = f"{A}x^2"
    if B > 0:
        poly_str += f" + {B}x"
    elif B < 0:
        poly_str += f" - {abs(B)}x"
    
    if C > 0:
        poly_str += f" + {C}"
    elif C < 0:
        poly_str += f" - {abs(C)}"

    question_text = (
        f"The polynomial ${poly_str}$ can be factored in the form "
        f"$({k}x + a)(dx + c)$ for some integers $a$, $c$, and $d$. "
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