# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]
    
    # Compute discriminant using native Python arithmetic
    delta = (b ** 2) - (4 * a * c)
    
    # Since coefficients are integers and delta is perfect square for this specific case:
    sqrt_delta = int(delta ** 0.5) if delta >= 0 else None
    
    # Compute roots using quadratic formula: (-b +/- sqrt(delta)) / (2*a)
    root1_num = -b + sqrt_delta
    root2_num = -b - sqrt_delta
    
    # Determine ascending order of roots
    if root1_num < root2_num:
        sorted_roots_tuple = (root1_num, root2_num)
    else:
        sorted_roots_tuple = (root2_num, root1_num)
    
    r1, r2 = sorted_roots_tuple
    
    # Construct factorization LaTeX string manually without external libraries
    # Factor form: a(x - r1)(x - r2) -> 1*(x - (-3))*(x - 4) -> (x + 3)(x - 4)
    term1_str = f"x {r1:+d}" if r1 != 0 else "x" # Handle sign correctly for LaTeX
    term2_str = f"x {r2:+d}" if r2 != 0 else "x"
    
    # Adjust signs for standard polynomial factorization notation (x - root)
    # If root is negative, it becomes +abs(root). If positive, -(root).
    sign1 = "+" if r1 < 0 else "-"
    val1 = abs(r1) if r1 != 0 else ""
    
    sign2 = "+" if r2 < 0 else "-"
    val2 = abs(r2) if r2 != 0 else ""
    
    factorization_latex_str = f"(x {sign1} {val1})(x {sign2} {val2})"
    
    # Construct roots LaTeX list: \\{r_1, r_2\\} with proper formatting for integers/rationals
    root1_tex = rf"\frac{{{root1_num}}}{{2*{a}}}}" if a != 0 else str(root1_num)
    root2_tex = rf"\frac{{{root2_num}}}{{2*{a}}}}" if a != 0 else str(root2_num)
    
    # Simplify fractions for LaTeX display (since we know exact integer roots here, simplify manually or use raw fraction)
    # For x^2 + 4x - 12 = 0, roots are integers: -6 and 2. 
    # Let's ensure the latex reflects simplified forms if they are integers.
    
    def format_root_latex(numerator):
        denom = 2 * a
        if numerator % denom == 0:
            val = numerator // denom
            return rf"\left( {val} \right)"
        else:
            # Use fraction notation for non-integers (though not expected here with these specific params)
            return rf"\frac{{{numerator}}}{{2*{a}}}"

    root1_latex_str = format_root_latex(root1_num)
    root2_latex_str = format_root_latex(root2_num)
    
    roots_latex_list_str = f"\\left( {root1_latex_str}, {root2_latex_str} \\right)"
    
    # Construct question text with formal LaTeX delimiters
    question_text = rf"The quadratic equation $x^2 + 4x - 12 = 0$ can be factored into $(x{sign1}{val1})(x{sign2}{val2})$. Find the roots of this polynomial."

    correct_answer_dict = {
        "roots": sorted_roots_tuple, # Tuple of integers/rationals in ascending order
        "factorization_latex": factorization_latex_str,
        "roots_latex": roots_latex_list_str
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }