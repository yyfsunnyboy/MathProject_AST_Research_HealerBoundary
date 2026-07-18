from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Frozen parameters
    candidates = [11, 12, 13, 14]
    n = 156
    
    # Find the correct answer
    correct_answer = None
    for c in candidates:
        # Check if c is prime
        is_c_prime = True
        if c < 2:
            is_c_prime = False
        else:
            for i in range(2, int(c**0.5) + 1):
                if IntegerOps.is_divisible(c, i):
                    is_c_prime = False
                    break
        
        if is_c_prime and IntegerOps.is_divisible(n, c):
            correct_answer = c
            break
            
    candidates_str = ", ".join(f"${c}$" for c in candidates)
    question_text = f"Which of the following is a prime factor of ${n}$?\nCandidates: {candidates_str}."
    
    oracle_payload = {
        "candidates": candidates,
        "n": n
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }