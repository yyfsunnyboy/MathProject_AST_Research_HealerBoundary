from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    # Step 1: Compute base ** exponent with native arithmetic (Python handles negative bases correctly)
    result = (-3) ** 3
    
    return {
        "question_text": r"計算\[(-3)^3.\]",
        "correct_answer": result,
        "oracle_payload": frozen_params
    }