def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    dividend_poly_str = r"6x^2 + 4x"
    divisor_poly_str = r"2x^2"
    
    # Perform polynomial division: (6x^2 + 4x) / (2x^2)
    # Quotient: 3, Remainder: 4x
    
    question_text = f"Determine the remainder when $P(x) = {dividend_poly_str}$ is divided by $D(x) = {divisor\_poly\_str}$. Express your answer in canonical form."
    
    correct_answer_remainder = "4x"
    canonical_latex = r"4x"
    
    return {
        "question_text": question_text,
        "correct_answer": f"{canonical_latex}",
        "oracle_payload": frozen_params
    }