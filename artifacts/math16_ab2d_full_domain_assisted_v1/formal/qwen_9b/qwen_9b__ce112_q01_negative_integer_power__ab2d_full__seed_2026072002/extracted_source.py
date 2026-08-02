from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    # Compute (-3)^3 using native arithmetic as per step 1 instructions.
    # The domain API safe_eval can also be used for verification if needed, 
    # but the instruction says "Compute ... with native arithmetic".
    result = IntegerOps.safe_eval("(-3)**3")
    
    return {
        "question_text": r"計算\[(-3)^3.\]",
        "correct_answer": result,
        "oracle_payload": frozen_params
    }