def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    coeff = 1
    temp = radicand
    d = 2
    while d * d <= temp:
        if temp % (d * d) == 0:
            coeff *= d
            temp //= (d * d)
        else:
            d += 1
            
    question_text = f"Simplify the radical: \\sqrt{{{radicand}}}"
    
    correct_answer = {
        "coefficient": coeff,
        "radicand": temp
    }
    
    oracle_payload = {
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }