from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {
        "candidates": [11, 12, 13, 14],
        "n": 156
    }
    
    factors = IntegerOps.prime_factorization(frozen["n"])
    
    correct_answer = None
    
    for candidate in frozen["candidates"]:
        if candidate == 1:
            continue
        
        is_divisible = IntegerOps.is_divisible(candidate, frozen["n"])
        
        if not is_divisible:
            continue
            
        prime_factors = factors.get(candidate)
        
        if prime_factors and prime_factors > 0:
            correct_answer = candidate
    
    question_text = "下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen
    }
