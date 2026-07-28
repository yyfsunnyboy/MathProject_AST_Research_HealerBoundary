import sys
sys.path.insert(0, '.')
from core.prompts.domain_function_library import IntegerOps.safe_eval, IntegerOps.fmt_num

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    expression_str = f"({fmt_num(base)})^{fmt_num(exponent)}"
    correct_answer_int = safe_eval(expression_str)
    
    question_text = r"\text{Calculate } $(-3)^3$."
    
    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer_int),
        "oracle_payload": frozen_params
    }