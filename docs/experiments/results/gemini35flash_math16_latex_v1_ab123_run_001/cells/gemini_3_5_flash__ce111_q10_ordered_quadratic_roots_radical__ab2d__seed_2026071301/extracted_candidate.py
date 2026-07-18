from core.prompts.domain_function_library import RadicalOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    oracle_payload = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Solve the equation (x-2)^2 = 3
    # Roots are x = 2 \pm \sqrt{3}
    # Since a > b, a = 2 + \sqrt{3} and b = 2 - \sqrt{3}
    # Target: 2a + b = 2(2 + \sqrt{3}) + (2 - \sqrt{3}) = 4 + 2\sqrt{3} + 2 - \sqrt{3} = 6 + \sqrt{3}
    
    # Simplify the radical term using domain API
    coeff, radicand = RadicalOps.simplify_term(1, 3)
    
    rational_val = FractionOps.create(6)
    
    question_text = (
        "Solve the equation $(x-2)^2=3$. Let its roots be $a$ and $b$ "
        "such that $a>b$. Find the value of $2a+b$."
    )
    
    correct_answer = {
        "result": {
            "rational": rational_val,
            "radical_coefficient": coeff,
            "radicand": radicand,
            "canonical_latex": "6+\\sqrt{3}"
        }
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }