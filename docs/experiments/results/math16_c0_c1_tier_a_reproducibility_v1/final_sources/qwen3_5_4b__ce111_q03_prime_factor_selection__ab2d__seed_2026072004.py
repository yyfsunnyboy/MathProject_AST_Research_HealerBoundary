import sys
sys.path.insert(0, '..')
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"candidates": [11, 12, 13, 14], "n": 156}
    
    candidates = frozen_params["candidates"]
    n = frozen_params["n"]
    
    correct_answer = None
    
    for candidate in candidates:
        if IntegerOps.is_divisible(n, candidate):
            correct_answer = candidate
            break
    
    question_text = r"Find the prime factor of $156$ from the given list."
    
    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer),
        "oracle_payload": frozen_params
    }