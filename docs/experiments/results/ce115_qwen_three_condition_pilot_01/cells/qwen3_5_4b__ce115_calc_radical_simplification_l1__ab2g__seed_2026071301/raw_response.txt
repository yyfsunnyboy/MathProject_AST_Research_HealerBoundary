def generate(level=1, **kwargs):
    radicand = 27
    
    # Calculate simplest radical form for sqrt(27)
    # 27 = 9 * 3 = 3^2 * 3
    # sqrt(27) = sqrt(3^2 * 3) = 3 * sqrt(3)
    
    coefficient = 3
    radicand_simplified = 3
    
    question_text = f"Simplify the radical expression: \\sqrt{{{radicand}}}"
    
    correct_answer = {
        "coefficient": int(coefficient),
        "radicand": int(radicand_simplified)
    }
    
    oracle_payload = {"radicand": radicand}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }