from core.prompts.domain_function_library import PolynomialOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    A, B, C = quadratic_coefficients
    k = template_left_x_coefficient
    
    # k * c = A => c = A // k
    c = A // k
    
    # Find integer a and d such that:
    # a * d = C
    # k * d + a * c = B
    a = None
    d = None
    for possible_a in [1, -1, 2, -2, 7, -7, 14, -14]:
        if possible_a == 0:
            continue
        if C % possible_a == 0:
            possible_d = C // possible_a
            if k * possible_d + possible_a * c == B:
                a = possible_a
                d = possible_d
                break
                
    # Verify using PolynomialOps.mul
    prod = PolynomialOps.mul([k, a], [c, d])
    assert prod == quadratic_coefficients
    
    correct_answer = a + 2 * c
    
    # Format the quadratic polynomial for the question
    poly_str = "39x^2 + 5x - 14"
    
    question_text = (
        f"The quadratic polynomial ${poly_str}$ can be factored in the form "
        f"$(3x + a)(cx + d)$ for some integers $a$, $c$, and $d$. "
        f"Find the value of $a + 2c$."
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