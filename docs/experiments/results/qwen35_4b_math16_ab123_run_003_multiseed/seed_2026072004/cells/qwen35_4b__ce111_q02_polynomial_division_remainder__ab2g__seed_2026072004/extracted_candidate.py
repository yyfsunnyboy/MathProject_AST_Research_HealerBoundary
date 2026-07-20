def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    # Polynomial division: (6x^2 + 4) / (2x^2) -> remainder is 4
    
    question_text = r"""Perform polynomial long division to find the remainder of $\frac{P(x)}{D(x)}$ where $P(x)$ has coefficients \([6, 4, 0]\) and \(D(x)\) has coefficients \([2, 0, 0]\). Find only the remainder."""
    
    correct_answer = {
        "remainder": 4,
        "canonical_latex": "\\text{Remainder} = 4"
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }