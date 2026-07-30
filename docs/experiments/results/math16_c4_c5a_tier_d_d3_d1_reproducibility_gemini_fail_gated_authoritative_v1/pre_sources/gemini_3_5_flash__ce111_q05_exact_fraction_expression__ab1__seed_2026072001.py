import re
from fractions import Fraction

def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Parse and evaluate
    expr_mod = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expression)
    val = eval(expr_mod, {"Fraction": Fraction})
    num = val.numerator
    den = val.denominator
    
    # Convert expression to LaTeX
    latex_expr = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', expression)
    latex_expr = latex_expr.replace('(', '\\left(').replace(')', '\\right)')
    
    question_text = f"Evaluate the following expression:\n\\[ {latex_expr} \\]\nWrite your answer as an irreducible fraction."
    
    canonical_latex = f"\\frac{{{num}}}{{{den}}}" if den != 1 else f"{num}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": num,
            "denominator": den,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "expression": expression
        }
    }