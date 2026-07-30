from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen parameters
    oracle_payload = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }
    
    # Calculate exact value
    total = Fraction(0)
    terms_latex = []
    for i, p in enumerate(oracle_payload["products"]):
        left_val = Fraction(p["left"])
        right_val = Fraction(p["right"])
        sign = p["sign"]
        total += sign * left_val * right_val
        
        # Format for LaTeX
        if left_val < 0:
            left_str = f"({p['left']})"
        else:
            left_str = p['left']
            
        if right_val < 0:
            right_str = f"({p['right']})"
        else:
            right_str = p['right']
            
        prod_str = f"{left_str} \\times {right_str}"
        
        if i == 0:
            if sign == -1:
                terms_latex.append(f"-{prod_str}")
            else:
                terms_latex.append(prod_str)
        else:
            if sign == 1:
                terms_latex.append(f"+ {prod_str}")
            elif sign == -1:
                terms_latex.append(f"- {prod_str}")
                
    expr_latex = " ".join(terms_latex)
    question_text = f"Calculate the exact value of the following expression:\n\n\\[ {expr_latex} \\]"
    
    # Format correct answer
    p = total.numerator
    q = total.denominator
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