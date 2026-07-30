from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Use the domain API
    quotient_coefficients, remainder_coefficients = PolynomialOps.div_qr(
        dividend_coefficients, divisor_coefficients
    )
    
    # Ensure they are list of ints
    quotient_coefficients = [int(x) for x in quotient_coefficients]
    remainder_coefficients = [int(x) for x in remainder_coefficients]
    
    def to_latex(coeffs):
        n = len(coeffs)
        if n == 0:
            return "0"
        terms = []
        for i, c in enumerate(coeffs):
            deg = n - 1 - i
            if c == 0:
                continue
            # sign
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
                    c = -c
            
            # coefficient and variable
            if deg == 0:
                term = f"{sign}{c}"
            elif deg == 1:
                coeff_str = "" if c == 1 else str(c)
                term = f"{sign}{coeff_str}x"
            else:
                coeff_str = "" if c == 1 else str(c)
                term = f"{sign}{coeff_str}x^{deg}"
            terms.append(term)
        if not terms:
            return "0"
        return "".join(terms)

    dividend_latex = to_latex(dividend_coefficients)
    divisor_latex = to_latex(divisor_coefficients)
    quotient_latex = to_latex(quotient_coefficients)
    remainder_latex = to_latex(remainder_coefficients)
    
    question_text = f"Find the quotient and remainder when the polynomial \\( {dividend_latex} \\) is divided by \\( {divisor_latex} \\)."
    
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