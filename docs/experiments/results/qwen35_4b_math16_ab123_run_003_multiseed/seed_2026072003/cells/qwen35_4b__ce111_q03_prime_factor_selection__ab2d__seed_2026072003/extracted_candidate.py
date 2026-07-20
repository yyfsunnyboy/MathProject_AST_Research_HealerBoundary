def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 156)
    
    from core.prompts.domain_function_library import IntegerOps
    
    if not IntegerOps.is_divisible(n, 1):
        raise ValueError("N must be divisible by 1")
        
    target_factor = None
    for candidate in candidates:
        try:
            result = IntegerOps.safe_eval(f"{n} / {candidate}")
            if isinstance(result, int) and n % candidate == 0:
                target_factor = candidate
                break
        except ValueError:
            continue
            
    correct_answer = target_factor
    
    return {
        "question_text": r"Find the smallest integer $c$ from the set $\{11, 12, 13, 14\}$ such that $n / c$ is an exact integer. Given $n = 156$, what is $c$?",
        "correct_answer": correct_answer,
        "oracle_payload": {**kwargs}
    }