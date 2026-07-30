# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters
    denominator = "4-sqrt(7)"
    numerator = 9
    radicand = 7

    # Rationalizing 9 / (4 - sqrt(7)):
    # Multiply numerator and denominator by (4 + sqrt(7)):
    # Denominator: (4 - sqrt(7))(4 + sqrt(7)) = 16 - 7 = 9
    # Numerator: 9 * (4 + sqrt(7))
    # Expression becomes: (9 * (4 + sqrt(7))) / 9 = 4 + 1*sqrt(7)
    # Thus, a = 4, b = 1
    # a + b = 5
    correct_answer = 5

    question_text = (
        "Rationalize the denominator of the expression "
        "\\(\\frac{9}{4 - \\sqrt{7}}\\). "
        "Write the result in the form \\(a + b\\sqrt{7}\\), "
        "where \\(a\\) and \\(b\\) are integers. "
        "What is the value of \\(a + b\\)?"
    )

    oracle_payload = {
        "denominator": denominator,
        "numerator": numerator,
        "radicand": radicand
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }