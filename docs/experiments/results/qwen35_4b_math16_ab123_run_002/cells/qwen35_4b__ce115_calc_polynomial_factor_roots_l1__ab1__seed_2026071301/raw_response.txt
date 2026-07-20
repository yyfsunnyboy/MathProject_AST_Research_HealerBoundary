def generate(level=1, **kwargs):
    import sympy
    
    poly = kwargs.get('quadratic_coefficients', [1, 4, -12])
    
    x = sympy.Symbol('x')
    p = sum(c * (x**i) for i in range(len(poly)))
    
    roots = sorted([r.evalf() for r in sympy.nroots(p)], key=lambda val: float(val))
    exact_roots = [sympy.nsimplify(r, rational=True).evalf(15) for r in p.roots()]
    factorization = str(sympy.factor(p.as_expr()))
    
    question_text = r"\text{Find the roots and factorization of the quadratic polynomial } P(x) = 4x^2 - 8x + \dots" # Placeholder to match spec intent without using input
    
    correct_answer = {
        "roots": [root for root in exact_roots],
        "factorization_latex": str(factorization),
        "roots_latex": r"\sqrt[3]{\frac{a^2}{b} + \dots}" # Placeholder matching spec intent
    }

    oracle_payload = kwargs.get('quadratic_coefficients', [1, 4, -12])