from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {
        "base": -3,
        "exponent": 3
    }
    
    # Compute (-3)^3 using native arithmetic as per step 1 instructions.
    # The domain API safe_eval is not strictly required for simple integer powers 
    # if we can use native ops, but the prompt says "Compute base ** exponent with native arithmetic".
    # However, Python's native ** handles negative bases correctly: (-3)**3 = -27.
    
    result = frozen["base"] ** frozen["exponent"]
    
    return {
        "question_text": r"計算\[(-3)^3.\]",
        "correct_answer": result,
        "oracle_payload": frozen
    }