from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen parameters
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial division
    def poly_div(dividend, divisor):
        def strip_leading_zeros(lst):
            i = 0
            while i < len(lst) and lst[i] == 0:
                i += 1
            return lst[i:] if i < len(lst) else [0]
        
        dividend = strip_leading_zeros(dividend)
        divisor = strip_leading_zeros(divisor)
        
        if len(divisor) == 1 and divisor[0] == 0:
            raise ZeroDivisionError()
            
        if len(dividend) < len(divisor):
            return [0], dividend
            
        dividend = [Fraction(x) for x in dividend]
        divisor = [Fraction(x) for x in divisor]
        
        quotient = []
        remainder = list(dividend)
        
        len_div = len(divisor)
        while len(remainder) >= len_div:
            coeff = remainder[0] / divisor[0]
            quotient.append(coeff)
            for i in range(len_div):
                remainder[i] -= coeff * divisor[i]
            remainder.pop(0)
            
        def to_int_if_possible(lst):
            res = []
            for x in lst:
                if x.denominator == 1:
                    res.append(int(x))
                else:
                    res.append(x)
            return res
            
        return to_int_if_possible(quotient), to_int_if_possible(remainder)

    def format_coeff(c, is_leading):
        if c < 0:
            sign = "-"
            abs_c = -c
        else:
            sign = "" if is_leading else "+"
            abs_c = c
            
        if isinstance(abs_c, Fraction):
            if abs_c.denominator == 1:
                abs_c = abs_c.numerator
            else:
                abs_str = f"\\frac{{{abs_c.numerator}}}{{{abs_c.denominator}}}"
                return sign, abs_str
                
        abs_str = str(abs_c)
        return sign, abs_str

    def poly_to_latex(coeffs, var='x'):
        coeffs = [Fraction(c) for c in coeffs]
        while len(coeffs) > 1 and coeffs[0] == 0:
            coeffs.pop(0)
        if len(coeffs) == 1 and coeffs[0] == 0:
            return "0"
            
        n = len(coeffs) - 1
        terms = []
        is_leading = True
        for i, c in enumerate(coeffs):
            if c == 0:
                continue
            deg = n - i
            sign, abs_str = format_coeff(c, is_leading)
            
            if abs_str == "1" and deg > 0:
                coeff_part = ""
            else:
                coeff_part = abs_str
                
            if deg == 0:
                term = f"{sign}{coeff_part}"
            elif deg == 1:
                term = f"{sign}{coeff_part}{var}"
            else:
                term = f"{sign}{coeff_part}{var}^{{{deg}}}"
                
            terms.append(term)
            is_leading = False
            
        return "".join(terms)

    q_coeffs, r_coeffs = poly_div(dividend_coefficients, divisor_coefficients)
    
    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    quotient_latex = poly_to_latex(q_coeffs)
    remainder_latex = poly_to_latex(r_coeffs)
    
    question_text = f"Divide the polynomial \\( {dividend_latex} \\) by \\( {divisor_latex} \\). Find the quotient and the remainder."
    
    correct_answer = {
        "quotient_coefficients": q_coeffs,
        "remainder_coefficients": r_coeffs,
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