def generate(level=1, **kwargs):
    frozen_params = {"radicand": 27}
    
    radicand = frozen_params["radicand"]
    
    # Simplify sqrt(27) -> 3*sqrt(3)
    coefficient = 3
    simplified_radicand = 3
    
    question_text = r"Simplify the radical expression: $\sqrt{" + str(radicand) + "}$."
    correct_answer_str = f"{coefficient}\\sqrt{{{simplified_radicand}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": frozen_params
    }