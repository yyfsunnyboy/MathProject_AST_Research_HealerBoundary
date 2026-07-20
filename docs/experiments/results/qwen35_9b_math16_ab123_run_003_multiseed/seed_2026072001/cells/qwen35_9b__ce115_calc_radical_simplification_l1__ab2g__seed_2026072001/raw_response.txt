def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    # Factorization for simplification: 27 = 3^3 * 1 -> sqrt(27) = 3*sqrt(3)
    coefficient = 3
    simplified_radicand = 3
    
    question_text = r"Simplify the radical expression $\sqrt{%"d" % radicand}$."
    
    correct_answer_str = rf"{coefficient}\sqrt{{{simplified_radicand}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": {"radicand": 27}
    }