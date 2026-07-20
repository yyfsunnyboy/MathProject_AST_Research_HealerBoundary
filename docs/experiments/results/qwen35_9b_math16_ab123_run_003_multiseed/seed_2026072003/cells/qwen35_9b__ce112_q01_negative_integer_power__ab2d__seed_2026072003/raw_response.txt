import re
from typing import Dict, Any
from math import pow as _pow

def generate(level=1, **kwargs):
    frozen = kwargs.get("frozen", {"base": -3, "exponent": 3})
    
    # Verify keys in oracle_payload match the contract (though we just return it)
    if not isinstance(frozen, dict):
        raise ValueError("oracle_payload must be a dict")
        
    base = frozen["base"]
    exponent = frozen["exponent"]
    
    try:
        correct_answer = int(_pow(base, exponent))
    except OverflowError:
        # Handle potential overflow if numbers are too large for standard types in this context
        # though Python handles arbitrarily large integers. The constraint is just to ensure it's an integer result.
        raise ValueError("Result exceeds reasonable bounds")

    question_text = f"Calculate $(-{base})^{{{exponent}}}$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen
    }