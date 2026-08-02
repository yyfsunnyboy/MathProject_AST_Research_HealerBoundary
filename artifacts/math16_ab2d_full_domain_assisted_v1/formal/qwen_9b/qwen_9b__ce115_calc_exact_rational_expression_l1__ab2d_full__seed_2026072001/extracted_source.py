from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Parse frozen_params from kwargs or default if needed (though task block provides it directly in context usually)
    # However, per instructions: "oracle_payload must exactly equal the frozen_params object provided"
    # We construct the question text and compute the answer.
    
    # 1. Construct Question Text based on frozen description logic but formatted as a stem string if needed.
    # The prompt gives specific numbers: 2.79, 89.3, -0.21, 89.3 with signs + and -.
    # Expression: 2.79 * 89.3 - (-0.21 * 89.3) which is equivalent to (2.79*89.3) + (0.21*89.3) or simply summing the signed products.
    
    # Define operands as strings for FractionOps.create
    term1_left = "2.79"
    term1_right = "89.3"
    sign1 = 1
    
    term2_left = "-0.21"
    term2_right = "89.3"
    sign2 = -1
    
    # Create fractions for the left parts of multiplication (including signs if handled by logic or passed to create)
    # FractionOps.create accepts legal numeric str, including negative numbers like "-0.21".
    
    f_left_1 = FractionOps.create(term1_left)
    f_right_common = FractionOps.create(term1_right)  # Same as term2_right
    
    f_left_2 = FractionOps.create(term2_left)
    
    # Calculate products
    prod1 = FractionOps.mul(f_left_1, f_right_common)
    prod2 = FractionOps.mul(f_left_2, f_right_common)
    
    # Accumulate with signs: result = sign1 * prod1 + sign2 * prod2
    # Since we need exact rational arithmetic and subtraction is available, let's do explicit addition/subtraction.
    # Expression structure in prompt: A - (B). Where B corresponds to (-0.21 * 89.3).
    # So it is prod1 + (-prod2) effectively if prod2 includes the negative sign from "-0.21".
    # Let's verify signs: 
    # Term 1: (+2.79) * 89.3 -> Positive product.
    # Term 2 part inside parens: (-0.21) * 89.3 -> Negative product.
    # Operation outside: minus (negative product) => plus positive magnitude? 
    # Wait, the expression is: 2.79*89.3 - (-0.21*89.3).
    # Let P1 = 2.79 * 89.3.
    # Let P2_inner = -0.21 * 89.3 (which is negative).
    # Expression = P1 - P2_inner = P1 + |P2_inner|.
    
    # Using FractionOps.sub(a, b) computes a - b.
    result = FractionOps.sub(prod1, prod2)
    
    # Get exact value string and latex
    val_str = FractionOps.to_exact(result)
    latex_str = FractionOps.to_latex(result)
    
    # Assemble correct_answer per contract: {"value": str, "canonical_latex": str}
    correct_answer = {
        "value": val_str,
        "canonical_latex": latex_str
    }
    
    # Oracle payload must match the provided frozen_params exactly.
    oracle_payload = {
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

    # Question text: Use the provided description formatted as a stem string if possible, 
    # or reconstruct based on values to ensure it matches the math exactly without approximation artifacts in display.
    question_text = f"精確計算\\n[2.79\\\\times 89.3-(-0.21\\\\times 89.3)].\\n答案不得使用近似值。"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }