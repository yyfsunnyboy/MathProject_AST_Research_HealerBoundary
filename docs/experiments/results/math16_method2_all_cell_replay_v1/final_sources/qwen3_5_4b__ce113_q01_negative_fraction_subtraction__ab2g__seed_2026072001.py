def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Calculate 3/7 + 1/4
    # Common denominator is 28
    # 3/7 = 12/28
    # 1/4 = 7/28
    # Sum = (12 + 7) / 28 = 19/28
    
    numerator = 19
    denominator = 28
    
    question_text = r"\text{Calculate the difference: } \frac{3}{7} - \left(-\frac{1}{4}\right)"
    
    # Check if irreducible (GCD of 19 and 28 is 1)
    import math
    gcd_val = math.gcd(numerator, denominator)
    
    canonical_latex = r"\frac{" + str(numerator // gcd_val) + "}{"} + str(denominator // gcd_val) + r"}"

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator // gcd_val,
            "denominator": denominator // gcd_val,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"expression": expression}
    }