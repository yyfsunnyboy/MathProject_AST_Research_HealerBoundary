from fractions import Fraction

def generate(level=1, **kwargs):
    oracle_payload = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }
    
    products = oracle_payload["products"]
    
    parts = []
    for i, p in enumerate(products):
        left = p["left"]
        right = p["right"]
        sign = p["sign"]
        
        left_str = f"({left})" if left.startswith('-') else left
        right_str = f"({right})" if right.startswith('-') else right
        prod_str = f"{left_str} * {right_str}"
        
        if i == 0:
            if sign == -1:
                parts.append(f"-{prod_str}")
            else:
                parts.append(prod_str)
        else:
            if sign == -1:
                parts.append(f" - {prod_str}")
            else:
                parts.append(f" + {prod_str}")
                
    expression = "".join(parts)
    question_text = f"Calculate the exact value of the following expression:\n{expression}"
    
    total = Fraction(0)
    for p in products:
        left = Fraction(p["left"])
        right = Fraction(p["right"])
        sign = p["sign"]
        total += left * right * sign
        
    if total.denominator == 1:
        value_str = str(total.numerator)
    else:
        value_str = f"{total.numerator}/{total.denominator}"
        
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": value_str
        },
        "oracle_payload": oracle_payload
    }