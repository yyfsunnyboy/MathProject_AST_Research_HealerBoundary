def generate(level=1, **kwargs):
    expression = "(2*sqrt(3) + sqrt(6))*sqrt(2)"
    question_text = "Simplify the expression: (2*sqrt(3) + sqrt(6))*sqrt(2)"
    
    # (2*sqrt(3) + sqrt(6))*sqrt(2) = 2*sqrt(6) + sqrt(12) = 2*sqrt(6) + 2*sqrt(3)
    # Sorted by increasing radicand: 2*sqrt(3) + 2*sqrt(6)
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