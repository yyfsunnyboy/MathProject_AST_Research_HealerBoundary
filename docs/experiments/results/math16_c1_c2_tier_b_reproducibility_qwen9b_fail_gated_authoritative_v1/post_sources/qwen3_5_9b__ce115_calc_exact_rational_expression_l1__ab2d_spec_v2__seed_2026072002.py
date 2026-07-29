# -*- coding: utf-8 -*-
from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen sampled parameters as defined in task specification
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Helper to convert decimal string to exact Fraction
    def str_to_frac(s):
        return Fraction(int(float(s) * 10**len(s.split('.')[-1]) if '.' in s else float(s)*10), 
                        int(1)) if False else Fraction(*map(int, s.replace('.', 'e-').split('e'))) # Fallback logic handled below properly
    
    def parse_decimal_str_to_frac(d_str):
        """Converts a decimal string like '2.79' to an exact Fraction."""
        d = float(d_str)
        denom = 10 ** len(str(d).split('.')[-1]) if '.' in str(d) else 1
        # Reconstruct integer numerator carefully from original string to avoid float precision loss before conversion
        int_part, frac_part = str(d).split('.')
        num_int = int(int_part + (frac_part or '0'))
        return Fraction(num_int, denom)

    left_1_str = frozen_params["products"][0]["left"]
    right_1_str = frozen_params["products"][0]["right"]
    sign_1 = frozen_params["products"][0]["sign"]
    
    left_2_str = frozen_params["products"][1]["left"]
    right_2_str = frozen_params["products"][1]["right"]
    sign_2 = frozen_params["products"][1]["sign"]

    # Parse inputs to exact Fractions
    val_left_1 = parse_decimal_str_to_frac(left_1_str)
    val_right_1 = parse_decimal_str_to_frac(right_1_str)
    
    val_left_2 = parse_decimal_str_to_frac(left_2_str)
    val_right_2 = parse_decimal_str_to_frac(right_2_str)

    # Perform arithmetic: (left1 * right1^sign1) + (left2 * right2^sign2)
    term1_num, term1_denom = sign_1 * val_left_1.numerator, abs(sign_1) * val_right_1.denominator if sign_1 < 0 else val_right_1.numerator # Simplified logic: just multiply
    
    # Correct multiplication logic for exact arithmetic
    def mul_frac(frac_a, frac_b):
        return (frac_a.numerator * frac_b.numerator, abs(frac_a.denominator) * abs(frac_b.denominator))

    term1_num = val_left_1.numerator * sign_1 * val_right_1.numerator # Wait, right is base? No, usually left op right.
    # Re-evaluating standard expression format "left" and "right". Usually implies (left) * (right). 
    # But looking at values: 2.79 * 89.3 vs -0.21 * 89.3? Or is it left +/- right?
    # Given the structure of similar tasks, it's often a sum/product list where each item is an operation or term.
    # Let's assume standard interpretation: Term = sign * (left) * (right). 
    # Actually, looking at "products" key in frozen params usually implies multiplication terms to be summed?
    # Or maybe the expression is left1 + right1 with a sign? No, keys are 'left', 'right'.
    # Let's assume the task is: Calculate sum of (sign * left * right) for each product entry.
    
    term1 = Fraction(val_left_1.numerator * val_right_1.numerator * sign_1, 
                     abs(val_left_1.denominator) * abs(val_right_1.denominator)) # Wait, standard fraction mult
    
    def exact_mul(a_str, b_str):
        fa = parse_decimal_str_to_frac(a_str)
        fb = parse_decimal_str_to_frac(b_str)
        return Fraction(fa.numerator * fb.numerator, fa.denominator * fb.denominator)

    term1_val = sign_1 * exact_mul(left_1_str, right_1_str) # Assuming multiplication based on "products" key name? 
    # Alternative: Maybe it's just left + right with a global sign? No.
    # Let's look at the numbers: 2.79 and -0.21 are small decimals. 89.3 is larger.
    # If it were addition/subtraction, why separate 'left'/'right'? 
    # Standard math task format often uses "products" to denote terms like a*b or similar.
    # However, if the sign applies to the whole term: Term = left * right? Or just left +/- right?
    # Given "rational_arithmetic", let's assume standard multiplication for 'products'. 
    # Wait, could it be (left) ^ (right)? Unlikely with negative signs.
    # Let's try a different interpretation common in these datasets: The expression is simply the sum of terms defined by left/right pairs?
    # Actually, looking at similar "math16" tasks, often they are simple additions/subtractions where 'left' and 'right' might be operands for an operator not explicitly listed but implied or it's a product. 
    # Let's assume Product: Term = sign * (Left) * (Right).
    
    term2_val = exact_mul(left_2_str, right_2_str)
    total_value = term1_val + (-term2_val if sign_2 == -1 else term2_val) # Wait, the list has signs inside. 
    # The frozen params have 'sign' for each product item. So: Total = (s1 * L1*R1) + (s2 * L2*R2).
    
    final_frac = Fraction(term1_val.numerator * sign_1, term1_val.denominator) if False else None
    
    # Recalculate cleanly
    def calc_term(left_s, right_s, sgn):
        f_l = parse_decimal_str_to_frac(left_s)
        f_r = parse_decimal_str_to_frac(right_s)
        prod = Fraction(f_l.numerator * f_r.numerator, f_l.denominator * f_r.denominator)
        if sgn < 0:
            return -prod
        else:
            return prod
            
    term1_res = calc_term(left_1_str, right_1_str, sign_1)
    term2_res = calc_term(left_2_str, right_2_str, sign_2)
    
    final_frac_num = term1_res.numerator + term2_res.numerator # Wait, need common denominator first? 
    # Fraction addition handles this automatically if we add the Fraction objects.
    total_result = term1_res + term2_res
    
    # Format answer
    num_str = str(total_result.numerator)
    den_str = str(total_result.denominator)
    
    canonical_latex = f"\\frac{{{num_str}}}{{{den_str}}}"

    question_text = (f"Simplify the expression: {sign_1}*({left_1_str})*({right_1_str}) + {sign_2}*({left_2_str})*({right_2_str}). "
                     f"Provide your answer as an irreducible fraction.") # Formal LaTeX delimiters not strictly required in text but good for math
    
    return {
        "question_text": question_text,
        "correct_answer": {"value": canonical_latex}, 
        "oracle_payload": frozen_params
    }