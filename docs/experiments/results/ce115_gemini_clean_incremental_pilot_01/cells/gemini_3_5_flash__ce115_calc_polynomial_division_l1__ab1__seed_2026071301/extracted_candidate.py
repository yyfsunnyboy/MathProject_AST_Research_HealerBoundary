from fractions import Fraction

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial division using exact arithmetic
    dividend = [Fraction(x) for x in dividend_coefficients]
    divisor = [Fraction(x) for x in divisor_coefficients]
    
    # Remove leading zeros
    while len(dividend) > 0 and dividend[0] == 0:
        dividend.pop(0)
    while len(divisor) > 0 and divisor[0] == 0:
        divisor.pop(0)
        
    if len(divisor) == 0:
        raise ZeroDivisionError("Division by zero polynomial.")
        
    if len(dividend) < len(divisor):
        quotient = []
        remainder = list(dividend)
    else:
        quotient = []
        remainder = list(dividend)
        while len(remainder) >= len(divisor):
            coeff = remainder[0] / divisor[0]
            quotient.append(coeff)
            for i in range(len(divisor)):
                remainder[i] -= coeff * divisor[i]
            remainder.pop(0)
            
    def format_coeff(f):
        if f.denominator == 1:
            return f.numerator
        else:
            num = f.numerator
            den = f.denominator
            if den < 0:
                num = -num
                den = -den
            return f"{num}/{den}"
            
    quotient_formatted = [format_coeff(x) for x in quotient]
    remainder_formatted = [format_coeff(x) for x in remainder]
    
    # Pad remainder to have degree lower than divisor
    target_len = len(divisor_coefficients) - 1
    while len(remainder_formatted) < target_len:
        remainder_formatted.insert(0, 0)
        
    # Format polynomials for question text
    def format_poly(coeffs):
        deg = len(coeffs) - 1
        terms = []
        for i, c in enumerate(coeffs):
            d = deg - i
            if c == 0:
                continue
            sign = "+" if c > 0 else "-"
            abs_c = abs(c)
            
            if abs_c == 1 and d > 0:
                c_str = ""
            else:
                c_str = str(abs_c)
                
            if d == 0:
                v_str = str(abs_c)
                c_str = ""
            elif d == 1:
                v_str = "x"
            else:
                v_str = f"x^{d}"
                
            term = f"{sign} {c_str}{v_str}"
            terms.append(term)
            
        if not terms:
            return "0"
            
        res = " ".join(terms)
        if res.startswith("+ "):
            res = res[2:]
        elif res.startswith("- "):
            res = "-" + res[2:]
        return res

    poly_dividend = format_poly(dividend_coefficients)
    poly_divisor = format_poly(divisor_coefficients)
    
    question_text = f"Divide the polynomial {poly_dividend} by {poly_divisor}. Find the quotient and the remainder."
    
    correct_answer = {
        "quotient_coefficients": quotient_formatted,
        "remainder_coefficients": remainder_formatted
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