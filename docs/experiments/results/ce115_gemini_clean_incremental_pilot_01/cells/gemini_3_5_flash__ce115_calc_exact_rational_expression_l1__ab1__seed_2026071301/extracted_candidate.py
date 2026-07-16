from fractions import Fraction

def generate(level=1, **kwargs):
    products = kwargs.get("products", [
        {"left": "2.79", "right": "89.3", "sign": 1},
        {"left": "-0.21", "right": "89.3", "sign": -1}
    ])
    
    val = Fraction(0)
    for p in products:
        val += Fraction(p['left']) * Fraction(p['right']) * p['sign']
        
    if val.denominator == 1:
        correct_answer_str = str(val.numerator)
    else:
        correct_answer_str = f"{val.numerator}/{val.denominator}"
        
    terms = []
    for i, p in enumerate(products):
        left_str = f"({p['left']})" if p['left'].startswith('-') else p['left']
        right_str = f"({p['right']})" if p['right'].startswith('-') else p['right']
        prod_str = f"{left_str} * {right_str}"
        if i == 0:
            if p['sign'] == 1:
                terms.append(prod_str)
            else:
                terms.append(f"-{prod_str}")
        else:
            op = "+" if p['sign'] == 1 else "-"
            terms.append(f"{op} {prod_str}")
            
    expr = " ".join(terms)
    question_text = f"Evaluate the following expression:\n{expr}"
    
    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_str},
        "oracle_payload": {
            "products": products
        }
    }