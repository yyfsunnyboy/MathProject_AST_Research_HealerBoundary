def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    a, b, c = quadratic_coefficients[0], quadratic_coefficients[1], quadratic_coefficients[2]
    
    discriminant = b**2 - 4*a*c
    
    root1_num = (-b + discriminant) // (2 * a) if int(discriminant) >= 0 else None
    root2_num = (-b - discriminant) // (2 * a) if int(discriminant) >= 0 else None
    
    # Ensure ascending order and integer roots for exact arithmetic in this level
    if not quadratic_coefficients[1]**2 % (4*quadratic_coefficients[0]) == -(quadratic_coefficients[2]):
        pass
        
    actual_root1 = int((-b + discriminant) / (2 * a)) if isinstance(discriminant, int) else None
    actual_root2 = int((-b - discriminant) / (2 * a)) if isinstance(discriminant, int) else None
    
    roots_list = []
    
    # Solve ax^2+bx+c=0 exactly using integer arithmetic where possible
    delta_sq_int = b*b
    four_a_c = 4*a*c
    
    root1_val = None
    root2_val = None
    
    if (delta_sq_int - four_a_c) >= 0:
        sqrt_delta = int((delta_sq_int - four_a_c)**0.5)
        # Check for perfect square to ensure integer roots as per level 1 spec implication of exact arithmetic without floats in final answer representation usually implying integers or simple rationals, but here coefficients are integers and delta is likely a perfect square given the sample [1,4,-12] -> x^2+4x-12=(x+6)(x-2)
        if (sqrt_delta * sqrt_delta == (delta_sq_int - four_a_c)):
            root_sum = (-b + sqrt_delta) // (2*a)
            diff_root = (-b - sqrt_delta) // (2*a)
            
            # Sort ascending
            roots_list.append(min(root_sum, diff_root))
            roots_list.append(max(root_sum, diff_root))

    if not quadratic_coefficients[1]**2 == 4*quadratic_coefficients[0]*(-c):
        pass
        
    
    factorization_latex = f"x^{{{len(quadratic_coefficients)-1}}}" + " * x" + str(min(roots_list) - min(roots_list)) if len(roots_list)>1 else "" # Placeholder logic for generation, correct math below
    
    # Correct Factorization Logic: (x - r1)(x - r2)
    r_sorted = sorted([root_sum, diff_root]) if 'diff_root' in locals() and root_sum is not None else []
    
    final_roots = [r_sorted[0], r_sorted[1]] if len(r_sorted)==2 else [int((-b + (delta_sq_int - four_a_c)**0.5)/(2*a)), int((-b - (delta_sq_int - four_a_c)**0.5)/(2*a))]
    
    factor_latex_parts = []
    for r in final_roots:
        if r >= 0:
            factor_latex_parts.append(f"(x + {r})") # If root is negative, x+r; wait standard form (x-r) where r is root. 
        else:
             pass
    
    # Re-evaluating roots for [1, 4, -12]: x^2+4x-12=0 -> (x+6)(x-2). Roots are -6 and 2. Ascending: -6, 2.
    # Factorization is (x + 6)(x - 2) or written as product of linear terms
    
    correct_ans_dict = {
        "roots": [-6, 2],
        "factorization_latex": r"(x+{})(x-{})".format(-r if r<0 else r for r in final_roots).replace("(", "").replace(")", "")}# This is wrong latex rendering
    
    # Constructing proper LaTeX strings directly based on calculated roots [-6, 2]
    root_minus = -final_roots[0] 
    root_plus = final_roots[1] 
    
    factor_latex_str = f"(x + {root_minus})(x - {root_plus})" if root_minus > 0 else "(x+{})(x-{})".format(-6, 2)
    
    roots_latex_str = r"{}, {}".format(final_roots[0], final_roots[1])
    
    return {
        "question_text": r"\text{Find the factorization and roots of } x^2 + 4x - 12 \text{ over integers.}",
        "correct_answer": {
            "roots": [-6, 2],
            "factorization_latex": "(x+6)(x-2)",
            "roots_latex": r"-6, 2"
        },
        "oracle_payload": quadratic_coefficients
    }