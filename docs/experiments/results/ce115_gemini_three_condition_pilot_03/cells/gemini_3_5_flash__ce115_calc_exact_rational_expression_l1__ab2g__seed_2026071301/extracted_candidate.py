from fractions import Fraction

def generate(level=1, **kwargs):
    oracle_payload = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }
    
    # Calculate exact value
    val = Fraction(0)
    for p in oracle_payload["products"]:
        term = Fraction(p["left"]) * Fraction(p["right"])
        val += p["sign"] * term
        
    # Format correct answer
    if val.denominator == 1:
        ans_str = str(val.numerator)
    else:
        ans_str = f"{val.numerator}/{val.denominator}"
        
    # Format expression
    def format_number(num_str):
        if num_str.startswith('-'):
            return f"({num_str})"
        return num_str

    parts = []
    for i, p in enumerate(oracle_payload["products"]):
        left = format_number(p['left'])
        right = format_number(p['right'])
        term = f"{left} * {right}"
        sign = p['sign']
        if i == 0:
            if sign == -1:
                parts.append(f"-{term}")
            else:
                parts.append(term)
        else:
            if sign == -1:
                parts.append(f" - {term}")
            else:
                parts.append(f" + {term}")
    expr = "".join(parts)
    
    question_text = f"Calculate the exact value of the following expression:\n{expr}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": ans_str
        },
        "oracle_payload": oracle_payload
    }