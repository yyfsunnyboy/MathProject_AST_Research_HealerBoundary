def generate(level=1, **kwargs):
    radicand_input = kwargs.get("radicand", 27)
    
    coefficient = 1
    temp_radicand = radicand_input
    d = 2
    while d * d <= temp_radicand:
        while temp_radicand % (d * d) == 0:
            coefficient *= d
            temp_radicand //= (d * d)
        d += 1
        
    question_text = f"Simplify the radical expression: \\sqrt{{{radicand_input}}}"
    
    correct_answer = {
        "coefficient": coefficient,
        "radicand": temp_radicand
    }
    
    oracle_payload = {
        "radicand": radicand_input
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }