from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    products = kwargs.get("products", [
        {"left": "2.79", "right": "89.3", "sign": 1},
        {"left": "-0.21", "right": "89.3", "sign": -1}
    ])
    
    # Calculate exact value using FractionOps
    total = FractionOps.create("0")
    for p in products:
        left_frac = FractionOps.create(p["left"])
        right_frac = FractionOps.create(p["right"])
        prod_frac = FractionOps.mul(left_frac, right_frac)
        sign_frac = FractionOps.create(str(p["sign"]))
        term_frac = FractionOps.mul(sign_frac, prod_frac)
        total = FractionOps.add(total, term_frac)
        
    # Format question text
    terms = []
    for i, p in enumerate(products):
        left_str = p["left"]
        right_str = p["right"]
        sign = p["sign"]
        
        l_fmt = f"({left_str})" if left_str.startswith('-') else left_str
        r_fmt = f"({right_str})" if right_str.startswith('-') else right_str
        
        if i == 0:
            if sign == 1:
                terms.append(f"{l_fmt} \\times {r_fmt}")
            else:
                terms.append(f"- {l_fmt} \\times {r_fmt}")
        else:
            if sign == 1:
                terms.append(f"+ {l_fmt} \\times {r_fmt}")
            else:
                terms.append(f"- {l_fmt} \\times {r_fmt}")

    expression = " ".join(terms)
    question_text = f"Calculate the exact value of the following expression:\n\\[\n{expression}\n\\]"
    
    # Format correct answer
    num = total.numerator
    den = total.denominator
    if den == 1:
        canonical_latex = str(num)
    else:
        if num < 0:
            canonical_latex = f"-\\frac{{{-num}}}{{{den}}}"
        else:
            canonical_latex = f"\\frac{{{num}}}{{{den}}}"
            
    correct_answer = {
        "value": str(total),
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "products": products
        }
    }