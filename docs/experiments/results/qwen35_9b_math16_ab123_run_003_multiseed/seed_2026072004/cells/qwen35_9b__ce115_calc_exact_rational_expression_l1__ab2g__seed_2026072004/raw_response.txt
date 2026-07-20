def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    from fractions import Fraction
    
    def parse_decimal(s):
        if '.' in s:
            parts = s.split('.')
            integer_part = int(parts[0]) * 10 ** len(parts[1]) + int(parts[1])
            return Fraction(integer_part, 10 ** len(parts[1]))
        else:
            return Fraction(int(s))

    def simplify_term(num_str):
        f_num = parse_decimal(num_str)
        
        # Handle implicit multiplication by the right side (89.3) for each product term
        base_val = parse_decimal("89.3")
        
        if frozen_params["products"][0]["sign"] == 1:
            term1 = f_num * base_val
        else:
            term2 = -f_num * base_val
            
        # Combine terms based on sign logic in the prompt structure (sum of products)
        # The task implies calculating A*B + C*D where signs are provided.
        total_term = frozen_params["products"][0]["left"] if frozen_params["products"][0]["sign"] == 1 else -frozen_params["products"][0]["parse_decimal"](frozen_params["products"][0]["right"]) # Correction: Re-reading logic
        
    # Correct implementation based on standard rational expression structure for this specific task ID
    term_a = parse_decimal("2.79") * parse_decimal("89.3")
    term_b = -1 * parse_decimal("-0.21") * parse_decimal("89.3") 
    
    # Re-evaluating the input: "left": "-0.21", sign: -1 implies value is (-(-0.21)) or just using the number with the sign?
    # Usually, these tasks represent terms like (A) + (B). 
    # Term 1: left=2.79, right=89.3, sign=1 -> 2.79 * 89.3
    # Term 2: left=-0.21, right=89.3, sign=-1 -> -(-0.21) * 89.3 OR (-0.21)*89.3 with a negative sign applied? 
    # Standard interpretation for these generated tasks: sum(left_i * right_i). The 'sign' field often dictates the operation or if it's added/subtracted.
    # Let's assume standard summation of products where left/right are values and sign indicates contribution direction relative to a baseline, but usually in math16_exact_rational_expression:
    # It is likely (2.79 * 89.3) + (-0.21 * 89.3). The 'sign' field might be redundant or indicate the operator if it wasn't always '+'. 
    # However, looking at typical datasets for this task ID: "products" list usually defines terms to sum.
    # If sign is -1 on "-0.21", does it mean subtract (-0.21 * 89.3) which adds positive? Or just multiply and add?
    # Let's calculate the raw values first without over-interpreting ambiguous 'sign' flags unless they denote operators. 
    # Hypothesis: The expression is simply sum(left_i * right_i). The sign field might be metadata for generation or specific operator logic (e.g., term 2 is subtracted).
    # If we strictly follow "sum of products":
    
    val1 = parse_decimal("2.79") * parse_decimal("89.3")
    val2 = -parse_decimal("-0.21") * parse_decimal("89.3") if frozen_params["products"][1]["sign"] == 1 else (-(parse_decimal("-0.21")) * parse_decimal("89.3")) # Wait, let's simplify logic:
    
    # Refined Logic for "math16_exact_rational_expression": 
    # It calculates the value of the expression defined by products. 
    # Term 1: 2.79 * 89.3
    # Term 2: -0.21 * 89.3 (if sign is part of the number) OR (-0.21)*89.3 added/subtracted?
    # Given "sign": -1, it likely means subtract this product from the first one? Or the term itself has a negative coefficient?
    # Let's assume the expression is: Term1 + (Sign_of_Term * Value_Left * Right). 
    # Actually, looking at similar tasks: The 'products' list defines additive terms. If sign is -1, it might mean subtract that specific product calculation from the total sum.
    # But wait, if left is "-0.21", calculating (-0.21)*89.3 gives a negative number. Subtracting a negative adds positive. 
    # Let's try: Result = (2.79 * 89.3) + (-1) * (-0.21 * 89.3).
    
    term_1 = parse_decimal("2.79") * parse_decimal("89.3")
    product_2_val = parse_decimal("-0.21") * parse_decimal("89.3")
    sign_factor = frozen_params["products"][1]["sign"] # -1
    
    final_result = term_1 + (sign_factor * product_2_val)
    
    irreducible_str = str(final_result.numerator) + "/" + str(final_result.denominator) if final_result.denominator != 1 else str(final_result.numerator)
    canonical_latex = f"{final_result.numerator}/{final_result.denominator}" if final_result.denominator != 1 else str(final_result.numerator)

    question_text = r"The value of the rational expression is $2.79 \times 89.3 + (-0.21) \times 89.3$." # Simplified text based on inputs
    
    return {
        "question_text": f"Calculate: ${r'\text{term}_1'} = ({frozen_params['products'][0]['left']}) \\cdot ({frozen_params['products'][0]['right']})) + ({sign_factor} \times (({frozen_params['products'][1]['left']}) \\cdot ({frozen_params['products'][1]['right']})))",
        "correct_answer": {
            "value": irreducible_str,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }