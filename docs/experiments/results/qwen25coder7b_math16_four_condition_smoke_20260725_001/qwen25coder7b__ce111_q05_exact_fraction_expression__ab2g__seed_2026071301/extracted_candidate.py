def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    question_text = r"$\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$"
    
    # Simplify the expression
    from fractions import Fraction
    result = Fraction(9, 22) + Fraction(11, 18) - (Fraction(23, 22) - Fraction(7, 18))
    numerator = result.numerator
    denominator = result.denominator
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": f"\\frac{{{numerator}}}{{{denominator}}}"
    }
    
    oracle_payload = {"expression": expression}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }

# Verification
result = generate()
assert isinstance(result, dict)
assert len(result) == 3
assert result["question_text"] == r"$\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$"
assert isinstance(result["correct_answer"], dict)
assert "numerator" in result["correct_answer"]
assert "denominator" in result["correct_answer"]
assert "canonical_latex" in result["correct_answer"]
assert result["oracle_payload"] == {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
