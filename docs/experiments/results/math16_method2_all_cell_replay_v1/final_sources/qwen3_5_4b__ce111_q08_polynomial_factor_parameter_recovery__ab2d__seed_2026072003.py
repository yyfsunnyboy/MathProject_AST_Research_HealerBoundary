import math
from fractions import Fraction as F
from typing import Dict, Any, List

# Frozen sampled parameters (must be preserved exactly)
frozen_params = {
    "factor_order_policy": "strict_source_template",
    "quadratic_coefficients": [39, 5, -14],
    "template_left_x_coefficient": 3
}

def generate(level=1, **kwargs):
    # Extract frozen parameters (do not redefine)
    factor_order_policy = frozen_params["factor_order_policy"]
    quadratic_coeffs = frozen_params["quadratic_coefficients"]
    template_left_x_coef = frozen_params["template_left_x_coefficient"]
    
    if level != 1:
        raise ValueError("Level must be 1 for this task")

    # Reconstruct polynomial from coefficients [a, b, c] -> ax^2 + bx + c
    a_quad, b_quad, c_quad = quadratic_coeffs
    
    # Factor form: (3x + A)(Bx + C) where B=1 based on standard monic assumption for the second factor if not specified otherwise in strict template usually implies one is linear with leading 1 or derived. 
    # Given "strict_source_template" and first factor fixed as (3x+a), we assume form:
    # P(x) = (3x + a)(bx + c). Expanding: 3b x^2 + (3c + ab)x + ac.
    # We have coefficients [a_quad, b_quad, c_quad]. So:
    # 1) 3*b = a_quad => b = a_quad / 3
    # 2) 3*c + a*b = b_quad
    # 3) a*c = c_quad
    
    # Calculate 'b' for the second factor (must be integer or rational, let's solve exactly)
    # From eq 1: b = 39 / 3 = 13. So second factor is (x + C). Wait, if B=1? 
    # Let's check consistency with a*c = c_quad (-14).
    
    # Solve for 'a' and 'c':
    # We know P(x) = 39x^2 + 5x - 14.
    # Factors: (3x+a)(bx+c) = 3b x^2 + (3c+ab)x + ac.
    # If we assume the second factor is monic (leading coeff 1), then b=1? 
    # Then 3*1 = 39 -> False. So it's not monic in that sense unless 'a_quad' was different.
    # Let's re-read: "first factor is fixed as (3x+a)". This implies the leading term of first factor is 3x.
    # The product must have leading coefficient a_quad = 39. 
    # So if P(x) = (3x + A)(B x + C), then 3*B = 39 => B = 13.
    # Then the factors are (3x+A) and (13x+C).
    
    # System of equations:
    # 1) a_quad * b_coeff = 39 -> 3 * b_coeff = 39 -> b_coeff = 13
    # 2) template_left_x_coef * c_const + A * b_coeff = b_quad -> 3*C + A*13 = 5
    # 3) A * C = c_quad -> A * C = -14
    
    # We need integer solutions for A and C.
    # Factors of -14: (1, -14), (-1, 14), (2, -7), (-2, 7).
    
    candidates_A_C = [
        (1, -14),
        (-1, 14),
        (2, -7),
        (-2, 7)
    ]
    
    found_solution = False
    for A_val, C_val in candidates_A_C:
        # Check eq 2: 3*C + A*13 == 5?
        lhs = 3 * C_val + (A_val * 13)
        if lhs == b_quad:
            found_solution = True
            break
    
    if not found_solution:
        raise RuntimeError("No integer solution found for factorization")

    # We have A and C. 
    # The question asks for correct_answer as "integer a+2c". Note the variable naming in prompt vs code.
    # Prompt says: first factor is (3x+a). So 'a' here corresponds to our calculated A_val.
    # And 'c' usually refers to constant term of second factor? Or maybe c from quadratic coeffs?
    # "correct_answer must be the integer a+2c". 
    # In context of polynomial factors (mx+n)(px+q), often parameters are n and q.
    # Let's assume: first factor is (3x + A_val). Second factor is (13x + C_val).
    # The prompt asks for "a" from the template (3x+a) -> this is our A_val.
    # And "c". In standard notation ax^2+bx+c, c is -14. But that would make a+2c = 1-28 = -27 or similar. 
    # However, usually in factor recovery tasks involving (mx+a)(nx+b), the parameters to recover are the constants of the factors.
    # Let's look at the structure: "correct_answer must be the integer a+2c".
    # If 'a' is from (3x+A) and 'c' is likely the constant term of the second factor (let's call it C_val), then answer = A + 2*C.
    # Let's verify with our found solution: 
    # Case 1: A=1, C=-14 -> Ans = 1 + 2*(-14) = -27. Check eq2: 3(-14)+1(13)= -42+13 != 5. Invalid.
    # Case 2: A=-1, C=14 -> Ans = -1 + 28 = 27. Check eq2: 3(14)+(-1)(13) = 42-13 = 29 != 5. Invalid.
    # Case 3: A=2, C=-7 -> Ans = 2 + 2*(-7) = -12. Check eq2: 3(-7)+2(13)= -21+26 = 5. Valid!
    # Case 4: A=-2, C=7 -> Ans = -2 + 14 = 12. Check eq2: 3(7)+(-2)(13) = 21-26 = -5 != 5. Invalid.
    
    # So the solution is A_val = 2, C_val = -7.
    # The "a" in (3x+a) is 2.
    # The "c" likely refers to the constant term of the second factor which is -7? Or maybe c from quadratic coeffs (-14)? 
    # If it meant quadratic 'c', answer would be 2 + 2*(-14) = -26. But usually these tasks ask for parameters derived from factors.
    # Given "a+2c", and we found A=2, C=-7 works perfectly with the polynomial structure (3x+A)(Bx+C), it is highly probable 'c' refers to the constant term of the second factor (-7). 
    # Let's assume c = -7.
    
    a_val = 2
    c_val = -7
    
    correct_answer_int = a_val + 2 * c_val

    # Generate LaTeX question text using formal delimiters $...$ or \(...\)
    # Construct the polynomial string: 39x^2+5x-14
    latex_poly = r"39x^{2}+5x-14"
    
    question_text = f"Solve for the integer parameters in the factorization of $latex\_poly$ given that one factor is fixed as $(3x+a)$."

    # Construct oracle_payload exactly matching frozen_params
    oracle_payload = dict(frozen_params)

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": oracle_payload
    }