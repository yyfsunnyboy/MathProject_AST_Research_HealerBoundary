import re
from fractions import Fraction

def generate(level=1, **kwargs):
    expression = kwargs.get("expression", "9/22 + 11/18 - (23/22 - 7/18)")
    
    # Convert expression to LaTeX
    latex_expr = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', expression)
    latex_expr = latex_expr.replace('(', '\\left(').replace(')', '\\right)')
    
    # Evaluate expression safely using Fraction
    eval_expr = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expression)
    result = eval(eval_expr, {"Fraction": Fraction})
    
    numerator = result.numerator
    denominator = result.denominator
    
    if denominator == 1:
        canonical_latex = str(numerator)
    else:
        canonical_latex = f"\\frac{{{numerator}}}{{{denominator}}}"
        
    question_text = f"Evaluate the following expression and write the result as an irreducible fraction:\n\n\\[ {latex_expr} \\]"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "expression": expression
        }
    }