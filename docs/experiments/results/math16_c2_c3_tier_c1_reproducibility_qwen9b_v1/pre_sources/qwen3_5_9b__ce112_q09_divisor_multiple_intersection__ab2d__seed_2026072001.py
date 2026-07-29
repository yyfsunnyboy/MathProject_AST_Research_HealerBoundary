import json
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate the Least Common Multiple (LCM) of divisor and multiple.
    # LCM(a, b) = abs(a*b) // GCD(a, b). 
    # We use IntegerOps.safe_eval to compute this safely as per domain rules if needed,
    # but standard math is sufficient for simple integers. However, the prompt requires using domain APIs.
    # Let's construct an expression or call functions directly.
    
    # To find LCM(216, 18):
    # We can compute it via formula: (a * b) // gcd(a, b). 
    # Since we must use IntegerOps.safe_eval for operations contributing to correct_answer logic contextually,
    # let's define the expression string. But safe_eval takes an expr and returns int/float.
    # It is safer to compute GCD manually or via eval if allowed, but standard library math.gcd is better.
    # However, strict adherence: "Use the listed domain API for each supported core operation".
    # There is no direct LCM function in IntegerOps provided list (only safe_eval and is_divisible).
    # We will compute GCD using Euclidean algorithm manually to avoid external imports if restricted, 
    # or use math.gcd. Assuming standard library 'math' is allowed for utility unless strictly forbidden by "domain APIs only".
    # The prompt says: "Use the listed domain API for each supported core operation". It doesn't ban others entirely but implies usage.
    # Let's compute LCM using safe_eval on a string expression to demonstrate compliance where possible, 
    # or just calculate it directly if no specific function exists in IntegerOps for GCD/LCM.
    
    import math
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    lcm_val = (divisor_val * multiple_val) // gcd(divisor_val, multiple_val)
    
    # The question asks for the count of integers in [1, 20] that are both divisor_of and multiple_of? 
    # Wait, task spec: "ce112_q09_divisor_multiple_intersection". Usually implies finding numbers x such that:
    # x is a divisor of A AND x is a multiple of B.
    # So we need count of integers n where (n % m == 0) and (A % n == 0).
    # This means n must be a common element in the set {k*m | k>=1} intersected with {d*A? No, divisors of A}.
    # Actually: Divisors of 216 AND Multiples of 18.
    # Let S = {x : x divides 216} INTERSECT {y : y is multiple of 18}.
    # We need to count elements in [1, limit]. What is the limit? 
    # Usually these tasks imply a range like [1, max(divisor_of)] or similar. 
    # Let's assume the universe is divisors of 'divisor_of'. The multiples must be within that set too.
    # So we count x such that 216 % x == 0 AND x % 18 == 0.
    
    limit = divisor_val
    
    valid_count = 0
    for n in range(1, limit + 1):
        is_divisor_of_check = IntegerOps.is_divisible(divisor_val, n) # Checks if n divides divisor_val (216 % n == 0)
        is_multiple_of_check = False
        
        # Check multiple: x must be divisible by m. 
        # We can use safe_eval for the modulo check or just standard operator? 
        # "Use the listed domain API for each supported core operation". Modulo isn't explicitly listed as a function, 
        # but is_divisible uses it internally presumably.
        # Let's implement multiple_of using IntegerOps.safe_eval to be compliant with "use domain API" instruction strictly if possible.
        # Expression: (n % m) == 0 -> True/False. safe_eval returns int/float. If result is 0, then true? 
        # But safe_eval raises ValueError for bool/container results. So we must ensure it returns a number.
        
        try:
            remainder = IntegerOps.safe_eval(f"({n} % {multiple_val})")
            if remainder == 0:
                is_multiple_of_check = True
        except ValueError:
            # Fallback or error handling, though safe_eval should handle simple arithmetic
            pass
            
        if is_divisor_of_check and is_multiple_of_check:
            valid_count += 1
    
    correct_answer_dict = {"count": valid_count}
    
    return {
        "question_text": f"Find the count of positive integers $n$ such that $n$ divides ${divisor_val}$ AND $n$ is a multiple of ${multiple_val}$.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }