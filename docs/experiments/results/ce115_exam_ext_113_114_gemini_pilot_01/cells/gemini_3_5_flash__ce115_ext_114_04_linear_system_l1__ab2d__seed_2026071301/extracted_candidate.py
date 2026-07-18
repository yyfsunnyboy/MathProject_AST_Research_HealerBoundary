import re
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    equations = ["37*x + 2*y = 81", "23*x - 2*y = 39"]
    target_expression = "x + 2*y"
    
    def parse_eq(eq_str):
        eq_str = eq_str.replace(" ", "")
        match = re.match(r'(-?\d+)\*x([+-]\d+)\*y=(-?\d+)', eq_str)
        if match:
            return tuple(map(int, match.groups()))
        raise ValueError(f"Could not parse equation: {eq_str}")

    a1, b1, c1 = parse_eq(equations[0])
    a2, b2, c2 = parse_eq(equations[1])
    
    D = a1 * b2 - a2 * b1
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1
    
    x_frac = FractionOps.create(f"{Dx}/{D}")
    y_frac = FractionOps.create(f"{Dy}/{D}")
    
    target_str = target_expression.replace(" ", "")
    match_target = re.match(r'(-?\d*)\*?x([+-]\d*)\*?y', target_str)
    if match_target:
        g1, g2 = match_target.groups()
        t_a = int(g1) if g1 and g1 != '-' else (-1 if g1 == '-' else 1)
        t_b = int(g2) if g2 and g2 not in ('+', '-') else (-1 if g2 == '-' else 1)
    else:
        t_a, t_b = 1, 2
        
    coeff_x = FractionOps.create(t_a)
    coeff_y = FractionOps.create(t_b)
    
    term1 = FractionOps.mul(coeff_x, x_frac)
    term2 = FractionOps.mul(coeff_y, y_frac)
    val_frac = FractionOps.add(term1, term2)
    
    def format_fraction(f):
        if f.denominator == 1:
            return int(f.numerator)
        else:
            return f"{f.numerator}/{f.denominator}"
            
    x_val = format_fraction(x_frac)
    y_val = format_fraction(y_frac)
    ans_val = format_fraction(val_frac)
    
    question_text = (
        f"Solve the system of linear equations:\n"
        f"{equations[0]}\n"
        f"{equations[1]}\n\n"
        f"Find the value of {target_expression}."
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "x": x_val,
            "y": y_val,
            "value": ans_val
        },
        "oracle_payload": {
            "equations": equations,
            "target_expression": target_expression
        }
    }