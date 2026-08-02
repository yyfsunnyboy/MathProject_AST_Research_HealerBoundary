from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "candidates": [11, 12, 13, 14],
        "n": 156
    }
    
    # Get prime factorization of n (156) to find the actual primes involved
    factors_dict = IntegerOps.prime_factorization(frozen_params["n"])
    
    # Find which candidate is a prime divisor by checking if it's in the keys of the factorization dict
    correct_answer = None
    for c in frozen_params["candidates"]:
        if c in factors_dict:
            correct_answer = c
            break
    
    return {
        "question_text": f"下列整數 (11, 12, 13, 14) 中，哪一個是 {frozen_params['n']} 的質因數？",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
