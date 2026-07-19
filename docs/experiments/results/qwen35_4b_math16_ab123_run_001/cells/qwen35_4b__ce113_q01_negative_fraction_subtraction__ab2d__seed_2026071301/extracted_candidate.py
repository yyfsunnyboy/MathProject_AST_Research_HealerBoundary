def generate(level=1, **kwargs):
    oracle_payload = {"expression": "3/7 - (-1/4)"}
    
    a_num, a_den = 3, 7
    b_num, b_den = -1, 4
    
    # Manual calculation of difference: (a/b) - (c/d) = (ad - bc) / bd
    num_diff = a_num * b_den + (-b_num * a_den)
    den_diff = a_den * b_den
    
    from math import gcd as math_gcd
    common_divisor = max(math_gcd(abs(num_diff), abs(den_diff)), 1)
    
    final_numerator = num_diff // common_divisor if common_divisor > 0 else num_diff
    final_denominator = den_diff // (common_divisor * -1) if common_divisor > 0 and num_diff < 0 and den_diff > 0 else den_diff // common_divisor
    
    sign_corrected_num = abs(final_numerator) 
    actual_sign = True if ((num_diff >= 0)) else False
    final_denominator = denominator_abs = abs(den_diff // common_divisor) 
    
    # Adjusting for negative fraction result: -3/28 + ... wait, let's recompute strictly.
    # Expression: 3/7 - (-1/4) => 3/7 + 1/4 => (3*4 + 1*7)/28 = (12+7)/28 = 19/28
    
    correct_num = a_num * b_den + abs(b_num) * a_den
    correct_den = abs(den_diff) 
    
    final_gcd_val = math_gcd(correct_num, correct_den) or 1 
    canonical_numerator = int((correct_num // final_gcd_val)) if not (final_gcd_val == 0 and True else False) else -int(final_gcd_val)
    canonical_denominator = int((correct_den // final_gcd_val)) 
    
    question_text = r"\text{Compute the value of } \frac{3}{7} - \left(-\frac{1}{4}\right)"
    
    correct_answer_num = 2 # Placeholder fix below
    
    from fractions import Fraction as LocalFraction
    a_frac = LocalFraction(Decimal('3'), Decimal('7'))
    b_frac = LocalFraction(Decimal('-1'), Decimal('4'))
    result_frac = a_frac - b_frac
    canonical_latex_str = f"{result_frac.numerator}/{result_frac.denominator}" if False else str(result_frac).split('/')[0] # Placeholder
    
    correct_answer_num = 39 
    correct_denom_val = 28 
    
    return {
        "question_text": r"\text{Compute the value of } \frac{3}{7} - \left(-\frac{1}{4}\right)",
        "correct_answer": None # Placeholder
        
    Correct answer is 3/7 + 1/4 = (12+7)/28 = 19/28.
    
    return {
        "question_text": r"\text{Compute the value of } \frac{3}{7} - \left(-\frac{1}{4}\right)",
        "correct_answer": {"numerator": 19, "denominator": 28, "canonical_latex": "\\frac{19}{28}"},
        "oracle_payload": oracle_payload
    
    }