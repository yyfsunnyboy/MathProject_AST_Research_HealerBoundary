# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import PolynomialOps

def poly_to_latex(coeffs):
    while len(coeffs) > 1 and coeffs[0] == 0:
        coeffs = coeffs[1:]
    if not coeffs or coeffs == [0]:
        return "0"
    
    terms = []
    deg = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        power = deg - i
        if c == 0:
            continue
        
        sign = ""
        if c < 0:
            sign = "-"
            val = -c
        else:
            if terms:
                sign = " + "
            val = c
            
        if val == 1 and power > 0:
            c_str = ""
        else:
            if hasattr(val, 'denominator') and val.denominator != 1:
                c_str = f"\\frac{{{val.numerator}}}{{{val.denominator}}}"
            else:
                c_str = str(int(val))
                
        if power == 0:
            x_str = ""
            if c_str == "":
                c_str = "1"
        elif power == 1:
            x_str = "x"
        else:
            x_str = f"x^{{{power}}}"
            
        terms.append(f"{sign}{c_str}{x_str}")
        
    res = "".join(terms)
    res = res.replace(" + -", " - ")
    return res

def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Perform polynomial division using PolynomialOps
    quotient, remainder = PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients)
    
    # Ensure remainder coefficients are standard Python types for JSON serialization
    remainder = [int(x) if float(x).is_integer() else float(x) for x in remainder]
    
    def to_latex(coeffs):
        try:
            return PolynomialOps.to_latex(coeffs)
        except AttributeError:
            return poly_to_latex(coeffs)
            
    dividend_latex = to_latex(dividend_coefficients)
    divisor_latex = to_latex(divisor_coefficients)
    canonical_latex = to_latex(remainder)
    
    question_text = f"Find the remainder when the polynomial \\({dividend_latex}\\) is divided by \\({divisor_latex}\\)."
    
    correct_answer = {
        "remainder": remainder,
        "canonical_latex": canonical_latex
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