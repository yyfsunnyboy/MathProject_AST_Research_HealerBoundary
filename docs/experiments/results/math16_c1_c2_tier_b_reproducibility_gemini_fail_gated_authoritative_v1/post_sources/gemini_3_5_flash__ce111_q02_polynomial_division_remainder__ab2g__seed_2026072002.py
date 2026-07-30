def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    from fractions import Fraction
    
    def poly_div(dividend, divisor):
        A = [Fraction(x) for x in dividend]
        B = [Fraction(x) for x in divisor]
        while len(A) > 0 and A[0] == 0:
            A.pop(0)
        while len(B) > 0 and B[0] == 0:
            B.pop(0)
        if len(B) == 0:
            raise ZeroDivisionError()
        if len(A) < len(B):
            return [Fraction(0)], A
        Q = [Fraction(0)] * (len(A) - len(B) + 1)
        for i in range(len(Q)):
            coeff = A[i] / B[0]
            Q[i] = coeff
            for j in range(len(B)):
                A[i+j] -= coeff * B[j]
        remainder = A[len(Q):]
        while len(remainder) > 0 and remainder[0] == 0:
            remainder.pop(0)
        if not remainder:
            remainder = [Fraction(0)]
        return Q, remainder

    def poly_to_latex(coeffs):
        n = len(coeffs) - 1
        terms = []
        for i, c in enumerate(coeffs):
            deg = n - i
            if c == 0:
                continue
            if c.denominator == 1:
                c_val = c.numerator
                c_str = str(abs(c_val))
            else:
                c_str = f"\\frac{{{abs(c.numerator)}}}{{{c.denominator}}}"
            sign = "+" if c > 0 else "-"
            if deg == 0:
                term = c_str
            elif deg == 1:
                if abs(c) == 1:
                    term = "x"
                else:
                    term = f"{c_str}x"
            else:
                if abs(c) == 1:
                    term = f"x^{{{deg}}}"
                else:
                    term = f"{c_str}x^{{{deg}}}"
            terms.append((sign, term))
        if not terms:
            return "0"
        res = ""
        for i, (sign, term) in enumerate(terms):
            if i == 0:
                if sign == "-":
                    res += "-" + term
                else:
                    res += term
            else:
                res += f" {sign} {term}"
        return res

    _, remainder_coeffs = poly_div(dividend_coefficients, divisor_coefficients)
    remainder_latex = poly_to_latex(remainder_coeffs)
    
    dividend_latex = poly_to_latex([Fraction(x) for x in dividend_coefficients])
    divisor_latex = poly_to_latex([Fraction(x) for x in divisor_coefficients])
    
    question_text = f"Find the remainder when \\({dividend_latex}\\) is divided by \\({divisor_latex}\\)."
    correct_answer = remainder_latex
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "dividend_coefficients": dividend_coefficients,
            "divisor_coefficients": divisor_coefficients
        }
    }