from fractions import Fraction
import re

def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Evaluate the expression using Fraction
    expr_eval = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expression)
    result = eval(expr_eval, {"Fraction": Fraction})
    
    numerator = result.numerator
    denominator = result.denominator
    
    # Format expression to LaTeX
    latex_expr = expression
    latex_expr = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', latex_expr)
    latex_expr = latex_expr.replace('(', '\\left(').replace(')', '\\right)')
    
    question_text = f"Evaluate the following expression and write the result as an irreducible fraction:\n\n\\[ {latex_expr} \\]"
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": f"\\frac{{{numerator}}}{{{denominator}}}"
    }
    
    oracle_payload = {
        "expression": expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }