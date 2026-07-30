from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen parameters
    products = [
        {"left": "2.79", "right": "89.3", "sign": 1},
        {"left": "-0.21", "right": "89.3", "sign": -1}
    ]
    
    # Calculate exact value
    total = Fraction(0)
    for p in products:
        left = Fraction(p["left"])
        right = Fraction(p["right"])
        sign = p["sign"]
        total += sign * left * right
        
    numerator = total.numerator
    denominator = total.denominator
    
    if denominator == 1:
        value_str = str(numerator)
        canonical_latex = str(numerator)
    else:
        value_str = f"{numerator}/{denominator}"
        canonical_latex = f"\\frac{{{numerator}}}{{{denominator}}}"
        
    question_text = "Evaluate the following expression:\n\\[ 2.79 \\times 89.3 - (-0.21) \\times 89.3 \\]"
    
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