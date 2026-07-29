import math
from core.prompts.domain_function_library import IntegerOps.safe_eval, IntegerOps.fmt_num


def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    # Calculate the power using safe evaluation to ensure integer result handling
    try:
        correct_answer_int = IntegerOps.safe_eval(f"{base}^{exponent}")
    except ValueError as e:
        raise RuntimeError("Failed to evaluate expression") from e
    
    question_text = r"Calculate $(-3)^{3}$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": frozen_params
    }
