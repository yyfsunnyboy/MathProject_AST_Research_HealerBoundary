def generate(level=1, **kwargs):
    expression = "9/(4 - sqrt(7))"
    required_form = "a + b*sqrt(7)"
    target_expression = "a + b"
    
    oracle_payload = {
        "expression": expression,
        "required_form": required_form,
        "target_expression": target_expression
    }
    
    a = 4
    b = 1
    radicand = 7
    value = a + b
    
    correct_answer = {
        "a": a,
        "b": b,
        "radicand": radicand,
        "value": value
    }
    
    question_text = (
        "Rationalize the denominator of the expression:\n"
        "$$\\frac{9}{4 - \\sqrt{7}}$$\n"
        "If the simplified expression is written in the form $a + b\\sqrt{7}$, "
        "where $a$ and $b$ are integers, find the value of $a + b$."
    )
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }