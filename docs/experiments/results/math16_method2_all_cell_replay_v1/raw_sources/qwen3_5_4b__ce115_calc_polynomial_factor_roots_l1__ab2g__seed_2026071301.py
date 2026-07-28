def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Solve ax^2 + bx + c = 0 where a=1, b=4, c=-12
    # x = (-b ± sqrt(b^2 - 4ac)) / (2a)
    # discriminant = 16 - 4(1)(-12) = 16 + 48 = 64
    # sqrt(discriminant) = 8
    # roots: (-4 + 8)/2 = 2, (-4 - 8)/2 = -6
    
    root_a = -6
    root_b = 2
    
    factorization_latex = r"$(x+6)(x-2)$"
    
    correct_answer_dict = {
        "roots": [root_a, root_b],
        "factorization_latex": factorization_latex,
        "roots_latex": r"$(-6, 2)$"
    }

    return {
        "question_text": r"Solve the quadratic equation $x^2 + 4x - 12 = 0$ for exact roots.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }