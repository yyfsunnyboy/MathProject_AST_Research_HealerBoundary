def generate(level=1, **kwargs):
    return {
        "question_text": r"Select all prime factors of $n = 156$ from the given candidates: $\{11, 12, 13, 14\}$.",
        "correct_answer": 13,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }