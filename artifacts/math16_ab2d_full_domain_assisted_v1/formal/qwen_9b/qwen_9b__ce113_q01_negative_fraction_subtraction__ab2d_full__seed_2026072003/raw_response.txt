from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Step 1: Construct operands from frozen expression "3/7 - (-1/4)"
    # Left operand: 3/7 -> numerator 3, denominator 7
    left = FractionOps.from_parts(3, 7)
    
    # Right operand: -1/4. The instruction says preserve the negative numerator.
    # So we create a fraction with numerator -1 and denominator 4.
    right = FractionOps.from_parts(-1, 4)
    
    # Step 2: Compute subtraction left - right
    result = FractionOps.sub(left, right)
    
    # Step 3: Assemble correct_answer according to the contract
    return {
        "question_text": "精確計算\n\\[\\frac{3}{7}-(-\\frac{1}{4}).\\]\n答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": FractionOps.to_latex(result)
        },
        "oracle_payload": {"expression": "3/7 - (-1/4)"}
    }