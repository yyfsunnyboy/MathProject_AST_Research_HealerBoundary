def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    a_list = frozen_params["quadratic_coefficients"]
    c = a_list[2]
    
    question_text = r"Given the quadratic polynomial $P(x) = (3x + a)(bx + c)$ where $b$ and $c$ are integers, determine the value of $a+2c$. Note that expanding $(3x+a)(bx+c)$ yields $39x^2 + 5x - 14$."
    
    correct_answer = None
    
    # Solve for a using the linear term coefficient: (3*b) + (b*a)? No.
    # Expansion of (3x+a)(bx+c) is 3b x^2 + (3c+ab)x + ac.
    # We have 39, 5, -14.
    # So 3b = 39 => b=13.
    # Then ac = -14. Since c=-14 from the list? Wait, quadratic_coefficients is [A, B, C] for Ax^2+Bx+C usually? 
    # The prompt says "quadratic_coefficients": [39, 5, -14]. This implies A=39, B=5, C=-14.
    # So ac = -14 and a+b*something... wait.
    # Let's re-read carefully: "first factor is fixed as (3x+a)". 
    # Expansion: 3b x^2 + (3c+ab)x + ac.
    # Given coeffs: [39, 5, -14]. So A=39, B=5, C=-14.
    # 3b = 39 -> b = 13.
    # ac = -14.
    # We need to find integer a such that there exists an integer c where ac = -14 AND the middle term matches? 
    # Wait, the frozen params say "quadratic_coefficients": [39, 5, -14]. These are usually A, B, C of Ax^2+Bx+C.
    # But in my expansion: Ac_term is ac. So c must be one factor of -14/a? 
    # Actually, the problem asks to recover parameters. The "correct_answer" is a+2c.
    # Is 'a' and 'c' uniquely determined? 
    # Factors of -14: (1, -14), (-1, 14), (2, -7), (-2, 7).
    # We also have the middle term constraint: 3c + ab = 5. With b=13 -> 3c + 13a = 5.
    # Let's test pairs for ac=-14 and 3c+13a=5.
    # If a=2, c=-7: 3(-7) + 13(2) = -21 + 26 = 5. Matches!
    # So a=2, c=-7 is the solution.
    
    correct_answer = (frozen_params["quadratic_coefficients"][0] // 3) * frozen_params["template_left_x_coefficient"] 
    # Wait, logic check: b = A/3 = 13. ac = C = -14. Middle term B = 3c + ab = 5.
    # We found a=2, c=-7 works for the system derived from coefficients [39, 5, -14].
    # So correct_answer is a+2c = 2 + 2(-7) = 2 - 14 = -12.
    
    # Let's recalculate strictly based on the frozen parameters provided in the prompt context to ensure correctness without external solving if possible, 
    # but here we must solve the system implied by [39, 5, -14].
    A, B, C = frozen_params["quadratic_coefficients"]
    
    b_val = A // 3
    
    # Solve ac = C and 3c + ab = B for integers a, c.
    # From first eq: c = C/a. Substitute into second: 3(C/a) + ab = B => 3C + a^2b = Ba? No.
    # 3*(C/a) + a*b_val = B
    # Multiply by a: 3C + a^2 * b_val = B*a
    # This is quadratic in a: (b_val)*a^2 - B*a + 3*C = 0
    import math
    
    def solve_quadratic(a_coeff, b_coeff, c_const):
        delta = b_coeff**2 - 4*a_coeff*c_const
        if delta < 0: return []
        sqrt_delta = int(math.isqrt(delta))
        if sqrt_delta * sqrt_delta != delta: return [] # Not a perfect square
        
        sol1 = (-b_coeff + sqrt_delta) / (2*a_coeff)
        sol2 = (-b_coeff - sqrt_delta) / (2*a_coeff)
        
        sols = set()
        for s in [sol1, sol2]:
            if abs(s - round(s)) < 1e-9: # Check integer
                sols.add(int(round(s)))
        return list(sols)

    candidate_as = solve_quadratic(b_val, -B, 3*C)
    
    valid_a = None
    for a in candidate_as:
        c_calc = C // a if (C % a == 0) else None # Should be integer division since ac=C and we expect integers
        # Re-verify with float to avoid div by zero or precision issues, though inputs are small ints.
        # Actually, just check the original equation: 3*c + b*a = B => c = (B - b*a)/3
        if a != 0:
            c_val = (B - b_val * a) / 3
            if abs(c_val - round(c_val)) < 1e-9 and C == int(a * c_val): # Check ac=C consistency
                valid_a = int(round(a))
                break
    
    if valid_a is not None:
        c_final = (B - b_val * valid_a) / 3
        correct_answer = valid_a + 2*c_final
        
    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer),
        "oracle_payload": oracle_payload
    }