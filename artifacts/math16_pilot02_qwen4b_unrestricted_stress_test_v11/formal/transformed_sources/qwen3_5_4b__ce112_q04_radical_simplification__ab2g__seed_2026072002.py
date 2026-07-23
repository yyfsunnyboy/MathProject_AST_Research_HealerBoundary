def generate(level=1, **kwargs):
    radicand = 135
    
    # Simplify sqrt(135)
    # 135 = 81 * 1.5 is wrong. 
    # 135 / 9 = 15 -> not a square.
    # 135 / 27 = 5 (not integer radicand simplification usually targets perfect squares).
    # Let's re-evaluate prime factorization: 135 = 5 * 27 = 5 * 3^3 = 3^2 * 5 * 3.
    # sqrt(135) = sqrt(9 * 15) = 3 * sqrt(15).
    
    coefficient = 3
    simplified_radicand = 15
    
    question_text = r"$$\sqrt{135}$$"
    correct_answer_coefficient = str(coefficient)
    correct_answer_simplified_radicand = str(simplified_radicand)
    canonical_latex = f"$\\sqrt{{{simplified_radicand}}}$"

    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": correct_answer_coefficient,
            "radicand": int(correct_answer_simplified_radicand),
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {'radicand': 135}
    }