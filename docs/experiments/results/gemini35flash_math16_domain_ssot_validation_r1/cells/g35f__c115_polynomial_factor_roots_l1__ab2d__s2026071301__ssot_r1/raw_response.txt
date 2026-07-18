from core.prompts.domain_function_library import PolynomialOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    quadratic_coefficients = [1, 4, -12]
    a, b, c = quadratic_coefficients
    
    # Factor the quadratic
    factors = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Parse factors and compute roots
    parsed_factors = []
    for f in factors:
        p = FractionOps.create(f['x_coefficient'])
        q = FractionOps.create(f['constant'])
        root = -q / p
        parsed_factors.append({
            'p': p,
            'q': q,
            'root': root
        })
    
    # Sort factors by root ascending
    parsed_factors.sort(key=lambda x: x['root'])
    
    # Extract sorted roots
    roots = []
    for pf in parsed_factors:
        r = pf['root']
        if r.denominator == 1:
            roots.append(int(r.numerator))
        else:
            roots.append(f"{r.numerator}/{r.denominator}")
            
    # Build factorization LaTeX
    factor_strings = []
    for pf in parsed_factors:
        p = pf['p']
        q = pf['q']
        
        # Format p
        if p == 1:
            p_str = "x"
        elif p == -1:
            p_str = "-x"
        else:
            p_str = f"{p}x"
            
        # Format q
        if q > 0:
            q_str = f" + {q}"
        elif q < 0:
            q_str = f" - {abs(q)}"
        else:
            q_str = ""
            
        factor_strings.append(f"({p_str}{q_str})")
        
    factorization_latex = "".join(factor_strings)
    
    # Build roots_latex
    roots_latex_parts = []
    for r in roots:
        roots_latex_parts.append(f"x = {r}")
    roots_latex = ", ".join(roots_latex_parts)
    
    # Format polynomial for question text
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
        poly_parts.append(f"- {abs(b)}x" if b != -1 else "- x")
        
    if c > 0:
        poly_parts.append(f"+ {c}")
    elif c < 0:
        poly_parts.append(f"- {abs(c)}")
        
    poly_latex = " ".join(poly_parts).replace("+ -", "- ")
    
    question_text = f"Factor the quadratic polynomial ${poly_latex}$ and find its roots."
    
    correct_answer = {
        "roots": roots,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "quadratic_coefficients": quadratic_coefficients
        }
    }