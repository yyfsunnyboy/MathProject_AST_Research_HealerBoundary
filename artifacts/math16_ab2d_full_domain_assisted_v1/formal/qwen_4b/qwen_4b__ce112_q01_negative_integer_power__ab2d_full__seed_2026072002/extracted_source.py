from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "base": -3,
        "exponent": 3
    }
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    # Compute (-3)^3 using native arithmetic (Python's built-in ** operator)
    result = base ** exponent
    
    return {
        "question_text": r"計算\n\[(-3)^3.\]",
        "correct_answer": result,
        "oracle_payload": frozen_params
    }
