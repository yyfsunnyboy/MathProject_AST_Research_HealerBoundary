def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135)
    
    # Simplify sqrt(135) -> sqrt(9*15) -> 3*sqrt(15)
    coefficient = 3
    simplified_radicand = 15
    
    question_text = r"Simplify the radical expression: \(\sqrt{%d}\)" % radicand
    correct_answer_latex = rf"{{coefficient}}\cdot\sqrt{{{simplified_radicand}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": f"{coefficient}*\\sqrt{{{simplified_radicand}}}",
        "oracle_payload": {"radicand": radicand}
    }