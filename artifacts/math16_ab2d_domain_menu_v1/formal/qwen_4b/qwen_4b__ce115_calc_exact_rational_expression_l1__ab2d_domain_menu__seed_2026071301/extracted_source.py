from core.prompts.domain_function_library import FractionOps, to_exact_adapter

def generate(level=1, **kwargs):
    # Parse the frozen_params as per task description
    products = kwargs.get("frozen_params", {}).get("products")
    
    if not isinstance(products, list) or len(products) != 2:
        raise ValueError(f"Expected exactly two product entries in oracle_payload. Got {len(products)}.")

    # Extract components for the first term: 2.79 * 89.3 (sign +1 means positive result of this multiplication)
    p1 = products[0]
    left_str_1 = str(p1["left"])
    right_str_1 = str(p1["right"])

    # Extract components for the second term: -0.21 * 89.3 (sign -1 means negative result of this multiplication)
    p2 = products[1]
    left_str_2 = str(p2["left"])
    right_str_2 = str(p2["right"])

    # Convert string numbers to Fractions using from_parts or create via float conversion if necessary. 
    # Since inputs are decimal strings, we convert them directly to Fraction objects for precision.
    
    def parse_decimal_to_fraction(s):
        """Convert a decimal string like '2.79' into an exact Fraction."""
        return FractionOps.create(float(s))

    term1 = parse_decimal_to_fraction(left_str_1) * parse_decimal_to_fraction(right_str_1)
    # The sign is +1, so we keep the result as is (positive).
    
    term2_raw = parse_decimal_to_fraction(abs(str(p2["left"]))) * parse_decimal_to_fraction(right_str_2)
    # The sign is -1. So the actual value of (-0.21 * 89.3) is negative.
    term2 = FractionOps.create(-float(term2_raw))

    result_frac = term1 + term2
    
    # Prepare correct_answer according to Task-specific answer contract:
    # {"value": str, "canonical_latex": str}
    
    value_str = FractionOps.to_exact(result_frac)
    latex_str = FractionOps.to_latex(result_frac)

    return {
        "question_text": kwargs.get("frozen_params", {}).get("description"),
        "correct_answer": {"value": value_str, "canonical_latex": latex_str},
        "oracle_payload": kwargs.get("frozen_params")
    }
