from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    oracle_payload = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    products = oracle_payload["products"]
    
    # Calculate using FractionOps
    total = FractionOps.create("0")
    for prod in products:
        left_frac = FractionOps.create(prod["left"])
        right_frac = FractionOps.create(prod["right"])
        sign_frac = FractionOps.create(str(prod["sign"]))
        
        term = FractionOps.mul(left_frac, right_frac)
        term = FractionOps.mul(term, sign_frac)
        total = FractionOps.add(total, term)
        
    # Format correct_answer
    p = total.numerator
    q = total.denominator
    if q == 1:
        value = f"{p}"
        canonical_latex = f"{p}"
    else:
        value = f"{p}/{q}"
        canonical_latex = f"\\frac{{{p}}}{{{q}}}"
        
    # Format question_text
    terms_latex = []
    for i, prod in enumerate(products):
        left_str = prod['left']
        right_str = prod['right']
        sign = prod['sign']
        
        if left_str.startswith('-'):
            left_fmt = f"({left_str})"
        else:
            left_fmt = left_str
            
        if right_str.startswith('-'):
            right_fmt = f"({right_str})"
        else:
            right_fmt = right_str
            
        term_str = f"{left_fmt} \\times {right_fmt}"
        
        if i == 0:
            if sign == -1:
                terms_latex.append(f"-{term_str}")
            else:
                terms_latex.append(term_str)
        else:
            if sign == 1:
                terms_latex.append(f"+ {term_str}")
            else:
                terms_latex.append(f"- {term_str}")

    expression_latex = " ".join(terms_latex)
    question_text = f"Calculate the exact value of the expression:\n\\[ {expression_latex} \\]"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": value,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }