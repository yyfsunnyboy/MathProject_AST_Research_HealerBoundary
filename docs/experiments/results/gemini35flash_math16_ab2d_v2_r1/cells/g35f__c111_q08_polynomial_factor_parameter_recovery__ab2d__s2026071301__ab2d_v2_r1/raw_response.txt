from core.prompts.domain_function_library import PolynomialOps
import math

def generate(level=1, **kwargs):
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    A, B, C = quadratic_coefficients
    p = template_left_x_coefficient
    
    c = A // p
    disc = B**2 - 4 * A * C
    sqrt_disc = int(math.isqrt(disc))
    
    a_candidates = []
    for sign in [-1, 1]:
        num = B + sign * sqrt_disc
        den = 2 * c
        if num % den == 0:
            a_candidates.append(num // den)
            
    a = None
    b = None
    for candidate_a in a_candidates:
        if candidate_a != 0 and C % candidate_a == 0:
            candidate_b = C // candidate_a
            if p * candidate_b + candidate_a * c == B:
                a = candidate_a
                b = candidate_b
                break
                
    assert a is not None and b is not None
    
    prod = PolynomialOps.mul([p, a], [c, b])
    assert prod == quadratic_coefficients
    
    correct_answer = a + 2 * c
    
    def format_poly(coeffs):
        A, B, C = coeffs
        term1 = f"{A}x^2"
        term2 = f"+ {B}x" if B > 0 else f"- {-B}x" if B < 0 else ""
        term3 = f"+ {C}" if C > 0 else f"- {-C}" if C < 0 else ""
        return f"{term1} {term2} {term3}".replace("  ", " ").strip()
        
    poly_str = format_poly(quadratic_coefficients)
    
    question_text = (
        f"The polynomial ${poly_str}$ can be factored as "
        f"$({p}x + a)(cx + b)$ where $a$, $b$, and $c$ are integers. "
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