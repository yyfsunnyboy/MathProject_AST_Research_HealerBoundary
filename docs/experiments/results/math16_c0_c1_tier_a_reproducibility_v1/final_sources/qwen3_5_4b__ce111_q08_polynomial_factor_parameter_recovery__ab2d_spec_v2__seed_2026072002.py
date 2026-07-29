# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters defined directly as per task specification.
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    # Native Python arithmetic to solve for factors (3x + a)(bx + c) = 39x^2 + 5x - 14.
    # Expansion: 3b x^2 + (3c + ab)x + ac = 0
    # Equations:
    # 1) 3 * b = 39 => b = 13
    # 2) a * c = -14
    # 3) 3*c + a*b = 5
    
    # Calculate 'b' from the leading coefficient.
    b_coefficient = quadratic_coefficients[0] // template_left_x_coefficient
    
    # Iterate through integer factors of ac (-14) to find valid (a, c).
    possible_ac_values = []
    
    for a in range(-39, 40):
        if a == 0:
            continue
        
        remainder = -14 // a
        if remainder * a != -14:
            continue
            
        # Check the middle term condition: 3*c + a*b = 5
        c_value = remainder
        check_middle_term = template_left_x_coefficient * c_value + (a * b_coefficient)
        
        if check_middle_term == quadratic_coefficients[1]:
            possible_ac_values.append((a, c_value))

    # Select the first valid pair found. The problem implies a unique solution or specific order.
    # Given coefficients 39, 5, -14:
    # Factors of -14 pairs (a,c): (-2,7), (2,-7), (-7,2), (7,-2) etc.
    # Try (-2, 7): a=-2, c=7 -> 3*7 + (-2)*13 = 21 - 26 = -5 != 5
    # Try (2, -7): a=2, c=-7 -> 3*(-7) + 2*13 = -21 + 26 = 5 == 5. This is the match.
    
    if not possible_ac_values:
        raise ValueError("No valid integer factors found for the given polynomial.")

    a_value, c_value = possible_ac_values[0]
    
    # Calculate correct_answer as per spec: a + 2c
    correct_answer_int = a_value + (2 * c_value)
    correct_answer_str = str(correct_answer_int)
    
    # Construct question text using formal LaTeX delimiters.
    # We construct the polynomial string manually to avoid external API calls, 
    # ensuring compliance with "Do not use domain APIs".
    coeffs = quadratic_coefficients
    
    if len(coeffs) == 3:
        x2_term = f"{coeffs[0]}x^2"
        x1_term = "+" + str(abs(coeffs[1])) + "x" if coeffs[1] > 0 else "-" + str(abs(coeffs[1])) + "x"
        const_term = str(coeffs[2])
        
        # Handle sign for the whole expression cleanly
        signs = []
        if coeffs[0] < 0:
            signs.append("-")
            x2_coeff = abs(coeffs[0])
        else:
            signs.append("+")
            x2_coeff = coeffs[0]
            
        middle_sign = "+" if coeffs[1] > 0 else "-"
        
        latex_parts = [f"{x2_coeff}x^2"]
        if len(signs) == 1 and signs[0] != "+": # Start with minus? No, standard form usually starts positive or handles sign.
            pass
            
        # Simpler construction:
        term_strs = []
        
        # x^2 term
        t1 = f"{coeffs[0]}x^{len(coeffs)-1}" if len(coeffs) > 1 else str(coeffs[0])
        term_strs.append(t1)
        
        # x term
        sign_x = "+" if coeffs[1] >= 0 else "-"
        val_x = abs(coeffs[1])
        t2 = f"{sign_x}{val_x}x"
        term_strs.append(t2)
        
        # constant term
        const_sign = ""
        c_val = str(abs(coeffs[2])) if coeffs[2] < 0 else str(coeffs[2])
        sign_char = "-" if coeffs[2] < 0 else "+"
        t3 = f"{sign_char}{c_val}"
        term_strs.append(t3)
        
        question_latex = r"\text{" + " ".join(term_strs) + r"}"

    # Ensure the latex string is properly formatted for math16 context.
    # Using standard LaTeX delimiters as requested: $...$ or \text{...} inside a sentence.
    # The prompt asks for formal LaTeX delimiters in question_text.
    
    final_question = f"Solve for integer parameters given polynomial factorization constraints." + " " + r"$" + term_strs[0] + "+" + term_strs[1] + "=" + str(coeffs[2]) + "$$"

    # Prepare oracle_payload exactly as frozen sampled parameters dict.
    oracle_payload_dict = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }

    return {
        "question_text": final_question,
        "correct_answer": correct_answer_str,
        "oracle_payload": oracle_payload_dict
    }