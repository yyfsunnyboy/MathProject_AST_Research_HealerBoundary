from core.prompts.domain_function_library import FractionOps, Decimal

def generate(level=1, **kwargs):
    # Parse the frozen parameters to extract numeric values and signs for products
    oracle_payload = kwargs.get("oracle_payload", {})
    
    # Helper function to convert string float to exact rational using Decimal then Fraction
    def str_to_fraction(s_str):
        d = Decimal(s_str)
        return FractionOps.from_parts(int(d.numerator), int(d.denominator))

    products = oracle_payload["products"]
    
    term1_n, term1_d = 0, 1
    term2_n, term2_d = 0, 1
    
    # Calculate first product: left * right (sign is usually absorbed or applied later)
    # The problem asks for A - B where A = 2.79*89.3 and B = (-0.21)*89.3? 
    # Actually the expression is 2.79*89.3 - (-0.21*89.3).
    # Let's parse based on oracle_payload structure:
    # Product 1: left="2.79", right="89.3", sign=1 -> Value = + (2.79 * 89.3)
    # Product 2: left="-0.21", right="89.3", sign=-1 -> This implies the term is - ( (-0.21)*89.3 )? 
    # Or does it mean calculate P = left*right, then apply sign to P in the sum?
    
    # Re-evaluating based on standard math problem generation:
    # Expression: 2.79 * 89.3 - ( -0.21 * 89.3 )
    # Term A = 2.79 * 89.3
    # Term B = (-0.21) * 89.3
    # Result = Term A - Term B
    
    p1_left_str, p1_right_str, _ = products[0]["left"], products[0]["right"], None
    p2_left_str, p2_right_str, sign_p2 = products[1]["left"], products[1]["right"], products[1]["sign"]
    
    # Construct Term A (positive)
    val_a_l = str_to_fraction(p1_left_str)
    val_a_r = str_to_fraction(p1_right_str)
    term_a = FractionOps.mul(val_a_l, val_a_r)
    
    # Construct Term B inside the parenthesis: (-0.21 * 89.3)
    # Note: left is "-0.21". We treat this as a string input to create fraction directly including sign?
    # str_to_fraction handles negative strings correctly (e.g., " -5" -> Fraction(-5, 1))
    val_b_l = str_to_fraction(p2_left_str)
    val_b_r = str_to_fraction(p2_right_str)
    term_b_inside = FractionOps.mul(val_b_l, val_b_r)
    
    # The expression is Term A - (Term B inside)
    final_result = FractionOps.sub(term_a, term_b_inside)
    
    # Prepare correct_answer according to contract: {"value": str, "canonical_latex": str}
    exact_value_str = FractionOps.to_exact(final_result)
    latex_val = FractionOps.to_latex(final_result)
    
    question_text = oracle_payload.get("question_description", "") or "" 
    # The prompt says "use as question_text" the frozen task description.
    # However, the contract requires 'question_text' key in return dict.
    # Usually we reconstruct a clean stem if provided in kwargs or use default.
    # Since no specific reconstruction logic is given other than using frozen desc:
    
    return {
        "question_text": r"精確計算\n\[2.79\times 89.3-\left(-0.21\times 89.3\right).\]\n答案不得使用近似值。",
        "correct_answer": {
            "value": exact_value_str,
            "canonical_latex": latex_val
        },
        "oracle_payload": oracle_payload
    }