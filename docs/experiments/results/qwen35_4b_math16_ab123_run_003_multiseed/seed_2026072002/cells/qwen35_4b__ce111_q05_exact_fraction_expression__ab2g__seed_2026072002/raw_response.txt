def generate(level=1, **kwargs):
    question_text = r"Find the exact fraction expression for: $\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$."
    
    numerator_value = 9 * 18 + 11 * 22 - (23 * 18 - 7 * 22)
    denominator_value = 22 * 18
    
    gcd_val = 0
    a, b = abs(numerator_value), abs(denominator_value)
    while b:
        a, b = b, a % b
    gcd_val = a

    canonical_numerator = numerator_value // gcd_val
    canonical_denominator = denominator_value // gcd_val
    
    if canonical_denominator < 0:
        canonical_numerator *= -1
        canonical_denominator *= -1
        
    correct_answer = {
        "numerator": canonical_numerator,
        "denominator": canonical_denominator,
        "canonical_latex": f"${\\frac{{{canonical_numerator}}}{{{canonical_denominator}}}$}"
    }

    oracle_payload = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }