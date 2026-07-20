def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    # Factorization for simplification: 27 = 3^3 * 3^(0) -> sqrt(27) = 3*sqrt(3)
    # For level 1 radical simplification of x^n where n is odd and > 1, we look for square factors.
    # 27 = 9 * 3 = 3^2 * 3. So sqrt(27) = 3 * sqrt(3).
    
    coefficient = 3
    simplified_radicand = 3
    
    question_text = f"Simplify the radical expression $\\sqrt{{{radicand}}}$."
    correct_answer_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"
    canonical_latex = correct_answer_latex

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_latex,
        "oracle_payload": {"radicand": radicand}
    }