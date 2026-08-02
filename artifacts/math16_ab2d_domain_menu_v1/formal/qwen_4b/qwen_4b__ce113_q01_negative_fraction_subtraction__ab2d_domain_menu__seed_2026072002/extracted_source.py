from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse the expression: 3/7 - (-1/4) which is equivalent to 3/7 + 1/4
    
    # Create fractions from parts (numerator, denominator)
    a = FractionOps.from_parts(3, 7)
    
    # The second term is negative of -1/4, so we are subtracting (-1/4), 
    # which equals adding 1/4. We create the fraction 1/4 and add it to a.
    b = FractionOps.from_parts(1, 4)
    
    # Perform addition: 3/7 + 1/4
    result_fraction = FractionOps.add(a, b)
    
    # Prepare correct_answer according to task-specific contract
    numerator = int(result_fraction.numerator)
    denominator = int(result_fraction.denominator)
    canonical_latex = str(FractionOps.to_exact(result_fraction))
    
    return {
        "question_text": r"精確計算\n\[\frac{3}{7}-\left(-\frac{1}{4}\right).\n答案須化為最簡分數。",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs.get("frozen_params", {"expression": "3/7 - (-1/4)"})
    }
