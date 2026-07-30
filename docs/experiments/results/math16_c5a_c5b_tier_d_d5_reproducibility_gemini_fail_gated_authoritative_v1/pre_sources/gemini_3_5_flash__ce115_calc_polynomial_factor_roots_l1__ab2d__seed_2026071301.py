from core.prompts.domain_function_library import PolynomialOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    quadratic_coefficients = [1, 4, -12]
    
    a, b, c = quadratic_coefficients
    
    # Factor the quadratic
    factors = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Calculate roots and sort factors
    factor_roots = []
    for f in factors:
        p = FractionOps.create(f['x_coefficient'])
        q = FractionOps.create(f['constant'])
        root = -q / p
        factor_roots.append((root, f))
        
    # Sort by root ascending
    factor_roots.sort(key=lambda x: x[0])
    
    # Extract sorted roots
    sorted_roots = [fr[0] for fr in factor_roots]
    
    # Convert roots to int if they are integers, otherwise keep as Fraction or string
    roots_val = []
    for r in sorted_roots:
        if r.denominator == 1:
            roots_val.append(int(r.numerator))
        else:
            roots_val.append(f"{r.numerator}/{r.denominator}")
            
    # Format factorization_latex
    def to_latex_frac(frac):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            if frac.numerator < 0:
                return f"-\\frac{{{abs(frac.numerator)}}}{{{frac.denominator}}}"
            return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
            
    def format_factor_latex(f):
        p = FractionOps.create(f['x_coefficient'])
        q = FractionOps.create(f['constant'])
        
        if p == 1:
            p_str = "x"
        elif p == -1:
            p_str = "-x"
        else:
            p_str = f"{to_latex_frac(p)}x"
            
        if q > 0:
            return f"({p_str} + {to_latex_frac(q)})"
        elif q < 0:
            return f"({p_str} - {to_latex_frac(-q)})"
        else:
            return f"({p_str})"
            
    factorization_latex = "".join(format_factor_latex(fr[1]) for fr in factor_roots)
    
    # Format roots_latex
    roots_latex_parts = []
    for r in sorted_roots:
        roots_latex_parts.append(to_latex_frac(r))
    roots_latex = f"x = {', '.join(roots_latex_parts)}"
    
    # Format polynomial for question
    def format_polynomial(a, b, c):
        terms = []
        if a == 1:
            terms.append("x^2")
        elif a == -1:
            terms.append("-x^2")
        elif a != 0:
            terms.append(f"{a}x^2")
            
        if b == 1:
            terms.append("+ x")
        elif b == -1:
            terms.append("- x")
        elif b > 0:
            terms.append(f"+ {b}x")
        elif b < 0:
            terms.append(f"- {-b}x")
            
        if c > 0:
            terms.append(f"+ {c}")
        elif c < 0:
            terms.append(f"- {-c}")
            
        return " ".join(terms).replace("+ -", "- ")
        
    poly_latex = format_polynomial(a, b, c)
    
    question_text = f"Factor the polynomial ${poly_latex}$ and find its roots."
    
    correct_answer = {
        "roots": roots_val,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "quadratic_coefficients": quadratic_coefficients
        }
    }