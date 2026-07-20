def generate(level=1, **kwargs):
    import math
    
    polynomials = [[39, 5, -14]]
    
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a = 2 * (math.sqrt(39**2 + (-1)*(-1)) // math.gcd(39, -1) if False else 0) # Placeholder logic to ensure integer solution exists based on context of typical polynomial factorization problems where roots are integers.
    
    actual_a = None
    
    for root in range(-50, 51):
        x_val = root
        y_val = quadratic_coefficients[2] + (quadratic_coefficients[1]*x_val) + (quadratic_coefficients[0]*(x_val**2)) # Value of polynomial at root? No.
        
    # Correct derivation for integer factorization: ax^2+bx+c=0 has rational roots if discriminant is square.
    a_temp, b_temp, c_temp = quadratic_coefficients
    
    delta = b_temp*b_temp - 4*a_temp*c_temp
    
    import math as m
    root_delta = m.sqrt(delta)
    
    x1 = (-b_temp + root_delta)/(2*a_temp)
    x2 = (-b_temp - root_delta)/(2*a_temp)
    
    # Assume integer roots for the challenge context usually implied by "integer a" in such specs.
    if not (x1.is_integer() and x2.is_integer()):
        # Fallback or specific case handling based on frozen params provided: 39, 5, -14
        # Roots of 39x^2 + 5x - 14 = 0
        # Delta = 25 - 4*39*(-14) = 25 + 1764 = 1789 (Not a perfect square? Let's recheck the problem type).
        # Perhaps it asks for factorization into linear terms over rationals or integers.
        # If factors are (x-r), then r is root.
        # Maybe coefficients represent something else? 
        # Re-reading spec: "factor_order_policy": "strict_source_template", first factor fixed as (3x+a).
        # This implies the polynomial P(x) = (3x + a)(bx + c).
        # Expanding: 3b x^2 + (3c+ab)x + ac.
        # Given coefficients [39, 5, -14]: 
        # 3b = 39 => b=13.
        # ac = -14.
        # 3c + ab = 5 => 3c + 13a = 5.
        
        a_val_candidates = []
        for c in range(-20, 21):
            if abs(c) > 0 and (-14/c).is_integer():
                actual_a_cand = -14 // c
                if (3*c + 13*actual_a_cand == 5):
                    a_val_candidates.append(actual_a_cand)
        
        # There might be multiple solutions, pick the first valid integer 'a' that fits.
        # Try to find unique or specific one? Usually such problems have a unique intended solution within range.
        if not a_val_candidates:
            raise ValueError("No integer factorization found")
            
        selected_a = a_val_candidates[0]
        
    correct_answer_int = selected_a + 2 * quadratic_coefficients[1] # Wait, spec says "a+2c". Which c? The constant term of the second factor.
    
    # Let's re-solve carefully:
    # Factors: (3x+a)(bx+c)
    # Coeffs: [A, B, C] = [39, 5, -14]
    # A = 3b => b = 13
    # C = ac => c * a = -14
    # B = 3c + ab = 3c + 13a
    
    solutions = []
    for div in [-20, -14, -7, -6, -5, -2, -1, 1, 2, 5, 6, 7, 14, 20]: # Divisors of -14 roughly
        if abs(div) == 0: continue
        c_val = div
        a_val = (-14 // c_val)
        
        check_mid = (3 * c_val + 13 * a_val)
        if check_mid == 5:
            solutions.append((a_val, c_val))
            
    # Pick the first solution found. In many such CTF challenges, there's often one specific 'a' intended or they are symmetric.
    # If multiple exist, usually the positive one or smallest magnitude is chosen unless specified. 
    # However, spec says "correct_answer must be the integer a+2c". Note: it doesn't specify which c if factors swapped? 
    # Spec also says "Do not redefine parameters after swapping factors." and "first factor is fixed as (3x+a)".
    # This implies we don't swap. The order is determined by solving for b=13 first.
    
    final_a = solutions[0][0] if len(solutions) > 0 else None
    c_final = solutions[0][1]
    
    oracle_payload = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }
    
    question_text = r"""Let $P(x) = 39x^2 + 5x - 14$. 
The polynomial factors as $(3x+a)(bx+c)$ where $a,b,c$ are integers. 
Given that the first factor is fixed as $(3x+a)$, find the value of $K = a+2c$.
"""
    
    return {
        "question_text": question_text,
        "correct_answer": int(final_a + 2 * c_final), # Note: The spec says "a+2c". Is it possible they mean something else? 
                                                # Usually in these problems 'c' is the constant term of the second factor.
                                                # But wait, if factors are (3x+a)(13x+c), then ac = -14 and 3c + 13a = 5.
                                                # Let's re-verify calculation with actual solutions found:
        "oracle_payload": oracle_payload
    }

# Debugging the math manually to ensure correct_answer is deterministic without runtime prints if possible, 
# but generate() returns the dict. The logic inside must be sound.
# Solving 3c + 13a = 5 and ac = -14:
# Pairs (a,c) for product -14: (-1,-14), (-2,-7), (-7,-2), (-14,-1), etc.
# Check sum: 
# a=-1, c=14 -> 3*14 + 13*(-1) = 42-13 != 5
# a=-2, c=7 -> 3*7 + 13*(-2) = 21 - 26 = -5 (Close!)
# a=-7, c=2 -> 3*2 + 13*(-7) = 6 - 91 != 5
# a=2, c=-7 -> 3*(-7) + 13*(2) = -21 + 26 = 5. **MATCH**
# So a=2, c=-7 is the solution.
# Correct answer formula: a+2c = 2 + 2(-7) = 2 - 14 = -12.

    # Final check of generated values logic within function scope to ensure no external state dependency issues for this single run.