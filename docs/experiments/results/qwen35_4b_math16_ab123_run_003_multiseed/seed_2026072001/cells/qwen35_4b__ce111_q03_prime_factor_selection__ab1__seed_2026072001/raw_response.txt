def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs.get("n", 0)
    
    # Calculate prime factors for each candidate to find the one that divides n exactly and has a specific property (e.g., sum of digits or index)
    # Based on typical selection tasks: Find c in candidates such that c is a divisor of n. If multiple, pick based on difficulty level logic.
    
    divisors = [c for c in candidates if n % c == 0]
    
    if not divisors:
        correct_answer = -1 # Fallback or error state
    else:
        # Simple selection rule: choose the largest divisor found among candidates that divides n exactly
        # For level 1, usually just finding any valid factor is sufficient, but to ensure uniqueness we pick the max.
        if len(divisors) == 0:
            correct_answer = -1
        else:
            correct_answer = max(divisors)

    question_text = r"Given $n = {n}$ and a set of candidate integers $\{c_1, c_2, \dots\} = [{candidates}]$, determine the largest integer from this set that is an exact divisor (factor) of $n$."
    
    return {
        "question_text": question_text.format(n=n, candidates=candidates),
        "correct_answer": correct_answer,
        "oracle_payload": kwargs
    }