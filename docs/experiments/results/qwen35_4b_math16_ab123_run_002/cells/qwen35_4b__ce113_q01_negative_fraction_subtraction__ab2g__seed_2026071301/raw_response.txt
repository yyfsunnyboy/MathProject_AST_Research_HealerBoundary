def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Perform subtraction: 3/7 - (-1/4) = 3/7 + 1/4
    # Common denominator is 28.
    # (3 * 4)/28 + (1 * 7)/28 = 12/28 + 7/28 = 19/28
    
    numerator = 19
    denominator = 28
    
    question_text = r"\text{Calculate the result of } \frac{3}{7} - \left(-\frac{1}{4}\right)."
    
    # Correct answer structure
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": r"\frac{19}{28}"
    }
    
    oracle_payload = {"expression": expression}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }