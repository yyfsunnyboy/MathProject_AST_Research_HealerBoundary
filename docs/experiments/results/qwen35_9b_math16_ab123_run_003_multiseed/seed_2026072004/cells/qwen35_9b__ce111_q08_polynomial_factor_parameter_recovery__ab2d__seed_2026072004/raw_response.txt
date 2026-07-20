from fractions import Fraction
import random

# Domain APIs (simulated as they are external imports in a real environment)
def mul(c1, c2):
    # Polynomial multiplication simulation returning list of coefficients [highest degree first]
    deg = len(c1) + len(c2) - 2
    res = [0] * (deg + 1)
    for i, v1 in enumerate(reversed(c1)):
        for j, v2 in enumerate(reversed(c2)):
            res[i+j+1] += v1 * v2
    return list(map(int, reversed(res)))

def create(value):
    # Fraction wrapper simulation; we use standard fractions but ensure exactness logic is handled by caller if needed.
    # For this specific task returning integer 'a', direct int works as valid Python object representing the answer.
    from fractions import Fraction as F
    return F(int(value))

def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }
    
    # Frozen parameters are extracted directly from kwargs or defaults if not passed (but spec says frozen sampled)
    # We must use the provided frozen_params structure exactly.
    factor_order_policy = frozen_params["factor_order_policy"]
    quad_coeffs = frozen_params["quadratic_coefficients"]  # [a, b, c] for ax^2 + bx + c -> here [39, 5, -14] implies 39x^2 + 5x - 14? 
    # Wait, standard polynomial representation usually highest degree first: a*x^2 + b*x + c.
    # So P(x) = 39x^2 + 5x - 14.
    
    template_left_x_coefficient = frozen_params["template_left_x_coefficient"] # LHS of (L*x + A)(R*x + B) -> Left is fixed as 3x + a
    
    policy = factor_order_policy
    if policy == "strict_source_template":
        left_factor_slope = template_left_x_coefficient
        
        # We need to find factors for P(x) = ax^2 + bx + c.
        # Form: (L*x + A)(R*x + B) = LR x^2 + (LB+RA)x + AB
        # Given L=3. Let R be the other slope, A and B intercepts.
        # a = 3*R => R = a/3 = 39/3 = 13. So Right factor is 13x + B.
        # c = A*B = -14.
        # b = L*B + R*A = 3*B + 13*A = 5.
        
        from fractions import Fraction as F
        
        a_quad = quad_coeffs[0]   # 39
        b_quad = quad_coeffs[1]   # 5
        c_quad = quad_coeffs[2]   # -14
        
        L_fixed = left_factor_slope # 3
        R_calc = F(a_quad) / L_fixed # 13
        
        # Solve system: A*B = C, 3B + 13A = B_linear (5)
        # From first eq: B = C/A. Substitute into second: 3(C/A) + 13A = b
        # Multiply by A: 3C + 13A^2 = b*A => 13A^2 - b*A + 3C = 0
        # Quadratic for A: 13x^2 - 5x + (3*-14) = 0 -> 13x^2 - 5x - 42 = 0
        
        disc = F(b_quad**2) - 4 * L_calc_coeff(13, R_calc_denom=1) # Wait logic check below
        # Actually solving: 13*A^2 - b*A + 3*c = 0. Here coeff of A^2 is 'R'? No.
        # Eq: L*B + R*A = b => B = (b - R*A)/L
        # Sub into AB=c: A*(b-R*A)/L = c => Ab - RA^2 = cL => -RA^2 + bA - cL = 0
        # Multiply by -1: RA^2 - bA + cL = 0.
        
        R_val = F(a_quad) / L_fixed
        C_const = c_quad * L_fixed
        
        # Equation for A (intercept of left factor): 
        # coeff_A_sq = R_val
        # coeff_A_lin = -b_quad
        # const_term = C_const
        # 13*A^2 - 5*A + (-42) = 0? No, c*L = -14 * 3 = -42. Correct.
        
        from math import sqrt
        
        a_sq_coef = R_val
        b_lin_coef = F(-b_quad)
        const_term = C_const
        
        delta = (b_lin_coef**2) - 4*a_sq_coef*const_term
        if delta < 0:
            # Should not happen for integer polynomials usually, but handle generically? 
            # Spec implies valid recovery.
            pass
            
        sqrt_delta_val = F(delta).sqrt()
        
        A_sol1 = (-b_lin_coef + sqrt_delta_val) / (2*a_sq_coef)
        A_sol2 = (-b_lin_coef - sqrt_delta_val) / (2*a_sq_coef)
        
        # Determine correct root based on integer constraints or just pick one if both valid? 
        # Usually strict template implies unique solution in context. Let's check which yields integers for B.
        candidates_A = []
        for A_cand in [A_sol1, A_sol2]:
            try:
                val_B = C_const / (L_fixed * A_cand) # Wait AB=c => B = c/A? No AB = -14. Yes B = c_quad / A_cand if L=3 handled separately? 
                # Re-derive: P(x) = (3x+A)(Rx+B).
                # 3R = a => R=a/3. Correct.
                # AB = c. So B = c/A.
                val_B = F(c_quad) / A_cand
                
                if val_B.denominator == 1:
                    candidates_A.append(A_cand)
            except ZeroDivisionError:
                continue
        
        if len(candidates_A) != 2:
             # If only one integer solution found, use it. 
             final_A = candidates_A[0] if candidates_A else F(0)
        else:
             # Ambiguity? Usually factor order fixes left as (3x+a). The 'a' in problem is the intercept of LEFT factor.
             # We need to recover specific A that satisfies strict_source_template context. 
             # Without further constraints, we assume standard ordering or just return one valid integer recovery if unique enough.
             # However, task asks for correct_answer = a+2c where 'a' here is the intercept of left factor?
             # Wait: "correct_answer must be the integer a+2c". 
             # In polynomial context (Lx+A)(Rx+B), usually parameters are coefficients.
             # If question text defines factors as (3x+a) and (?x+b), then 'a' is intercept of left factor.
             # Let's assume standard convention where we pick the one that makes sense or both if symmetric? 
             # Actually, for integer polynomials, usually only one pair yields integers unless discriminant is square of rational leading to two rationals.
             # If multiple valid A exist (e.g., 13x^2 -5x -42 = (A-7)(13A+6)? Roots: 7 and -6/13). 
             # Only A=7 gives integer B (-2). So unique integer solution.
             
             if len(candidates_A) > 0:
                 final_A = candidates_A[0]

        # Calculate correct_answer as defined in spec: "integer a+2c"
        # Here 'a' refers to the intercept of the left factor (Final A). 
        # And 'c' refers to the constant term of the polynomial? Or parameter c from frozen params?
        # Frozen param key is "quadratic_coefficients". Usually [A, B, C]. So last element is C.
        # Spec: correct_answer = integer a + 2*c. 
        # Let's interpret 'a' as Final_A and 'c' as quad_coeffs[2] (constant term).
        
        answer_val = int(final_A) + 2 * quad_coeffs[2]

    else:
        raise ValueError("Unsupported policy")

    question_text = r"Given the polynomial $P(x)$ with coefficients $\{39, 5, -14\}$ and a strict factor order where the left factor is $(3x+a)$, find the value of $a+2c$."
    
    # Correct answer must be integer. 
    correct_answer = int(answer_val)

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }