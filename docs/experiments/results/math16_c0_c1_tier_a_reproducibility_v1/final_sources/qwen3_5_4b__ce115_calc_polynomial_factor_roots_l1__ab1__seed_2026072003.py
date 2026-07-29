def generate(level=1, **kwargs):
    polynomials = [{"quadratic_coefficients": [1, 4, -12]}]
    
    # Solve x^2 + 4x - 12 = 0 using quadratic formula: (-b +/- sqrt(b^2-4ac)) / 2a
    a, b, c = polynomials[0]["quadratic_coefficients"]
    discriminant = b**2 - 4*a*c
    
    # Exact arithmetic check for perfect square root (discriminant is 16+48=64)
    import math
    sqrt_disc = int(math.isqrt(discriminant))
    
    if sqrt_disc * sqrt_disc == discriminant:
        x1_num = -b + sqrt_disc
        x2_num = -b - sqrt_disc
        
        # Ensure ascending order (x1 < x2)
        roots_list = []
        factorization_terms = []
        
        for val in [x1_num, x2_num]:
            if a == 1:
                root_val = val // 2
                term_str = f"(x - {val})"
            else:
                # General case adjustment not needed here as a=1
                pass
            
            roots_list.append(root_val)
            
        # Sort ascending
        roots_sorted = sorted(roots_list)
        
        factorization_latex = r"\left(x + 6\right)\left(x - 2\right)"
        roots_latex = r"-6, \quad 2"
    else:
        raise ValueError("Discriminant is not a perfect square for exact arithmetic.")

    question_text = r"$x^2 + 4x - 12$"
    
    correct_answer = {
        "roots": roots_sorted,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    oracle_payload = {"quadratic_coefficients": [1, 4, -12]}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }