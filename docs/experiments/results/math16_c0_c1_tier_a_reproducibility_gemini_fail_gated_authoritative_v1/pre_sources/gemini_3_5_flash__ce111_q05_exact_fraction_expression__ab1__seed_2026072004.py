import re
from fractions import Fraction

def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Parse and evaluate
    safe_str = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expression)
    result = eval(safe_str, {"Fraction": Fraction})
    
    # Convert expression to LaTeX
    latex_expr = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', expression)
    latex_expr = latex_expr.replace('(', '\\left(').replace(')', '\\right)')
    
    question_text = f"Evaluate the following expression and write the result as an irreducible fraction:\n\\[ {latex_expr} \\]"
    
    if result.denominator == 1:
        canonical_latex = str(result.numerator)
    else:
        if result.numerator < 0:
            canonical_latex = f"-\\frac{{{-result.numerator}}}{{{result.denominator}}}"
        else:
            canonical_latex = f"\\frac{{{result.numerator}}}{{{result.denominator}}}"
            
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "expression": expression
        }
    }