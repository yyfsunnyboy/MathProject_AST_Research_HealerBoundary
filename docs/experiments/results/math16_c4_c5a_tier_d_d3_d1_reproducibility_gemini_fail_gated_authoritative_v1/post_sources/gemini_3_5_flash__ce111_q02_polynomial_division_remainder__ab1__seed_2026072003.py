def generate(level=1, **kwargs):
    dividend_coefficients = kwargs.get("dividend_coefficients", [6, 4, 0])
    divisor_coefficients = kwargs.get("divisor_coefficients", [2, 0, 0])
    
    num = list(dividend_coefficients)
    den = list(divisor_coefficients)
    
    while len(num) > 0 and num[0] == 0:
        num.pop(0)
    while len(den) > 0 and den[0] == 0:
        den.pop(0)
        
    if not den:
        raise ZeroDivisionError()
        
    if len(num) < len(den):
        rem = num
    else:
        num = [float(x) for x in num]
        den = [float(x) for x in den]
        while len(num) >= len(den):
            mult = num[0] / den[0]
            for i in range(len(den)):
                num[i] -= mult * den[i]
            num.pop(0)
        rem = [int(x) if x.is_integer() else x for x in num]
        
    while len(rem) > 0 and rem[0] == 0:
        rem.pop(0)
    if not rem:
        rem = [0]
        
    def format_poly(coeffs):
        n = len(coeffs)
        if n == 0:
            return "0"
        terms = []
        for i, c in enumerate(coeffs):
            deg = n - 1 - i
            if c == 0:
                continue
            
            if c > 0:
                sign = " + " if terms else ""
            else:
                sign = " - " if terms else "-"
            
            abs_c = abs(c)
            if abs_c == 1 and deg > 0:
                coeff_str = ""
            else:
                coeff_str = str(abs_c)
                
            if deg == 0:
                term = f"{sign}{abs_c}"
            elif deg == 1:
                term = f"{sign}{coeff_str}x"
            else:
                term = f"{sign}{coeff_str}x^{deg}"
            terms.append(term)
        
        if not terms:
            return "0"
        return "".join(terms)

    dividend_str = format_poly(dividend_coefficients)
    divisor_str = format_poly(divisor_coefficients)
    remainder_str = format_poly(rem)
    
    question_text = f"Find the remainder when \\({dividend_str}\\) is divided by \\({divisor_str}\\)."
    correct_answer = remainder_str
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "dividend_coefficients": dividend_coefficients,
            "divisor_coefficients": divisor_coefficients
        }
    }