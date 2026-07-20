def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the number of positive integers that are both a divisor of 216 and a multiple of 18.",
        "correct_answer": {"count": 3},
        "oracle_payload": {"divisor_of": 216, "multiple_of": 18}
    }