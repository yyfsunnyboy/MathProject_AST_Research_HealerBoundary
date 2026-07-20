def generate(level=1, **kwargs):
    base = -3
    exponent = 3
    
    result = int(base ** exponent)
    
    return {
        "question_text": r"Calculate $(-3)^{3}$.",
        "correct_answer": result,
        "oracle_payload": {"base": base, "exponent": exponent}
    }