from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "base": -3,
        "exponent": 3
    }
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    # Calculate the result using IntegerOps.safe_eval
    expr = f"({base})**{exponent}"
    correct_answer = int(IntegerOps.safe_eval(expr))
    
    question_text = "計算\n\\[\n(-3)^3.\n\\]"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }