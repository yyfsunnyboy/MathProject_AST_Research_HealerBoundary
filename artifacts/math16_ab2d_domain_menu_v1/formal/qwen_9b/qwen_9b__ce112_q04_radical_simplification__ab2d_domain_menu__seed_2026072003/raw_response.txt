from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135)
    
    # Simplify the term to get coefficient and square-free radicand
    coeff_simplified, rest_radical = RadicalOps.simplify_term(1, radicand)
    
    return {
        "question_text": r"將\[\sqrt{135}\]化為最簡根式。",
        "correct_answer": {
            "coefficient": int(coeff_simplified),
            "radicand": rest_radical,
            "canonical_latex": RadicalOps.format_term(int(coeff_simplified), rest_radical)
        },
        "oracle_payload": {"radicand": 135}
    }