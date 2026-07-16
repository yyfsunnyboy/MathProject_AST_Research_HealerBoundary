import json
from fractions import Fraction

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
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
                
            term = f"{c_str}{v_str}"
            terms.append((sign, term))
            
        if not terms:
            return "0"
            
        res = ""
        for i, (sign, term) in enumerate(terms):
            if i == 0:
                if sign == "-":
                    res += "-" + term
                else:
                    res += term
            else:
                res += f" {sign} {term}"
        return res

    poly_dividend = format_poly(dividend_coefficients)
    poly_divisor = format_poly(divisor_coefficients)
    
    question_text = f"Divide the polynomial ${poly_dividend}$ by ${poly_divisor}$. Find the quotient and the remainder."
    
    dividend = [Fraction(x) for x in dividend_coefficients]
    divisor = [Fraction(x) for x in divisor_coefficients]
    
    while len(dividend) > 0 and dividend[0] == 0:
        dividend.pop(0)
    while len(divisor) > 0 and divisor[0] == 0:
        divisor.pop(0)
        
    quotient = []
    remainder = list(dividend)
    
    deg_div = len(divisor) - 1
    lead_div = divisor[0]
    
    while len(remainder) >= len(divisor):
        deg_rem = len(remainder) - 1
        lead_rem = remainder[0]
        
        coeff = lead_rem / lead_div
        quotient.append(coeff)
        
        for i in range(len(divisor)):
            remainder[i] -= coeff * divisor[i]
            
        remainder.pop(0)
        
    if not quotient:
        quotient = [Fraction(0)]
    if not remainder:
        remainder = [Fraction(0)]
        
    def format_frac(f):
        if f.denominator == 1:
            return int(f.numerator)
        else:
            return f"{f.numerator}/{f.denominator}"
            
    quotient_coeffs = [format_frac(x) for x in quotient]
    remainder_coeffs = [format_frac(x) for x in remainder]
    
    correct_answer = {
        "quotient_coefficients": quotient_coeffs,
        "remainder_coefficients": remainder_coeffs
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