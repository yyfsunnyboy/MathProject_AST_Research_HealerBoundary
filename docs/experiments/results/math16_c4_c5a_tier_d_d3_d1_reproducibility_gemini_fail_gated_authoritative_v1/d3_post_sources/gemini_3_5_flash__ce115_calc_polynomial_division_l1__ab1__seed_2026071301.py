def generate(level=1, **kwargs):
    dividend = [6, 0, 6]
    divisor = [1, -4]
    
    from fractions import Fraction
    
    def poly_div(dividend, divisor):
        A = [Fraction(x) for x in dividend]
        B = [Fraction(x) for x in divisor]
        
        while len(A) > 1 and A[0] == 0:
            A.pop(0)
        while len(B) > 1 and B[0] == 0:
            B.pop(0)
            
        deg_A = len(A) - 1
        deg_B = len(B) - 1
        
        if deg_A < deg_B:
            return [0], dividend
            
        quot = [Fraction(0)] * (deg_A - deg_B + 1)
        rem = list(A)
        
        for i in range(deg_A - deg_B + 1):
            coeff = rem[i] / B[0]
            quot[i] = coeff
            for j in range(len(B)):
                rem[i + j] -= coeff * B[j]
                
        remainder = rem[deg_A - deg_B + 1:]
        while len(remainder) > 1 and remainder[0] == 0:
            remainder.pop(0)
            
        quot_ints = [int(x) if x.denominator == 1 else x for x in quot]
        rem_ints = [int(x) if x.denominator == 1 else x for x in remainder]
        
        return quot_ints, rem_ints

    def poly_to_latex(coeffs):
        n = len(coeffs) - 1
        terms = []
        for i, c in enumerate(coeffs):
            deg = n - i
            if c == 0:
                continue
            sign = ""
            if c < 0:
                sign = "-"
                val = -c
            else:
                if len(terms) > 0:
                    sign = "+"
                val = c
                
            if val == 1 and deg > 0:
                coeff_str = ""
            else:
                coeff_str = str(val)
                
            if deg == 0:
                var_str = ""
                if val == 1 and coeff_str == "":
                    coeff_str = "1"
            elif deg == 1:
                var_str = "x"
            else:
                var_str = f"x^{deg}"
                
            terms.append(f"{sign}{coeff_str}{var_str}")
            
        if not terms:
            return "0"
        return "".join(terms)

    quot, rem = poly_div(dividend, divisor)
    
    dividend_latex = poly_to_latex(dividend)
    divisor_latex = poly_to_latex(divisor)
    quot_latex = poly_to_latex(quot)
    rem_latex = poly_to_latex(rem)
    
    question_text = f"Divide the polynomial \\({dividend_latex}\\) by \\({divisor_latex}\\). Find the quotient and the remainder."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": quot,
            "remainder_coefficients": rem,
            "quotient_latex": quot_latex,
            "remainder_latex": rem_latex
        },
        "oracle_payload": {
            "dividend_coefficients": dividend,
            "divisor_coefficients": divisor
        }
    }