from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "candidates": [11, 12, 13, 14],
        "n": 156
    }
    
    # We need to find which candidate is a prime factor of n.
    # A number x is a prime factor if:
    # 1. IntegerOps.is_divisible(n, x) is True (x divides n)
    # 2. The result of IntegerOps.prime_factorization(x) has exactly one key and its value is 1
    
    target_n = frozen_params["n"]
    candidates_list = frozen_params["candidates"]
    
    correct_answer = None
    
    for candidate in candidates_list:
        if IntegerOps.is_divisible(target_n, candidate):
            # Check if it's prime by factorization
            factors = IntegerOps.prime_factorization(candidate)
            
            # A number is prime if its factorization dict has exactly one entry with exponent 1
            # Note: The API returns {} for ±1. Our candidates are >1, so we don't worry about that edge case here.
            if len(factors) == 1 and list(factors.values())[0] == 1:
                correct_answer = candidate
    
    return {
        "question_text": "下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }