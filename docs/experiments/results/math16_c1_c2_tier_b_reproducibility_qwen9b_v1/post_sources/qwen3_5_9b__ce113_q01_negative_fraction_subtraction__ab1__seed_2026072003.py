def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Parse and compute manually to ensure correctness without external libraries
    import math
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    num1, den1 = 3, 7
    sign2_str = "-(-1/4)" # The second term is subtracted, but the operand itself has a negative sign in standard form? 
    # Actually expression "3/7 - (-1/4)" means: (3/7) + (1/4).
    
    num2, den2 = 1, 4
    
    lcm_denom = abs(den1 * den2 // gcd(den1, den2))
    factor1 = lcm_denom // den1
    factor2 = lcm_denom // den2
    
    new_num1 = num1 * factor1
    new_num2 = num2 * factor2
    
    # Operation: 3/7 - (-1/4) => (3*4 + 1*7) / 28 ? 
    # Wait, standard subtraction of a negative is addition.
    # Term 1: 3/7 -> numerator contribution: 3 * 4 = 12
    # Term 2: - (-1/4) => effectively adding 1/4 -> numerator contribution: 1 * 7 = 7
    total_numerator = new_num1 + new_num2
    
    common_divisor = gcd(total_numerator, lcm_denom)
    
    final_numer = total_numerator // common_divisor
    final_denom = (lcm_denom // common_divisor)
    
    if final_denom < 0:
        final_numer *= -1
        final_denom *= -1
        
    canonical_latex = f"\\frac{{{final_numer}}}{{{final_denom}}}"
    
    question_text = f"Simplify the expression $3/7 - (-1/4)$."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": final_numer,
            "denominator": final_denom,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"expression": expression}
    }