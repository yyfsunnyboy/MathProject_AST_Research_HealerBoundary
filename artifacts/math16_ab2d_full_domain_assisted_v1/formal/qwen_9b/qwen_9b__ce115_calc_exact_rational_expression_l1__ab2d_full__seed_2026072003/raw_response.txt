from core.prompts.domain_function_library import FractionOps, Fraction

def generate(level=1, **kwargs):
    # Parse frozen_params from kwargs or default structure if needed for robustness
    # However, per instructions: "oracle_payload must exactly equal the frozen_params object provided"
    # We assume the task block's frozen_params is passed in kwargs under 'frozen_params' 
    # OR we construct it internally to match the requirement. 
    # Since the prompt says "Frozen task description (use as question_text)" and provides a specific JSON for frozen_params,
    # we must ensure oracle_payload matches that exact structure.
    
    # Reconstructing the logic based on the provided frozen_params in the prompt text:
    # Product 1: 2.79 * 89.3 (sign +1)
    # Product 2: -0.21 * 89.3 (effectively sign -1 applied to magnitude, or left is negative string)
    
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

    # Step 1: Create operands as Fractions from strings to ensure exactness
    val_279 = FractionOps.create("2.79")
    val_neg021 = FractionOps.create("-0.21")
    val_893 = FractionOps.create("89.3")

    # Step 2: Calculate products
    prod1 = FractionOps.mul(val_279, val_893) * frozen_params["products"][0]["sign"]
    
    # For the second product, we can either multiply magnitudes and apply sign or use the negative fraction directly.
    # The prompt's left is "-0.21". Let's create it as a positive magnitude then subtract? 
    # Or just create "-0.21" which handles the sign internally in FractionOps.create usually (if supported) 
    # but standard Fraction creation from string " -x " works if library supports negative strings.
    # Given `FractionOps.create` accepts legal numeric str, let's assume it parses signs correctly or we handle manually.
    # To be safe with the specific frozen_params structure where left is "-0.21", 
    # and sign is explicitly -1 in the second item... wait.
    # If I create Fraction("-0.21"), that includes the negative sign. Then multiplying by 89.3 gives a negative result.
    # The 'sign' field in frozen_params might be redundant if left already has it, OR 
    # maybe the system expects us to use magnitude and apply sign?
    # Let's look at `FractionOps.create` example: `create("2/7")`. It likely handles "-0.21" as a negative number directly.
    # However, the frozen_params explicitly lists "left": "-0.21". 
    # If I create Fraction("-0.21"), it is -21/100. Multiplying by 89.3 gives correct product.
    # Why is there a 'sign' field? Perhaps to handle cases where left is positive but sign flips?
    # Or maybe the library `create` expects magnitude and we apply sign manually? 
    # Let's assume standard behavior: create parses string including sign. But if the frozen_params implies an operation structure,
    # let's calculate product 2 using magnitudes to be consistent with typical math problem generation patterns where 'sign' is explicit control.
    
    # Actually, looking at `FractionOps.create` boundary: "inputs: int, finite float, legal numeric str...". 
    # It likely parses "-0.21" correctly. But the frozen_params has a separate 'sign'. 
    # Let's assume we should use magnitudes for creation and apply sign explicitly to avoid ambiguity or specific library quirks.
    
    mag_021 = FractionOps.create("0.21")
    prod2_mag = FractionOps.mul(mag_021, val_893)
    # Apply the explicit sign from frozen_params for product 2
    prod2 = prod2_mag * (-frozen_params["products"][1]["sign"]) if frozen_params["products"][1]["sign"] == -1 else prod2_mag
    
    # Wait, simpler approach: Just calculate based on values. 
    # Product 1: positive result.
    # Product 2: negative result (since left is "-0.21" or sign is -1).
    # Let's just compute the sum of signed products directly from the frozen_params logic.
    
    p1 = FractionOps.mul(FractionOps.create(frozen_params["products"][0]["left"]), 
                         FractionOps.create(frozen_params["products"][0]["right"])) * frozen_params["products"][0]["sign"]
                         
    # For p2, if left is "-0.21", creating it directly works. But let's follow the 'sign' hint in data structure strictly?
    # If I create " -0.21 ", result is negative. Multiplying by sign (-1) would make it positive (wrong).
    # So likely: Create magnitude, then apply sign from field.
    
    p2_mag = FractionOps.mul(FractionOps.create(frozen_params["products"][1]["left"].lstrip('-')), 
                             FractionOps.create(frozen_params["products"][1]["right"]))
    if frozen_params["products"][1]["sign"] == -1:
        p2 = -p2_mag
    else:
        p2 = p2_mag
        
    # Total sum
    total = p1 + p2
    
    # Step 3 & 4: Assemble correct_answer according to contract
    # Contract: {"value": str, "canonical_latex": str}
    # value should be exact rational string (e.g., 'p/q') or int. 
    # Use FractionOps.to_exact for the serialization of the final result?
    # Boundary says: `FractionOps.to_exact` serializes to JSON-safe int|'p/q'.
    
    val_str = FractionOps.to_exact(total)
    latex_str = FractionOps.to_latex(total, mixed=False)

    return {
        "question_text": "精確計算\n\\[2.79\times 89.3-\left(-0.21\times 89.3\right).\\]\n答案不得使用近似值。",
        "correct_answer": {
            "value": val_str,
            "canonical_latex": latex_str
        },
        "oracle_payload": frozen_params
    }