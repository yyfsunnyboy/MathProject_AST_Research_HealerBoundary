from fractions import Fraction

def generate(level=1, **kwargs):
    oracle_payload = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }
    
    total = Fraction(0)
    expr_parts = []
    for i, p in enumerate(oracle_payload["products"]):
        left = Fraction(p["left"])
        right = Fraction(p["right"])
        sign = p["sign"]
        total += left * right * sign
        
        term_str = f"({p['left']} * {p['right']})"
        if i == 0:
            if sign == 1:
                expr_parts.append(term_str)
            else:
                expr_parts.append(f"-{term_str}")
        else:
            if sign == 1:
                expr_parts.append(f"+ {term_str}")
            else:
                expr_parts.append(f"- {term_str}")
                
    question_text = f"Calculate the exact value of: {' '.join(expr_parts)}"
    
    if total.denominator == 1:
        correct_answer_val = str(total.numerator)
    else:
        correct_answer_val = f"{total.numerator}/{total.denominator}"
        
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": correct_answer_val
        },
        "oracle_payload": oracle_payload
    }