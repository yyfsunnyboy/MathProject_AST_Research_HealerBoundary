from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    # Compute (-3)^3 using native arithmetic as per step 1 instructions.
    # The domain API safe_eval is available but the instruction says "Compute ... with native arithmetic".
    # However, to ensure robustness and adherence to allowed ops (arithmetic), we can use ** directly 
    # or IntegerOps.safe_eval if strictly required by a hidden constraint not visible here.
    # Given "Allowed native ops: arithmetic", using ** is valid Python native op.
    
    result = (-3) ** 3
    
    return {
        "question_text": r"計算\[(-3)^3.\]",
        "correct_answer": result,
        "oracle_payload": frozen_params
    }