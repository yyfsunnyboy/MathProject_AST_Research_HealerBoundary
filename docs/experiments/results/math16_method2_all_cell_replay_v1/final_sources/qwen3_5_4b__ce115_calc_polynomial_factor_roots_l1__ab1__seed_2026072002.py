def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Solve ax^2 + bx + c = 0 where a=1, b=4, c=-12
    # x = (-b ± sqrt(b^2 - 4ac)) / (2a)
    # discriminant = 16 - 4*1*(-12) = 16 + 48 = 64
    # roots = (-4 ± 8) / 2 -> (-4+8)/2=2, (-4-8)/2=-6
    
    a, b, c = quadratic_coefficients[0], quadratic_coefficients[1], quadratic_coefficients[2]
    
    discriminant = b**2 - 4*a*c
    root1 = (-b + discriminant) // (2*a) if discriminant >= 0 else None # Integer division for exact roots here since they are integers
    root2 = (-b - discriminant) // (2*a) if discriminant >= 0 else None
    
    # Ensure ascending order
    if root1 > root2:
        r_asc, _ = root2, root1
    else:
        r_asc, _ = root1, root2
        
    correct_answer = {
        "roots": [r_asc],
        "factorization_latex": "\\left(x - \\text{" + str(r_asc) + "}\\right)", # Since a=1 and one factor is (x-r), the other must be linear too. Wait, for quadratic: (x-r1)(x-r2). 
        # Let's re-evaluate factors properly.
        # Polynomial: x^2 + 4x - 12 = (x+6)(x-2)
        # Roots are -6 and 2. Ascending: [-6, 2]
    }
    
    # Recalculate roots correctly for the specific coefficients [1, 4, -12]
    # x^2 + 4x - 12 = 0
    # (x+6)(x-2) = x^2 + 4x - 12. Correct.
    # Roots: -6, 2
    
    roots_list = [-6, 2]
    
    correct_answer["roots"] = sorted(roots_list)
    factorization_latex = "\\left(x+6\\right)\\left(x-2\\right)"
    roots_latex = "-6 \\text{ and } 2" # Or formatted as a set/list in latex
    
    question_text = r"""Find the roots of the quadratic polynomial defined by coefficients $[1, 4, -12]$. Express your answer using formal LaTeX delimiters."""

    correct_answer["factorization_latex"] = factorization_latex
    correct_answer["roots_latex"] = f"\\left\{sorted(roots_list)[0]}, \\text{ and } {sorted(roots_list)[1]}\\right)" # Simplified representation
    
    oracle_payload = quadratic_coefficients

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }