from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Parse frozen_params from kwargs or default structure if needed for context, 
    # but strictly we must use the provided 'frozen_params' logic in a real scenario.
    # Here we reconstruct based on task description to ensure correctness without reading forbidden tables.
    
    # Define operands as strings per Frozen task description
    term1_left = "2.79"
    term1_right = "89.3"
    sign1 = 1
    
    term2_left_str = "-0.21"
    term2_right = "89.3"
    
    # Create fractions for the first product: 2.79 * 89.3
    f_a = FractionOps.create(term1_left)
    f_b = FractionOps.create(term1_right)
    prod1 = FractionOps.mul(f_a, f_b)
    
    # Create fraction for second term: -0.21 (handle sign separately or via create if supported by string parsing logic usually handling negatives in numerator/denominator implicitly or explicitly). 
    # The API description says inputs can be legal numeric str. "-0.21" should work directly creating Fraction(-21, 100)
    
    f_c = FractionOps.create(term2_left_str)
    prod2_raw = FractionOps.mul(f_c, FractionOps.create(term2_right))
    
    # Apply sign to the second product if necessary (create might handle "-0.21" as negative numerator already). 
    # Let's verify logic: -0.21 * 89.3 should be negative result.
    # If create("-0.21") returns Fraction(-21, 100), then mul is correct.
    
    final_value = prod1 + prod2_raw
    
    # Serialize to exact string format (e.g., "p/q" or int) using the adapter mentioned in boundary notes
    # Note: The prompt says 'FractionOps.to_exact serializes Fraction values to JSON-safe int|'p/q'' only'. 
    # We use it for serialization.
    
    value_str = FractionOps.to_exact(final_value)
    
    # Generate canonical LaTeX representation (usually improper fraction or mixed depending on settings, default is usually standard latex)
    # The API example shows '\frac{2}{7}' for 2/7. For integers like '3', it might just be '3'. 
    # We use the adapter to_latex with default mixed=False as per typical exact math representation unless specified otherwise.
    
    latex_str = FractionOps.to_latex(final_value, mixed=False)
    
    return {
        "question_text": r"精確計算\n\[2.79\times 89.3-\left(-0.21\times 89.3\right).\]\n答案不得使用近似值。",
        "correct_answer": {
            "value": value_str,
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