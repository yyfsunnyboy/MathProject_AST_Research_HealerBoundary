def generate(level=1, **kwargs):
    polynomials = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }
    
    dividend_poly = sum(c * (x**i) for i, c in enumerate(reversed(polynomials["dividend_coefficients"])) if len([c for c in polynomials["dividend_coefficients"]]) > 1 and not isinstance(c, float)) or "6 + 4x" # Simplified representation based on coefficients [6, 4, 0] -> 6 + 4x
    divisor_poly = sum(c * (x**i) for i, c in enumerate(reversed(polynomials["divisor_coefficients"])) if len([c for c in polynomials["divisor_coefficients"]]) > 1 and not isinstance(c, float)) or "2" # Simplified representation based on coefficients [2, 0, 0] -> 2
    
    dividend_str = f"{polynomials['dividend_coefficients'][0]} + {polynomials['dividend_coefficients'][1]}x"
    divisor_str = str(polynomials["divisor_coefficients"][0])
    
    # Perform polynomial division manually for [6, 4, 0] divided by [2] (constant)
    # Dividing a quadratic-like structure represented as coefficients [a, b, c] where c=0 effectively means linear if we treat it strictly. 
    # However, standard interpretation of coeffs [c_n, ..., c_1, c_0]: 6 + 4x divided by 2.
    # Quotient: (6/2) + (4/2)x = 3 + 2x. Remainder: 0.
    
    remainder_val = 0
    
    question_text = r"Find the remainder when dividing $P(x)$ by $Q(x)$, where $P(x)$ has coefficients $\{6, 4, 0\}$ and $Q(x)$ has coefficients $\{2, 0, 0\}$. Express your answer in LaTeX."
    correct_answer = f"Remainder: {remainder_val}, Canonical Latex: \\text{{\\$}}0\\text{{\\$}}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": polynomials
    }