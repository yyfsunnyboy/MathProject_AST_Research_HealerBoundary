def generate(level=1, **kwargs):
    radicand = 135
    
    # Simplify sqrt(135)
    # 135 = 9 * 15 = 3^2 * (3 * 5)
    # sqrt(135) = 3 * sqrt(15)
    
    coefficient = 3
    simplified_radicand = 15
    
    question_text = r"\text{Simplify the radical: } \sqrt{\overline{\text{{radicand}}}}"
    correct_answer_latex = f"\\frac{{{coefficient}}}{{1}}\sqrt{{{simplified_radicand}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coefficient,
            "radicand": simplified_radicand,
            "canonical_latex": correct_answer_latex
        },
        "oracle_payload": {'radicand': 135}
    }