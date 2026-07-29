# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    a, b, c = frozen_params["quadratic_coefficients"]
    
    # Compute discriminant: D = b^2 - 4ac
    d = b * b - 4 * a * c
    
    # Since coefficients are integers and result in perfect square for this case (16 + 48 = 64)
    sqrt_d = int(d ** 0.5)
    
    # Compute roots using exact arithmetic logic, then convert to float only if necessary for representation, 
    # but the spec requires "Exact arithmetic; no floats" in correct_answer structure implies symbolic or integer representation where possible.
    # However, standard polynomial roots are often non-integers unless specified otherwise.
    # For x^2 + 4x - 12 = (x+6)(x-2), roots are integers: -6 and 2.
    
    root1_num = (-b + sqrt_d) // (2 * a) if d % ((2*a)**2) == 0 else float((-b + d**0.5)/(2*a)) # Simplified logic for integer check first
    # Actually, let's compute precisely:
    # x = [-4 +/- sqrt(16 - 4*1*(-12))] / 2
    # x = [-4 +/- sqrt(64)] / 2
    # x = (-4 + 8)/2 = 2, (-4 - 8)/2 = -6
    
    root_a_num = -b + sqrt_d
    root_b_num = -b - sqrt_d
    
    if (root_a_num % (2 * a)) == 0:
        root1 = int(root_a_num // (2 * a))
        root2 = int(root_b_num // (2 * a))
    else:
        # Fallback for non-integer roots, though spec says exact arithmetic. 
        # Given the frozen params [1, 4, -12], roots are integers.
        pass
    
    if root1 > root2:
        r_asc = [root2, root1]
    else:
        r_asc = [root1, root2]
    
    # Generate LaTeX strings for factorization and roots
    # Factorization of x^2 + 4x - 12 is (x+6)(x-2) or generally a(x-r1)(x-r2) if non-integers.
    # Here: (x - (-6))(x - 2) -> (x+6)(x-2)
    
    factorization_latex = r"\\left(x + \\frac{-b_0}{a} + \\sqrt{\\frac{D}{4a^2}}\\right)\\left(x + \\frac{-b_0}{a} - \\sqrt{\\frac{D}{4a^2}}\\right)"
    # Substitute values for clean LaTeX: (x+6)(x-2)
    factorization_latex = r"(x + 6)(x - 2)"
    
    roots_latex_list = [str(r) if isinstance(r, int) else f"{r:.10g}" for r in r_asc]
    roots_latex_str = ", ".join(roots_latex_list)

    question_text = r"Find the factorization and roots of the quadratic polynomial $x^2 + 4x - 12$."
    
    correct_answer = {
        "roots": [r for r in sorted([root_a_num // (2*a), root_b_num // (2*a)]) if isinstance(r, int) else [-6.0, 2.0], # Ensure list of numbers
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex_str
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }