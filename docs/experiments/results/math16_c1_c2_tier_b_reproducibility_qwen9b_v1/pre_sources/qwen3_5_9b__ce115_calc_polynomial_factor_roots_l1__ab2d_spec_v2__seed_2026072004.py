# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Coefficients for ax^2 + bx + c = 0
    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]
    
    # Calculate discriminant: D = b^2 - 4ac
    delta = (b ** 2) - (4 * a * c)
    
    # Since we know roots are integers for this specific problem, calculate them directly.
    # Roots formula: (-b +/- sqrt(D)) / (2a)
    # D = 16 - 4(1)(-12) = 16 + 48 = 64
    # sqrt(D) = 8
    
    root_diff_sq = delta
    root_diff_int = int(root_diff_sq ** 0.5)
    
    root1_num = (-b + root_diff_int)
    root2_num = (-b - root_diff_int)
    
    denom = (2 * a)
    
    # Calculate exact roots as fractions to ensure ascending order and no floats in final representation logic if needed, 
    # but the spec asks for "Exact arithmetic; no floats". We will represent them as integers since they divide evenly.
    root1_val = root1_num // denom
    root2_val = root2_num // denom
    
    # Ensure ascending order
    roots_list_asc = sorted([root1_val, root2_val])
    
    # Construct LaTeX strings manually without external libraries
    # Roots latex: x_1 and x_2 formatted nicely. Let's use simple text representation in math mode or explicit list.
    # Spec says "roots_latex". Usually implies a set like \{x_1, x_2\} or just the values. 
    # Given "ascending", let's format as comma separated within braces: {root_a, root_b}
    
    r_str = str(roots_list_asc[0]) + ", " + str(roots_list_asc[1]) if len(roots_list_asc) > 1 else str(roots_list_asc[0])
    roots_latex = f"\\{{{r_str}\\}}"
    
    # Factorization: a(x - r1)(x - r2) -> (x - root_a)(x - root_b) since a=1
    term1 = f"(x {root1_val})" if root1_val < 0 else f"(x - {roots_list_asc[0]})" # Wait, logic check: x - (-4) is x+4. 
    # Correct construction for (x - r):
    sign1 = "+" if roots_list_asc[0] < 0 else "-"
    val_str1 = str(abs(roots_list_asc[0])) if roots_list_asc[0] != 0 else ""
    
    term2 = f"(x {sign1} {val_str1})" # Handle zero case? c=-12 so no zero root.
    
    sign2 = "+" if roots_list_asc[1] < 0 else "-"
    val_str2 = str(abs(roots_list_asc[1])) if roots_list_asc[1] != 0 else ""
    
    term3 = f"(x {sign2} {val_str2})"
    
    factorization_latex = f"{term1}{term3}" # Order doesn't strictly matter for multiplication, but usually ascending inside? 
    # Let's just output the product. The order of factors is not specified as strict, but roots are sorted in answer.
    # Re-evaluating term construction:
    if roots_list_asc[0] < 0:
        factor1 = f"(x + {abs(roots_list_asc[0])})"
    else:
        factor1 = f"(x - {roots_list_asc[0]})"
        
    if roots_list_asc[1] < 0:
        factor2 = f"(x + {abs(roots_list_asc[1])})"
    else:
        factor2 = f"(x - {roots_list_asc[1]})"
        
    # Combine factors. Standard form usually lists smaller root first or just product.
    factorization_latex = f"{factor1}{factor2}"

    question_text = (f"Solve the quadratic equation $\\displaystyle \\{{{a}\\}x^{{2}} + {b}x + {c}\\} = 0$ "
                     f"by factoring and finding its roots. Express your answer as a set of integers in ascending order.")

    correct_answer = {
        "roots": roots_list_asc,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }