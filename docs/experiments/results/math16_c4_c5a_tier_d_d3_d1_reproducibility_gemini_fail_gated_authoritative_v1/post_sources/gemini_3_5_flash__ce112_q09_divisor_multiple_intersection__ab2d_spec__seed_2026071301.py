# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    divisor_of = 216
    multiple_of = 18

    count = 0
    if divisor_of % multiple_of == 0:
        for x in range(multiple_of, divisor_of + 1, multiple_of):
            if divisor_of % x == 0:
                count += 1

    question_text = (
        f"How many positive integers $x$ are both a multiple of {multiple_of} "
        f"and a divisor of {divisor_of}?"
    )

    correct_answer = {
        "count": count
    }

    oracle_payload = {
        "divisor_of": divisor_of,
        "multiple_of": multiple_of
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }