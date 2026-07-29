# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    coeffs = frozen_params["quadratic_coefficients"]
    # Polynomial is: 39x^2 + 5x - 14
    
    A = coeffs[0]  # 39
    B = coeffs[1]  # 5
    C = coeffs[2]  # -14

    # We need to factor Ax^2 + Bx + C into (mx + n)(px + q) such that mp=A, mq+np=B, nq=C.
    # The template requires the first factor to be fixed as (3x + a).
    # So m = 3. Then p must be A / m = 39 / 3 = 13.
    
    left_x_coefficient = frozen_params["template_left_x_coefficient"]  # 3
    
    if A % left_x_coefficient != 0:
        raise ValueError("Template coefficient does not divide leading term.")

    p = A // left_x_coefficient
    
    # Now we have factors (left_x_coefficient * x + a) and (p * x + c).
    # Expansion: (3x + a)(13x + c) = 39x^2 + (3c + 13a)x + ac.
    # We know B = 5, C = -14.
    
    # System of equations for integers a and c:
    # 1) ac = C => ac = -14
    # 2) 3c + 13a = B => 3c + 13a = 5
    
    # From (1), possible integer pairs (a, c): divisors of -14.
    # Divisors: +/-1, +/-2, +/-7, +/-14.
    
    solutions = []
    for a in range(-abs(C) - 10, abs(C) + 10): # Broad search around zero to be safe with bounds logic if needed, though divisors are small
        if C % a == 0:
            c = C // a
            if 3 * c + 13 * a == B:
                solutions.append((a, c))

    if not solutions:
        # Fallback or error handling for unexpected cases in strict template logic
        raise ValueError("No integer solution found matching the quadratic coefficients and template.")
    
    # The problem implies a unique recovery based on "strict_source_template". 
    # Usually there is only one valid pair satisfying both conditions.
    if len(solutions) > 1:
        # In standard math problems of this type, uniqueness is guaranteed by constraints not shown here or implicit domain limits.
        # We take the first found solution which should be unique for well-formed inputs.
        a_val, c_val = solutions[0]
    else:
        raise ValueError("Ambiguous or no solution.")

    # Correct answer definition from spec: integer value of a + 2c
    correct_answer_int = a_val + 2 * c_val
    
    # Construct LaTeX question text using native string formatting (no external API calls)
    # Format: "Factor the polynomial {poly} into two linear factors. The first factor is fixed as ({left_x_coefficient}x + a). Find the value of a + 2c."
    
    poly_str = f"{A}x^2 + {B}x{'' if C >= 0 else ''}{C}" # Simple formatting, handle sign manually for clean LaTeX
    
    # Constructing proper LaTeX string with delimiters
    term1_sign = '+' if B >= 0 else '-'
    abs_B = -B if B < 0 else B
    poly_latex_str = f"{A}x^2 {term1_sign}{abs_B}x{'' if C == 0 else ''}"
    
    # Handling constant term sign for LaTeX cleanliness
    const_term_part = ""
    if C > 0:
        const_term_part += f" + {C}"
    elif C < 0:
        abs_C = -C
        const_term_part += f" - {abs_C}"
    
    poly_latex_str += const_term_part
    
    question_text = (f"Solve for the polynomial $\\left({left_x_coefficient}x + a\\right)\\left({p}x + c\\right)$ "
                     f"given that it expands to ${poly_latex_str}. Find the integer value of $a + 2c$.")

    # Oracle payload must exactly equal frozen sampled parameters
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": oracle_payload
    }