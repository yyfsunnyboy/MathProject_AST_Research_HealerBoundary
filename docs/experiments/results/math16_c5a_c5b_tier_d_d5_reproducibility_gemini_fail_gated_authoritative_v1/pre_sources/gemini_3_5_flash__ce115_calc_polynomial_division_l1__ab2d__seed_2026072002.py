from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Call the domain API
    quotient, remainder = PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients)
    
    # Convert to int
    quotient_coefficients = [int(x) for x in quotient]
    remainder_coefficients = [int(x) for x in remainder]
    
    # Helper to format polynomial to LaTeX
    def poly_to_latex(coeffs):
        n = len(coeffs)
        if n == 0:
            return "0"
        terms = []
        for i, c in enumerate(coeffs):
            power = n - 1 - i
            if c == 0:
                continue
            sign = ""
            if c > 0:
                if terms:
                    sign = "+"
            else:
                sign = "-"
            
            abs_c = abs(c)
            if power == 0:
                coeff_str = str(abs_c)
                var_str = ""
            elif power == 1:
                coeff_str = "" if abs_c == 1 else str(abs_c)
                var_str = "x"
            else:
                coeff_str = "" if abs_c == 1 else str(abs_c)
                var_str = f"x^{{{power}}}"
                
            term = f"{sign}{coeff_str}{var_str}"
            terms.append(term)
            
        if not terms:
            return "0"
        return "".join(terms)

    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    quotient_latex = poly_to_latex(quotient_coefficients)
    remainder_latex = poly_to_latex(remainder_coefficients)
    
    question_text = f"Divide the polynomial \\({dividend_latex}\\) by \\({divisor_latex}\\). Find the quotient and the remainder."
    
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