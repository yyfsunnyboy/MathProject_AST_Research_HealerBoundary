# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification.
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # Extract coefficients: ax^2 + bx + c -> coeffs[0]=a, coeffs[1]=b, coeffs[2]=c
    a_quad = frozen_params["quadratic_coefficients"][0]
    b_quad = frozen_params["quadratic_coefficients"][1]
    c_quad = frozen_params["quadratic_coefficients"][2]

    # Template: (3x + A)(bx + C) where 3 is the left x coefficient.
    # Expansion: 3b*x^2 + (3C + Ab)*x + AC
    # We know: 
    #   3*b = a_quad => b = a_quad / 3
    #   A*C = c_quad
    #   3*C + A*b = b_quad
    
    left_x_coeff = frozen_params["template_left_x_coefficient"]
    
    # Calculate the coefficient of x^2 in the second factor (b)
    # Since factors are integers, a_quad must be divisible by left_x_coeff.
    if a_quad % left_x_coeff != 0:
        raise ValueError("Invalid coefficients for strict_source_template policy.")

    b = a_quad // left_x_coeff
    
    # Now we have system: 
    #   A * C = c_quad
    #   3*C + A*b = b_quad
    # Substitute C = c_quad / A into second eq:
    #   3*(c_quad/A) + A*b = b_quad
    # Multiply by A:
    #   3*c_quad + A^2 * b = b_quad * A
    #   b*A^2 - b_quad*A + 3*c_quad = 0
    
    # Solve quadratic for A: b*A^2 - b_quad*A + (3*c_quad) = 0? 
    # Wait, let's re-derive carefully.
    # Factors: (left_x_coeff * x + A) and (b * x + C)
    # Product: left_x_coeff*b*x^2 + (left_x_coeff*C + b*A)*x + A*C
    # Match with ax^2 + bx + c
    
    term1 = a_quad  # Should equal left_x_coeff * b. Check consistency.
    
    # We need to find integer roots for the quadratic equation derived from matching coefficients.
    # Equation: (left_x_coeff)*C + A*b = b_quad
    # And A*C = c_quad => C = c_quad / A
    
    # Substitute C: left_x_coeff*(c_quad/A) + A*b = b_quad
    # Multiply by A: left_x_coeff*c_quad + A^2 * b = b_quad * A
    # Rearrange: b*A^2 - b_quad*A + (left_x_coeff*c_quad) = 0
    
    B_eqn_b = b
    B_eqn_a = b_quad
    const_term = left_x_coeff * c_quad
    
    discriminant = B_eqn_a**2 - 4*B_eqn_b*const_term
    
    if discriminant < 0:
        raise ValueError("No real solution for factors.")
    
    sqrt_discriminant = int(discriminantsqrt := discriminant ** 0.5)
    # Check perfect square just in case, though math guarantees it here given valid inputs usually.
    if sqrt_discriminant * sqrt_discriminant != discriminant:
        raise ValueError("Discriminant is not a perfect square.")

    # Two possible solutions for A (the constant term of the first factor)
    sol1 = (-B_eqn_a + sqrt_discriminant) // (2*B_eqn_b) if B_eqn_b != 0 else -const_term / B_eqn_a
    sol2 = (-B_eqn_a - sqrt_discriminant) // (2*B_eqn_b) if B_eqn_b != 0 else -const_term / B_eqn_a
    
    # Determine which solution yields integer C and matches the specific template constraint.
    # The problem states "first factor is fixed as (3x+a)". This implies we must find 'a' such that 
    # when paired with some other linear term, it reconstructs the polynomial.
    # However, factoring order matters for recovery if not unique? Usually polynomials have unique factors up to unit scaling (-1).
    # Given "strict_source_template", likely one specific integer solution is intended or both are valid but we need 'a'.
    # Let's check which A produces an integer C.
    
    candidates = []
    for val in [sol1, sol2]:
        if isinstance(val, float) and not val.is_integer(): continue
        int_val = int(round(val))
        
        # Check divisibility of c_quad by this candidate to get integer C
        if const_term != 0: 
            rem = c_quad % int_val
            if rem == 0:
                candidates.append(int_val)
        else:
             # If c is 0, then one factor constant must be 0. A=0 or C=0.
             # Equation becomes left_x_coeff*C + b*A = b_quad and AC=0.
             pass

    if not candidates:
         raise ValueError("No integer solution found.")
    
    # We need to pick the 'a' for (3x+a). 
    # The problem asks for correct_answer = a+2c. Which c? The constant of the OTHER factor? Or is it ambiguous?
    # "correct_answer must be the integer a+2c". Usually in these tasks, if factors are F1=(mx+n) and F2=(px+q), 
    # there might be an ordering convention or specific mapping. 
    # Let's assume standard recovery: find A such that (3x+A)(bx+C) = poly.
    # Then we have two pairs {(A, C)} if discriminant allows non-unique factorization over integers? No, unique up to sign swap of both factors (-1*-1).
    # But here coefficients are fixed positive/negative specific values. 
    # Let's just pick the valid A that makes sense with the context or return one consistent answer.
    # Given "Do not redefine parameters after swapping factors", implies uniqueness is expected in this instance setup.
    
    selected_a = candidates[0] if len(candidates) == 1 else (candidates[0]) 
    # If multiple exist, usually only one fits the 'strict_source_template' logic which might imply specific ordering or sign conventions not fully detailed but implied by unique solution existence in test cases.
    # Let's compute C for selected_a to ensure it works.
    
    if const_term != 0:
        c = c_quad // selected_a
    else:
        # If AC=0, then either A=0 or C=0. 
        # From linear eq: left_x_coeff*C + b*A = b_quad
        # If A=0 -> left_x_coeff*C = b_quad => C = b_quad/left_x_coeff (must be int)
        if selected_a == 0:
            c = b_quad // left_x_coeff
        else:
             # Then C must be 0? 
             pass
    
    # Re-calculate strictly to avoid float issues in logic above.
    # Solve Diophantine directly or use the quadratic formula result which should yield integers.
    
    valid_a_list = []
    for val in [sol1, sol2]:
        if isinstance(val, int):
            A_test = val
            C_test = c_quad // A_test if A_test != 0 else (b_quad - left_x_coeff*0) # If A=0, term is b_quad/left_x_coeff? No.
            
            if A_test == 0:
                if const_term == 0 and b_quad % left_x_coeff == 0:
                    C_test = b_quad // left_x_coeff
                    valid_a_list.append(A_test) # (3x+0)(bx+C) -> 3b x^2 + 3C x. Matches? 
            else:
                if c_quad % A_test == 0:
                     C_test = c_quad // A_test
                     # Verify linear term
                     check_linear = left_x_coeff * C_test + b * A_test
                     if check_linear == b_quad:
                         valid_a_list.append(A_test)

    if not valid_a_list:
        raise ValueError("No integer factorization found.")
        
    a_val = valid_a_list[0] # Pick the first valid one. In strict template, usually unique or specific sign chosen.
    
    # Calculate C corresponding to this A
    c_val = 0
    if const_term != 0:
        c_val = c_quad // a_val
    else:
         # Handle AC=0 case specifically if needed by logic above, but let's re-eval linear eq for safety.
         # If we found valid_a_list via check_linear == b_quad, then C is implicitly defined and integer.
         pass

    # Recalculate c_val safely using the verified pair from valid_a_list[0]
    if a_val != 0:
        c_val = c_quad // a_val
    else:
        # If A=0 was in list (unlikely for generic quadratic unless constant term is 0)
         # Check linear eq again to find C.
         pass

    # Actually, simpler approach since we verified validity:
    if const_term != 0 and a_val != 0:
        c_val = c_quad // a_val
    elif const_term == 0:
        # AC=0 implies one is zero. 
        # If A=a_val (which might be 0), then C must satisfy linear eq.
        if a_val == 0:
            c_val = b_quad // left_x_coeff
        else:
             # Then C must be 0? Check consistency.
             pass

    # Final check on answer formula: "a+2c". 
    # Is 'c' the constant of the second factor (bx+c)? Yes, standard notation F1=(mx+a), F2=(nx+c).
    
    correct_answer = a_val + 2 * c_val
    
    # Construct question text using native string formatting or simple latex construction without external libs.
    # Format: Factorize {poly} into factors of form (3x+{a}) and ({b}x+{c}). Find integer value of a+2c.
    
    poly_str = f"{a_quad}x^2 + {b_quad}x + {c_quad}"
    factor1_str = f"({left_x_coeff}x + {a_val})"
    # For the second factor, coefficient b is calculated as left_x_coeff * x term coeff? 
    # Wait, expansion was: (3x+A)(bx+C). The 'b' in my derivation above corresponds to the x-coeff of 2nd factor.
    # Let's call it B_factor = a_quad // left_x_coeff.
    
    b_factor_val = a_quad // left_x_coeff
    
    if c_val != 0:
        factor2_str = f"({b_factor_val}x + {c_val})"
    else:
        factor2_str = f"({b_factor_val}x)"

    question_text = (f"Given the polynomial $P(x) = {poly_str}$, it can be factored as "
                     f"$P(x) = ({left_x_coeff}x + a)(B x + c)$ where $a$ and $c$ are integers. "
                     f"Determine the integer value of $a + 2c$.")

    # Replace B with actual calculated b_factor_val in text for clarity if needed, but prompt asks to recover parameters.
    # Better: show full factors? 
    question_text = (f"Given the polynomial $P(x) = {poly_str}$, it can be factored as "
                     f"$({left_x_coeff}x + a)(B x + c)$ where $a$ and $c$ are integers. "
                     f"Determine the integer value of $a + 2c$.")

    # Wait, I should probably output the specific B found to make it self-contained or just leave as variable? 
    # The task says "recover parameters". Usually implies finding a and c given the structure.
    # Let's refine question_text to be precise about what is known vs unknown if possible, but standard format usually gives full poly.
    
    return {
        "question_text": f"Given the polynomial $P(x) = {poly_str}$, it can be factored as $(3x + a)(B x + c)$ where $a$ and $c$ are integers. Determine the integer value of $a + 2c$. Note that one factor is fixed starting with $3x$.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }