def generate(level=1, **kwargs):
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    A, B, C = quadratic_coefficients
    k = template_left_x_coefficient
    
    c = A // k
    
    a_val = None
    d_val = None
    for a in range(-abs(C), abs(C) + 1):
        if a == 0:
            continue
        if C % a == 0:
            d = C // a
            if k * d + a * c == B:
                a_val = a
                d_val = d
                break
                
    if a_val is None:
        raise ValueError("No solution found")
        
    ans = a_val + 2 * c
    
    # Format polynomial
    term1 = f"{A}x^2" if A != 1 else "x^2"
    if A == -1:
        term1 = "-x^2"
    
    if B > 0:
        term2 = f" + {B}x" if B != 1 else " + x"
    elif B < 0:
        term2 = f" - {-B}x" if B != -1 else " - x"
    else:
        term2 = ""
        
    if C > 0:
        term3 = f" + {C}"
    elif C < 0:
        term3 = f" - {-C}"
    else:
        term3 = ""
        
    poly_str = term1 + term2 + term3
    
    question_text = (
        f"The polynomial ${poly_str}$ can be factored into the form "
        f"$({k}x + a)(cx + d)$ where $a$, $c$, and $d$ are integers. "
        f"Find the value of $a + 2c$."
    )
    
    return {
        "question_text": question_text,
        "correct_answer": str(ans),
        "oracle_payload": {
            "factor_order_policy": factor_order_policy,
            "quadratic_coefficients": quadratic_coefficients,
            "template_left_x_coefficient": template_left_x_coefficient
        }
    }