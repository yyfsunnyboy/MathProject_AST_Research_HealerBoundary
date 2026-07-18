from fractions import Fraction
from core.prompts.domain_function_library import FractionOps, RadicalOps

def generate(level=1, **kwargs):
    # Frozen parameters
    equation = "(x-2)^2=3"
    order = "a>b"
    target = "2a+b"
    
    # The equation is (x-2)^2 = 3
    # Roots are x = 2 +/- sqrt(3)
    # Since a > b, a = 2 + sqrt(3) and b = 2 - sqrt(3)
    # We want to find 2a + b = 2(2 + sqrt(3)) + (2 - sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3)
    
    # Simplify the radical term using RadicalOps
    coeff, radicand = RadicalOps.simplify_term(1, 3)
    
    # Create the rational part using FractionOps
    rational_val = FractionOps.create(6)
    
    # Canonical LaTeX representation
    canonical_latex = "6+\\sqrt{3}"
    
    question_text = (
        "Let $a$ and $b$ be the roots of the quadratic equation $(x-2)^2=3$ such that $a > b$. "
        "Find the value of $2a+b$. Write your answer in the form $p + q\\sqrt{r}$ where $p, q$ are rational and $r$ is a square-free integer."
    )
    
    correct_answer = {
        "result": {
            "rational": rational_val,
            "radical_coefficient": coeff,
            "radicand": radicand,
            "canonical_latex": canonical_latex
        }
    }
    
    oracle_payload = {
        "equation": equation,
        "order": order,
        "target": target
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }