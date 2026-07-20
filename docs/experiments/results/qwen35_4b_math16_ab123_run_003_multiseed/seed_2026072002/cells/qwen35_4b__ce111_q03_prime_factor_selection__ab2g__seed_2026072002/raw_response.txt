def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    
    # Calculate prime factors of n (156)
    # 156 / 2 = 78
    # 78 / 2 = 39
    # 39 / 3 = 13
    # So, 156 = 2^2 * 3^1 * 13^1
    prime_factors = [2, 2, 3, 13]
    
    correct_answer = sum(prime_factors)
    
    question_text = r"Find the sum of all unique prime factors of $n$. Given: $n = 156$."

    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer),
        "oracle_payload": {"candidates": candidates, "n": n}
    }