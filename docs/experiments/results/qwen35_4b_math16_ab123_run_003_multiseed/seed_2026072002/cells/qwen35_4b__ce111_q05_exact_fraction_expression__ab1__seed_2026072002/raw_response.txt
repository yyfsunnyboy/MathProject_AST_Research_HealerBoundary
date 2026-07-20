def generate(level=1, **kwargs):
    question_text = r"\text{Compute } \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)."
    
    # Calculate the exact fraction step by step
    # Expression: 9/22 + 11/18 - (23/22 - 7/18)
    # Group terms with common denominators where possible or compute directly.
    # Let's simplify inside parentheses first:
    # 23/22 - 7/18 = (23*9)/(22*9) - (7*11)/(18*11) = 207/198 - 77/198 = 130/198
    # Simplify 130/198: divide by 2 -> 65/99
    
    # Now the expression is: 9/22 + 11/18 - 65/99
    # Find common denominator for 22, 18, 99.
    # LCM(22, 18) = LCM(2*11, 2*3^2) = 2 * 3^2 * 11 = 198
    # Check if 99 divides 198: yes (2). So LCD is 198.
    
    # Convert fractions to denominator 198:
    # 9/22 = (9*9)/198 = 81/198
    # 11/18 = (11*11)/198 = 121/198
    
    # Term inside parentheses result was 65/99. Convert to 198:
    # 65/99 = (65*2)/(99*2) = 130/198
    
    # Combine numerators over common denominator:
    # Numerator = 81 + 121 - 130
    # Numerator = 202 - 130 = 72
    
    # Resulting fraction: 72 / 198
    numerator_raw = 72
    denominator_raw = 198
    
    # Simplify the fraction by dividing both by GCD(72, 198)
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    common_divisor = gcd(numerator_raw, denominator_raw)
    
    numerator_final = numerator_raw // common_divisor
    denominator_final = denominator_raw // common_divisor
    
    canonical_latex = rf"\frac{{{numerator_final}}}{{denominator_final}}"
    
    correct_answer_dict = {
        "numerator": str(numerator_final),
        "denominator": str(denominator_final),
        "canonical_latex": canonical_latex
    }

    oracle_payload = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }