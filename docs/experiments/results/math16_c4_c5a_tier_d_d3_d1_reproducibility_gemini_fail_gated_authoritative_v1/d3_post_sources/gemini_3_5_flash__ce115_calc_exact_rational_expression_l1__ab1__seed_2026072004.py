def generate(level=1, **kwargs):
    oracle_payload = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    products = oracle_payload["products"]
    
    terms = []
    for i, prod in enumerate(products):
        left = prod["left"]
        right = prod["right"]
        sign = prod["sign"]
        
        left_fmt = f"({left})" if left.startswith('-') else left
        right_fmt = f"({right})" if right.startswith('-') else right
        
        term_str = f"{left_fmt} \\times {right_fmt}"
        if i == 0:
            if sign == -1:
                terms.append(f"-{term_str}")
            else:
                terms.append(term_str)
        else:
            if sign == 1:
                terms.append(f" + {term_str}")
            else:
                terms.append(f" - {term_str}")
                
    expr_latex = "".join(terms)
    question_text = f"Calculate the exact value of the following expression:\n\\[\n{expr_latex}\n\\]"
    
    from fractions import Fraction
    val = Fraction(0)
    for prod in products:
        val += prod["sign"] * Fraction(prod["left"]) * Fraction(prod["right"])
        
    p = val.numerator
    q = val.denominator
    if q == 1:
        value_str = f"{p}"
        canonical_latex = f"{p}"
    else:
        value_str = f"{p}/{q}"
        canonical_latex = f"\\frac{{{p}}}{{{q}}}"
        
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": value_str,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }