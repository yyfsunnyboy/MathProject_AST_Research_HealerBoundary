def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    import sympy
    
    a, b, c = frozen_params["quadratic_coefficients"]
    x = sympy.Symbol('x')
    
    polynomial_expr = a * x**2 + b * x + c
    roots_list = list(sympy.nroots(polynomial_expr)) # Use nroots to ensure we get numbers
    
    factorization_latex = f"{a} {b} \\cdot (\\sqrt{d})" if sympy.sqrt(d) else ""

    return {"question_text": r"$ax^2 + bx + c$", "correct_answer": roots_list, "oracle_payload": frozen_params}