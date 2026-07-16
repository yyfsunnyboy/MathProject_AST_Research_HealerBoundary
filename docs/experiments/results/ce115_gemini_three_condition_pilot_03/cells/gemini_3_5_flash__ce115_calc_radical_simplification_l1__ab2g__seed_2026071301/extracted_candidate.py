def generate(level=1, **kwargs):
    radicand_input = 27
    
    coefficient = 1
    temp = radicand_input
    d = 2
    while d * d <= temp:
        while temp % (d * d) == 0:
            coefficient *= d
            temp //= (d * d)
        d += 1
        
    question_text = f"Simplify the radical expression: \\sqrt{{{radicand_input}}}"
    
    correct_answer = {
        "coefficient": coefficient,
        "radicand": temp
    }
    
    oracle_payload = {
        "radicand": radicand_input
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }