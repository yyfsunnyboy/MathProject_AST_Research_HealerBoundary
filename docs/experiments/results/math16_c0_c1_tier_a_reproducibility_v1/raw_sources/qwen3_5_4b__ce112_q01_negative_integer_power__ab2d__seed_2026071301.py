import sys
sys.path.insert(0, '.')
from core.prompts.domain_function_library import IntegerOps.safe_eval, IntegerOps.fmt_num

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    # Calculate (-3)^3 using safe_eval to ensure correct integer handling
    expression = f"({base})^{exponent}"
    result = IntegerOps.safe_eval(expression)
    
    question_text = r"\text{Calculate } $(-3)^3$."
    correct_answer = int(result)
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }