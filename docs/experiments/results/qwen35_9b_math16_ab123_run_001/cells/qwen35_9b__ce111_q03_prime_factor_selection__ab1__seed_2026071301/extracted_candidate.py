def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the number of integers $x$ such that $1 \le x \le 450$, where $\gcd(x, 6) = 1$.",
        "correct_answer": 300,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }