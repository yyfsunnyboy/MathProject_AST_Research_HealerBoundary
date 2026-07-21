def generate(level=1, **kwargs):
    denominator_str = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    import re
    match = re.match(r"(\d+)-sqrt\((\d+)\)", denominator_str)
    if match:
        A = int(match.group(1))
        B = int(match.group(2))
    else:
        A = 4
        B = 7
        
    correct_answer = A + B
    
    question_text = (
        f"Rationalize the denominator of \\(\\frac{{{numerator}}}{{{A} - \\sqrt{{{B}}}}}\\). "
        f"If the result is expressed in the form \\(a + \\sqrt{{b}}\\), where \\(a\\) and \\(b\\) are integers, "
        f"find the value of \\(a + b\\)."
    )
    
    oracle_payload = {
        "denominator": denominator_str,
        "numerator": numerator,
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }