import json
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate the Least Common Multiple (LCM) of divisor and multiple to find a valid intersection point.
    # LCM(a, b) = abs(a*b) // GCD(a, b). We can use IntegerOps.safe_eval for calculation if needed, 
    # but standard math is safer here unless forced. However, the prompt requires using domain APIs for operations.
    # Let's compute GCD first to get LCM. Since we don't have a direct GCD API in the list, 
    # we must rely on safe_eval or implement logic that uses allowed functions if possible.
    # The constraint says "Use the listed domain API for each supported core operation".
    # We will use IntegerOps.safe_eval to compute LCM directly using math library inside eval string? 
    # No, better to stick strictly to provided APIs. If GCD is not an API, we might need safe_eval with a helper or just calculate manually if allowed.
    # Re-reading: "Use the listed domain API for each supported core operation". It implies standard arithmetic might be fallback or via eval.
    # Let's use IntegerOps.safe_eval to compute LCM using math.gcd logic embedded in string? 
    # Actually, let's just calculate manually and verify divisibility with is_divisible if needed.
    
    import math
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    lcm_val = (divisor_val * multiple_val) // gcd(divisor_val, multiple_val)
    
    # We need to find the count of integers in some range? The task description "ce112_q09_divisor_multiple_intersection" 
    # usually implies finding numbers that are both divisors and multiples. 
    # A number X is a divisor of D if D % X == 0.
    # A number Y is a multiple of M if Y % M == 0.
    # Intersection: Numbers that divide 'divisor_of' AND are multiples of 'multiple_of'.
    # Let N be such a number. 
    # Condition 1: divisor_val % N == 0 (N divides divisor_val)
    # Condition 2: N is multiple of multiple_val => N = k * multiple_val for integer k >= 1.
    
    count = 0
    
    # Iterate through multiples of 'multiple_of' up to 'divisor_of'.
    # Since N must divide divisor_val, N cannot exceed divisor_val (assuming positive integers).
    current_multiple = multiple_val
    while current_multiple <= divisor_val:
        if IntegerOps.is_divisible(divisor_val, current_multiple):
            count += 1
        current_multiple += multiple_val
        
    correct_answer_dict = {"count": count}
    
    return {
        "question_text": r"Find the number of positive integers that are both divisors of $216$ and multiples of $18$. Let this count be denoted by $C$. Return $\{ \text{"count"}: C \}$.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }