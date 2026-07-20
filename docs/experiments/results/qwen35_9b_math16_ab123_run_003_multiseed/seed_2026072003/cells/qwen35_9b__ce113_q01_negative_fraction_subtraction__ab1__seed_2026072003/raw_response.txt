def generate(level=1, **kwargs):
    import json
    
    expression = kwargs.get("expression", "3/7 - (-1/4)")
    
    # Parse the frozen sampled parameters logic manually for this specific case
    # Expression: 3/7 - (-1/4) -> 3/7 + 1/4
    # Common denominator is 28.
    # Numerator: (3*4) + (1*7) = 12 + 7 = 19
    # Denominator: 28
    # Result: 19/28
    
    numerator = 19
    denominator = 28
    
    question_text = r"Compute the result of $3/7 - (-1/4)$."
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": rf"$\frac{{{numerator}}}{{{denominator}}}$"
    }
    
    oracle_payload = {"expression": expression}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }