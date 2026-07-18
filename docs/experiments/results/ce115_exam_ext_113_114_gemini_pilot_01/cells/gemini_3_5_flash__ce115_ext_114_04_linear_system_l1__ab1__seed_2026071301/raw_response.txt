import re
from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen parameters
    equations = ["37*x + 2*y = 81", "23*x - 2*y = 39"]
    target_expression = "x + 2*y"
    
    # Parse equations
    def parse_equation(eq_str):
        eq_str = eq_str.replace(" ", "")
        lhs, rhs = eq_str.split('=')
        c = int(rhs)
        
        x_match = re.search(r'([+-]?\d*)\*?x', lhs)
        if x_match:
            x_coeff_str = x_match.group(1)
            if x_coeff_str in ('', '+'):
                a = 1
            elif x_coeff_str == '-':
                a = -1
            else:
                a = int(x_coeff_str)
        else:
            a = 0
            
        y_match = re.search(r'([+-]?\d*)\*?y', lhs)
        if y_match:
            y_coeff_str = y_match.group(1)
            if y_coeff_str in ('', '+'):
                b = 1
            elif y_coeff_str == '-':
                b = -1
            else:
                b = int(y_coeff_str)
        else:
            b = 0
        return a, b, c

    a1, b1, c1 = parse_equation(equations[0])
    a2, b2, c2 = parse_equation(equations[1])
    
    D = a1 * b2 - a2 * b1
    Dx = c1 * b2 - c2 * b1
    Dy = a1 * c2 - a2 * c1
    
    x_frac = Fraction(Dx, D)
    y_frac = Fraction(Dy, D)
    
    # Parse target expression
    def parse_expression(expr_str):
        expr_str = expr_str.replace(" ", "")
        x_match = re.search(r'([+-]?\d*)\*?x', expr_str)
        if x_match:
            x_coeff_str = x_match.group(1)
            if x_coeff_str in ('', '+'):
                a = 1
            elif x_coeff_str == '-':
                a = -1
            else:
                a = int(x_coeff_str)
        else:
            a = 0
            
        y_match = re.search(r'([+-]?\d*)\*?y', expr_str)
        if y_match:
            y_coeff_str = y_match.group(1)
            if y_coeff_str in ('', '+'):
                b = 1
            elif y_coeff_str == '-':
                b = -1
            else:
                b = int(y_coeff_str)
        else:
            b = 0
        return a, b

    ta, tb = parse_expression(target_expression)
    val_frac = ta * x_frac + tb * y_frac
    
    def format_fraction(f):
        if f.denominator == 1:
            return f.numerator
        else:
            return f"{f.numerator}/{f.denominator}"
            
    correct_answer = {
        "x": format_fraction(x_frac),
        "y": format_fraction(y_frac),
        "value": format_fraction(val_frac)
    }
    
    question_text = f"Solve the system of linear equations:\n{equations[0]}\n{equations[1]}\n\nFind the value of {target_expression}."
    
    oracle_payload = {
        "equations": equations,
        "target_expression": target_expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }