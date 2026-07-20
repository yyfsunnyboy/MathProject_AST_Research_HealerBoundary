def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    
    correct_answer = None
    for candidate in candidates:
        temp_n = n
        count = 0
        divisor = 2
        while temp_n > 1:
            if temp_n % divisor == 0:
                count += 1
                temp_n //= divisor
            else:
                divisor += 1
        
    question_text = r"Find the integer from the set $\{11, 12, 13, 14\}$ that divides $n=156$ exactly once."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"candidates": candidates, "n": n}
    }