from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    products = [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]
    
    # Calculate using FractionOps
    total = FractionOps.create(0)
    for term in products:
        left_f = FractionOps.create(term["left"])
        right_f = FractionOps.create(term["right"])
        prod = FractionOps.mul(left_f, right_f)
        sign_f = FractionOps.create(term["sign"])
        term_val = FractionOps.mul(sign_f, prod)
        total = FractionOps.add(total, term_val)
        
    numerator = total.numerator
    denominator = total.denominator
    if denominator == 1:
        value_str = str(numerator)
    else:
        value_str = f"{numerator}/{denominator}"
        
    # Build question text
    parts = []
    for i, term in enumerate(products):
        sign = term["sign"]
        left = term["left"]
        right = term["right"]
        term_str = f"({left}) * ({right})"
        if i == 0:
            if sign == -1:
                parts.append(f"-{term_str}")
            else:
                parts.append(term_str)
        else:
            if sign == -1:
                parts.append(f" - {term_str}")
            else:
                parts.append(f" + {term_str}")
                
    question_text = "Evaluate the following expression: " + "".join(parts)
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": value_str
        },
        "oracle_payload": {
            "products": products
        }
    }