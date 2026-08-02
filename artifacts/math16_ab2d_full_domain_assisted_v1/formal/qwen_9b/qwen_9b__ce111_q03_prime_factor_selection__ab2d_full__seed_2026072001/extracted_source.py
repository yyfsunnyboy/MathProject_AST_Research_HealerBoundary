from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "candidates": [11, 12, 13, 14],
        "n": 156
    }
    
    prime_factors = IntegerOps.prime_factorization(frozen_params["n"])
    
    correct_answer = None
    for candidate in frozen_params["candidates"]:
        if candidate in prime_factors:
            correct_answer = candidate
            break
            
    return {
        "question_text": "下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }