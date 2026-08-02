from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {
        "products": [
            {
                "left": "2.79",
                "right": "89.3",
                "sign": 1
            },
            {
                "left": "-0.21",
                "right": "89.3",
                "sign": -1
            }
        ]
    }

    # Parse the first product: 2.79 * 89.3
    term1_left = FractionOps.create("2.79")
    term1_right = FractionOps.create("89.3")
    prod1 = FractionOps.mul(term1_left, term1_right)

    # Parse the second product: -0.21 * 89.3
    # Note: The sign is handled by the 'left' value "-0.21" in frozen_params
    term2_left = FractionOps.create("-0.21")
    term2_right = FractionOps.create("89.3")
    prod2 = FractionOps.mul(term2_left, term2_right)

    # The expression is: (prod1) - (prod2_sign_adjusted?) 
    # Wait, the frozen_params structure implies we calculate two products and sum them based on signs?
    # Let's re-read the math problem: 2.79*89.3 - (-0.21*89.3)
    # This equals (2.79 * 89.3) + (0.21 * 89.3).
    # However, frozen_params has "left": "-0.21" and "sign": -1 for the second item.
    # If we strictly follow the algebraic expansion of the text:
    # Term A = 2.79 * 89.3
    # Term B = (-0.21) * 89.3 (which is negative)
    # Expression = Term A - Term B = Term A + |Term B|
    
    # Let's calculate the two raw products as defined by the frozen params components directly first to ensure consistency with oracle_payload logic if needed, 
    # but usually we solve the math problem presented.
    # Math: 2.79 * 89.3 - (-0.21 * 89.3)
    
    val_a = FractionOps.mul(FractionOps.create("2.79"), FractionOps.create("89.3"))
    val_b_inner = FractionOps.mul(FractionOps.create("-0.21"), FractionOps.create("89.3")) # This is negative
    
    # The operation is subtraction of the second product: - (val_b_inner)
    final_result = FractionOps.sub(val_a, val_b_inner)

    question_text = "精確計算\n\\[\n2.79\times 89.3-\\left(-0.21\times 89.3\\right).\n\\\]\n答案不得使用近似值。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": FractionOps.to_exact(final_result),
            "canonical_latex": FractionOps.to_latex(final_result)
        },
        "oracle_payload": frozen_params
    }