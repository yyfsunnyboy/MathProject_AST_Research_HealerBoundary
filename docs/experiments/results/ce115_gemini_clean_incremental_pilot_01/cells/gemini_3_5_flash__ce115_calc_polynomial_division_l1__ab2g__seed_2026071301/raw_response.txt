from fractions import Fraction

def format_poly(coeffs):
    deg = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        if c == 0:
            continue
        power = deg - i
        sign = ""
        if c < 0:
            sign = "-"
        elif len(terms) > 0:
            sign = "+"
            
        abs_c = abs(c)
        coeff_str = str(abs_c)
        if abs_c == 1 and power > 0:
            coeff_str = ""
            
        if power == 0:
            term = f"{sign}{abs_c}"
        elif power == 1:
            term = f"{sign}{coeff_str}x"
        else:
            term = f"{sign}{coeff_str}x^{power}"
            
        if len(terms) > 0:
            term = f" {term[0]} {term[1:]}"
        terms.append(term)
    if not terms:
        return "0"
    return "".join(terms)

def poly_div(dividend_coeffs, divisor_coeffs):
    A = [Fraction(x) for x in dividend_coeffs]
    B = [Fraction(x) for x in divisor_coeffs]
    
    while len(A) > 1 and A[0] == 0:
        A.pop(0)
    while len(B) > 1 and B[0] == 0:
        B.pop(0)
        
    if len(B) == 1 and B[0] == 0:
        raise ZeroDivisionError("Division by zero polynomial.")
        
    if len(A) < len(B):
        return [Fraction(0)], A
        
    deg_A = len(A) - 1
    deg_B = len(B) - 1
    
    quotient = [Fraction(0)] * (deg_A - deg_B + 1)
    remainder = list(A)
    
    for i in range(len(quotient)):
        coeff = remainder[i] / B[0]
        quotient[i] = coeff
        for j in range(len(B)):
            remainder[i + j] -= coeff * B[j]
            
    rem_coeffs = remainder[len(quotient):]
    while len(rem_coeffs) > 1 and rem_coeffs[0] == 0:
        rem_coeffs.pop(0)
        
    return quotient, rem_coeffs

def format_fraction(f):
    if f.denominator == 1:
        return int(f.numerator)
    else:
        return f"{f.numerator}/{f.denominator}"

def generate(level=1, **kwargs):
    # Frozen parameters
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Compute division
    q_raw, r_raw = poly_div(dividend_coefficients, divisor_coefficients)
    
    quotient_coefficients = [format_fraction(x) for x in q_raw]
    remainder_coefficients = [format_fraction(x) for x in r_raw]
    
    p_str = format_poly(dividend_coefficients)
    d_str = format_poly(divisor_coefficients)
    
    question_text = (
        f"Find the quotient and remainder when the polynomial "
        f"P(x) = {p_str} is divided by D(x) = {d_str}."
    )
    
    correct_answer = {
        "quotient_coefficients": quotient_coefficients,
        "remainder_coefficients": remainder_coefficients
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