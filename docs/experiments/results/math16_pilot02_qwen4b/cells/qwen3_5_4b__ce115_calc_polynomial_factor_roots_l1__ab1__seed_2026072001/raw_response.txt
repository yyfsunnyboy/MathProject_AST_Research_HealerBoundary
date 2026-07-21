def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Solve ax^2 + bx + c = 0 where a=1, b=4, c=-12
    # x = (-b ± sqrt(b^2 - 4ac)) / (2a)
    # discriminant = 16 - 4(1)(-12) = 16 + 48 = 64
    # roots = (-4 ± 8) / 2 -> x1 = (-4+8)/2 = 2, x2 = (-4-8)/2 = -6
    
    root1 = 2
    root2 = -6
    
    sorted_roots = [root2, root1] # ascending: [-6, 2]
    
    factorization_latex = r"$(x + 6)(x - 2)$"
    roots_latex = r"$-6,\ 2$"
    
    question_text = r"""Find the roots and factorization of the quadratic polynomial defined by coefficients $1$, $4$, and $-12$ (i.e., solve $x^2 + 4x - 12 = 0$). Express your answer with exact arithmetic.

**Question:** Factorize the polynomial $P(x) = x^2 + 4x - 12$. List its roots in ascending order."""
    
    correct_answer = {
        "roots": sorted_roots,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    oracle_payload = quadratic_coefficients
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }