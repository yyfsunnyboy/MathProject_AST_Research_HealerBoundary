def generate(level=1, **kwargs):
    import json
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    # Parse inputs as fractions to ensure exact arithmetic
    def parse_fraction(s):
        if '.' in s:
            num, den = str(int(float(s) * 100), int(100))
            return Fraction(num, den)
        else:
            return Fraction(int(s), 1)

    from fractions import Fraction
    
    p1_left = parse_fraction("2.79") # 279/100
    p1_right = parse_fraction("89.3") # 893/10
    sign1 = frozen_params["products"][0]["sign"]

    p2_left = parse_fraction("-0.21") # -21/100
    p2_right = parse_fraction("89.3") # 893/10
    sign2 = frozen_params["products"][1]["sign"]

    term1 = Fraction(p1_left) * (Fraction(sign1, 1) * Fraction(p1_right))
    term2 = Fraction(p2_left) * (Fraction(sign2, 1) * Fraction(p2_right))
    
    result = term1 + term2
    
    # Format canonical answer: integer or irreducible p/q with positive denominator
    if result.denominator == 1:
        ans_str = str(result.numerator)
    else:
        q_sign = -1 if result.denominator < 0 else 1
        num_abs = abs(result.numerator)
        den_abs = abs(result.denominator)
        # Ensure positive denominator in string representation per spec "positive denominator"
        ans_str = f"{q_sign * num_abs}/{den_abs}"

    question_text = f"What is the exact value of {frozen_params['products'][0]['left']} × {frozen_params['products'][0]['right']}{'' if frozen_params['products'][0]['sign']==1 else '× -'} + {frozen_params['products'][1]['left']} × {frozen_params['products'][1]['right']}{'' if frozen_params['products'][1]['sign']==-1 else '× -'}?"
    
    correct_answer = {"value": ans_str}
    oracle_payload = json.dumps(frozen_params)

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }