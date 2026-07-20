def generate(level=1, **kwargs):
    base = kwargs.get("base", -3)
    exponent = kwargs.get("exponent", 3)
    
    if level == 0:
        question_text = r"Calculate $(-3)^{3}$."
        correct_answer = -27
        oracle_payload = {"base": -3, "exponent": 3}
        
    elif level == 1:
        question_text = r"Evaluate the expression $a^b$ where $a=-3$ and $b=3$."
        correct_answer = -27
        oracle_payload = {"base": -3, "exponent": 3}
    
    else:
        raise ValueError("Invalid level")

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }