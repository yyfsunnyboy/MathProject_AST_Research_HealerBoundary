import math16_negative_integer_power as mnp
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base_val = frozen_params["base"]
    exp_val = frozen_params["exponent"]
    
    correct_answer = mnp.safe_eval(base_str=str(base_val), exponent_str=str(exp_val))
    
    question_text = r"$(-3)^{3}$"
    
    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer),
        "oracle_payload": frozen_params
    }