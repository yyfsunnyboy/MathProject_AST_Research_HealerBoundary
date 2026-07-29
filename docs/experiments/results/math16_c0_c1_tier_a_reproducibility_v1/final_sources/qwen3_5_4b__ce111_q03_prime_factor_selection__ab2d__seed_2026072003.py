def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import IntegerOps
    
    frozen_params = {"candidates": [11, 12, 13, 14], "n": 156}
    
    candidates = frozen_params["candidates"]
    n = frozen_params["n"]
    
    correct_answer = None
    for c in candidates:
        if IntegerOps.is_divisible(n, c):
            correct_answer = c
            break
    
    question_text = r"Find the prime factor of $156$ from the given list."
    
    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer),
        "oracle_payload": frozen_params
    }