def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    # Convert decimal strings to exact fractions for arithmetic
    from fractions import Fraction
    
    def parse_decimal(s):
        if '.' in s:
            parts = s.split('.')
            integer_part = int(parts[0])
            fractional_part_str = parts[1]
            numerator = int(fractional_part_str) + (integer_part * 10 ** len(fractional_part_str))
            denominator = 10 ** len(fractional_part_str)
            return Fraction(numerator, denominator)
        else:
            return Fraction(int(s), 1)

    # Process first product term
    left1 = parse_decimal("2.79")   # 279/100
    right1 = parse_decimal("89.3")  # 893/10
    
    if frozen_params["products"][0]["sign"] == 1:
        val1 = left1 * right1       # (279*893)/(100*10)
    else:
        val1 = -(left1 * right1)

    # Process second product term
    left2 = parse_decimal("-0.21")  # -21/100
    right2 = parse_decimal("89.3")  # 893/10
    
    if frozen_params["products"][1]["sign"] == 1:
        val2 = left2 * right2       # (-21*893)/(100*10)
    else:
        val2 = -(left2 * right2)

    total_value = val1 + val2
    
    # Simplify the result to irreducible p/q form if needed (Fraction does this automatically)
    numerator, denominator = total_value.numerator, total_value.denominator
    
    correct_answer_str = f"{numerator}/{denominator}"
    
    question_text = r"Compute the exact value of: $2.79 \times 89.3 + (-0.21) \times 89.3$"
    canonical_latex = rf"\frac{{{numerator}}}{{{{{denominator}}}}}"

    return {
        "question_text": question_text,
        "correct_answer": f"value={correct_answer_str}, canonical_latex={canonical_latex}",
        "oracle_payload": frozen_params
    }