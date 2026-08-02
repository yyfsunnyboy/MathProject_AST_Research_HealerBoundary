from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    # Frozen params
    quadratic_coefficients = [1, 4, -12]
    
    # Factor the quadratic
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
    
    # Calculate roots and sort them
    parsed_factors = []
    for f in factors:
        xc = int(f["x_coefficient"])
        c = int(f["constant"])
        root = -c / xc
        parsed_factors.append((root, f))
        
    # Sort by root ascending
    parsed_factors.sort(key=lambda x: x[0])
    
    roots = [int(r[0]) if r[0].is_integer() else r[0] for r in parsed_factors]
    
    # Format factorization_latex
    latex_factors = []
    for root, f in parsed_factors:
        xc = int(f["x_coefficient"])
        c = int(f["constant"])
        if xc == 1:
            xc_str = "x"
        elif xc == -1:
            xc_str = "-x"
        else:
            xc_str = f"{xc}x"
            
        if c > 0:
            c_str = f"+{c}"
        elif c < 0:
            c_str = f"{c}"
        else:
            c_str = ""
        latex_factors.append(f"({xc_str}{c_str})")
        
    factorization_latex = "".join(latex_factors)
    roots_latex = ", ".join(str(r) for r in roots)
    
    question_text = "將一元二次方程式\n\\[\nx^2+4x-12=0\n\\]\n的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": roots,
            "factorization_latex": factorization_latex,
            "roots_latex": roots_latex
        },
        "oracle_payload": {
            "quadratic_coefficients": quadratic_coefficients
        }
    }