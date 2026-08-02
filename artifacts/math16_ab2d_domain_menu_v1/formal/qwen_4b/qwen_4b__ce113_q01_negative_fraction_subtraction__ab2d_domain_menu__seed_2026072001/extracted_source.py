from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse the expression: 3/7 - (-1/4) which is equivalent to 3/7 + 1/4
    
    # Create fractions from parts
    a = FractionOps.from_parts(3, 7)
    
    # The second term is negative of -1/4, so we subtract it (which adds positive 1/4)
    # Or equivalently: result = a - (-b) where b = Fraction(-1, 4)
    # Let's create the fraction for 1/4 first and negate its sign during subtraction
    
    b_numerator = -1
    b_denominator = 4
    b = FractionOps.from_parts(b_numerator, b_denominator)
    
    # Perform the subtraction: a - b where b is negative (-1/4), so we are adding positive value
    # Actually the expression is 3/7 minus (negative one fourth)
    # So it's 3/7 + 1/4
    
    # Let me recalculate properly: 
    # Expression: 3/7 - (-1/4) = 3/7 + 1/4
    
    b_positive = FractionOps.from_parts(1, 4)
    
    value = FractionOps.add(a, b_positive)
    
    # Get the canonical representation as per task-specific answer contract
    numerator = int(value.numerator)
    denominator = int(value.denominator)
    canonical_latex = str(FractionOps.to_exact(value)) if isinstance(FractionOps.to_exact(value), str) else FractionOps.to_latex(value)

    return {
        "question_text": r"精確計算\n\[\frac{3}{7}-\left(-\frac{1}{4}\right).\n答案須化為最簡分數。",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs.get("frozen_params") or {"expression": "3/7 - (-1/4)"}
    }
