from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Parse frozen_params from kwargs or default structure if needed for robustness
    # The prompt implies we use the provided frozen description logic but must return specific schema.
    # We reconstruct the calculation based on the "Frozen task description" values: 2.79*89.3 - (-0.21*89.3)
    
    # Step 1: Create fractions from string inputs as per instructions
    val_1 = FractionOps.create("2.79")
    val_2 = FractionOps.create("89.3")
    val_neg_sign = FractionOps.create("-0.21")
    
    # Note: The expression is 2.79 * 89.3 - (-0.21 * 89.3)
    # This equals (2.79 * 89.3) + (0.21 * 89.3) effectively, or strictly following the text:
    # Term A = val_1 * val_2
    # Term B = (-val_neg_sign) * val_2  -> wait, input is "-0.21". 
    # Let's stick to exact string parsing provided in frozen_params logic if available, 
    # but here we generate the math directly from the text description values.
    
    term_a = FractionOps.mul(val_1, val_2)
    
    # The second part is - (-0.21 * 89.3). 
    # Let's create the negative fraction explicitly to handle signs correctly in accumulation logic if needed,
    # or just compute the product of "-0.21" and "89.3".
    term_b_product = FractionOps.mul(FractionOps.create("-0.21"), val_2)
    
    # The expression is: Term A - (Term B Product)
    # Since Term B Product includes the negative sign in its value (-0.21 * 89.3), 
    # subtracting it means adding the absolute magnitude of that product.
    final_result = FractionOps.sub(term_a, term_b_product)
    
    # Step 4: Assemble correct_answer exactly according to the Answer contract
    # Schema: {"value": str, "canonical_latex": str}
    # Use to_exact for serialization if needed, but value should be string representation of exact rational.
    # FractionOps.to_exact returns int or 'p/q'. We need it as a string in the dict.
    
    exact_val = FractionOps.to_exact(final_result)
    latex_str = FractionOps.to_latex(final_result)
    
    return {
        "question_text": "精確計算\n\\[2.79\times 89.3-(-0.21\times 89.3).\\]\n答案不得使用近似值。",
        "correct_answer": {
            "value": str(exact_val), # Ensure it's a string for JSON safety as per contract requirement usually implying serializable form
            "canonical_latex": latex_str
        },
        "oracle_payload": {
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
    }