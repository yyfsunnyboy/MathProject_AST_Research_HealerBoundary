def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Extract coefficients a, b, c from the quadratic list
    coeffs = frozen_params["quadratic_coefficients"]
    a_int = int(coeffs[0])
    b_int = int(coeffs[1])
    c_int = int(coeffs[2])
    
    # Calculate discriminant and roots exactly using integer arithmetic to avoid float issues
    D = b_int*b_int - 4*a_int*c_int
    
    if D < 0:
        return {"question_text": "", "correct_answer": {}, "oracle_payload": {}}
    
    sqrt_D = int(D**0.5)
    if sqrt_D * sqrt_D != D:
        return {"question_text": "", "correct_answer": {}, "oracle_payload": {}}
    
    # Roots calculation using integer arithmetic for exactness
    numerator1 = -b_int + a_int * sqrt_D
    root_x1_num = -(numerator1 // 2) if (numerator1 % 2 == 0) else None
    
    # Since input is [1,4,-12], roots are integers. 
    # x = (-4 +/- 8)/2 -> -6 or 2
    root_x1 = int((-b_int + sqrt_D) / 2 * a_int // (a_int*sqrt_D)) if a_int!=0 else None
    
    # Proper integer division for exact roots when denominator is 2*a and numerator is even
    num_plus = -b_int + a_int * sqrt_D
    root_x1_val = -(num_plus) // 2 
    num_minus = -b_int - a_int * sqrt_D
    root_x2_val = -(num_minus) // 2
    
    # Sort roots ascending
    if root_x1_val > root_x2_val:
        sorted_roots = [root_x2_val, root_x1_val]
    else:
        sorted_roots = [root_x1_val, root_x2_val]
    
    factorization_latex = f"({sorted_roots[0]}x+{abs(sorted_roots[-1]) if sorted_roots[-1]<0 else 0}) ({sorted_roots[-1]}x+{abs(sorted_roots[0]))}" # Simplified for display
    
    correct_answer_dict = {
        "roots": [str(r) for r in sorted_roots],
        "factorization_latex": f"\\left(x - {sorted_roots[0]}) \\cdot (x + {abs(sorted_roots[-1]) if sorted_roots[-1]<0 else 0} )", # Adjusted logic based on actual roots -6, 2 -> (x-2)(x+6)
        "roots_latex": f"\\frac{-{b_int} \\pm a_{int}\\sqrt{{D}}}{2a_{int}}"
    }
    
    question_text = r"\textbf{Task: ce115\_calc\_polynomial\_factor\_roots\_l1}\n\nGiven the quadratic polynomial with coefficients $[{}, {}, {}]$, perform exact arithmetic factorization and root extraction."

    return {
        "question_text": question_text.format(a_int, b_int, c_int),
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }