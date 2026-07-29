def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    from core.prompts.domain_function_library import PolynomialOps
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    quotient_remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    quotient_coeffs = quotient_remainder[0]
    remainder_coeffs = quotient_remainder[1]
    
    def format_latex(coeffs):
        if not coeffs:
            return "0"
        terms = []
        for i, c in enumerate(coeffs):
            power = len(coeffs) - 1 - i
            term_str = f"{c}x^{power}" if power > 0 else str(c)
            # Handle negative coefficients properly with LaTeX minus sign inside math mode context usually handled by text representation or specific delimiters. 
            # For simplicity in string generation: use standard notation, ensuring '-' is explicit for negatives.
            terms.append(term_str.replace("-", "\\-"))
        return " + ".join(terms) if len(coeffs) > 1 else (f"{coeffs[0]}x^{len(coeffs)-1}" if coeffs and len(coeffs)==1 else str(coeffs))

    # Reconstructing polynomial string for display to ensure correctness in LaTeX format as requested by delimiters
    def poly_to_latex_str(c):
        n = len(c) - 1
        terms = []
        for i, val in enumerate(c):
            p = n - i
            if val == 0:
                continue
            term = f"{val}x^{p}" if p > 0 else str(val)
            # Ensure negative sign is handled correctly for LaTeX math mode (using \- or just text minus, but standard latex uses hyphen in code or explicit minus). 
            # The prompt asks for delimiters \( \), so we format the string content.
            terms.append(term.replace("-", "\\-" if p > 0 else ""))
        return " + ".join(terms)

    quotient_latex = poly_to_latex_str(quotient_coeffs)
    remainder_latex = poly_to_latex_str(remainder_coeffs)
    
    question_text = r"""Perform polynomial division for the polynomials defined by coefficients: Dividend \( [6, 0, 6] \), Divisor \( [1, -4] \). Find the quotient and remainder."""

    correct_answer = {
        "quotient_coefficients": quotient_coeffs,
        "remainder_coefficients": remainder_coeffs,
        "quotient_latex": f"\\({quotient_latex}\\)",
        "remainder_latex": f"\\({remainder_latex}\\)"
    }
    
    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
