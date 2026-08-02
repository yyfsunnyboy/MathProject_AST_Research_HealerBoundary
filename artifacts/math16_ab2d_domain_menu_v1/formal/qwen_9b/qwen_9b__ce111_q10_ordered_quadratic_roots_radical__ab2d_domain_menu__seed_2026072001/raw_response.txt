from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # Solve (x-2)^2 = 3 => x - 2 = ±sqrt(3) => x = 2 ± sqrt(3)
    # Roots: a = 2 + sqrt(3), b = 2 - sqrt(3) since a > b.
    # Target expression: 2a + b = 2*(2+sqrt(3)) + (2-sqrt(3)) 
    #                   = 4 + 2*sqrt(3) + 2 - sqrt(3)
    #                   = 6 + sqrt(3)
    
    # Construct the LinearRadical dict for term: coefficient=1, radicand=3
    term_dict = {
        "rational": 6,      # The rational part of the result (6)
        "radical_coefficient": 1, # Coefficient of sqrt(3)
        "radicand": 3       # The square-free radicand
    }

    return {
        "question_text": r"一元二次方程式\n\[(x-2)^2=3\]\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。",
        "correct_answer": {
            "result": term_dict,
            "canonical_latex": RadicalOps.format_expression(term_dict)
        },
        "oracle_payload": {
            "equation": "(x-2)^2=3",
            "order": "a>b",
            "target": "2a+b"
        }
    }