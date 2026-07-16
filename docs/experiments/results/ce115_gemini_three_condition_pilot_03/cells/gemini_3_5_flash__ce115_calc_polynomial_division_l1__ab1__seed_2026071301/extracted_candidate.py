from fractions import Fraction

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    dividend = [Fraction(x) for x in dividend_coefficients]
    divisor = [Fraction(x) for x in divisor_coefficients]
    
    quotient = []
    remainder = list(dividend)
    
    lead_div = divisor[0]
    
    while len(remainder) >= len(divisor):
        lead_rem = remainder[0]
        q_coeff = lead_rem / lead_div
        quotient.append(q_coeff)
        
        for i in range(len(divisor)):
            remainder[i] -= q_coeff * divisor[i]
            
        remainder.pop(0)
        
    if not quotient:
        quotient = [Fraction(0)]
    if not remainder:
        remainder = [Fraction(0)]
        
    def format_coeff(val):
        if val.denominator == 1:
            return val.numerator
        else:
            return f"{val.numerator}/{val.denominator}"
            
    quotient_coeffs = [format_coeff(x) for x in quotient]
    remainder_coeffs = [format_coeff(x) for x in remainder]
    
    def format_poly(coeffs):
        n = len(coeffs) - 1
        terms = []
        for i, c in enumerate(coeffs):
            deg = n - i
            if c == 0:
                continue
            if deg == 0:
                term = f"{c}"
            elif deg == 1:
                if c == 1:
                    term = "x"
                elif c == -1:
                    term = "-x"
                else:
                    term = f"{c}x"
            else:
                if c == 1:
                    term = f"x^{deg}"
                elif c == -1:
                    term = f"-x^{deg}"
                else:
                    term = f"{c}x^{deg}"
            terms.append(term)
        if not terms:
            return "0"
        res = terms[0]
        for term in terms[1:]:
            if term.startswith("-"):
                res += " - " + term[1:]
            else:
                res += " + " + term
        return res

    poly_dividend = format_poly(dividend_coefficients)
    poly_divisor = format_poly(divisor_coefficients)
    
    question_text = f"Divide the polynomial {poly_dividend} by {poly_divisor}. Find the quotient and the remainder."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": quotient_coeffs,
            "remainder_coefficients": remainder_coeffs
        },
        "oracle_payload": {
            "dividend_coefficients": dividend_coefficients,
            "divisor_coefficients": divisor_coefficients
        }
    }