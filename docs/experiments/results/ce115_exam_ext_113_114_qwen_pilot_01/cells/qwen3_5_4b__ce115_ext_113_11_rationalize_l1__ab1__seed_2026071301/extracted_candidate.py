def generate(level=1, **kwargs):
    import json
    
    expression = "9/(4 - sqrt(7))"
    
    # Rationalize: 9 / (4 - sqrt(7)) * (4 + sqrt(7)) / (4 + sqrt(7))
    # Numerator: 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7)
    # Denominator: 16 - 7 = 9
    
    a = 36 // 9
    b = 9 // 9
    radicand = 7
    
    correct_answer = {
        "a": int(a),
        "b": int(b),
        "radicand": int(radicand),
        "value": int(a + b)
    }
    
    oracle_payload = {"expression": expression, "required_form": "a + b*sqrt(7)", "target_expression": f"{int(correct_answer['a'])} + {int(correct_answer['b'])}"}
    
    return {
        "question_text": f"Simplify the expression: {expression}. Express your answer in the form a + b*{radicand}, where a and b are integers.",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }