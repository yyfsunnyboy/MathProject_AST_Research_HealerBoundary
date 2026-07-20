def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    question_text = r"Calculate the value of $(-3)^{3}$."
    
    try:
        correct_answer = IntegerOps.safe_eval(f"{fmt_num(base)}^{fmt_num(exponent)}")
    except ValueError as e:
        return {"question_text": question_text, "correct_answer": str(e), "oracle_payload": frozen_params}

    oracle_payload = frozen_params
    
    result_dict = {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
    
    return result_dict