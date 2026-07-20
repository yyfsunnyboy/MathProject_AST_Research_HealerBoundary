def generate(level=1, **kwargs):
    base = kwargs.get("base", -3)
    exponent = kwargs.get("exponent", 3)
    
    result = base ** exponent
    
    question_text = f"Calculate $(-{abs(base)})^{{ {exponent} }}$." if abs(base) > 0 else "Compute the power of the given integer to the specified non-negative exponent."
    correct_answer = int(result)
    oracle_payload = {"base": base, "exponent": exponent}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }