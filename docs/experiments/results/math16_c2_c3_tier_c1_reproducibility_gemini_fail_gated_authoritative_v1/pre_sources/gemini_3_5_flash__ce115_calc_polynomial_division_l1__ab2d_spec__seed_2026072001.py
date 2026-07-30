# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]

    # Polynomial division algorithm
    def div_qr(dividend, divisor):
        dividend = list(dividend)
        divisor = list(divisor)
        while len(dividend) > 0 and dividend[0] == 0:
            dividend.pop(0)
        while len(divisor) > 0 and divisor[0] == 0:
            divisor.pop(0)
        if not divisor:
            raise ZeroDivisionError()
        if not dividend:
            return [0], [0]
        
        quotient = []
        while len(dividend) >= len(divisor):
            lead_dividend = dividend[0]
            lead_divisor = divisor[0]
            q_coeff = lead_dividend // lead_divisor
            quotient.append(q_coeff)
            
            for i in range(len(divisor)):
                dividend[i] -= q_coeff * divisor[i]
            dividend.pop(0)
        
        while len(dividend) > 0 and dividend[0] == 0:
            dividend.pop(0)
        if not dividend:
            dividend = [0]
        if not quotient:
            quotient = [0]
        return quotient, dividend

    def poly_to_latex(coeffs):
        n = len(coeffs)
        if n == 0:
            return "0"
        terms = []
        for i, c in enumerate(coeffs):
            deg = n - 1 - i
            if c == 0:
                continue
            sign = ""
            if c > 0:
                if terms:
                    sign = " + "
            else:
                if terms:
                    sign = " - "
                    c = -c
                else:
                    sign = "-"
            
            if deg == 0:
                term = f"{c}"
            elif deg == 1:
                if c == 1:
                    term = "x"
                else:
                    term = f"{c}x"
            else:
                if c == 1:
                    term = f"x^{deg}"
                else:
                    term = f"{c}x^{deg}"
            terms.append(f"{sign}{term}")
        if not terms:
            return "0"
        return "".join(terms)

    quotient, remainder = div_qr(dividend_coefficients, divisor_coefficients)

    dividend_latex = poly_to_latex(dividend_coefficients)
    divisor_latex = poly_to_latex(divisor_coefficients)
    quotient_latex = poly_to_latex(quotient)
    remainder_latex = poly_to_latex(remainder)

    question_text = f"Divide the polynomial \\({dividend_latex}\\) by \\({divisor_latex}\\). Find the quotient and the remainder."

    correct_answer = {
        "quotient_coefficients": quotient,
        "remainder_coefficients": remainder,
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