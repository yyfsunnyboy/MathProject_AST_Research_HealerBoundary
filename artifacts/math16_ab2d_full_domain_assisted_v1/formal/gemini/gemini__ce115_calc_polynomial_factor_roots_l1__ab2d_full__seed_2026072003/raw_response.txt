from core.prompts.domain_function_library import PolynomialOps
from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen task description
    question_text = "將一元二次方程式\n\\[\nx^2+4x-12=0\n\\]\n的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"
    
    oracle_payload = {
        "quadratic_coefficients": [1, 4, -12]
    }
    
    coeffs = oracle_payload["quadratic_coefficients"]
    a, b, c = coeffs[0], coeffs[1], coeffs[2]
    
    factors = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Parse factors and compute roots
    parsed_factors = []
    for f in factors:
        def parse_val(v):
            if isinstance(v, int):
                return Fraction(v)
            if isinstance(v, str):
                if '/' in v:
                    num, den = map(int, v.split('/'))
                    return Fraction(num, den)
                return Fraction(int(v))
            return Fraction(v)
        
        coeff = parse_val(f["x_coefficient"])
        const = parse_val(f["constant"])
        root = -const / coeff
        parsed_factors.append({
            "coeff": coeff,
            "const": const,
            "root": root,
            "orig": f
        })
    
    # Sort by root ascending
    parsed_factors.sort(key=lambda x: x["root"])
    
    # Format roots
    roots = []
    for pf in parsed_factors:
        r = pf["root"]
        if r.denominator == 1:
            roots.append(r.numerator)
        else:
            roots.append(float(r))
            
    # Format roots_latex
    def format_frac_latex(frac):
        if frac.denominator == 1:
            return str(frac.numerator)
        sign = "-" if frac < 0 else ""
        num = abs(frac.numerator)
        den = frac.denominator
        return f"{sign}\\frac{{{num}}}{{{den}}}"
        
    r1_latex = format_frac_latex(parsed_factors[0]["root"])
    r2_latex = format_frac_latex(parsed_factors[1]["root"])
    roots_latex = f"x_1 = {r1_latex}, x_2 = {r2_latex}"
    
    # Format factorization_latex
    factor_strings = []
    for pf in parsed_factors:
        coeff = pf["coeff"]
        const = pf["const"]
        
        if coeff == 1:
            term1 = "x"
        elif coeff == -1:
            term1 = "-x"
        else:
            term1 = f"{format_frac_latex(coeff)}x"
            
        if const == 0:
            f_str = term1
        elif const > 0:
            f_str = f"({term1}+{format_frac_latex(const)})"
        else:
            f_str = f"({term1}-{format_frac_latex(-const)})"
        factor_strings.append(f_str)
        
    factorization_latex = "".join(factor_strings)
    
    correct_answer = {
        "roots": roots,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }