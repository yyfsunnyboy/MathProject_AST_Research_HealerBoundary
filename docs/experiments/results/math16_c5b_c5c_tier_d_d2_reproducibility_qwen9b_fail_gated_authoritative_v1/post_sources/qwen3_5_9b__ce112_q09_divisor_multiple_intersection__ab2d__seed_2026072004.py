import json
from typing import Dict, Any

# Mocking the required imports from a hypothetical library structure as per instructions
class IntegerOps:
    @staticmethod
    def is_divisible(a: int, b: int) -> bool:
        if b == 0: return False
        try:
            result = core_prompts_domain_function_library_safe_eval(f"{a} % {b}")
            return result == 0
        except ValueError:
            # Fallback for direct calculation in mock environment
            return a % b != 0

    @staticmethod
    def safe_eval(expr: str) -> Any:
        try:
            return eval(expr)
        except Exception as e:
            raise ValueError(f"Safe evaluation failed on {expr}: {e}")


# Re-exporting the module to satisfy import statements if needed in a real context, 
# but here we define it locally for self-containment within this script.
core_prompts_domain_function_library_safe_eval = IntegerOps.safe_eval

def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    # Frozen sampled parameters as per task specification
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]

    # Logic: Find the smallest positive integer that is a multiple of 'multiple_val' 
    # and also divides 'divisor_val'. This implies finding GCD(multiple, divisor) if we were looking for commonality,
    # but strictly "is a multiple OF X" means n = k*X. "Divides Y" means Y % n == 0.
    # We need smallest positive integer N such that:
    # 1. N is a multiple of 'multiple_val' (N % multiple_val == 0)
    # 2. N divides 'divisor_val' ('divisor_val' % N == 0)
    
    # Let's iterate to find the smallest positive integer satisfying both conditions.
    count = 0
    
    # We can start checking from multiples of `multiple_of` upwards until we exceed `divisor_of`.
    current_multiple = multiple_val
    while True:
        is_divisible_check = IntegerOps.is_divisible(divisor_val, current_multiple)
        
        if is_divisible_check:
            count += 1
        
        # Optimization: If the next candidate (current + step) exceeds divisor, stop.
        # However, since we need multiples of `multiple_of`, let's just iterate by steps of `multiple_of`.
        # Actually, simply iterating integers and checking both conditions is safer for small numbers, 
        # but iterating only candidates (multiples of multiple_val) is more efficient.
        
        if current_multiple > divisor_val:
            break
            
        current_multiple += multiple_val
        
    correct_answer = {"count": count}

    question_text = f"Find the number of positive integers that are both a {multiple_val}-th multiple and divide {divisor_val}. Specifically, find how many $n$ satisfy: $n \\equiv 0 \\pmod{{{multiple\_val}}}$ AND ${divisor\\_val} \\equiv 0 \\pmod n$."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }