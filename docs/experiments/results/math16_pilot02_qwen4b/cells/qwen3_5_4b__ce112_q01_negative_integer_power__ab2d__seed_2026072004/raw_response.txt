import sys
sys.path.insert(0, '..')  # Adjust path as needed based on environment structure if running locally without full setup
from core.prompts.domain_function_library import IntegerOps.safe_eval, IntegerOps.fmt_num

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    # Calculate (-3)^3 using safe_eval to ensure correct type handling per domain API requirements
    result = IntegerOps.safe_eval(f"({base})^{exponent}")
    
    question_text = f"What is the value of $(-{abs(base)})^{{\\text{{{str(exponent)}}}}}$?"
    formatted_answer = fmt_num(result) if isinstance(result, float) else str(int(result))
    
    return {
        "question_text": question_text,
        "correct_answer": int(result),
        "oracle_payload": frozen_params
    }