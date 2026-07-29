def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    # Parse first product: 2.79 * 89.3
    left1_num, left1_den = int(279), 100
    right1_num, right1_den = int(893), 10
    
    prod1_sign = frozen_params["products"][0]["sign"]
    
    # Parse second product: -0.21 * 89.3
    left2_num, left2_den = int(-21), 100
    right2_num, right2_den = int(893), 10
    
    prod2_sign = frozen_params["products"][1]["sign"]
    
    # Calculate Product 1: (279/100) * (893/10)
    p1_numerator = left1_num * right1_num
    p1_denominator = left1_den * right1_den
    
    # Calculate Product 2: (-21/100) * (893/10)
    p2_numerator = left2_num * right2_num
    p2_denominator = left2_den * right2_den
    
    # Combine products based on signs and structure implied by "products" list in context of expression evaluation.
    # Assuming the task is to compute sum or difference? The spec says "rational_arithmetic". 
    # Given two product terms with specific signs, likely it's a summation: Term1 + Term2 OR Term1 - |Term2| depending on sign field interpretation.
    # Let's assume standard algebraic expansion where 'sign' applies to the term itself relative to zero or previous context.
    # However, looking at typical "products" lists in such tasks, it often implies a sum of products: (A*B) + (C*D). 
    # But here signs are explicit fields. Let's treat them as signed terms added together.
    
    total_numerator = prod1_sign * p1_numerator + prod2_sign * p2_numerator
    total_denominator = p1_denominator  # Denominators might differ, need common denominator
    
    if p1_denominator != p2_denominator:
        lcm_denom = (p1_denominator * p2_denominator) // gcd(p1_denominator, p2_denominator)
        
        term1_adj_numerator = prod1_sign * p1_numerator * (lcm_denom // p1_denominator)
        term2_adj_numerator = prod2_sign * p2_numerator * (lcm_denom // p2_denominator)
        
        total_numerator = term1_adj_numerator + term2_adj_numerator
        total_denominator = lcm_denominator
    
    # Simplify fraction
    common_divisor = gcd(abs(total_numerator), abs(total_denominator))
    
    simplified_num = total_numerator // common_divisor
    simplified_denom = total_denominator // common_divisor
    
    if simplified_denom < 0:
        simplified_num *= -1
        simplified_denom *= -1
        
    # Construct LaTeX string for the answer value (irreducible p/q)
    correct_answer_value_str = f"{simplified_num}/{simplified_denom}"
    
    # Reconstruct original expression text from frozen params to build question_text
    term1_left = frozen_params["products"][0]["left"]
    term1_right = frozen_params["products"][0]["right"]
    sign1_str = "+" if frozen_params["products"][0]["sign"] == 1 else "-"
    
    term2_left = frozen_params["products"][1]["left"]
    term2_right = frozen_params["products"][1]["right"]
    # The second sign in the list is -1. If it's a sum of terms, we write + (-0.21 * 89.3) or just use the value directly? 
    # Usually questions ask to evaluate an expression like "Evaluate: (2.79)(89.3) + (-0.21)(89.3)"
    
    question_text = f"Evaluate the following rational arithmetic expression:\n\n$$({term1_left}) \\cdot ({term1_right}) {sign1_str} ({term2_left}) \\cdot ({term2_right})$$"
    
    # Canonical LaTeX for answer usually just the simplified fraction or mixed number if integer. Here it's a fraction.
    canonical_latex = f"${correct_answer_value_str}$"
    
    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_value_str, "canonical_latex": canonical_latex},
        "oracle_payload": frozen_params
    }

def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)