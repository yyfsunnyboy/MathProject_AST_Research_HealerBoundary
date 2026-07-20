def generate(level=1, **kwargs):
    question_text = r"Express $\sqrt{135}$ in simplest radical form."
    coefficient = 3
    radicand = 3
    canonical_latex = f"{coefficient}\\sqrt{{{radicand}}}"
    correct_answer = rf"${canonical_latex}$"
    oracle_payload = {"radicand": 135}
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }