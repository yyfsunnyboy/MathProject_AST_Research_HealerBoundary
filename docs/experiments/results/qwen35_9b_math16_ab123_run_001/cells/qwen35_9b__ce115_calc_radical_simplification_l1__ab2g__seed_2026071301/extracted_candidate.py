def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    coefficient = 3
    simplified_radicand = 3
    
    question_text = r"Simplify $\sqrt{" + str(radicand) + "}$."
    
    correct_answer_latex = f"{coefficient}\sqrt{{{simplified_radicand}}}"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_latex,
        "oracle_payload": {"radicand": radicand}
    }