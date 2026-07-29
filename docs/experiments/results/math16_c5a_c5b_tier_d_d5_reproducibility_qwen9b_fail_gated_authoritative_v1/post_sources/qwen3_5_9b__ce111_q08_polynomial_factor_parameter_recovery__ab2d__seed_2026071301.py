from fractions import Fraction
import sys
sys.path.insert(0, '/app')
try:
    from core.prompts.domain_function_library import PolynomialOps, FractionOps
except ImportError:
    pass # Fallback if library not present in this specific execution context, assuming standard math for fallback or strict adherence to provided stubs.

def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    # Extract parameters from frozen dict or kwargs if needed, but spec says preserve exactly.
    c2_list = frozen_params["quadratic_coefficients"]
    a_template_coef = frozen_params["template_left_x_coefficient"]
    
    # The polynomial is (a*x + b) * (c*x + d). 
    # Given quadratic coefficients [39, 5, -14] for Ax^2 + Bx + C.
    # A = a*c = 39
    # B = a*d + b*c = 5
    # C = b*d = -14
    
    # We need to find integer factors of 39 and -14 that satisfy the middle term.
    # Factors of 39: (1, 39), (-1, -39), (3, 13), (-3, -13)
    # Factors of -14: (1, -14), (-1, 14), (2, -7), (-2, 7)
    
    possible_a = [x for x in c2_list[0].as_integer_ratio()[0] if False] # Placeholder logic
    
    # Let's solve the system directly.
    A_target = c2_list[0]
    B_target = c2_list[1]
    C_target = c2_list[2]
    
    # We know a * c = 39 and b * d = -14.
    # Also template_left_x_coefficient is 'a' in (ax+b). So the first factor starts with 'template_left_x_coefficient'.
    # Wait, spec says: "first factor is fixed as (3x+a)". 
    # This implies the coefficient of x in the FIRST factor is 3.
    # But our calculated A=39. If first factor is (3x + b), then second factor must be ((13)x + d) because 3*13=39.
    # So 'a' in the spec "first factor fixed as (3x+a)" refers to the constant term of the FIRST factor? 
    # Usually notation (mx+k). Here it says (3x+a), so coefficient is 3, constant is a.
    # Let's re-read: "correct_answer must be the integer a+2c". This implies 'a' and 'c' are specific variables from the factors.
    # If factor1 = (3*x + b) and factor2 = (13*x + d). 
    # Then A=39, B=5, C=-14.
    # 3*d + b*13 = 5 => 3d + 13b = 5.
    # b*d = -14.
    
    solutions = []
    factors_C = [(-2, 7), (2, -7), (-1, 14), (1, -14)] # Pairs for bd=-14
    # Check which pair satisfies 3d + 13b = 5
    
    valid_b_d_pairs = []
    for b_val, d_val in factors_C:
        if 3 * d_val + 13 * b_val == B_target:
            valid_b_d_pairs.append((b_val, d_val))
            
    # There might be multiple solutions or none. The problem implies a unique recovery task usually.
    # Let's assume the first found solution is the one to use for generation if strict_source_template requires specific logic.
    # However, "strict_source_template" often means using the exact parameters provided in frozen state as ground truth.
    # If multiple integer solutions exist, we pick one? Or maybe only one exists.
    
    chosen_b = None
    chosen_d = None
    
    if valid_b_d_pairs:
        b_val, d_val = valid_b_d_pairs[0]
        chosen_b = b_val
        chosen_d = d_val
        
    # Now construct the factors based on "first factor fixed as (3x+a)". 
    # In my derivation above, I used 'b' for constant of first factor. The spec calls it 'a'.
    # So Factor1 = 3*x + a_specified where a_specified = chosen_b.
    # Factor2 = c_x * x + d_specified where c_x is derived from A/3 = 13. And d_specified = chosen_d.
    
    spec_a_const = chosen_b
    spec_c_coeff = int(A_target / 3) if (A_target % 3 == 0) else None # Should be integer
    
    # The question asks for "a+2c". 
    # Here 'a' is the constant term of first factor (spec_a_const).
    # And 'c' likely refers to the x-coefficient of the second factor? Or maybe c from standard form ax^2... no.
    # Spec: "correct_answer must be the integer a+2c". 
    # Context: Factor 1 is (3x + a). Factor 2 is (cx + d)? No, usually factors are (mx+n)(px+q).
    # If factor order policy is strict_source_template and first is fixed as (3x+a), then the variable 'a' in "a+2c" refers to that constant.
    # What is c? In standard polynomial ax^2+bx+c, c is the constant term of the whole poly (-14). 
    # But here it says integer a+2c. If c was -14, result would be spec_a_const + 2*(-14).
    # Alternatively, maybe 'c' refers to the x-coefficient of the second factor? Let's assume standard variable naming in these tasks:
    # Factor 1: (x_coeff_1 * X + const_1) -> Spec says (3*X + a), so const_1 = a.
    # Factor 2: (c * X + d). So c is the x-coefficient of second factor.
    # Let's calculate with this assumption.
    
    if spec_c_coeff is not None and chosen_b is not None and chosen_d is not None:
        question_text = r"Given that $P(x) = (3x+a)(cx+d)$ expands to the polynomial with coefficients corresponding to $[39, 5, -14]$, find the integer value of $a+2c$."
        
        # Calculate correct_answer
        val_a = spec_a_const
        val_c = spec_c_coeff
        
        correct_ans_int = int(val_a + 2 * val_c)
        
    else:
        # Fallback if no solution found (should not happen with valid inputs for this task type usually)
        question_text = r"Error in parameter recovery."
        correct_ans_int = 0

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_ans_int,
        "oracle_payload": oracle_payload
    }