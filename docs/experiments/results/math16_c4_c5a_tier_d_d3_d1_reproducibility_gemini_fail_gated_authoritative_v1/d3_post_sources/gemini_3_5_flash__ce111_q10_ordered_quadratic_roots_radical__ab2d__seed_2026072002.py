from core.prompts.domain_function_library import RadicalOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    equation = "(x-2)^2=3"
    order = "a>b"
    target = "2a+b"
    
    # Solve:
    # (x-2)^2 = 3 => x - 2 = \pm \sqrt{3} => x = 2 \pm \sqrt{3}
    # Since a > b, a = 2 + \sqrt{3}, b = 2 - \sqrt{3}
    # target = 2a + b = 2(2 + \sqrt{3}) + (2 - \sqrt{3}) = 4 + 2\sqrt{3} + 2 - \sqrt{3} = 6 + \sqrt{3}
    
    # Using domain APIs
    coeff, radicand = RadicalOps.simplify_term(1, 3)
    rational_val = FractionOps.create(6)
    rational_int = int(rational_val)
    
    # Format expression using RadicalOps
    terms_dict = {1: rational_int, radicand: coeff}
    canonical_latex = RadicalOps.format_expression(terms_dict)
    
    question_text = (
        "Solve the equation \\((x-2)^2=3\\). "
        "Let its roots be \\(a\\) and \\(b\\) with \\(a > b\\). "
        "Find the value of \\(2a+b\\)."
    )
    
    correct_answer = {
        "result": {
            "rational": rational_int,
            "radical_coefficient": int(coeff),
            "radicand": int(radicand),
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