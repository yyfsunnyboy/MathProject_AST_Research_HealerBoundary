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
    
    # 1) IntegerOps.prime_factorization(n)
    factors = IntegerOps.prime_factorization(n)
    
    # 2) Choose the candidate that appears as a prime key
    chosen = None
    for c in candidates:
        if c in factors:
            chosen = c
            break
            
    # 3) Assemble correct_answer exactly according to the Answer contract
    question_text = "下列整數 \\(11,12,13,14\\) 中，哪一個是 \\(156\\) 的質因數？"
    
    return {
        "question_text": question_text,
        "correct_answer": chosen,
        "oracle_payload": frozen_params
    }