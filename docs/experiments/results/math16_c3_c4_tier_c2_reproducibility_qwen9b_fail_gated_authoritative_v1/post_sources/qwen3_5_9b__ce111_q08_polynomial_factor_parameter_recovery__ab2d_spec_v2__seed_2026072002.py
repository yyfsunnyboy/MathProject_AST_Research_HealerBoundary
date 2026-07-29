# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per strict_source_template policy.
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    # Parse coefficients: ax^2 + bx + c -> a=quadratic[0], b=quadratic[1], c=quadratic[2]
    A_quad = quadratic_coefficients[0]
    B_quad = quadratic_coefficients[1]
    C_quad = quadratic_coefficients[2]

    # Template: (3x + a)(bx + c) -> 3b x^2 + (3c + ab)x + ac
    # We know A=39, so 3*b = 39 => b = 13.
    factor_b = A_quad // template_left_x_coefficient
    
    # Now we have: (3x + a)(13x + c) -> x^2 term matches.
    # Middle term: 3c + ab = B_quad => 3c + 3*a*factor_b? No, wait.
    # Expansion of (L_x + L_a)(R_x + R_c):
    # Coeffs: 
    #   x^2: L*R = 3 * factor_b = A_quad -> factor_b is correct as calculated above.
    #   x^1: L*c + a*factor_b = B_quad => 3*c + a*factor_b? No, the first term is (template_left_x_coefficient*x + a).
    #       So it's (3x + a)(bx + c) -> coeff of x is 3c + ab. Wait, no: 
    #       (Ax+B)(Cx+D) = AC x^2 + (AD+BC)x + BD.
    #       Here first factor is fixed as (template_left_x_coefficient*x + a). Let's call it Lx+a.
    #       Second factor must be derived from the quadratic coefficients given A and B.
    
    # Re-evaluating based on standard factoring logic for this specific task type:
    # The polynomial is P(x) = 39x^2 + 5x - 14.
    # We assume factors are (3x + a)(bx + c).
    # Then b must be A_quad / template_left_x_coefficient = 39/3 = 13.
    # So second factor is (13x + c).
    # Expansion: (3x + a)(13x + c) = 39x^2 + (3c + 13a)x + ac.
    # We have: 
    #   3c + 13a = B_quad (=5)
    #   ac = C_quad (-14)
    
    # Solve for a and c integers.
    # From ac = -14, possible pairs (a,c): (1,-14), (-1,14), (2,-7), (-2,7), (7,-2), (-7,2), (14,-1), (-14,1).
    # Check 3c + 13a = 5 for these pairs.
    
    possible_a_values = []
    found_solution = False
    
    # Iterate through divisors of C_quad to find integer a and c
    abs_c_val = abs(C_quad)
    if C_quad == 0:
        pass 
    else:
        for i in range(1, int(abs_c_val**0.5)+2):
            if abs_c_val % i == 0:
                divisors = [i, -i, abs_c_val//i, -(abs_c_val//i)]
                # Check combinations (a, c) such that a*c = C_quad
                for cand_a in [-C_quad // d, C_quad // d]: 
                    pass
        
        # Simpler iteration over all integer factors of C_quad
        limit = int(abs(C_quad)**0.5) + 2
        candidates = []
        if abs(C_quad) == 1:
            candidates = [(-1, -C_quad), (1, -C_quad)] # Wait logic error here. 
            pass
            
        # Generate all integer pairs (a,c) such that a*c == C_quad
        for i in range(1, int(abs(C_quad)**0.5)+2):
             if abs(C_quad) % i == 0:
                 q = abs(C_quad)//i
                 candidates.append((i, -q))   # positive * negative
                 candidates.append((-i, q))
                 candidates.append((-i, -q))  # Wait, signs. 
                 pass
        
        # Correct generation of pairs (a,c) where a*c == C_quad:
        for i in range(1, int(abs(C_quad)**0.5)+2):
            if abs(C_quad) % i == 0:
                q = abs(C_quad)//i
                candidates.append((i, -q))   # If C is neg
                pass
        
    # Let's just brute force small integers since coefficients are usually small in these tasks.
    for a_test in range(-20, 21):
        if C_quad == 0:
            c_test = 0
        else:
            if C_quad % a_test != 0: continue
            c_test = C_quad // a_test
        
        # Check middle term condition: (template_left_x_coefficient * c) + (a * factor_b) == B_quad? 
        # Wait, expansion of (3x+a)(bx+c):
        # x^2 coeff: 3*b. We set b=13. So 3*13 = 39. Correct.
        # x term coeff: a*b + c*template_left_x_coefficient? 
        # No, expansion is (Lx+a)(Rx+c) -> L*R x^2 + (L*c + R*a)x + ac.
        # Here L=3, R=b=13.
        # So middle term = 3*c + b*a = 5.
        
        if a_test * factor_b + c_test * template_left_x_coefficient == B_quad:
            found_solution = True
            
    # If no solution in small range (unlikely for this difficulty), fallback or error? 
    # Assuming valid input always has integer solutions within reasonable bounds.
    
    # Calculate correct_answer = a + 2c using the first valid pair found.
    if not found_solution:
        raise ValueError("No integer factors found matching constraints.")

    return {
        "question_text": r"Given the polynomial $39x^2 + 5x - 14$, which can be factored as $(3x+a)(bx+c)$ with integers $a, b, c$. Find the value of $a+2c$.",
        "correct_answer": a_test + 2 * c_test,
        "oracle_payload": {
            "factor_order_policy": factor_order_policy,
            "quadratic_coefficients": quadratic_coefficients,
            "template_left_x_coefficient": template_left_x_coefficient
        }
    }