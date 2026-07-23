from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    products = [
        {"left": "2.79", "right": "89.3", "sign": 1},
        {"left": "-0.21", "right": "89.3", "sign": -1}
    ]
    
    # Calculate the exact value using FractionOps
    total_frac = FractionOps.create("0")
    for p in products:
        left_f = FractionOps.create(p["left"])
        right_f = FractionOps.create(p["right"])
        prod_f = FractionOps.mul(left_f, right_f)
        sign_f = FractionOps.create(str(p["sign"]))
        term_f = FractionOps.mul(sign_f, prod_f)
        total_frac = FractionOps.add(total_frac, term_f)
        
    num = total_frac.numerator
    den = total_frac.denominator
    
    if den == 1:
        value_str = f"{num}"
        canonical_latex = f"{num}"
    else:
        value_str = f"{num}/{den}"
        canonical_latex = f"\\frac{{{num}}}{{{den}}}"
        
    # Build LaTeX expression
    latex_parts = []
    for i, p in enumerate(products):
        sign = p["sign"]
        left = p["left"]
        right = p["right"]
        
        if left.startswith("-"):
            left_str = f"({left})"
        else:
            left_str = left
            
        if right.startswith("-"):
            right_str = f"({right})"
        else:
            right_str = right
            
        term_str = f"{left_str} \\times {right_str}"
        
        if i == 0:
            if sign == -1:
                latex_parts.append(f"-{term_str}")
            else:
                latex_parts.append(term_str)
        else:
            if sign == 1:
                latex_parts.append(f"+ {term_str}")
            else:
                latex_parts.append(f"- {term_str}")
                
    latex_expr = " ".join(latex_parts)
    
    question_text = f"Calculate the exact value of the following expression:\n\\[ {latex_expr} \\]"
    
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