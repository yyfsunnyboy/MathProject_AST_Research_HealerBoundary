from core.prompts.domain_function_library import FractionOps, RadicalOps

def generate(level=1, **kwargs):
    # Frozen parameters
    equation = "(x-2)^2=3"
    order = "a>b"
    target = "2a+b"
    
    # Roots of (x-2)^2 = 3 are 2 + sqrt(3) and 2 - sqrt(3)
    # Since a > b, a = 2 + sqrt(3), b = 2 - sqrt(3)
    # Target is 2a + b = 2(2 + sqrt(3)) + (2 - sqrt(3)) = 6 + sqrt(3)
    
    # Use domain APIs
    coeff, radicand = RadicalOps.simplify_term(FractionOps.create(1), 3)
    rational = FractionOps.create(6)
    
    # Construct canonical latex
    canonical_latex = "6 + \\sqrt{3}"
    
    question_text = (
        "Solve the equation \\((x-2)^2=3\\). "
        "Let the roots be \\(a\\) and \\(b\\) such that \\(a>b\\). "
        "Find the value of \\(2a+b\\)."
    )
    
    oracle_payload = {
        "equation": equation,
        "order": order,
        "target": target
    }
    
    result_dict = {
        "rational": rational,
        "radical_coefficient": coeff,
        "radicand": radicand,
        "canonical_latex": canonical_latex
    }
    
    correct_answer = {
        "rational": rational,
        "radical_coefficient": coeff,
        "radicand": radicand,
        "canonical_latex": canonical_latex,
        "result": result_dict
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }