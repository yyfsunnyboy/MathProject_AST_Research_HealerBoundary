# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]

    # Polynomial division helper
    def poly_div(num, den):
        num = list(num)
        den = list(den)
        while len(num) > 1 and num[0] == 0:
            num.pop(0)
        while len(den) > 1 and den[0] == 0:
            den.pop(0)
        if den == [0]:
            raise ZeroDivisionError()
        
        if len(num) < len(den):
            return [0], num
            
        quot = [0] * (len(num) - len(den) + 1)
        rem = list(num)
        
        for i in range(len(quot)):
            coeff = rem[i] / den[0]
            if coeff == int(coeff):
                coeff = int(coeff)
            quot[i] = coeff
            for j in range(len(den)):
                rem[i + j] -= coeff * den[j]
                if rem[i + j] == int(rem[i + j]):
                    rem[i + j] = int(rem[i + j])
                    
        while len(rem) > 1 and rem[0] == 0:
            rem.pop(0)
        return quot, rem

    # Polynomial to LaTeX helper
    def poly_to_latex(coeffs):
        if not coeffs or coeffs == [0]:
            return "0"
        while len(coeffs) > 1 and coeffs[0] == 0:
            coeffs = coeffs[1:]
        
        n = len(coeffs) - 1
        terms = []
        for i, c in enumerate(coeffs):
            if c == 0:
                continue
            power = n - i
            
            if c > 0:
                sign = "+" if terms else ""
            else:
                sign = "-"
                
            abs_c = abs(c)
            if abs_c == 1 and power > 0:
                coeff_str = ""
            else:
                coeff_str = str(abs_c)
                
            if power == 0:
                term = f"{sign}{abs_c}"
            elif power == 1:
                term = f"{sign}{coeff_str}x"
            else:
                term = f"{sign}{coeff_str}x^{{{power}}}"
            terms.append(term)
            
        return "".join(terms)

    # Compute quotient and remainder
    quotient, remainder = poly_div(dividend_coefficients, divisor_coefficients)
    
    # Format to LaTeX
    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    remainder_latex = poly_to_latex(remainder)

    question_text = f"Find the remainder when the polynomial ${dividend_latex}$ is divided by ${divisor_latex}$."
    
    correct_answer = {
        "remainder": remainder,
        "canonical_latex": remainder_latex
    }
    
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }