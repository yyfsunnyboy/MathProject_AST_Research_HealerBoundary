def generate(level=1, **kwargs):
    expression = "(2*sqrt(3) + sqrt(6))*sqrt(2)"
    question_text = f"Simplify the expression: {expression}"
    correct_answer = {
        "terms": [
            {"coefficient": 2, "radicand": 3},
            {"coefficient": 2, "radicand": 6}
        ]
    }
    oracle_payload = {
        "expression": expression
    }
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }