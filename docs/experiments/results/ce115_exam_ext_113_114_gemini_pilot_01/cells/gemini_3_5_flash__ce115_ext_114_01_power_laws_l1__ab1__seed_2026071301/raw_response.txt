import ast
from fractions import Fraction

def eval_node(node):
    if isinstance(node, ast.Constant):
        return Fraction(node.value)
    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -eval_node(node.operand)
        elif isinstance(node.op, ast.UAdd):
            return eval_node(node.operand)
    elif isinstance(node, ast.BinOp):
        left = eval_node(node.left)
        right = eval_node(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return Fraction(left, right)
    raise ValueError("Unsupported node in eval")

def get_exponent(node, base):
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Mult):
            return get_exponent(node.left, base) + get_exponent(node.right, base)
        elif isinstance(node.op, ast.Div):
            return get_exponent(node.left, base) - get_exponent(node.right, base)
        elif isinstance(node.op, ast.Pow):
            if isinstance(node.left, ast.Constant) and node.left.value == base:
                return eval_node(node.right)
            else:
                return get_exponent(node.left, base) * eval_node(node.right)
    elif isinstance(node, ast.Constant) and node.value == base:
        return Fraction(1)
    raise ValueError("Unsupported node")

def to_latex(node):
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, ast.Mult):
            return f"{to_latex(node.left)} \\cdot {to_latex(node.right)}"
        elif isinstance(node.op, ast.Div):
            return f"\\frac{{{to_latex(node.left)}}}{{{to_latex(node.right)}}}"
        elif isinstance(node.op, ast.Pow):
            return f"{to_latex(node.left)}^{{{to_latex(node.right)}}}"
    elif isinstance(node, ast.Constant):
        return str(node.value)
    elif isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return f"-{to_latex(node.operand)}"
    return ""

def generate(level=1, **kwargs):
    base = kwargs.get("base", 7)
    expression = kwargs.get("expression", "7**10 * 7**2 / 7**4")
    required_form = kwargs.get("required_form", "power_of_same_base")
    
    node = ast.parse(expression, mode='eval').body
    exponent_fraction = get_exponent(node, base)
    
    if exponent_fraction.denominator == 1:
        exponent = int(exponent_fraction.numerator)
    else:
        exponent = f"{exponent_fraction.numerator}/{exponent_fraction.denominator}"
        
    latex_expr = to_latex(node)
    question_text = f"Simplify the following expression and write the result as a power of {base}:\n\n$${latex_expr}$$"
    
    correct_answer = {
        "base": int(base),
        "exponent": exponent
    }
    
    oracle_payload = {
        "base": base,
        "expression": expression,
        "required_form": required_form
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }