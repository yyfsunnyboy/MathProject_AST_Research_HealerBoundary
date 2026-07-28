def generate(level=1, **kwargs):
    radicand = 27
    coefficient = 3
    
    question_text = r"$$\sqrt{27} = \textbf{\underline{\hspace{1cm}}}\sqrt[?]{\textbf{\underline{\hspace{0.5cm}}}}$$"
    
    correct_answer = {
        "coefficient": coefficient,
        "radicand": 3,
        "canonical_latex": r"\sqrt{27} = \mathbf{3}\sqrt[1]{\mathbf{3}}"
    }
    
    oracle_payload = {"radicand": radicand}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }