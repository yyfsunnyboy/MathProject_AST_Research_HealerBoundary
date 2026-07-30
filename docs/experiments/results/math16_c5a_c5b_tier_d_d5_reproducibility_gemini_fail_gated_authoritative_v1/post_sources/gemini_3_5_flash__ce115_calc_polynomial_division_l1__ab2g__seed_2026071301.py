from fractions import Fraction

def poly_to_latex(coeffs):
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
        if c < 0:
            sign = "-"
            val = -c
        else:
            if terms:
                sign = "+"
            val = c
        
        # coefficient string
        if val == 1 and deg > 0:
            c_str = ""
        else:
            c_str = str(val)
            
        # x part
        if deg == 0:
            x_str = str(val) if val == 1 and c_str == "" else c_str
        elif deg == 1:
            x_str = c_str + "x"
        else:
            x_str = c_str + f"x^{deg}"
            
        terms.append(f"{sign}{x_str}")
    if not terms:
        return "0"
    res = ""
    for i, t in enumerate(terms):
        if i == 0:
            res += t
        else:
            if t.startswith("+"):
                res += " + " + t[1:]
            elif t.startswith("-"):
                res += " - " + t[1:]
            else:
                res += " + " + t
    return res

def divide_polynomials(dividend, divisor):
    while len(divisor) > 1 and divisor[0] == 0:
        divisor = divisor[1:]
    while len(dividend) > 1 and dividend[0] == 0:
        dividend = dividend[1:]
        
    if len(divisor) == 1 and divisor[0] == 0:
        raise ZeroDivisionError("Division by zero polynomial.")
        
    dividend = [Fraction(x) for x in dividend]
    divisor = [Fraction(x) for x in divisor]
    
    n = len(dividend) - 1
    m = len(divisor) - 1
    
    if n < m:
        return [Fraction(0)], dividend
        
    quotient = [Fraction(0)] * (n - m + 1)
    remainder = list(dividend)
    
    for i in range(n - m + 1):
        coeff = remainder[i] / divisor[0]
        quotient[i] = coeff
        for j in range(len(divisor)):
            remainder[i + j] -= coeff * divisor[j]
            
    rem_coeffs = remainder[n - m + 1:]
    while len(rem_coeffs) > 1 and rem_coeffs[0] == 0:
        rem_coeffs = rem_coeffs[1:]
    if not rem_coeffs:
        rem_coeffs = [Fraction(0)]
        
    while len(quotient) > 1 and quotient[0] == 0:
        quotient = quotient[1:]
        
    return quotient, rem_coeffs

def to_ints_if_possible(coeffs):
    res = []
    for x in coeffs:
        if x.denominator == 1:
            res.append(int(x))
        else:
            res.append(x)
    return res

def generate(level=1, **kwargs):
    # Frozen parameters
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Perform division
    q_frac, r_frac = divide_polynomials(dividend_coefficients, divisor_coefficients)
    
    quotient_coefficients = to_ints_if_possible(q_frac)
    remainder_coefficients = to_ints_if_possible(r_frac)
    
    quotient_latex = poly_to_latex(quotient_coefficients)
    remainder_latex = poly_to_latex(remainder_coefficients)
    
    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    
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