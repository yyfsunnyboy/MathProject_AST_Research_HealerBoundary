def generate(level=1, **kwargs):
    radicand = 27
    coefficient = 3
    
    question_text = r"$$\sqrt{27} = \text{coefficient} \cdot \sqrt{\text{radicand}}$$"
    
    correct_answer = {
        "coefficient": 3,
        "radicand": 3,
        "canonical_latex": "$$\\sqrt{27} = 3 \\sqrt{3}$$"
    }
    
    oracle_payload = {"radicand": radicand}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }