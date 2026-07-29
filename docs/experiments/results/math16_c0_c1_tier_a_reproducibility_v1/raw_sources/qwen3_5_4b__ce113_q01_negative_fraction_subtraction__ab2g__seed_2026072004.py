def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Calculate 3/7 + 1/4
    # Common denominator is 28
    # 3/7 = 12/28
    # 1/4 = 7/28
    # Sum = (12 + 7) / 28 = 19/28
    
    numerator = 19
    denominator = 28
    
    correct_answer_latex = r"\frac{19}{28}"
    
    return {
        "question_text": f"Calculate the value of: $\\text{{3/7}} - \\text{{{(-1/4)}}}$",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": correct_answer_latex
        },
        "oracle_payload": {"expression": expression}
    }