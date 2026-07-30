def generate(level=1, **kwargs):
    from fractions import Fraction

    dividend_coefficients = kwargs.get("dividend_coefficients", [6, 4, 0])
    divisor_coefficients = kwargs.get("divisor_coefficients", [2, 0, 0])

    def strip(lst):
        while len(lst) > 1 and lst[0] == 0:
            lst = lst[1:]
        return lst

    def poly_to_latex(coeffs):
        coeffs = strip(list(coeffs))
        if len(coeffs) == 1 and coeffs[0] == 0:
            return "0"
        
        terms = []
        deg = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            if c == 0:
                continue
            power = deg - i
            
            # Sign and spacing
            if c < 0:
                sign = " - " if terms else "-"
                val = -c
            else:
                sign = " + " if terms else ""
                val = c
                
            # Coefficient string
            is_one = (val == 1)
            
            if isinstance(val, Fraction):
                if val.denominator == 1:
                    val_num = val.numerator
                    is_one = (val_num == 1)
                    c_str = str(val_num)
                else:
                    c_str = f"\\frac{{{val.numerator}}}{{{val.denominator}}}"
                    is_one = False
            else:
                c_str = str(val)
                
            if is_one and power > 0:
                c_str = ""
                
            # Variable
            if power == 0:
                var_str = ""
                if is_one:
                    c_str = "1"
            elif power == 1:
                var_str = "x"
            else:
                var_str = f"x^{power}" if power < 10 else f"x^{{{power}}}"
                
            terms.append(f"{sign}{c_str}{var_str}")
            
        return "".join(terms)

    dividend = strip([Fraction(x).limit_denominator() for x in dividend_coefficients])
    divisor = strip([Fraction(x).limit_denominator() for x in divisor_coefficients])

    if len(divisor) == 1 and divisor[0] == 0:
        raise ZeroDivisionError("Division by zero polynomial.")

    remainder = list(dividend)
    while len(remainder) >= len(divisor) and not (len(remainder) == 1 and remainder[0] == 0):
        lead_rec = remainder[0]
        lead_div = divisor[0]
        factor = lead_rec / lead_div
        
        for i in range(len(divisor)):
            remainder[i] -= factor * divisor[i]
            
        remainder = strip(remainder)

    question_text = f"Find the remainder when ${poly_to_latex(dividend_coefficients)}$ is divided by ${poly_to_latex(divisor_coefficients)}$."
    correct_answer = poly_to_latex(remainder)

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "dividend_coefficients": dividend_coefficients,
            "divisor_coefficients": divisor_coefficients
        }
    }