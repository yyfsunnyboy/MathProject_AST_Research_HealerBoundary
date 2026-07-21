def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    correct_answer = base ** exponent
    
    question_text = r"Calculate $(-3)^3$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }