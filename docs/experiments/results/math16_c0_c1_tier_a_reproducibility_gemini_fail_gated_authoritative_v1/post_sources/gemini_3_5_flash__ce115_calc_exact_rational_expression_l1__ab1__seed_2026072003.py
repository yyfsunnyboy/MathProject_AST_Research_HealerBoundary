def generate(level=1, **kwargs):
    from fractions import Fraction

    products = [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]
    
    val = Fraction(0)
    for prod in products:
        sign = prod['sign']
        left = Fraction(prod['left'])
        right = Fraction(prod['right'])
        val += sign * left * right
        
    numerator = val.numerator
    denominator = val.denominator
    
    if denominator == 1:
        value_str = str(numerator)
        canonical_latex = str(numerator)
    else:
        value_str = f"{numerator}/{denominator}"
        if numerator < 0:
            canonical_latex = f"-\\frac{{{-numerator}}}{{{denominator}}}"
        else:
            canonical_latex = f"\\frac{{{numerator}}}{{{denominator}}}"
            
    latex_parts = []
    for i, prod in enumerate(products):
        sign = prod['sign']
        left = prod['left']
        right = prod['right']
        
        if i == 0:
            if sign == -1:
                prefix = "-"
            else:
                prefix = ""
        else:
            if sign == -1:
                prefix = " - "
            else:
                prefix = " + "
                
        left_str = f"({left})" if left.startswith('-') else left
        right_str = f"({right})" if right.startswith('-') else right
        
        latex_parts.append(f"{prefix}{left_str} \\cdot {right_str}")
        
    expression_latex = "".join(latex_parts)
    question_text = f"Calculate the exact value of the following expression:\n\\[ {expression_latex} \\]"
    
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