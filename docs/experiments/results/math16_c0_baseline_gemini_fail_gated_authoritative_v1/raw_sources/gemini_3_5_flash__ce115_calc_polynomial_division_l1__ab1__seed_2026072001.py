def poly_to_latex(coeffs, var='x'):
    from fractions import Fraction
    start = 0
    while start < len(coeffs) - 1 and coeffs[start] == 0:
        start += 1
    coeffs = coeffs[start:]
    
    if len(coeffs) == 1 and coeffs[0] == 0:
        return "0"
        
    n = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        deg = n - i
        if c == 0:
            continue
        
        if c < 0:
            sign = "-"
        else:
            sign = "+" if terms else ""
            
        abs_c = abs(c)
        
        if abs_c == 1 and deg > 0:
            c_str = ""
        else:
            if isinstance(abs_c, Fraction):
                if abs_c.denominator == 1:
                    c_str = str(abs_c.numerator)
                else:
                    c_str = f"\\frac{{{abs_c.numerator}}}{{{abs_c.denominator}}}"
            else:
                c_str = str(abs_c)
                
        if deg == 0:
            var_str = ""
            if abs_c == 1 and c_str == "":
                c_str = "1"
        elif deg == 1:
            var_str = var
        else:
            var_str = f"{var}^{deg}"
            
        terms.append(f"{sign}{c_str}{var_str}")
        
    return "".join(terms)

def poly_div(A, B):
    from fractions import Fraction
    while len(B) > 0 and B[0] == 0:
        B = B[1:]
    if not B:
        raise ZeroDivisionError("Division by zero polynomial")
    
    A = [Fraction(x) for x in A]
    B = [Fraction(x) for x in B]
    
    len_A = len(A)
    len_B = len(B)
    
    if len_A < len_B:
        return [0], [int(x) if x.denominator == 1 else x for x in A]
    
    Q = [Fraction(0)] * (len_A - len_B + 1)
    
    for i in range(len(Q)):
        coeff = A[i] / B[0]
        Q[i] = coeff
        for j in range(len_B):
            A[i + j] -= coeff * B[j]
            
    R = A[len(Q):]
    
    while len(Q) > 1 and Q[0] == 0:
        Q = Q[1:]
    while len(R) > 1 and R[0] == 0:
        R = R[1:]
        
    def to_int_or_fraction(x):
        if x.denominator == 1:
            return int(x.numerator)
        return x
        
    Q = [to_int_or_fraction(x) for x in Q]
    R = [to_int_or_fraction(x) for x in R]
    return Q, R

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    Q_coeffs, R_coeffs = poly_div(dividend_coefficients, divisor_coefficients)
    
    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    quotient_latex = poly_to_latex(Q_coeffs)
    remainder_latex = poly_to_latex(R_coeffs)
    
    question_text = f"Divide the polynomial \\( {dividend_latex} \\) by \\( {divisor_latex} \\). Find the quotient and the remainder."
    
    correct_answer = {
        "quotient_coefficients": Q_coeffs,
        "remainder_coefficients": R_coeffs,
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