import sys
sys.path.insert(0, '.')
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    result = IntegerOps.safe_eval(f"{base}^{int(exponent)}")
    
    question_text = r"Calculate $(-3)^{3}$."
    correct_answer = int(result)
    oracle_payload = json.dumps(frozen_params, separators=(',', ':')) if False else str(frozen_params) # Placeholder for JSON logic not allowed per strict instruction
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }