from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Use the domain API
    quotient_coefficients, remainder_coefficients = PolynomialOps.div_qr(
        dividend_coefficients, divisor_coefficients
    )
    
    def poly_to_latex(coeffs):
        n = len(coeffs)
        if n == 0:
            return "0"
        terms = []
        for i, c in enumerate(coeffs):
            deg = n - 1 - i
            if c == 0:
                continue
            sign = ""
            if c > 0:
                if terms:
                    sign = " + "
            else:
                if terms:
                    sign = " - "
                    c = -c
                else:
                    sign = "-"
            
            if deg == 0:
                term = f"{c}"
            elif deg == 1:
                if c == 1:
                    term = "x"
                else:
                    term = f"{c}x"
            else:
                if c == 1:
                    term = f"x^{{{deg}}}"
                else:
                    term = f"{c}x^{{{deg}}}"
            terms.append(f"{sign}{term}")
        if not terms:
            return "0"
        return "".join(terms)

    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    quotient_latex = poly_to_latex(quotient_coefficients)
    remainder_latex = poly_to_latex(remainder_coefficients)
    
    question_text = f"Divide the polynomial \\( {dividend_latex} \\) by \\( {divisor_latex} \\). Find the quotient and the remainder."
    
    correct_answer = {
        "quotient_coefficients": quotient_coefficients,
        "remainder_coefficients": remainder_coefficients,
        "quotient_latex": quotient_latex,
        "remainder_latex": remainder_latex
    }
    
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }