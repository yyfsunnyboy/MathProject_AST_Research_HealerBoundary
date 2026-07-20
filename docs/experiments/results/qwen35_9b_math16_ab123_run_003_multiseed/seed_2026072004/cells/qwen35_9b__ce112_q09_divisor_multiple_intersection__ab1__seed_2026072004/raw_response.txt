def generate(level=1, **kwargs):
    return {
        "question_text": r"Let $D = 216$ and $M = 18$. Find the number of positive integers that are both a divisor of $D$ and a multiple of $M$.",
        "correct_answer": {"count": 4},
        "oracle_payload": {"divisor_of": 216, "multiple_of": 18}
    }