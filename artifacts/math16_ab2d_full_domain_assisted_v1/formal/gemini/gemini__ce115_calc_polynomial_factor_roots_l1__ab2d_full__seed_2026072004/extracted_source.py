from core.prompts.domain_function_library import PolynomialOps
from fractions import Fraction

def generate(level=1, **kwargs):
    # Default or provided quadratic coefficients
    quadratic_coefficients = kwargs.get("quadratic_coefficients", [1, 4, -12])
    
    a, b, c = quadratic_coefficients
    factors = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    def parse_val(v):
        if isinstance(v, int):
            return Fraction(v, 1)
        if isinstance(v, str):
            if '/' in v:
                num, den = map(int, v.split('/'))
                return Fraction(num, den)
            return Fraction(int(v), 1)
        return Fraction(v)
        
    parsed_factors = []
    for f in factors:
        xc = parse_val(f["x_coefficient"])
        const = parse_val(f["constant"])
        parsed_factors.append((xc, const))
        
    roots_with_factors = []
    for xc, const in parsed_factors:
        root = -const / xc
        roots_with_factors.append((root, xc, const))
        
    # Sort by root ascending
    roots_with_factors.sort(key=lambda item: item[0])
    
    sorted_roots = [item[0] for item in roots_with_factors]
    sorted_factors = [(item[1], item[2]) for item in roots_with_factors]
    
    def format_frac_latex(f):
        if f.denominator == 1:
            return str(f.numerator)
        if f < 0:
            return f"-\\frac{{{-f.numerator}}}{{{f.denominator}}}"
        return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"
        
    def format_factor_latex(x_coeff, const):
        if x_coeff == 1:
            part1 = "x"
        elif x_coeff == -1:
            part1 = "-x"
        else:
            part1 = f"{format_frac_latex(x_coeff)}x"
            
        if const == 0:
            part2 = ""
        elif const > 0:
            part2 = f"+{format_frac_latex(const)}"
        else:
            part2 = f"-{format_frac_latex(-const)}"
            
        return f"({part1}{part2})"
        
    factorization_latex = "".join(format_factor_latex(xc, const) for xc, const in sorted_factors)
    
    r1_str = format_frac_latex(sorted_roots[0])
    r2_str = format_frac_latex(sorted_roots[1])
    roots_latex = f"x = {r1_str}, {r2_str}"
    
    roots_json = [int(r) if r.denominator == 1 else float(r) for r in sorted_roots]
    
    question_text = (
        "將一元二次方程式\n"
        "\\[\n"
        "x^2+4x-12=0\n"
        "\\]\n"
        "的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": roots_json,
            "factorization_latex": factorization_latex,
            "roots_latex": roots_latex
        },
        "oracle_payload": {
            "quadratic_coefficients": quadratic_coefficients
        }
    }