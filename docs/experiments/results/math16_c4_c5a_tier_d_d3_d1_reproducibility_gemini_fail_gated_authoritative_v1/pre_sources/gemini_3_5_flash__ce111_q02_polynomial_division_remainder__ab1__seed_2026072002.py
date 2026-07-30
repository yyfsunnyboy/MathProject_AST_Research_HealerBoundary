from fractions import Fraction

def generate(level=1, **kwargs):
    dividend_coefficients = kwargs.get("dividend_coefficients", [6, 4, 0])
    divisor_coefficients = kwargs.get("divisor_coefficients", [2, 0, 0])
    
    def format_poly(coeffs):
        coeffs = [Fraction(c) for c in coeffs]
        while len(coeffs) > 1 and coeffs[0] == 0:
            coeffs.pop(0)
        if not coeffs or (len(coeffs) == 1 and coeffs[0] == 0):
            return "0"
        
        deg = len(coeffs) - 1
        parts = []
        for i, c in enumerate(coeffs):
            power = deg - i
            if c == 0:
                continue
            
            if c < 0:
                sign = " - " if parts else "-"
                abs_c = -c
            else:
                sign = " + " if parts else ""
                abs_c = c
                
            if abs_c == 1 and power > 0:
                coeff_str = ""
            else:
                if abs_c.denominator == 1:
                    coeff_str = str(abs_c.numerator)
                else:
                    coeff_str = f"\\frac{{{abs_c.numerator}}}{{{abs_c.denominator}}}"
                    
            if power == 0:
                var_str = ""
                if abs_c == 1:
                    coeff_str = "1"
            elif power == 1:
                var_str = "x"
            else:
                var_str = f"x^{{{power}}}"
                
            parts.append(f"{sign}{coeff_str}{var_str}")
            
        return "".join(parts)

    num = [Fraction(x) for x in dividend_coefficients]
    den = [Fraction(x) for x in divisor_coefficients]
    
    while len(num) > 0 and num[0] == 0:
        num.pop(0)
    while len(den) > 0 and den[0] == 0:
        den.pop(0)
        
    if not den:
        raise ZeroDivisionError()
        
    if not num:
        remainder_coeffs = [0]
    else:
        while len(num) >= len(den):
            coeff = num[0] / den[0]
            for i in range(len(den)):
                num[i] -= coeff * den[i]
            num.pop(0)
        remainder_coeffs = num

    dividend_latex = format_poly(dividend_coefficients)
    divisor_latex = format_poly(divisor_coefficients)
    remainder_latex = format_poly(remainder_coeffs)
    
    question_text = f"Find the remainder when ${dividend_latex}$ is divided by ${divisor_latex}$."
    correct_answer = remainder_latex
    
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }