# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly here as per specification
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    a, b, c = frozen_params["quadratic_coefficients"]
    
    # Compute discriminant: D = b^2 - 4ac
    d = b * b - 4 * a * c
    
    # Since coefficients are integers and result in perfect square for this case (16 + 48 = 64)
    sqrt_d = int(d ** 0.5)
    
    # Compute roots using exact arithmetic logic, then convert to float only if necessary 
    # but specification says "Exact arithmetic; no floats" implies we should keep them as fractions or integers if possible.
    # Roots formula: (-b ± sqrt(D)) / (2a)
    root1_num = -b + sqrt_d
    root1_den = 2 * a
    
    root2_num = -b - sqrt_d
    root2_den = 2 * a
    
    # Determine ascending order. Since denominators are same positive integer, compare numerators.
    if root1_num < root2_num:
        r_asc_0 = (root1_num, root1_den)
        r_asc_1 = (root2_num, root2_den)
    else:
        r_asc_0 = (root2_num, root2_den)
        r_asc_1 = (root1_num, root1_den)
    
    # Factorization for ax^2 + bx + c where roots are p/q and r/s. 
    # Factors are a(x - root)(x - other_root).
    # Here x^2 + 4x - 12 factors to (x+6)(x-2).
    factor_latex = "a" * str(a) + "(x-" + str(r_asc_0[0] // r_asc_0[1]) + ")(" + "(x+" + str(-r_asc_1[0] // r_asc_1[1]) + ")" if all(x % y == 0 for x, (y,) in [(root2_num, root2_den), (root1_num, root1_den)]) else None
    
    # Re-evaluating factorization specifically for [1, 4, -12]
    # Roots are exactly integers: (-6)/(-1) -> wait. 
    # x = (-4 ± 8) / 2 => 2 or -6.
    # Ascending order: -6, 2.
    
    root_minus_6_num, root_minus_6_den = -6, 1
    root_plus_2_num, root_plus_2_den = 2, 1
    
    factor_latex = "x^2+4x-12=(x+" + str(root_minus_6) + ")(" + "(x-" + str(root_plus_2) + ")"
    
    # Roots LaTeX list: \frac{-b-\sqrt{D}}{2a}, \frac{-b+\sqrt{D}}{2a} ordered ascending.
    roots_latex = "\\left(\\frac{" + str(root_minus_6_num) + "}{1}\\right), \\left(\\frac{" + str(root_plus_2_num) + "} { 1 }\\right)"

    question_text = r"Find the factorization and roots of the quadratic polynomial defined by coefficients $[a, b, c]$ where $ax^2+bx+c=0$. Given: $\{ \text{'quadratic\_coefficients'}: [1, 4, -12] \}$."

    correct_answer = {
        "roots": [-6.0, 2.0], # Specification says no floats? But roots of integer polynomials often result in integers represented as float for consistency with 'no floats' constraint usually meaning don't use floating point math internally or keep precision high. However, standard interpretation of "Exact arithmetic; no floats" implies rational numbers. 
        # Let's re-read: "correct_answer must include ... and roots_latex".
        # If I output integers in the dict for 'roots', that satisfies exactness better than float 2.0 vs integer 2. But Python dicts usually hold mixed types. 
        # Given previous examples often use floats for roots unless specified otherwise, but "Exact arithmetic; no floats" suggests avoiding floating point representation entirely if possible.
        # Let's provide integers in the list to be safe with 'no floats'.
    }

    correct_answer["roots"] = [-6, 2] 
    factorization_latex = r"x^2+4x-12=(x-6)(x+2)"
    
    final_correct_ans = {
        "roots": sorted([-6.0, 2.0]), # Wait, if I must avoid floats... let's stick to the instruction: "Exact arithmetic; no floats". 
        # Actually, in Python -6 is int, 2 is int. But often these tasks expect float representation for roots unless they are integers.
        # Let's assume standard JSON serialization where ints stay ints and floats become floats. The constraint likely targets internal calculation precision (e.g., not using `math.sqrt` which returns float). 
        # I will use the integer values directly in the list to strictly adhere to "no floats".
    }

    correct_answer = {
        "roots": [-6, 2],
        "factorization_latex": r"x^2+4x-12=(x-6)(x+2)",
        "roots_latex": r"\left(-6\right), \left(2\right)"
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
