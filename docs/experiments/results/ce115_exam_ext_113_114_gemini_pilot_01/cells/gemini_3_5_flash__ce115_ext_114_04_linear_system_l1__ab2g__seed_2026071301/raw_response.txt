import json
from fractions import Fraction

def generate(level=1, **kwargs):
    equations = ["37*x + 2*y = 81", "23*x - 2*y = 39"]
    target_expression = "x + 2*y"
    
    # Solving the system:
    # 37*x + 2*y = 81
    # 23*x - 2*y = 39
    # Adding them: 60*x = 120 => x = 2
    # 2*y = 81 - 37*(2) = 7 => y = 7/2
    # Target: x + 2*y = 2 + 2*(7/2) = 9
    
    x_frac = Fraction(2, 1)
    y_frac = Fraction(7, 2)
    val_frac = Fraction(9, 1)
    
    def format_fraction(f):
        if f.denominator == 1:
            return int(f.numerator)
        return f"{f.numerator}/{f.denominator}"
    
    correct_answer = {
        "x": format_fraction(x_frac),
        "y": format_fraction(y_frac),
        "value": format_fraction(val_frac)
    }
    
    question_text = (
        "Solve the system of linear equations:\n"
        f"{equations[0]}\n"
        f"{equations[1]}\n\n"
        f"Find the value of the expression: {target_expression}"
    )
    
    oracle_payload = {
        "equations": equations,
        "target_expression": target_expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }