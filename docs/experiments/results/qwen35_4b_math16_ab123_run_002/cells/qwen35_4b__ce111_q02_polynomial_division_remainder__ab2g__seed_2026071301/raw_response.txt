def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    dividend_poly = f"6x^2 + 4x$"
    divisor_poly = f"2x^3$"
    
    question_text = r"""Compute the remainder when dividing $P(x) = 6x^2 + 4x$ by $Q(x) = 2x^3$. Express your answer in canonical form.

$$\frac{6x^2 + 4x}{2x^3}$$
"""
    
    # Polynomial division: degree(dividend)=2, degree(divisor)=3
    # Since dividend degree < divisor degree, the quotient is 0 and remainder equals dividend.
    correct_remainder = "6x^2 + 4x"
    canonical_latex = r"\text{remainder} = 6x^2 + 4x"
    
    return {
        "question_text": question_text,
        "correct_answer": f"{canonical_latex}\nAnswer: {correct_remainder}",
        "oracle_payload": frozen_params
    }