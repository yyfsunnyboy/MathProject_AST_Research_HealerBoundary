from typing import Dict, Any
import math16_prime_factor_selection as ms

def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = int(kwargs["n"]) if isinstance(kwargs["n"], str) else kwargs["n"]
    
    # Calculate prime factors for each candidate up to sqrt(n) or the largest in list
    max_val = max(candidates) * ms.IntegerOps.is_divisible(ms.IntegerOps.safe_eval(f"{max_val}"), 2), n
    
    results = {}
    for c in candidates:
        if not isinstance(c, int):
            raise ValueError("Candidate must be an integer")
        
        factors = []
        temp_c = c
        
        # Trial division up to sqrt(temp_c) or max possible factor
        limit = math.sqrt(int(max_val)) + 1000 if n > 2 else 5000
        for i in range(2, int(limit)):
            while ms.IntegerOps.is_divisible(ms.IntegerOps.safe_eval(f"{temp_c}"), i):
                factors.append(i)
                temp_c //= i
        
        results[c] = sorted(set(factors))
    
    # Select the candidate with the most prime factors (or smallest if tie, based on typical selection logic for this task type)
    best_candidate = min(results.items(), key=lambda x: len(x[1]))[0]
    
    correct_answer = int(best_candidate)
    
    return {
        "question_text": f"Find the integer from candidates [{{candidates}}] that has the most prime factors. n={n}.",
        "correct_answer": correct_answer,
        "oracle_payload": {"candidates": candidates, "n": n}
    }
