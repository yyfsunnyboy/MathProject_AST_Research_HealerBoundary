def generate(level=1, **kwargs):
    base = kwargs.get("base", -3)
    exponent = kwargs.get("exponent", 3)
    
    question_text = f"Calculate $(-{abs(base)})^{{{exponent}}}$. Express your answer as an integer."
    correct_answer = base ** exponent
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"base": -3, "exponent": 3}
    }