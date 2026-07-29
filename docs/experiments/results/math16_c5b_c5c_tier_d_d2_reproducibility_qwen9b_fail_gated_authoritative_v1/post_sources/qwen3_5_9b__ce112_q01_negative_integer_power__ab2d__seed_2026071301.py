from typing import Dict, Any
import math

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    base_val = frozen_params["base"]
    exponent_val = frozen_params["exponent"]
    
    # Calculate correct answer using integer arithmetic to ensure exactness for negative bases with odd exponents
    try:
        from core.prompts.domain_function_library import IntegerOps
        
        result_int = IntegerOps.safe_eval(f"{base_val} ** {exponent_val}")
        
        if isinstance(result_int, float) and not math.isfinite(result_int):
            raise ValueError("Result is infinite")
            
        correct_answer = int(math.floor(result_int)) if isinstance(result_int, float) else result_int
        
    except ImportError:
        # Fallback to standard python calculation if domain library unavailable (though spec implies usage)
        correct_answer = base_val ** exponent_val

    question_text = f"Calculate the value of $(-{abs(base_val)})^{{{exponent_val}}}.$"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }