from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "candidates": [
            11,
            12,
            13,
            14
        ],
        "n": 156
    }
    
    n = frozen_params["n"]
    candidates = frozen_params["candidates"]
    
    factors = IntegerOps.prime_factorization(n)
    
    correct_answer = None
    for c in candidates:
        if c in factors:
            correct_answer = c
            break
            
    question_text = "下列整數 \\(11,12,13,14\\) 中，哪一個是 \\(156\\) 的質因數？"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
