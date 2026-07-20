def generate(level=1, **kwargs):
    base = kwargs.get("base", -3)
    exponent = kwargs.get("exponent", 3)
    
    correct_answer = int(base ** exponent)
    
    question_text = f"Calculate $(-{abs(base)})^{{\\text{{{str(exponent)}}}}}$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"base": base, "exponent": exponent}
    }