def generate(level=1, **kwargs):
    import sympy
    
    quadratic_coefficients = [1, 4, -12]
    
    x = sympy.Symbol('x')
    poly_expr = sum(c * (x**i) for i, c in enumerate(quadratic_coefficients))
    poly = sympy.Poly(poly_expr, x)
    
    roots = sorted([r.evalf() if r.is_complex else int(r) for r in poly.all_roots()], key=lambda val: float(val))
    factorization_latex = str(poly.factor_list()[0][1])
    roots_latex = ', '.join(['%s' % (int(root).evalf()) for root in roots])
    
    question_text = r"Factor the polynomial $P(x) = x^2 + 4x - 12$ and find its roots."
    
    correct_answer = {
        "roots": [3, -4],
        "factorization_latex": "(x - 3)(x + 4)",
        "roots_latex": "$3, -4$"
    }
    
    oracle_payload = quadratic_coefficients
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }