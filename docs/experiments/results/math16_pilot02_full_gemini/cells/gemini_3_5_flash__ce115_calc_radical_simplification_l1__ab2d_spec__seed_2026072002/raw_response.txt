# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters
    radicand_input = 27
    
    # Use RadicalOps to simplify the radical expression
    try:
        from core.prompts.domain_function_library import RadicalOps
        coeff, rad = RadicalOps.simplify_term(1, radicand_input)
    except ImportError:
        # Fallback implementation to avoid leaking and ensure robustness
        import math
        val = radicand_input
        coeff = 1
        for i in range(2, int(math.isqrt(val)) + 1):
            while val % (i * i) == 0:
                coeff *= i
                val //= (i * i)
        rad = val

    # Format canonical LaTeX
    if coeff == 1:
        canonical_latex = f"\\sqrt{{{rad}}}"
    else:
        canonical_latex = f"{coeff}\\sqrt{{{rad}}}"

    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand_input}}}$."

    correct_answer = {
        "coefficient": int(coeff),
        "radicand": int(rad),
        "canonical_latex": canonical_latex
    }

    oracle_payload = {
        "radicand": radicand_input
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }