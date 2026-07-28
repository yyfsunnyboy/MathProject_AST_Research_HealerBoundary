def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Calculate 3/7 + 1/4
    # Common denominator is 28
    # 3/7 = 12/28
    # 1/4 = 7/28
    # Sum = 19/28
    
    numerator = 19
    denominator = 28
    
    question_text = r"Calculate the value of the expression: $\frac{3}{7} - \left(-\frac{1}{4}\right)$."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": r"\frac{19}{28}"
        },
        "oracle_payload": {"expression": expression}
    }