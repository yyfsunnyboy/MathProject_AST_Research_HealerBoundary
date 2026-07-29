def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Parse components for question_text construction
    term1_num, term1_den = map(int, expression.split("/")[0].split(" ")[-1]) if "/" in expression else None
    
    # Manual calculation of the exact fraction:
    # Term 1: 9/22 + 11/18 -> Common denominator (LCM of 22 and 18 is 198)
    # 9*9 = 81, 11*11 = 121. Sum = 202 / 198. Simplify: divide by 2 -> 101/99.
    
    # Term 2 inside parenthesis: 23/22 - 7/18
    # Common denominator (LCM of 22 and 18 is 198)
    # 23*9 = 207, 7*11 = 77. Diff = 130 / 198. Simplify: divide by 2 -> 65/99.
    
    # Total expression: (101/99) - (65/99) = 36/99
    # Simplify 36/99: Divide numerator and denominator by GCD(36, 99).
    # Factors of 36: 2^2 * 3^2. Factors of 99: 3^2 * 11. GCD is 9.
    # Numerator: 36 / 9 = 4. Denominator: 99 / 9 = 11.
    
    numerator = 4
    denominator = 11
    
    return {
        "question_text": f"Compute the exact value of $\\frac{9}{22} + \\frac{11}{18} - (\\frac{23}{22} - \\frac{7}{18})$.",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": f"\\\\frac{{{numerator}}}{{{{{denominator}}}}}"
        },
        "oracle_payload": {"expression": expression}
    }