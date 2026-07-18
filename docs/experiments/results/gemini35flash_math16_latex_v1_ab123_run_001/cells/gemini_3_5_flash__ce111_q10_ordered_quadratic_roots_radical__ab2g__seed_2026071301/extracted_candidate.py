def generate(level=1, **kwargs):
    # Frozen parameters
    equation = "(x-2)^2=3"
    order = "a>b"
    target = "2a+b"
    
    # Question text using formal LaTeX delimiters
    question_text = (
        "Let \\(a\\) and \\(b\\) be the roots of the equation \\((x-2)^2=3\\) "
        "such that \\(a>b\\). Find the value of \\(2a+b\\)."
    )
    
    # Correct answer with structured representation of 6 + \sqrt{3}
    correct_answer = {
        "result": {
            "rational": 6,
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": "6+\\sqrt{3}"
        }
    }
    
    # Oracle payload matching the frozen parameters
    oracle_payload = {
        "equation": equation,
        "order": order,
        "target": target
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }