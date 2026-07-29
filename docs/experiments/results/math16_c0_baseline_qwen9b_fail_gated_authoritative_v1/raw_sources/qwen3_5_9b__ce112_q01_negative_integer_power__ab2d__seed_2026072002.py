from typing import Dict, Any
import math
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"base": -3, "exponent": 3})
    
    base_val = frozen_params["base"]
    exponent_val = frozen_params["exponent"]
    
    # Calculate result using IntegerOps.safe_eval to adhere to domain API constraints for math operations if applicable.
    # However, standard power operation is fundamental. We will compute the value directly but format it via fmt_num for consistency with domain usage where possible.
    # Since safe_eval expects an expression string and returns int/float:
    try:
        result = IntegerOps.safe_eval(f"{base_val} ** {exponent_val}")
    except ValueError as e:
        # Fallback if specific evaluation fails, though standard power should work for integers within limits.
        result = base_val ** exponent_val
    
    formatted_result_str = IntegerOps.fmt_num(result)
    
    question_text = (
        r"Calculate the value of $(-3)^{3}$."
    )
    
    correct_answer_int = int(formatted_result_str) if isinstance(formatted_result_str, str) else result
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": frozen_params
    }