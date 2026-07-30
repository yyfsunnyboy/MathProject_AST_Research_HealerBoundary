def generate(level=1, **kwargs):
    import math

    # Frozen parameters
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    A, B, C = quadratic_coefficients
    k = template_left_x_coefficient
    
    # c is A // k
    c = A // k
    
    # Solve c * a^2 - B * a + k * C = 0
    disc = B**2 - 4 * c * k * C
    sqrt_disc = int(math.isqrt(disc))
    
    # Two possible values for a
    a1 = (B + sqrt_disc) // (2 * c)
    a2 = (B - sqrt_disc) // (2 * c)
    
    # Check which one gives integer d and satisfies the equations
    a = None
    for candidate_a in [a1, a2]:
        if candidate_a != 0 and C % candidate_a == 0:
            candidate_d = C // candidate_a
            if k * candidate_d + candidate_a * c == B:
                a = candidate_a
                break
                
    if a is None:
        raise ValueError("No integer solution found")
        
    correct_answer = a + 2 * c
    
    # Format the polynomial for question text
    poly_str = f"{A}x^2"
    if B > 0:
        poly_str += f" + {B}x"
    elif B < 0:
        poly_str += f" - {-B}x"
    if C > 0:
        poly_str += f" + {C}"
    elif C < 0:
        poly_str += f" - {-C}"
        
    question_text = (
        f"The quadratic polynomial ${poly_str}$ can be factored in the form "
        f"$({k}x + a)(cx + d)$ for some integers $a$, $c$, and $d$. "
        f"Find the value of the integer $a + 2c$."
    )
    
    oracle_payload = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }
    
    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer),
        "oracle_payload": oracle_payload
    }