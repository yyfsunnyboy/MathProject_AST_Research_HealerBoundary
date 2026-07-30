from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 156)
    
    correct_answer = None
    for c in candidates:
        is_c_prime = True
        if c < 2:
            is_c_prime = False
        else:
            for i in range(2, c):
                if IntegerOps.is_divisible(c, i):
                    is_c_prime = False
                    break
        
        if is_c_prime and IntegerOps.is_divisible(n, c):
            correct_answer = c
            break
            
    candidates_str = ", ".join(f"${cand}$" for cand in candidates)
    question_text = f"Which of the following is a prime factor of ${n}$?\nCandidates: {candidates_str}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "candidates": candidates,
            "n": n
        }
    }