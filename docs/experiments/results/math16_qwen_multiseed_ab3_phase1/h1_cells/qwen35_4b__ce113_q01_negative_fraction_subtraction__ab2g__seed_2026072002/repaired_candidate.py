def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Calculate correct answer: 3/7 + 1/4 = (12+7)/28 = 19/28
    numerator = 19
    denominator = 28
    
    question_text = r"\text{Calculate the result of } \frac{3}{7} - \left(-\frac{1}{4}\right)"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": r"\frac{19}{28}"
        },
        "oracle_payload": {'expression': '3/7 - (-1/4)'}
    }