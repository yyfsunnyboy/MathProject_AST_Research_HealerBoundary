def generate(level=1, **kwargs):
    import sympy
    
    # Frozen parameters as per task specification
    expression_str = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Parse and simplify the fraction using SymPy for exact arithmetic
    expr = sympy.sympify(expression_str)
    simplified_expr = sympy.simplify(expr)
    
    # Extract numerator, denominator, and canonical LaTeX representation
    num = int(simplified_expr.as_numer_denom()[0])
    den = int(simplified_expr.as_numer_denom()[1])
    
    # Ensure the fraction is in simplest form (SymPy simplify does this by default for rationals)
    if den < 0:
        num, den = -num, -den
    
    canonical_latex = f"{int(num)}/{int(den)}"
    
    return {
        "question_text": r"$\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$",
        "correct_answer": {
            "numerator": int(num),
            "denominator": int(den),
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"expression": expression_str}
    }
