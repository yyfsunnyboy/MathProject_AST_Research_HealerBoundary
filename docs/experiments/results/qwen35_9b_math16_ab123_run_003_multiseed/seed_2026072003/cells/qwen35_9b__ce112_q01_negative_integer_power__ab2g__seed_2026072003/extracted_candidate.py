def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters from task specification context
    base = -3
    exponent = 3
    
    question_text = r"Calculate $(-3)^{3}$."
    
    correct_answer = int(math.pow(base, exponent))
    
    oracle_payload = {
        "base": base,
        "exponent": exponent
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }