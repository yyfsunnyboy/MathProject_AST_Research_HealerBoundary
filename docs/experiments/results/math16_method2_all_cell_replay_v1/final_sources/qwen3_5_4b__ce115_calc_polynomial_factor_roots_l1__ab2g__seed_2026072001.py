def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Solve ax^2 + bx + c = 0 where a=1, b=4, c=-12
    # x = (-b ± sqrt(b^2 - 4ac)) / (2a)
    # discriminant = 4^2 - 4*1*(-12) = 16 + 48 = 64
    # sqrt(64) = 8
    # roots: (-4 + 8)/2 = 2, (-4 - 8)/2 = -6
    
    root_a = -6
    root_b = 2
    
    factorization_latex = r"$(x+6)(x-2)$"
    roots_latex = r"$\{-6, 2\}$"
    
    question_text = r"\text{Factor the polynomial } x^2 + 4x - 12 \text{ and find its roots.}"
    
    correct_answer = {
        "roots": [root_a, root_b],
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": quadratic_coefficients
    }