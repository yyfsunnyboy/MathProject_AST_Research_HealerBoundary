def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    from fractions import Fraction

    def strip_leading_zeros(lst):
        while len(lst) > 1 and lst[0] == 0:
            lst = lst[1:]
        return lst

    div_d = strip_leading_zeros(list(dividend_coefficients))
    div_s = strip_leading_zeros(list(divisor_coefficients))

    dividend = [Fraction(x) for x in div_d]
    divisor = [Fraction(x) for x in div_s]

    remainder = list(dividend)

    while len(remainder) >= len(divisor):
        coeff = remainder[0] / divisor[0]
        deg_diff = len(remainder) - len(divisor)
        subtrahend = [coeff * x for x in divisor] + [Fraction(0)] * deg_diff
        remainder = [r - s for r, s in zip(remainder, subtrahend)]
        remainder = strip_leading_zeros(remainder)

    remainder_coeffs = [int(x) if x.denominator == 1 else float(x) for x in remainder]

    def poly_to_latex(coeffs, var='x', spaced=False):
        while len(coeffs) > 1 and coeffs[0] == 0:
            coeffs = coeffs[1:]
        if len(coeffs) == 1 and coeffs[0] == 0:
            return "0"
        
        terms = []
        deg = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            power = deg - i
            if c == 0:
                continue
            
            if c > 0:
                if terms:
                    sign = " + " if spaced else "+"
                else:
                    sign = ""
            else:
                if terms:
                    sign = " - " if spaced else "-"
                else:
                    sign = "-"
            
            abs_c = abs(c)
            if abs_c == 1 and power > 0:
                c_str = ""
            else:
                if isinstance(abs_c, float) and abs_c.is_integer():
                    c_str = str(int(abs_c))
                else:
                    c_str = str(abs_c)
            
            if power == 0:
                v_str = str(abs_c) if c_str == "" else c_str
            elif power == 1:
                v_str = f"{c_str}{var}"
            else:
                v_str = f"{c_str}{var}^{{{power}}}"
                
            terms.append(f"{sign}{v_str}")
            
        return "".join(terms)

    dividend_latex = poly_to_latex(dividend_coefficients, spaced=True)
    divisor_latex = poly_to_latex(divisor_coefficients, spaced=True)
    remainder_latex = poly_to_latex(remainder_coeffs, spaced=False)

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