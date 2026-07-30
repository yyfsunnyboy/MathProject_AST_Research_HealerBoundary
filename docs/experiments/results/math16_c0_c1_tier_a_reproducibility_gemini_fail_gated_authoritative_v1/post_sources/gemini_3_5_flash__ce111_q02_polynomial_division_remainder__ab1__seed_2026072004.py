def generate(level=1, **kwargs):
    from fractions import Fraction

    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    def strip_leading_zeros(lst):
        i = 0
        while i < len(lst) and lst[i] == 0:
            i += 1
        return lst[i:] if i < len(lst) else [0]
        
    A = [Fraction(x) for x in strip_leading_zeros(dividend_coefficients)]
    B = [Fraction(x) for x in strip_leading_zeros(divisor_coefficients)]
    
    if B == [0]:
        raise ZeroDivisionError()
        
    if len(A) < len(B):
        rem = A
    else:
        rem = list(A)
        while len(rem) >= len(B) and rem != [0]:
            lead_rem = rem[0]
            lead_B = B[0]
            q_coeff = lead_rem / lead_B
            
            for i in range(len(B)):
                rem[i] -= q_coeff * B[i]
                
            rem = strip_leading_zeros(rem)
            
    def format_poly(coeffs):
        deg = len(coeffs) - 1
        terms = []
        for i, c in enumerate(coeffs):
            power = deg - i
            if c == 0:
                continue
            
            if c.denominator == 1:
                c_val = c.numerator
                c_str = str(abs(c_val))
            else:
                c_str = f"\\frac{{{abs(c.numerator)}}}{{{c.denominator}}}"
                
            sign = "+" if c > 0 else "-"
            
            if abs(c) == 1 and power > 0:
                c_str = ""
                
            if power == 0:
                if abs(c) == 1:
                    c_str = "1"
                term = c_str
            elif power == 1:
                term = f"{c_str}x"
            else:
                term = f"{c_str}x^{{{power}}}"
                
            terms.append((sign, term))
            
        if not terms:
            return "0"
            
        result = ""
        for i, (sign, term) in enumerate(terms):
            if i == 0:
                if sign == "-":
                    result += "-" + term
                else:
                    result += term
            else:
                result += f" {sign} {term}"
        return result

    dividend_latex = format_poly([Fraction(x) for x in dividend_coefficients])
    divisor_latex = format_poly([Fraction(x) for x in divisor_coefficients])
    remainder_latex = format_poly(rem)
    
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