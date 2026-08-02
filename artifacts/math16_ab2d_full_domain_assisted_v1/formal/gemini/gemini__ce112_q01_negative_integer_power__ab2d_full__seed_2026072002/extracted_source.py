from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "base": -3,
        "exponent": 3
    }
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    # Compute base ** exponent
    ans = base ** exponent
    
    question_text = "計算\n\\[\n(-3)^3.\n\\]"
    
    return {
        "question_text": question_text,
        "correct_answer": ans,
        "oracle_payload": frozen_params
    }
