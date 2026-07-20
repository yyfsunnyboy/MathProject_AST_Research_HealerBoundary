def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Calculate the result: 3/7 + 1/4 = (12 + 7) / 28 = 19/28
    numerator = 19
    denominator = 28
    
    question_text = r"Calculate $ \frac{3}{7} - \left( -\frac{1}{4} \right) $"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": f"\\frac{{{numerator}}}{{{denominator}}}"
        },
        "oracle_payload": expression
    }