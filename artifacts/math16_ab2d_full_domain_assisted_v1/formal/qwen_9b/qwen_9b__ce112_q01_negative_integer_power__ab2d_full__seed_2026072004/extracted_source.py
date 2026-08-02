from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    # Compute (-3)^3 using native arithmetic as per step 1 instructions.
    # The domain API safe_eval is not strictly needed for simple integer power if we use **, 
    # but the contract says "Compute base ** exponent with native arithmetic".
    # However, to ensure JSON safety and adherence to allowed ops without relying on Python's ** directly 
    # (if that were forbidden by some hidden constraint) or simply using it:
    # The prompt allows native ops. (-3)**3 is -27.
    
    base = frozen_params["base"]
    exponent = frozen_params["exponent"]
    
    result = base ** exponent
    
    return {
        "question_text": r"計算\[(-3)^3.\]",
        "correct_answer": result,
        "oracle_payload": frozen_params
    }