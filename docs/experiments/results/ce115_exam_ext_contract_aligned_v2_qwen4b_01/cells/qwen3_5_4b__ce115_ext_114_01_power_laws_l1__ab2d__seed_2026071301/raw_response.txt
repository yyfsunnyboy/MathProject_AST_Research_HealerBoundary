def generate(level=1, **kwargs):
    frozen_params = {"base": 7, "expression": "7**10 * 7**2 / 7**4", "required_form": "power_of_same_base"}
    
    # Calculate exponent: 10 + 2 - 4 = 8
    correct_exponent = 8
    
    def get_correct_answer():
        return {"base": frozen_params["base"], "exponent": correct_exponent}

    question_text = f"Calculate the result of {frozen_params['expression']}. Express your answer as a power with the same base."
    
    oracle_payload = frozen_params.copy()
    
    return {
        "question_text": question_text,
        "correct_answer": get_correct_answer(),
        "oracle_payload": oracle_payload
    }