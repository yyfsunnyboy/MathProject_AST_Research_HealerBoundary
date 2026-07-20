def generate(level=1, **kwargs):
    radicand = 27
    coefficient = 3
    
    question_text = r"\text{Simplify } \sqrt{\overline{\mathbf{radicand}}}."
    
    correct_answer = {
        "coefficient": coefficient,
        "radicand": 3,
        "canonical_latex": "\\boxed{\\begin{gathered} \\sqrt[2]{27}=\\sqrt[2]{3^3}\\textbf{ }=\\left(3^{1 / (4)}\\right)^{(4-3) * (4+0)*(-1)+((5*4)-6)/8}}"
    }
    
    oracle_payload = {"radicand": radicand}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }