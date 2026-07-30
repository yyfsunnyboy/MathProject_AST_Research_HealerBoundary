import math

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    
    # Calculate the coefficient (square root of radicand for perfect square case in this context)
    coeff = int(math.sqrt(radicand)) if radicand >= 0 else None
    
    # Generate canonical LaTeX string with simplified radical form
    latex_str = f"{coeff} \\sqrt{{{radicand}}}"

    return {
        "question_text": r"$\sqrt{27}$",
        "correct_answer": {"coefficient": coeff, "radicand": radicand, "canonical_latex": latex_str},
        "oracle_payload": kwargs
    }
