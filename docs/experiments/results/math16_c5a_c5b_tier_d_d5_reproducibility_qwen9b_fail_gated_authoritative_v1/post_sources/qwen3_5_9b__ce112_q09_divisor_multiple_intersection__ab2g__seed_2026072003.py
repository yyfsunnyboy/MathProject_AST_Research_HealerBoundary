def generate(level=1, **kwargs):
    question_text = r"""Find the number of positive integers $n$ such that $n$ is a divisor of 216 and simultaneously a multiple of 18."""
    correct_answer = {"count": 3}
    oracle_payload = {"divisor_of": 216, "multiple_of": 18}
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }