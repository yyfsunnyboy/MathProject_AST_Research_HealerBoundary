def generate(level=1, **kwargs):
    products = kwargs.get("products", [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}])

    def parse_decimal_to_fraction(s):
        if '.' in s:
            numerator = int(float(s) * (10 ** len(s.split('.')[1])))
            denominator = 10 ** len(s.split('.')[1])
        else:
            numerator = int(s)
            denominator = 1
        return Fraction(numerator, denominator)

    from fractions import Fraction

    def compute_expression(expr_list):
        result = Fraction(0)
        for item in expr_list:
            left_val = parse_decimal_to_fraction(item["left"])
            right_val = parse_decimal_to_fraction(item["right"])
            sign = item["sign"]
            if sign == 1:
                term = left_val * right_val
            else:
                term = - (left_val * right_val)
            result += term
        return result

    expr_list = products
    exact_result = compute_expression(expr_list)

    numerator_str, denominator_str = str(exact_result.numerator), str(exact_result.denominator)
    
    question_text = r"\text{Calculate the value of } \sum_{i=1}^{2} (\pm 0.79 \times 89.3 + (-0.21) \times 89.3)"

    correct_answer_dict = {
        "value": f"{numerator_str}/{denominator_str}",
        "canonical_latex": r"\frac{{" + numerator_str + "}}{{" + denominator_str + "}}"
    }

    oracle_payload = products

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }