import sympy as sp

def generate(level=1, **kwargs):
    # Frozen parameters
    expression_str = kwargs.get("expression", "(5*x**2 - 2*x) - (4 - 3*x)")
    
    # Parse expression
    x = sp.Symbol('x')
    expr = sp.sympify(expression_str)
    poly = sp.Poly(expr, x)
    
    # Get coefficients for degrees 2, 1, 0
    coeffs = {}
    for deg in [2, 1, 0]:
        coeff = poly.nth(deg)
        if isinstance(coeff, sp.Rational):
            if coeff.q == 1:
                coeffs[str(deg)] = int(coeff.p)
            else:
                coeffs[str(deg)] = f"{coeff.p}/{coeff.q}"
        else:
            coeffs[str(deg)] = int(coeff)
            
    question_text = f"Simplify the following polynomial expression:\n\n{expression_str}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficients": coeffs
        },
        "oracle_payload": {
            "expression": expression_str
        }
    }