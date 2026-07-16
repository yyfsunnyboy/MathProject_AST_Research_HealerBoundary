from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    oracle_payload = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }
    
    products = oracle_payload["products"]
    
    terms_vals = []
    for p in products:
        left_frac = FractionOps.create(p["left"])
        right_frac = FractionOps.create(p["right"])
        prod_frac = FractionOps.mul(left_frac, right_frac)
        if p["sign"] == -1:
            minus_one = FractionOps.create("-1")
            prod_frac = FractionOps.mul(prod_frac, minus_one)
        terms_vals.append(prod_frac)
        
    total = terms_vals[0]
    for val in terms_vals[1:]:
        total = FractionOps.add(total, val)
        
    num = total.numerator
    den = total.denominator
    if den == 1:
        correct_answer_str = str(num)
    else:
        correct_answer_str = f"{num}/{den}"
        
    terms_strs = []
    for i, p in enumerate(products):
        left = p["left"]
        right = p["right"]
        sign = p["sign"]
        
        left_str = f"({left})" if left.startswith("-") else left
        right_str = f"({right})" if right.startswith("-") else right
        prod_str = f"{left_str} * {right_str}"
        
        if i == 0:
            if sign == -1:
                terms_strs.append(f"-({prod_str})")
            else:
                terms_strs.append(prod_str)
        else:
            if sign == -1:
                terms_strs.append(f"- ({prod_str})")
            else:
                terms_strs.append(f"+ ({prod_str})")
                
    expr_str = " ".join(terms_strs)
    question_text = f"Calculate the exact value of: {expr_str}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": correct_answer_str
        },
        "oracle_payload": oracle_payload
    }