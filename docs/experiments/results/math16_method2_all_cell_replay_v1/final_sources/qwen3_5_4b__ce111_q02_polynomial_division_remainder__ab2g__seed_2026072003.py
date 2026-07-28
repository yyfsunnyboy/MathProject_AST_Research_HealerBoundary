def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    # Convert coefficients to polynomials: a_n*x^n + ... + a_1*x + a_0
    def poly_to_expr(coeffs):
        terms = []
        for i, c in enumerate(reversed(coeffs)):
            if c != 0:
                x_power = "x" * (len(coeffs) - i)
                term = f"{c}{x_power}" if len(x_power) > 1 else str(c) + ("^2" if len(x_power)==2 and int(term[-1]) == '4' else "") # Simplified logic for specific case [6,4,0] -> 6x^3+4
                terms.append(f"{c} * x^{len(coeffs)-i}" if c != 0 else "0")
        return "+".join(terms)

    dividend_str = poly_to_expr(dividend_coeffs).replace("+", "\\+")
    
    # Perform polynomial division manually for [6, 4, 0] / [2, 0, 0] (which is 2x^3 + 0x^2 + 0x -> wait, divisor coeffs are [2,0,0] meaning degree 2? 
    # Standard convention: coeff list usually starts from highest power.
    # Divisor [2, 0, 0] implies 2*x^2 + 0*x + 0 = 2x^2.
    # Dividend [6, 4, 0] implies 6*x^3 + 4*x^2 + 0*x = 6x^3 + 4x^2.
    
    # Division: (6x^3 + 4x^2) / (2x^2)
    # Quotient term 1: 6/2 * x^(3-2) = 3x
    
    correct_answer_remainder = "0"
    canonical_latex_quotient = r"3x"

    question_text = f"""Perform polynomial division to find the remainder of $\\frac{6x^3 + 4x^2}{2x^2}$. 
The quotient is {canonical_latex_quotient}. What is the remainder?
$$ \\text{Remainder: } \_\_ $$"""

    return {
        "question_text": question_text,
        "correct_answer": f"{{'remainder': '{correct_answer_remainder}', 'quotient': '{canonical_latex_quotient}'}}", # String representation of dict for JSON compatibility if needed, but spec says include remainder and canonical latex. Let's format as a string containing both clearly or just the values. 
        # Re-reading: "correct_answer must include only remainder and canonical_latex".
        # I will return them in a structured way within the text or separate fields? The key is 'correct_answer'.
        # It says "include", so likely a formatted string or dict representation. Given it's an answer field, let's make it clear.
        correct_answer: f"Remainder: {correct_answer_remainder}, Quotient (for reference): {{canonical_latex_quotight}}" if False else None 
    }

# Correct implementation following spec strictly
    
def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"] # [6, 4, 0] -> 6x^3 + 4x^2
    divisor_coeffs = frozen_params["divisor_coefficients"]   # [2, 0, 0] -> 2x^2
    
    dividend_str_latex = r"6x^3+4x^2"
    divisor_str_latex = r"2x^2"
    
    # Division: (6x^3 + 4x^2) / (2x^2) = 3x. Remainder is 0.
    remainder_val = "0"
    quotient_latex = r"3x"

    question_text = f"""Calculate the polynomial division of $\\frac{6x^3+4x^2}{2x^2}$. 
Find the **remainder**. The canonical form of the quotient is {quotient_latex}.
$$ \\text{Remainder: } \_\_ $$"""

    return {
        "question_text": question_text,
        "correct_answer": f"{{'remainder': '{remainder_val}', 'canonical_quotient': '{quotient_latex}'}}", # Ensuring both are present as requested. 
        "oracle_payload": frozen_params
    }
