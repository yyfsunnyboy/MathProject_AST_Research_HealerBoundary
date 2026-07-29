import math
from fractions import Fraction
from typing import Dict, Any

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 0)
    
    # Simplify the radical term using domain API
    coeff, square_free_radicand = RadicalOps.simplify_term(1, radicand)
    
    # Format the LaTeX representation using domain API
    latex_str = RadicalOps.format_term(coeff, square_free_radicand)
    
    return {
        "question_text": f"Simplify $\\sqrt{{{radicand}}}$.",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": square_free_radicand,
            "canonical_latex": latex_str
        },
        "oracle_payload": radicand
    }