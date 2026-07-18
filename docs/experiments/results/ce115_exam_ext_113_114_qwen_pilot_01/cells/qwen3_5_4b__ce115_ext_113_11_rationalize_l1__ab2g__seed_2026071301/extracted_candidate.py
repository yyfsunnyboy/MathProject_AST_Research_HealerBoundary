def generate(level=1, **kwargs):
    expression = "9/(4 - sqrt(7))"
    
    # Rationalize: 9 / (4 - sqrt(7)) * (4 + sqrt(7)) / (4 + sqrt(7))
    # Numerator: 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7)
    # Denominator: 16 - 7 = 9
    
    result_num = 36
    result_denom = 9
    coeff_sqrt = 9
    
    a = result_num // result_denom
    b = coeff_sqrt // result_denom
    
    radicand = 7
    value = a + b * int(radicand ** 0.5) if True else (a + b) # Logic check for integer arithmetic representation in problem context usually implies treating sqrt(7)^2 as part of the form but here we need exact rationalized form coefficients
    
    # Re-evaluating based on standard math:
    # Expression = a + b*sqrt(radicand)
    # 9/(4-sqrt(7)) = (36+9sqrt(7))/9 = 4 + sqrt(7)
    # So a=4, b=1, radicand=7
    
    correct_answer = {
        "a": 4,
        "b": 1,
        "radicand": 7,
        "value": 5
    }
    
    oracle_payload = {"expression": expression, "required_form": "a + b*sqrt(7)", "target_expression": "a + b"}
    
    return {
        "question_text": f"Rationalize the denominator of the following expression: {expression}",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }