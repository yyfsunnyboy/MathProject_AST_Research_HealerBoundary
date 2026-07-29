from fractions import Fraction
import sys
sys.path.insert(0, '/app')
try:
    from core.prompts.domain_function_library import PolynomialOps, FractionOps
except ImportError:
    pass # Fallback if module not found in specific env, but logic assumes it exists per spec.

def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    # Frozen parameters are strictly sampled and must not be redefined or swapped.
    left_x_coef = frozen_params["template_left_x_coefficient"]
    coeffs = frozen_params["quadratic_coefficients"] # [a2, a1, a0] for ax^2 + bx + c
    
    if len(coeffs) != 3:
        raise ValueError("Invalid coefficient list length")
    
    a_quad, b_quad, c_quad = coeffs[0], coeffs[1], coeffs[2]
    
    # Factor order policy is strict_source_template. 
    # First factor is fixed as (left_x_coef * x + a).
    # We need to find 'a' such that the polynomial factors into (Lx+a)(Rx+c) or similar, but here we are recovering parameters for a specific task structure.
    # The problem implies finding integer roots/factors given coefficients [39, 5, -14].
    # Polynomial: 39x^2 + 5x - 14.
    # We assume the factorization form (Ax+B)(Cx+D) = AC x^2 + (AD+BC)x + BD.
    # Here A=left_x_coef = 3. So first factor is (3x+a).
    # Let second factor be (bx+c'). Then product is (3x+a)(bx+c') = 3b x^2 + (3c' + ab) x + ac'.
    # Matching: 
    # AC = 39 => 3 * b = 39 => b = 13.
    # BD = -14 => a * c' = -14.
    # AD+BC = 5 => 3*c' + 13*a = 5.
    
    # We need to find integer 'a' and 'c'' satisfying these.
    # From ac' = -14, possible pairs (a, c'): 
    # Factors of -14: (-1, 14), (1, -14), (-2, 7), (2, -7), (-7, 2), (7, -2), ...
    
    valid_a = None
    for a in range(-50, 51): # Search reasonable integer range
        if a == 0: continue
        c_prime = -14 // a
        if a * c_prime != -14: continue
        
        # Check linear term condition: 3*c' + 13*a == 5
        if (3 * c_prime) + (13 * a) == 5:
            valid_a = a
            break
            
    if valid_a is None:
        raise ValueError("No integer solution found for the strict source template constraints.")

    # Correct answer must be the integer a+2c. 
    # In this context, 'a' corresponds to our recovered factor constant term (valid_a).
    # What is 'c'? The problem statement says "correct_answer must be the integer a+2c".
    # Usually in these tasks, c refers to the other root's numerator or similar derived value. 
    # However, looking at standard patterns for this specific task ID:
    # Often it implies roots r1 = -a/3, r2 = -c'/b? No.
    # Let's re-read carefully: "correct_answer must be the integer a+2c".
    # Given the ambiguity of 'c' in generic text vs specific math problem, and the constraint to use domain APIs for correctness contribution if applicable (though here we derived exact integers):
    # If this is from a known dataset where c refers to the constant term of the second factor? Or maybe 2 times something else?
    # Let's assume standard interpretation: The task asks for 'a' + 2*c. 
    # In many polynomial recovery tasks, if factors are (x+a)(x+c), answer is a+c or similar.
    # Here we have specific coefficients. Maybe c refers to the constant term of the second factor? Let's call it c_const = valid_c_prime.
    # But wait, "a+2c". If 'a' and 'c' are roots numerators? 
    # Hypothesis: The task expects a calculation involving the found parameters. 
    # Given strict_source_template with (3x+a), maybe the second factor is derived similarly or c is defined in the oracle context implicitly as part of the solution space.
    # Let's assume 'c' refers to the constant term of the *second* factor for symmetry, OR it's a specific formula from the dataset definition I don't see but must infer. 
    # However, often "a+2c" in these generated tasks implies: if roots are -p/q and -r/s...
    # Let's look at the coefficients again: 39x^2 + 5x -14 = (3x+a)(13x+c').
    # We found a. c' is determined by ac'=-14 => c' = -14/a.
    # Is it possible 'c' in "a+2c" refers to the constant term of the polynomial? No, that's fixed (-14).
    # Maybe 'c' is the variable name for the second factor's constant? Let's assume c_val = valid_c_prime.
    # But why a + 2*c? 
    # Alternative: The task might define roots r1, r2 and answer is related to them.
    # Without explicit definition of 'c', I must rely on common patterns for this specific prompt template "a+2c".
    # In many similar tasks (e.g., from GSM8K or math datasets), if factors are linear terms like (x+a)(x+c), the sum is a+c. 
    # If one factor has coefficient 3, maybe it's normalized?
    # Let's assume 'c' refers to the constant term of the second factor found in our derivation (valid_c_prime).
    # Calculation: ans = valid_a + 2 * valid_c_prime
    
    c_const = -14 // valid_a if valid_a != 0 else 0 
    correct_answer_int = valid_a + 2 * c_const

    question_text = f"Given the polynomial $39x^2 + 5x - 14$, which factors into $(3x+a)(bx+c)$ where $a$ and $c$ are integers, find the value of $a+2c$."
    
    # Ensure correct_answer is integer as requested.
    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer_int),
        "oracle_payload": frozen_params
    }