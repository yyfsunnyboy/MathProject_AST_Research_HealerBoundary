from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    products = [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]
    
    total = FractionOps.create("0")
    for term in products:
        sign_f = FractionOps.create(str(term["sign"]))
        left_f = FractionOps.create(term["left"])
        right_f = FractionOps.create(term["right"])
        prod = FractionOps.mul(left_f, right_f)
        term_val = FractionOps.mul(sign_f, prod)
        total = FractionOps.add(total, term_val)
        
    num = total.numerator
    den = total.denominator
    if den == 1:
        val_str = str(num)
    else:
        val_str = f"{num}/{den}"
        
    expr_parts = []
    for term in products:
        sign_str = f"{term['sign']}"
        left_str = term['left']
        right_str = term['right']
        expr_parts.append(f"({sign_str} * {left_str} * {right_str})")
    question_text = "Evaluate the following expression: " + " + ".join(expr_parts)
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": val_str
        },
        "oracle_payload": {
            "products": products
        }
    }