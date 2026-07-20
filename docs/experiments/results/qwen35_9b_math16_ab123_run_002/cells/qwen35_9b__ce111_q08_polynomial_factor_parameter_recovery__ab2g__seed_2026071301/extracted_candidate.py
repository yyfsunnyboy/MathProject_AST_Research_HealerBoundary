def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    # Frozen sampled parameters from the prompt specification
    factor_order_policy = frozen_params["factor_order_policy"]
    quadratic_coefficients = frozen_params["quadratic_coefficients"]
    template_left_x_coefficient = frozen_params["template_left_x_coefficient"]

    a, b, c = quadratic_coefficients
    
    # Factor order policy: first factor is fixed as (3x+a)
    # The polynomial is 3x^2 + bx + c. 
    # Factoring form: (mx + n)(px + q). Since template_left_x_coefficient is 3 and it's a quadratic, likely one linear term has x coeff 3.
    # Standard factoring for Ax^2+Bx+C where A=3: (3x + u)(1x + v) or similar.
    # Let the factors be (template_left_x_coefficient * x + n) and (m*x + p).
    # Product = 3x^2 + bx + c.
    # Factor 1: (3x + a_val) ? Wait, 'a' in problem context usually refers to constant term of first factor if fixed as (3x+a). 
    # However, the prompt says "first factor is fixed as (3x+a)". Here 'a' is likely an unknown integer parameter.
    # But we have quadratic coefficients [A=39? No, list order matters]. Usually [coeff_x2, coeff_x1, const] or similar? 
    # Let's assume standard math notation for polynomial 3*x^2 + b*x + c given the coeffs list might be different.
    # Re-reading: "quadratic_coefficients": [39, 5, -14]. This is likely [A, B, C] or similar? 
    # But if template_left_x_coefficient is 3, then A must be divisible by something related to that. 
    # If the polynomial is P(x) = (3x + a)(mx + n), then product x^2 term is 3m.
    # The list [39, 5, -14] likely represents coefficients of a specific form or perhaps roots? 
    # Let's assume the standard task interpretation: Recover parameters for polynomial factorization.
    # Often in these datasets (like MATH), "quadratic_coefficients" might refer to the expanded form A*x^2 + B*x + C.
    # If so, 3x^2... wait, if coeffs are [39, 5, -14], maybe it's not monic or scaled? 
    # Or perhaps the list is [a, b] for ax^2+bx+c where a=3? No, length is 3.
    # Let's assume the polynomial is A*x**2 + B*x + C = (mx+n)(px+q).
    # If template_left_x_coefficient is 3, then one factor starts with 3x.
    # Then P(x) = (3x + n)(1x + q) -> x^2 coeff is 3. But our list has 39? 
    # Maybe the coefficients are scaled or I am misinterpreting [39, 5, -14].
    # Alternative: The polynomial is defined by these specific numbers regardless of 'template_left_x_coefficient' logic for generation, but we must use them.
    # Let's assume the quadratic is P(x) = (x + a)(3x + b)? No, template says first factor fixed as (3x+a). 
    # So Factor1 = 3*x + param_a. Factor2 = m*x + param_b.
    # Product x^2 coeff = 3*m. If the given quadratic coeffs imply a specific polynomial, we must match it.
    # Hypothesis: The "quadratic_coefficients" list is [A, B, C] for A*x**2+B*x+C. 
    # Here [39, 5, -14]. So P(x) = 39x^2 + 5x - 14?
    # If Factor1 starts with 3x, then m must be such that 3*m = 39 => m=13.
    # Then (3x + n)(13x + q). 
    # We need to find integer roots/n factors for 39x^2+5x-14? Discriminant = 25 - 4*39*(-14) = 25 + 2184 = 2209. sqrt(2209)=47.
    # Roots: (-5 +/- 47)/ (2*39). 
    # x1 = 42/78 = 7/13. x2 = -52/78 = -2/3.
    # Factors would be proportional to (x - 7/13) and (x + 2/3).
    # Clearing denominators: (13x - 7)(3x + 4)? 
    # Check product: 13*3 x^2 = 39. Constant -7*4 = -28 != -14. Scale needed?
    # Wait, roots calculation check: sum of roots = -5/39. Product = -14/39.
    # (x - r1)(x - r2) scaled by 39. 
    # Factors could be (13x + something)(3x + something).
    # Let's try to fit integers n, q such that (3x+n)(13x+q) = 39x^2 + (3q+13n)x + nq.
    # We need 3q+13n = 5 and nq = -14.
    # Pairs for -14: (-1, 14), (1, -14), etc.
    # Try n=2, q=-7 -> 3(-7)+13(2) = -21+26 = 5. Matches! 
    # So factors are (3x + 2)(13x - 7). Constant is 2*-7 = -14. Correct.
    # Here 'a' in "first factor fixed as (3x+a)" corresponds to n=2.
    # The correct_answer must be a+2c? Wait, spec says: "correct_answer must be the integer a+2c". 
    # What is c here? In quadratic Ax^2+Bx+C, C=-14. So c = -14? Or maybe 'a' and 'b' from prompt text map differently?
    # Usually in math problems of this type (recovery), parameters are the constants in factors.
    # If factor is (3x+a) and other is (mx+b). 
    # Spec says "correct_answer must be the integer a+2c". This implies 'a' and 'c' are specific variables defined by the task context not fully explicit here, but likely:
    # a = constant term of first factor. c = ? Maybe coefficient from second factor? Or C/constant term of polynomial? 
    # Given "quadratic_coefficients": [39, 5, -14], let's assume standard mapping A=39, B=5, C=-14.
    # But formula a+2c is weird if c=C. Let's re-read carefully: "correct_answer must be the integer a+2c". 
    # Maybe 'a' and 'b' are from (ax+b)? No, first factor fixed as (3x+a). So constant is 'a'.
    # Perhaps the second factor is defined such that its constant is related to c? Or maybe 'c' refers to C/constant of poly? 
    # Let's assume a standard hidden variable convention where we calculate based on derived values.
    # However, without explicit definition of 'c', I must infer from "a+2c". If it's not C (polynomial constant), what is c?
    # Maybe the polynomial was generated as (3x+a)(cx+d)? Then x^2 coeff 3c = A => c=A/3. 
    # In our case, A=39, so c=13. 
    # Let's test this hypothesis: Factor form (3x+a)(cx+b).
    # Our derived factors were (3x+2) and (13x-7). Here 3*13 = 39 matches A. So second x-coeff is 13. This fits c=13 perfectly!
    # And the constant term of second factor is -7. 
    # Is "c" in the answer formula a+2c referring to this 'c' (the coefficient of x in the second factor)? Or C?
    # If it refers to the variable name used for that parameter, then c=13. 
    # Then correct_answer = a + 2*c_param? a=2, c_param=13 => 2+26=28.
    # OR does "c" refer to C (constant term of polynomial)? If so, -14 is not an integer in the sense of positive usually but it says "integer". 
    # But if 'c' is a variable name for the coefficient in the second factor (which we called c above), then calculation holds.
    # Let's assume the task implies generating parameters where:
    # Factor 1: 3x + a
    # Factor 2: cx + b (where c = A/3)
    # Then correct_answer = a + 2*c_coefficient_of_second_factor? 
    # Wait, usually 'c' in ax^2+bx+c is the constant term. But here we have specific variable names "a" and "b"? No.
    # Let's stick to the most robust interpretation: The frozen params give us the polynomial coefficients directly [39, 5, -14]. 
    # We factor it into (3x+a)(cx+b). 
    # A=39 -> c = 39/3 = 13.
    # B=5 -> 3b + ac = 5 => 3(-7) + a(13) ? Wait, in our solution n=2, q=-7 (using previous notation). 
    # So factor is (3x+2)(13x-7). Here 'a'=2. The coefficient of x in second factor is 13. Let's call this c_coeff = 13.
    # If the formula asks for a + 2*c, and c refers to that linear coefficient: 2 + 2*13 = 28.
    # If c refers to polynomial constant C=-14: 2 + 2*(-14) = -26. 
    # Which is more likely? "a+2c" often appears in specific challenge templates where 'c' is a parameter of the second factor or similar. 
    # Given "quadratic_coefficients", maybe they are [A, B, C]. But we derived c=13 naturally from A/3.
    # Let's assume the variable name for the x-coefficient of the second factor is 'c' in the context of the answer formula.
    # However, to be safe against "Do not redefine parameters", I will use the values strictly derived from factoring [39, 5, -14] with first term 3x.
    # Resulting factors: (3*x + a) and (c*x + b). 
    # We found a=2, c=13, b=-7. 
    # Answer = a + 2*c? Or maybe the 'b' is meant to be used? No, prompt says "a+2c".
    # I will proceed with calculating based on factorization of [39, 5, -14] into (3x+a)(cx+b).
    
    A = quadratic_coefficients[0]
    B = quadratic_coefficients[1]
    C_poly = quadratic_coefficients[2]

    # Reconstruct factors: (3*x + a) * (c_x * x + b)
    c_x = A // 3
    
    # Solve for integers a, b such that:
    # 3*c_x*A? No. 
    # Expansion: 3*c_x * x^2 + (3*b + a*c_x)*x + a*b
    # Match coeffs:
    # 3*c_x = A -> c_x check passed if divisible.
    # a*b = C_poly
    # 3*b + a*c_x = B
    
    import math

    # Find factors of C_poly for 'a' and 'b'
    solutions = []
    
    # Iterate divisors of C_poly to find integer pairs (a, b) such that a*b == C_poly
    abs_C = abs(C_poly)
    limit = int(math.sqrt(abs_C)) + 1
    
    possible_a_list = []
    for i in range(-abs_C, abs_C+1):
        if i != 0 and C_poly % i == 0:
            val_b = C_poly // i
            # Check linear term condition: 3*val_b + a*c_x == B? 
            # Wait, factor order is strict. First factor (3x+a). Second (c_x x + b).
            # So we need to check if there exists an integer 'a' such that the corresponding 'b' satisfies linear term.
            
    # Let's just solve directly: a*b = C_poly AND 3*b + c_x*a = B
    # From second eq: b = (B - c_x*a) / 3
    # Substitute into first: a * ((B - c_x*a)/3) = C_poly
    # => a*(B - c_x*a) = 3*C_poly
    # => -c_x*a^2 + B*a - 3*C_poly = 0
    # Quadratic in 'a': c_x*a^2 - B*a + 3*C_poly = 0
    
    if A % 3 != 0:
        raise ValueError("Template coefficient must divide leading coefficient for integer factors.")

    ax_coeff_in_eqn = c_x
    b_lin_term = B
    const_term_in_eqn = C_poly * 3 # Because we multiplied by 3? 
    # Equation: a*(B - c_x*a) / 3 = C_poly => a*B - c_x*a^2 = 3*C_poly => c_x*a^2 - B*a + 3*C_poly = 0
    
    disc = b_lin_term**2 - 4 * ax_coeff_in_eqn * (C_poly * 3)
    
    if disc < 0:
        raise ValueError("No real solution for parameters.")
        
    sqrt_disc = int(math.isqrt(disc))
    if sqrt_disc * sqrt_disc != disc:
         # Should be perfect square for integer params usually, but let's handle float root if needed? 
         # Task implies parameter recovery from frozen sampled ints. Must have exact match.
        pass
        
    delta = math.sqrt(disc)
    
    a1 = (b_lin_term + delta) / (2 * ax_coeff_in_eqn)
    a2 = (b_lin_term - delta) / (2 * ax_coeff_in_eqn)
    
    # We expect integer solutions. Pick the one that matches our specific instance logic or just pick valid int.
    candidates_a = []
    for val in [a1, a2]:
        if abs(val - round(val)) < 1e-9:
            cand = int(round(val))
            # Verify consistency
            b_calc = (b_lin_term - ax_coeff_in_eqn * cand) / 3
            if C_poly == cand * b_calc and isinstance(b_calc, int):
                candidates_a.append(cand)
                
    # In our specific case [39,5,-14]: 
    # c_x=13. Eq: 13*a^2 - 5a + (-42) = 0? Wait C_poly=-14 -> 3*C = -42.
    # Discriminant = 25 - 4*13*(-42) = 25 + 2184 = 2209 (sqrt=47).
    # a = (5 +/- 47)/26. 
    # a1 = 52/26 = 2. b = (5 - 13*2)/3 = (5-26)/3 = -21/3 = -7. Correct.
    # a2 = -42/26 -> not int.
    
    if candidates_a:
        chosen_a = candidates_a[0]
        b_val = (b_lin_term - ax_coeff_in_eqn * chosen_a) // 3
        c_x_final = ax_coeff_in_eqn
        
        # Determine 'c' for the answer formula "a+2c". 
        # Contextual guess: 'c' refers to the coefficient of x in the second factor (which we named c_x).
        # Let's assume variable name convention where 'c' is that parameter.
        ans_val = chosen_a + 2 * c_x_final
        
    else:
         raise ValueError("Could not recover integer parameters.")

    result_dict = {
        "question_text": r"Given the quadratic polynomial $39x^2 + 5x - 14$, which factors as $(3x+a)(cx+b)$ with integers $a, b, c$. Find the value of $a+2c$.",
        "correct_answer": str(ans_val),
        "oracle_payload": frozen_params
    }

    return result_dict