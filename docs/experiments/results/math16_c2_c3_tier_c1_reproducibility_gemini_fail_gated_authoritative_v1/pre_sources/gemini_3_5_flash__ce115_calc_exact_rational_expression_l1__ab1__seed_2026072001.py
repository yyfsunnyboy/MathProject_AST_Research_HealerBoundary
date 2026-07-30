from fractions import Fraction

def generate(level=1, **kwargs):
    products = [
        {"left": "2.79", "right": "89.3", "sign": 1},
        {"left": "-0.21", "right": "89.3", "sign": -1}
    ]
    
    latex_terms = []
    for i, p in enumerate(products):
        sign = p["sign"]
        left = p["left"]
        right = p["right"]
        
        if i == 0:
            op = "" if sign == 1 else "-"
        else:
            op = " + " if sign == 1 else " - "
            
        if left.startswith("-"):
            if i == 0 and sign == 1:
                left_fmt = left
            else:
                left_fmt = f"({left})"
        else:
            left_fmt = left
            
        if right.startswith("-"):
            right_fmt = f"({right})"
        else:
            right_fmt = right
            
        latex_terms.append(f"{op}{left_fmt} \\times {right_fmt}")
        
    expr_latex = "".join(latex_terms)
    question_text = f"Evaluate the following expression:\n\\[\n{expr_latex}\n\\]"
    
    total = Fraction(0)
    for p in products:
        total += Fraction(p["left"]) * Fraction(p["right"]) * p["sign"]
        
    if total.denominator == 1:
        value_str = str(total.numerator)
        canonical_latex = str(total.numerator)
    else:
        value_str = f"{total.numerator}/{total.denominator}"
        if total.numerator < 0:
            canonical_latex = f"-\\frac{{{-total.numerator}}}{{{total.denominator}}}"
        else:
            canonical_latex = f"\\frac{{{total.numerator}}}{{{total.denominator}}}"
            
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": value_str,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "products": products
        }
    }