def generate(level=1, **kwargs):
    quadratic_coefficients = kwargs.get("quadratic_coefficients", [1, 4, -12])
    a, b, c = quadratic_coefficients
    
    import math
    D = b**2 - 4*a*c
    sqrt_D = int(math.isqrt(D))
    r1 = (-b - sqrt_D) // (2*a)
    r2 = (-b + sqrt_D) // (2*a)
    roots = sorted([r1, r2])
    
    def format_factor(r):
        if r == 0:
            return "x"
        elif r < 0:
            return f"(x + {-r})"
        else:
            return f"(x - {r})"
            
    factorization_latex = format_factor(roots[0]) + format_factor(roots[1])
    roots_latex = f"{roots[0]}, {roots[1]}"
    
    poly_parts = []
    if a == 1:
        poly_parts.append("x^2")
    elif a == -1:
        poly_parts.append("-x^2")
    else:
        poly_parts.append(f"{a}x^2")
        
    if b > 0:
        poly_parts.append(f"+ {b}x" if b != 1 else "+ x")
    elif b < 0:
        poly_parts.append(f"- {-b}x" if b != -1 else "- x")
        
    if c > 0:
        poly_parts.append(f"+ {c}")
    elif c < 0:
        poly_parts.append(f"- {-c}")
        
    poly_str = " ".join(poly_parts).replace("+ -", "- ")
    
    question_text = f"Factor the polynomial \\(f(x) = {poly_str}\\) and find its roots."
    
    correct_answer = {
        "roots": roots,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    oracle_payload = {
        "quadratic_coefficients": quadratic_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }