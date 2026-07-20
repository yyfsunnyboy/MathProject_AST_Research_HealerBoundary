def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    # Extract coefficients from the list: ax^2 + bx + c -> a=39, b=5, c=-14
    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]
    
    # Construct the first factor as (template_left_x_coefficient * x + A)
    left_coef = frozen_params["template_left_x_coefficient"]  # 3
    
    # The polynomial is P(x) = a*x^2 + b*x + c.
    # We are told to treat it under strict_source_template where first factor is (left_coef * x + alpha).
    # Let the factors be (m1*x + n1)(m2*x + n2).
    # m1*m2 = a => 3 * m2 = 39 => m2 = 13.
    # m1*n2 + m2*n1 = b => 3*n2 + 13*n1 = 5.
    # n1*n2 = c => n1*n2 = -14.
    
    # Substitute n2 = -14/n1 into the linear equation:
    # 3*(-14/n1) + 13*n1 = 5
    # -42/n1 + 13*n1 = 5
    # Multiply by n1: -42 + 13*n1^2 = 5*n1
    # 13*n1^2 - 5*n1 - 42 = 0
    
    import math
    
    discriminant = (-5)**2 - 4*13*(-42)
    sqrt_discriminant = int(math.isqrt(discrimant)) if discriminant >= 0 else None # Should be perfect square for integer roots usually, but let's solve carefully.
    
    n1_candidates = []
    delta = math.sqrt(discriminant)
    sol_n1_1 = (5 + delta) / (2 * 13)
    sol_n1_2 = (5 - delta) / (2 * 13)
    
    # Check for valid integer solutions or rational ones that fit the context. 
    # However, the problem asks to recover parameters and return a+2c as correct_answer.
    # It implies there is a specific 'a' in the factor expression derived from the template.
    # The prompt says: "first factor is fixed as (3x+a)". Note: here 'a' is used for the constant term of the first factor, 
    # distinct from coefficient 'a'. Let's call the constant term k1 to avoid confusion with quadratic coeff a=39.
    
    # Re-evaluating based on standard "factor recovery" tasks where integer roots are expected or specific constraints apply.
    # 13*n1^2 - 5*n1 - 42 = 0 -> n1 approx (5 +/- sqrt(25 + 2184))/26 = (5 +/- sqrt(2209))/26 = (5 +/- 47)/26.
    # Case 1: (5+47)/26 = 52/26 = 2. So n1=2. Then n2 = -14/2 = -7.
    # Check linear term: 3*(-7) + 13*(2) = -21 + 26 = 5. Correct.
    
    k1 = 2   # This is the 'a' in (3x+a) requested by "first factor fixed as (3x+a)"
    n2 = -7
    
    # The correct_answer must be the integer a+2c where 'a' here refers to the constant term of the first factor? 
    # Or does it refer to coefficient 'a'? Context: "correct_answer must be the integer a+2c".
    # Usually in these tasks, if we have (3x + k1)(mx + n), and we define the answer based on recovered parameters.
    # Let's assume the variable name 'a' in the instruction "integer a+2c" refers to the constant term of the first factor found above? 
    # Or is it strictly coefficient_a * 2 + c_coefficient? No, usually these are specific variables defined in the problem logic.
    # Given "first factor fixed as (3x+a)", let's assume 'a' in the answer formula refers to that constant term k1=2.
    # And 'c' refers to quadratic coefficient c = -14.
    # Answer = 2 + 2*(-14) = 2 - 28 = -26.
    
    recovered_a_const_term = int(sol_n1_1 if sol_n1_1 == 2 else sol_n1_2) 
    calculated_answer = recovered_a_const_term + 2 * c
    
    question_text = (f"Given the quadratic polynomial $P(x) = {a}x^2 + {b}x + {c}$, "
                    f"and knowing that one factor is of the form $(\\text{template\_left}\\_x\\_coefficient)x + \\alpha$, "
                    f"determine the value defined as $\\alpha + 2c$ based on strict source template recovery.")
    
    # Refining question text for formal LaTeX and clarity matching typical task formats:
    question_text = (f"Consider the polynomial $P(x) = {a}x^2 + {b}x + {c}$ which factors into $(\\text{template\_left}\\_x\\_coefficient)x + \\alpha$)(mx + n). "
                     f"If we enforce strict source template recovery where the first factor is fixed as $(3x+a)$, find the integer value $a+2c$.")

    return {
        "question_text": question_text.replace("\\text{template_left_x_coefficient}", str(left_coef)),
        "correct_answer": calculated_answer,
        "oracle_payload": frozen_params
    }