from fractions import Fraction

def generate(level=1, **kwargs):
    dividend_coefficients = kwargs.get("dividend_coefficients", [6, 0, 6])
    divisor_coefficients = kwargs.get("divisor_coefficients", [1, -4])
    
    def poly_div(dividend, divisor):
        dividend = [Fraction(x) for x in dividend]
        divisor = [Fraction(x) for x in divisor]
        
        while len(dividend) > 0 and dividend[0] == 0:
            dividend.pop(0)
        while len(divisor) > 0 and divisor[0] == 0:
            divisor.pop(0)
            
        if not divisor:
            raise ZeroDivisionError("Division by zero polynomial.")
        if not dividend:
            return [Fraction(0)], [Fraction(0)]
            
        quotient = []
        remainder = list(dividend)
        
        while len(remainder) >= len(divisor):
            lead_coeff = remainder[0] / divisor[0]
            quotient.append(lead_coeff)
            for i in range(len(divisor)):
                remainder[i] -= lead_coeff * divisor[i]
            remainder.pop(0)
            
        while len(remainder) > 0 and remainder[0] == 0:
            remainder.pop(0)
        if not remainder:
            remainder = [Fraction(0)]
        if not quotient:
            quotient = [Fraction(0)]
            
        return quotient, remainder

    quot, rem = poly_div(dividend_coefficients, divisor_coefficients)
    
    quot_coeffs = [int(x) if x.denominator == 1 else float(x) for x in quot]
    rem_coeffs = [int(x) if x.denominator == 1 else float(x) for x in rem]
    
    def poly_to_latex(coeffs):
        n = len(coeffs)
        if n == 0:
            return "0"
        coeffs = [Fraction(c) for c in coeffs]
        while len(coeffs) > 1 and coeffs[0] == 0:
            coeffs.pop(0)
        if len(coeffs) == 1 and coeffs[0] == 0:
            return "0"
            
        terms = []
        for i, c in enumerate(coeffs):
            deg = len(coeffs) - 1 - i
            if c == 0:
                continue
            if c < 0:
                sign = "-"
                abs_c = -c
            else:
                sign = "+" if len(terms) > 0 else ""
                abs_c = c
                
            if abs_c.denominator == 1:
                c_str = str(abs_c.numerator)
            else:
                c_str = f"\\frac{{{abs_c.numerator}}}{{{abs_c.denominator}}}"
                
            if deg == 0:
                term = f"{sign}{c_str}"
            elif deg == 1:
                coeff_part = "" if abs_c == 1 else c_str
                term = f"{sign}{coeff_part}x"
            else:
                coeff_part = "" if abs_c == 1 else c_str
                term = f"{sign}{coeff_part}x^{{{deg}}}"
            terms.append(term)
            
        res = ""
        for i, t in enumerate(terms):
            if i == 0:
                res = t
            else:
                op = t[0]
                val = t[1:]
                res += f" {op} {val}"
        return res

    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    quotient_latex = poly_to_latex(quot)
    remainder_latex = poly_to_latex(rem)
    
    question_text = f"Divide the polynomial \\({dividend_latex}\\) by \\({divisor_latex}\\). Find the quotient and the remainder."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": quot_coeffs,
            "remainder_coefficients": rem_coeffs,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": {
            "dividend_coefficients": dividend_coefficients,
            "divisor_coefficients": divisor_coefficients
        }
    }