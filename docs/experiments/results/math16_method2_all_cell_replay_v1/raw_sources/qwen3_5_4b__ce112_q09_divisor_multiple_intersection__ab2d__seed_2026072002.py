import json
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate LCM using the formula: lcm(a,b) = (a*b)/gcd(a,b)
    # Since we need numbers that are multiples of 'multiple_val' AND divisible by 'divisor_val',
    # these numbers must be common multiples. The smallest positive integer satisfying both conditions is their LCM.
    
    from core.prompts.domain_function_library import IntegerOps
    
    try:
        gcd_result = IntegerOps.safe_eval(f"import math; math.gcd({multiple_val}, {divisor_val})")
        lcm_num = (multiple_val * divisor_val) // int(gcd_result)
        
        # Verify the logic with domain APIs if needed, but direct calculation is robust for integers.
        # Check: Is lcm divisible by multiple? Yes. Is it a multiple of divisor? Yes.
    except Exception as e:
        raise ValueError(f"Calculation failed: {e}")

    correct_answer = {"count": int(lcm_num)}
    
    question_text = r"""Find the smallest positive integer that is both a multiple of $18$ and divisible by $216$. Express your answer as an integer."""
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }