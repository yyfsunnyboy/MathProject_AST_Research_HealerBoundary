def format_poly(coeffs):
    while len(coeffs) > 1 and coeffs[0] == 0:
        coeffs = coeffs[1:]
    if not coeffs:
        return "0"
    
    terms = []
    deg = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        d = deg - i
        if c == 0:
            continue
        
        if c > 0:
            sign = "+" if terms else ""
        else:
            sign = "-"
        
        abs_c = abs(c)
        if abs_c == 1 and d > 0:
            coeff_str = ""
        else:
            coeff_str = str(abs_c)
            
        if d == 0:
            term_str = f"{coeff_str}"
        elif d == 1:
            term_str = f"{coeff_str}x"
        else:
            term_str = f"{coeff_str}x^{d}"
            
        terms.append(f"{sign}{term_str}")
        
    if not terms:
        return "0"
    
    res = ""
    for i, t in enumerate(terms):
        if i == 0:
            res += t
        else:
            op = t[0]
            val = t[1:]
            res += f" {op} {val}"
    return res

def generate(level=1, **kwargs):
    dividend_coefficients = kwargs.get("dividend_coefficients", [6, 4, 0])
    divisor_coefficients = kwargs.get("divisor_coefficients", [2, 0, 0])
    
    from fractions import Fraction
    
    num = [Fraction(x) for x in dividend_coefficients]
    den = [Fraction(x) for x in divisor_coefficients]
    
    while len(num) > 0 and num[0] == 0:
        num.pop(0)
    while len(den) > 0 and den[0] == 0:
        den.pop(0)
        
    if not den:
        raise ZeroDivisionError()
        
    rem = list(num)
    while len(rem) >= len(den) and len(rem) > 0:
        coeff = rem[0] / den[0]
        for i in range(len(den)):
            rem[i] -= coeff * den[i]
        rem.pop(0)
        
    rem_coeffs = []
    for x in rem:
        if x.denominator == 1:
            rem_coeffs.append(int(x))
        else:
            rem_coeffs.append(float(x))
            
    dividend_str = format_poly(dividend_coefficients)
    divisor_str = format_poly(divisor_coefficients)
    remainder_str = format_poly(rem_coeffs)
    
    question_text = f"Find the remainder when \\({dividend_str}\\) is divided by \\({divisor_str}\\)."
    correct_answer = remainder_str
    
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }