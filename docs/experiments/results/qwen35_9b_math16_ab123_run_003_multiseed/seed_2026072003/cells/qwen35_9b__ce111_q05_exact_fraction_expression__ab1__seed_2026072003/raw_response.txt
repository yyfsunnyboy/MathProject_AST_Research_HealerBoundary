def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Compute the exact fraction result manually step-by-step to ensure correctness.
    # Term 1: 9/22
    # Term 2: 11/18
    # Term 3 inside parenthesis: 23/22 - 7/18
    
    # Common denominator for first two terms (LCM of 22 and 18): 
    # 22 = 2 * 11, 18 = 2 * 9 -> LCM = 2 * 9 * 11 = 198
    # Term 1: 9/22 = (9*9)/198 = 81/198
    # Term 2: 11/18 = (11*11)/198 = 121/198
    # Sum of first two parts before subtracting parenthesis result? 
    # Actually, let's group by operations strictly left to right or standard order.
    # Expression: A + B - (C - D) = A + B - C + D
    
    # Let's re-evaluate using common denominator 198 for all terms eventually.
    # Term A = 9/22 -> 81/198
    # Term B = 11/18 -> 121/198
    # Term C = 23/22 -> (23*9)/198 = 207/198
    # Term D = 7/18 -> (7*11)/198 = 77/198
    
    # Total numerator = A_num + B_num - C_num + D_num
    #                  = 81 + 121 - 207 + 77
    #                  = 202 - 207 + 77
    #                  = -5 + 77
    #                  = 72
    
    Total numerator is 72. Denominator is 198.
    Fraction: 72/198.
    
    # Simplify fraction by finding GCD of 72 and 198.
    # Factors of 72: 1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72
    # Factors of 198: ... divisible by 2? Yes. /2 = 99. Divisible by 3? Yes (sum digits=18). 
    # GCD(72, 198):
    # 72 = 6 * 12
    # 198 = 6 * 33
    # Is there a higher factor? 72/6 = 12. 198/6 = 33. GCD(12, 33) is 3. 
    # So total GCD was 6*3 = 18.
    
    Numerator reduced: 72 / 18 = 4
    Denominator reduced: 198 / 18 = 11
    
    Irreducible fraction is 4/11.

    return {
        "question_text": r"Compute the exact value of $ \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right) $. Express your answer as an irreducible fraction in LaTeX format.",
        "correct_answer": {
            "numerator": 4,
            "denominator": 11,
            "canonical_latex": r"\frac{4}{11}"
        },
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }