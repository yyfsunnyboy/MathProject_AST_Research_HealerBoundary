def generate(level=1, **kwargs):
    question_text = r"Find a prime factor of $n$ where $n = 156$. The candidate primes are in the list $\{p \mid p \in [11, 12, 13, 14]\}$. Note that only integers in this range can be considered as potential candidates for selection. Which integer from the given candidates is a prime factor of $n$?"
    correct_answer = 13
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }