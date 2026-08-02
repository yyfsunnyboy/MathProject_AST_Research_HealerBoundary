from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = {
        "candidates": [11, 12, 13, 14],
        "n": 156
    }
    
    # Determine the correct answer by checking divisibility for each candidate
    candidates_list = frozen["candidates"]
    n_val = frozen["n"]
    
    found_answer = None
    
    for cand in candidates_list:
        if IntegerOps.is_divisible(n_val, cand):
            found_answer = cand
            break
            
    return {
        "question_text": "下列整數 \(11,12,13,14\) 中，哪一個是 \(156\) 的質因數？",
        "correct_answer": found_answer,
        "oracle_payload": frozen
    }