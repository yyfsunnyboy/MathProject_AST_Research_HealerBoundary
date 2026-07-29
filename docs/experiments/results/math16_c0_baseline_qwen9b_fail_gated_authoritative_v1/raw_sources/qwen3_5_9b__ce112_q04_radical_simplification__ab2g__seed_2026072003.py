def generate(level=1, **kwargs):
    # Frozen sampled parameters from task specification
    radicand = 135
    
    # Simplify radical: sqrt(135) -> sqrt(9 * 15) -> 3*sqrt(15)
    coefficient = 3
    simplified_radicand = 15
    
    # Construct LaTeX strings for the question and answer components
    radicand_latex = f"\\sqrt{{{radicand}}}"
    
    # Question text: Simplify \\sqrt{135}
    question_text = "Simplify $\\\\sqrt{" + str(radicand) + "}$. Express your answer in simplest radical form."
    
    # Correct answer components for the dict
    correct_answer_coefficient = coefficient
    correct_answer_radicand = simplified_radicand
    
    # Canonical LaTeX format: 3\\sqrt{15}
    canonical_latex = f"{coefficient}*\\\\sqrt{{{simplified_radicand}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": correct_answer_coefficient,
            "radicand": correct_answer_radicand,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"radicand": radicand}
    }