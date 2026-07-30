def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    def divide_polynomials(dividend, divisor):
        dividend = list(dividend)
        divisor = list(divisor)
        while len(dividend) > 1 and dividend[0] == 0:
            dividend.pop(0)
        while len(divisor) > 1 and divisor[0] == 0:
            divisor.pop(0)
        
        if len(divisor) == 1 and divisor[0] == 0:
            raise ZeroDivisionError()
            
        if len(dividend) < len(divisor):
            return [0], dividend
            
        quotient = []
        remainder = dividend[:]
        
        while len(remainder) >= len(divisor):
            coeff = remainder[0] // divisor[0]
            quotient.append(coeff)
            for i in range(len(divisor)):
                remainder[i] -= coeff * divisor[i]
            remainder.pop(0)
            
        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)
            
        return quotient, remainder

    def poly_to_latex(coeffs):
        deg = len(coeffs) - 1
        if deg < 0:
            return "0"
        terms = []
        for i, c in enumerate(coeffs):
            power = deg - i
            if c == 0:
                continue
            
            if len(terms) == 0:
                sign = "-" if c < 0 else ""
            else:
                sign = " - " if c < 0 else " + "
                
            abs_c = abs(c)
            if power == 0:
                term = f"{sign}{abs_c}"
            elif power == 1:
                coeff_str = "" if abs_c == 1 else str(abs_c)
                term = f"{sign}{coeff_str}x"
            else:
                coeff_str = "" if abs_c == 1 else str(abs_c)
                term = f"{sign}{coeff_str}x^{power}"
            terms.append(term)
        if not terms:
            return "0"
        return "".join(terms)

    q_coeffs, r_coeffs = divide_polynomials(dividend_coefficients, divisor_coefficients)
    
    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    q_latex = poly_to_latex(q_coeffs)
    r_latex = poly_to_latex(r_coeffs)
    
    question_text = (
        f"Find the quotient and remainder when the polynomial "
        f"\( {dividend_latex} \) is divided by \( {divisor_latex} \)."
    )
    
    correct_answer = {
        "quotient_coefficients": q_coeffs,
        "remainder_coefficients": r_coeffs,
        "quotient_latex": q_latex,
        "remainder_latex": r_latex
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