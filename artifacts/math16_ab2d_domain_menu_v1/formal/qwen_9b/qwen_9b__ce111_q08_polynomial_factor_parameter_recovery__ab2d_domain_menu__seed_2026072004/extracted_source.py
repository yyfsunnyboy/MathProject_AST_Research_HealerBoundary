def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # The task asks to solve for a+2c given the factorization (3x+a)(bx+c) = 39x^2 + 5x - 14.
    # We expand (3x+a)(bx+c) -> 3b x^2 + (3c+ab)x + ac.
    # Comparing coefficients:
    # 3b = 39 => b = 13.
    # ac = -14.
    # 3c + ab = 5 => 3c + a*13 = 5.
    
    # We need to find integer pairs (a, c) such that:
    # 1. a * c = -14
    # 2. 3*c + 13*a = 5
    
    # Factors of -14: (-1, 14), (1, -14), (-2, 7), (2, -7), (-7, 2), (7, -2), ...
    
    possible_pairs = []
    for a in range(-100, 100): # Search space sufficient for factors of small numbers
        if a == 0: continue
        c = -14 // a
        if a * c != -14: continue
        
        # Check linear equation constraint
        lhs_linear = 3*c + 13*a
        if lhs_linear == 5:
            possible_pairs.append((a, c))

    # According to the contract "factor_order_policy=strict_source_template; first factor fixed as (3x+a)", 
    # we assume there is a unique solution or we pick the one consistent with standard ordering.
    # Let's verify which pair works:
    # If a = -7, c = 2 -> 3(2) + 13(-7) = 6 - 91 != 5
    # If a = 7, c = -2 -> 3(-2) + 13(7) = -6 + 91 = 85 != 5
    # Wait, let me re-solve manually to ensure logic.
    # b=13 is fixed by leading term 3x * bx = 3bx^2 = 39x^2 -> b=13.
    # ac = -14.
    # 3c + ab = 5 => 3c + 13a = 5.
    
    # Try a=-7, c=2: 3(2) + 13(-7) = 6 - 91 = -85 (No)
    # Try a=7, c=-2: 3(-2) + 13(7) = -6 + 91 = 85 (No)
    # Did I swap signs? 
    # Factors of -14:
    # (-1, 14): 3(14)+13(-1)=42-13=29
    # (1, -14): 3(-14)+13(1)=-42+13=-29
    # (-2, 7): 3(7)+13(-2)=21-26=-5. Close! Maybe sign error in problem interpretation? 
    # (2, -7): 3(-7)+13(2)=-21+26=5. YES.
    
    # So a = 2, c = -7 is the solution.
    # Check: (3x + 2)(13x - 7) = 39x^2 - 21x + 26x - 14 = 39x^2 + 5x - 14. Correct.
    
    a_val, c_val = possible_pairs[0] # Should be (2, -7)
    
    result_value = a_val + 2 * c_val
    
    return {
        "question_text": frozen_params["quadratic_coefficients"][-3], # Placeholder logic to avoid error if key missing? No.
        "correct_answer": result_value,
        "oracle_payload": frozen_params
    }

# Correction: The function must use the provided frozen_params directly in the return dict for oracle_payload
# and construct question_text from the description or a standard string based on coefficients.
# Since I cannot read external files, I will reconstruct the text using the coeffs to be safe, 
# but the prompt says "use as question_text" referring to the Frozen task description provided in the block.
# However, that block is markdown/text. The function needs to return a string for 'question_text'.
# Usually in these tasks, if not explicitly passed as an argument, we might need to format it or use a default.
# But looking at the "Frozen task description" section: 
# It contains LaTeX math. I should probably reconstruct this text using the coeffs from frozen_params 
# to ensure correctness without hardcoding strings that might vary by locale/encoding if not careful.
# Or, simpler: The prompt implies `frozen_params` is what we have. 
# Let's construct the question_text string dynamically based on coefficients for robustness.

def generate(level=1, **kwargs):
    frozen = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }
    
    # Re-derive solution logic inside to be self-contained and robust
    a_coeffs = frozen["quadratic_coefficients"]
    A, B, C = a_coeffs[0], a_coeffs[1], a_coeffs[2]
    
    # Equation: (template_left_x_coefficient * x + a) * (b*x + c) = Ax^2 + Bx + C
    # Let L_coef = template_left_x_coefficient
    # A = L_coef * b  => b = A / L_coef
    # C = a * c
    # B = L_coef*c + a*b
    
    if frozen["template_left_x_coefficient"] == 0:
        raise ValueError("Leading coefficient of first factor cannot be zero")

    b_val = A // frozen["template_left_x_coefficient"]
    
    # We need integer solutions for a, c such that:
    # ac = C
    # L_coef*c + a*b = B
    
    found_a = None
    found_c = None
    
    if abs(C) <= 100 and abs(B) <= 100: 
        # Iterate through divisors of C
        for i in range(1, int(abs(C)) + 2):
            if C % i == 0:
                candidates_a_pos = [i]
                candidates_c_pos = [C // i]
                
                pairs_to_check = []
                signs_combinations = [(1, 1), (1, -1), (-1, 1)] # a*c sign logic handled by values
                
                for sgn in [-1, 1]:
                    val_a = sgn * i
                    val_c = C // val_a
                    
                    pairs_to_check.append((val_a, val_c))

            if abs(C) == 0: continue
            
        # Simpler iteration over range is safer than divisor logic for small numbers
        search_range = max(1, int(abs(A)), int(abs(B))) + 5
        
        solutions = []
        for a in range(-search_range*2, search_range*2):
            if a == 0: continue
            c = C // a
            if a * c != C: continue
            
            # Check linear term
            calc_B = frozen["template_left_x_coefficient"] * c + a * b_val
            if calc_B == B:
                solutions.append((a, c))

    if not solutions:
        raise ValueError("No integer solution found for the polynomial factorization parameters.")
    
    # The problem implies a unique answer. 
    # In case of multiple (unlikely here given constraints), we take the first or specific one?
    # Usually math problems have unique answers under these constraints.
    sol_a, sol_c = solutions[0]
    
    final_answer_int = sol_a + 2 * sol_c
    
    # Construct question text from frozen data to match expected format roughly
    # Using f-string with coefficients
    q_text = (f"已知 {A}x^2+{B}x+C={frozen['template_left_x_coefficient']}x+a)(bx+c), "
              f"其中 a,b,c 均為整數，求 a+2c。") 
    # Wait, C is negative in the example. Python formatting needs care for negatives if not handled by math module or explicit check.
    # Better to use raw values directly without string interpolation of variables that might be complex?
    # Actually, just reconstructing from frozen["quadratic_coefficients"] and template_left_x_coefficient
    
    A_val = frozen["quadratic_coefficients"][0]
    B_val = frozen["quadratic_coefficients"][1]
    C_val = frozen["quadratic_coefficients"][2]
    
    # Formatting numbers: handle negative signs cleanly if needed, but simple f-string works for ints.
    q_text = (f"已知 {A_val}x^2+{B_val}x+C={frozen['template_left_x_coefficient']}x+a)(bx+c), "
              f"其中 a,b,c 均為整數，求 a+2c。") 
    # Wait, the C in the equation is -14. The string should be "-14". Python handles this automatically if I use the variable.
    # But wait, the example text had "C=" inside? No, it was specific numbers: 39x^2+5x-14=(3x+a)(bx+c).
    # My reconstruction above put 'C=' literally. That is wrong. It should be the value of C_val.
    
    q_text = (f"已知 {A_val}x^2+{B_val}x+C={C_val}={(frozen['template_left_x_coefficient'])}x+a)(bx+c), " # Still messy
    
    # Let's just build it cleanly:
    term1 = f"{A_val}x^2" if A_val != 0 else ""
    term2 = f"+{B_val}x" if B_val >= 0 else f"-{-B_val}x"
    term3 = str(C_val) # -14
    
    eq_part = (f"{term1}{term2}" + ("+"+str(abs(term3)) if C_val > 0 else "") 
                .replace("+-", "-").split("+")[0] + "x^2") # This is getting too complex for a simple string.
    
    # Simple approach: just format the numbers directly into the known structure from the prompt's example text style.
    # The prompt gave: 已知 [39]x^2+[5]x+[-14]=(3x+a)(bx+c) ...
    # Let's construct it precisely.
    
    sign_B = "+" if B_val >= 0 else "-"
    abs_B = -B_val if B_val < 0 else B_val
    
    q_text = (f"已知 {A_val}x^2{sign_B}{abs_B}x+{C_val}=" 
               f"{frozen['template_left_x_coefficient']}x+a)(bx+c), "
               f"其中 a,b,c 均為整數，求 a+2c。")

    return {
        "question_text": q_text,
        "correct_answer": final_answer_int,
        "oracle_payload": frozen
    }