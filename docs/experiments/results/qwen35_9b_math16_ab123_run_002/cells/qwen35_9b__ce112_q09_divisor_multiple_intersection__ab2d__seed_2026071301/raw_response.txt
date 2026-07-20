import json
from math import gcd
try:
    from core.prompts.domain_function_library import IntegerOps
except ImportError:
    def is_divisible(a, b):
        return a % b == 0 if b != 0 else False
    
    class IntegerOps:
        @staticmethod
        def safe_eval(expr):
            # Simplified implementation for integer arithmetic context
            try:
                result = eval(expr)
                if isinstance(result, bool) or (isinstance(result, float) and not result.is_integer()):
                    raise ValueError("Result must be an int")
                return int(result)
            except Exception as e:
                raise ValueError(f"Safe evaluation failed: {e}")

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate the smallest positive integer that is a multiple of 'multiple_val' 
    # and also a divisor of 'divisor_val'.
    # This is equivalent to finding multiples of M: k*M, such that (k*M) divides D.
    # The set of common elements between {x | x % M == 0} and {y | y % D == 0}.
    
    count = 0
    
    # Iterate through all divisors of divisor_val to check if they are multiples of multiple_val
    for i in range(1, divisor_val + 1):
        is_divisor_of_check = IntegerOps.is_divisible(divisor_val, i)
        
        if is_divisor_of_check:
            is_multiple_of_check = False
            
            # Check divisibility using domain API where possible or fallback logic
            try:
                rem = IntegerOps.safe_eval(f"{i} % {multiple_val}")
                if rem == 0:
                    is_multiple_of_check = True
            except ValueError:
                pass
                
            if is_multiple_of_check:
                count += 1
    
    # Alternatively, using GCD property: 
    # The number of common elements between multiples of A and divisors of B.
    # Let S_A be set of multiples of M within [1, D]. Count = floor(D/M).
    # We need those x where x is multiple of M AND x divides D.
    # This means x must divide gcd(M*M*k, D) logic? 
    # Actually simpler: iterate divisors of D and count how many are multiples of M.
    
    correct_answer = {"count": count}
    
    return {
        "question_text": r"Find the number of positive integers that are both a divisor of $216$ and a multiple of $18$. Use formal LaTeX delimiters for math expressions.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }