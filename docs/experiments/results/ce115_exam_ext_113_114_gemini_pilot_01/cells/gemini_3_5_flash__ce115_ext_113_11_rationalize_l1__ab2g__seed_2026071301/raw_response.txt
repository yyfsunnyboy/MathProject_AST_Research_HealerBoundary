def generate(level=1, **kwargs):
    oracle_payload = {
        "expression": "9/(4 - sqrt(7))",
        "required_form": "a + b*sqrt(7)",
        "target_expression": "a + b"
    }
    
    # Rationalizing 9 / (4 - sqrt(7)):
    # Multiply numerator and denominator by (4 + sqrt(7))
    # Denominator: (4 - sqrt(7))(4 + sqrt(7)) = 16 - 7 = 9
    # Numerator: 9 * (4 + sqrt(7))
    # Fraction: 9 * (4 + sqrt(7)) / 9 = 4 + 1 * sqrt(7)
    # Thus, a = 4, b = 1, radicand = 7
    # value = a + b = 5
    
    a = 4
    b = 1
    radicand = 7
    value = a + b
    
    question_text = (
        "Rationalize the denominator of the expression:\n"
        "$$\\frac{9}{4 - \\sqrt{7}}$$\n"
        "Write the result in the form $a + b\\sqrt{7}$, where $a$ and $b$ are integers.\n"
        "Find the value of $a + b$."
    )
    
    correct_answer = {
        "a": a,
        "b": b,
        "radicand": radicand,
        "value": value
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }