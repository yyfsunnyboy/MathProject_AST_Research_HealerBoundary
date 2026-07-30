# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    def div_qr(dividend, divisor):
        if len(divisor) == 0 or divisor == [0]:
            raise ZeroDivisionError()
        
        while len(divisor) > 0 and divisor[0] == 0:
            divisor = divisor[1:]
        while len(dividend) > 0 and dividend[0] == 0:
            dividend = dividend[1:]
            
        if len(dividend) < len(divisor):
            return [0], dividend
            
        quot_len = len(dividend) - len(divisor) + 1
        quot = [0] * quot_len
        rem = list(dividend)
        
        for i in range(quot_len):
            coeff = rem[i] / divisor[0]
            quot[i] = coeff
            for j in range(len(divisor)):
                rem[i + j] -= coeff * divisor[j]
                
        rem = rem[quot_len:]
        while len(rem) > 0 and rem[0] == 0:
            rem = rem[1:]
        if not rem:
            rem = [0]
            
        quot = [int(x) if x == int(x) else x for x in quot]
        rem = [int(x) if x == int(x) else x for x in rem]
        return quot, rem

    def to_latex(coeffs):
        n = len(coeffs)
        if n == 0 or coeffs == [0]:
            return "0"
        
        terms = []
        for i, c in enumerate(coeffs):
            if c == 0:
                continue
            deg = n - 1 - i
            
            sign = ""
            if c < 0:
                sign = "-"
                val = -c
            else:
                if len(terms) > 0:
                    sign = "+"
                val = c
                
            if val == 1 and deg > 0:
                c_str = ""
            else:
                c_str = str(val)
                
            if deg == 0:
                var_str = ""
                if val == 1 and c_str == "":
                    c_str = "1"
            elif deg == 1:
                var_str = "x"
            else:
                var_str = f"x^{deg}"
                
            terms.append(f"{sign}{c_str}{var_str}")
            
        latex_str = ""
        for i, term in enumerate(terms):
            if i == 0:
                latex_str += term
            else:
                op = term[0]
                rest = term[1:]
                latex_str += f" {op} {rest}"
        return latex_str

    quotient_coefficients, remainder_coefficients = div_qr(dividend_coefficients, divisor_coefficients)
    quotient_latex = to_latex(quotient_coefficients)
    remainder_latex = to_latex(remainder_coefficients)
    
    dividend_latex = to_latex(dividend_coefficients)
    divisor_latex = to_latex(divisor_coefficients)
    
    question_text = f"Divide the polynomial \\({dividend_latex}\\) by \\({divisor_latex}\\). Find the quotient and the remainder."
    
    correct_answer = {
        "quotient_coefficients": quotient_coefficients,
        "remainder_coefficients": remainder_coefficients,
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