from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse the expression: 3/7 - (-1/4) = 3/7 + 1/4
    
    # Create fractions from parts
    a = FractionOps.from_parts(3, 7)
    
    # The second term is negative of -1/4, which becomes positive 1/4 in subtraction: x - (-y) = x + y
    b = FractionOps.from_parts(-1, 4)
    
    # Perform the operation: a - b. 
    # Note: In Python's fraction arithmetic, subtracting a negative is handled correctly by sub(a, b).
    result_fraction = FractionOps.sub(a, b)
    
    # Prepare correct_answer according to Task-specific answer contract
    numerator = int(result_fraction.numerator)
    denominator = int(result_fraction.denominator)
    canonical_latex = str(FractionOps.to_exact(result_fraction))  # Use string representation for 'p/q' format
    
    return {
        "question_text": r"精確計算\n\[\frac{3}{7}-\left(-\frac{1}{4}\right).\n答案須化為最簡分數。",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs.get("frozen_params") or {"expression": "3/7 - (-1/4)"}  # Ensure oracle_payload matches frozen_params if provided in context, otherwise default to the expression given. 
    }
