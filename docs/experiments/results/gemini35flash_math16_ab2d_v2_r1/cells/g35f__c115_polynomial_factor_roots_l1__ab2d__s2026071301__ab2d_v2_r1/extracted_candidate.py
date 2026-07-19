from core.prompts.domain_function_library import PolynomialOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    quadratic_coefficients = [1, 4, -12]
    a, b, c = quadratic_coefficients
    
    # Factor the quadratic using the domain API
    factors = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Compute roots and pair them with factors
    roots_with_factors = []
    for factor in factors:
        p = FractionOps.create(factor['x_coefficient'])
        q = FractionOps.create(factor['constant'])
        # root is -q / p
        root = -q / p
        roots_with_factors.append((root, factor))
        
    # Sort by root ascending
    roots_with_factors.sort(key=lambda x: x[0])
    
    # Format roots
    roots_formatted = []
    for r, _ in roots_with_factors:
        if r.denominator == 1:
            roots_formatted.append(str(r.numerator))
        else:
            roots_formatted.append(f"{r.numerator}/{r.denominator}")
            
    roots_ascending_str = ", ".join(roots_formatted)
    roots_latex = ", ".join(roots_formatted)
    
    # Format factorization
    factor_strings = []
    for r, factor in roots_with_factors:
        p = factor['x_coefficient']
        q = factor['constant']
        
        if p == 1:
            p_str = ""
        elif p == -1:
            p_str = "-"
        else:
            p_str = str(p)
            
        if q > 0:
            q_str = f" + {q}"
        elif q < 0:
            q_str = f" - {abs(q)}"
        else:
            q_str = ""
            
        if p_str or q_str:
            factor_strings.append(f"({p_str}x{q_str})")
        else:
            factor_strings.append("x")
            
    factorization_latex = "".join(factor_strings)
    
    question_text = f"Factor the polynomial $x^2 + 4x - 12$ and find its roots."
    correct_answer = f"Factorization: ${factorization_latex}$, Roots: {roots_ascending_str} (or $x = {roots_latex}$)"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "quadratic_coefficients": quadratic_coefficients
        }
    }