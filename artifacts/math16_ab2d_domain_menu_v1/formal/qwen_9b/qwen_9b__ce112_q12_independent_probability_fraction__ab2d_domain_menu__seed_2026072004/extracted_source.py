from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Define the two independent events based on frozen_params
    # Event 1: 2 favorable out of 6 total -> Probability = 2/6
    num1 = kwargs["frozen_params"]["p1"][0]
    den1 = kwargs["frozen_params"]["p1"][1]
    
    # Event 2: 1 favorable out of 5 total -> Probability = 1/5
    num2 = kwargs["frozen_params"]["p2"][0]
    den2 = kwargs["frozen_params"]["p2"][1]

    p1_frac = FractionOps.from_parts(num1, den1)
    p2_frac = FractionOps.from_parts(num2, den2)

    # Calculate the product of probabilities for independent events
    combined_prob = FractionOps.mul(p1_frac, p2_frac)

    return {
        "question_text": kwargs["frozen_params"]["description"],
        "correct_answer": {
            "numerator": int(combined_prob.numerator),
            "denominator": int(combined_prob.denominator),
            "canonical_latex": FractionOps.to_latex(combined_frac=combined_prob) if hasattr(FractionOps, 'to_latex') else str(combined_prob).replace('Fraction(', '').replace('/', '/').replace(')', '') # Fallback logic handled by API usually returning string directly or needing manual formatting. 
            # However, looking at the API definition: FractionOps.to_latex(val, mixed=False) returns a str like '\frac{2}{7}'
            # The previous line was wrong in thought process regarding arguments. Correct call below.
        },
        "oracle_payload": kwargs["frozen_params"]
    }

# Correction for the return statement inside the function to ensure correct API usage:
def generate(level=1, **kwargs):
    frozen = kwargs.get("frozen_params", {})
    
    # Extract parameters from oracle payload
    p1_num = frozen["p1"][0]
    p1_den = frozen["p1"][1]
    p2_num = frozen["p2"][0]
    p2_den = frozen["p2"][1]

    # Create fractions for the two independent probabilities
    prob_a = FractionOps.from_parts(p1_num, p1_den)
    prob_b = FractionOps.from_parts(p2_num, p2_den)

    # Multiply to get joint probability (independent events)
    result_frac = FractionOps.mul(prob_a, prob_b)

    return {
        "question_text": frozen["description"],
        "correct_answer": {
            "numerator": int(result_frac.numerator),
            "denominator": int(result_frac.denominator),
            "canonical_latex": FractionOps.to_latex(result_frac)
        },
        "oracle_payload": frozen
    }