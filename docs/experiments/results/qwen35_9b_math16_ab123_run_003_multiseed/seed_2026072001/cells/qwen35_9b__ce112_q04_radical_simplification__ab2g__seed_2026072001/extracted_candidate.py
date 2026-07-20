def generate(level=1, **kwargs):
    frozen_params = {"radicand": 135}
    
    radicand = frozen_params["radicand"]
    # Factorize radicand to simplify radical: 135 = 27 * 5 = (3^3) * 5
    # sqrt(135) = sqrt(9*3*5) -> wait, 135 = 81 * ? no. 
    # 135 / 9 = 15. So sqrt(135) = sqrt(9)*sqrt(15) = 3*sqrt(15).
    
    simplified_coefficient = 3
    simplified_radicand = 15
    
    question_text = r"Express $\sqrt{135}$ in the form $a\sqrt{b}$, where $a$ and $b$ are integers and $b$ has no perfect square factors other than 1."

    correct_answer_latex = f"{simplified_coefficient}\\sqrt{{{simplified_radicand}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_latex,
        "oracle_payload": frozen_params
    }