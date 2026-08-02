from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # Solve (x-2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots: a = 2 + sqrt(3), b = 2 - sqrt(3) since a > b.
    # Target expression: 2a + b = 2*(2+sqrt(3)) + (2-sqrt(3)) 
    #                  = 4 + 2*sqrt(3) + 2 - sqrt(3)
    #                  = 6 + sqrt(3)
    
    # Construct the term for sqrt(3): coefficient=1, radicand=3
    coeff = RadicalOps.exact_integer(Fraction(1))
    radicand = RadicalOps.exact_integer(Fraction(3))
    
    # Simplify to ensure canonical form (though 3 is square-free)
    simplified_coeff, simplified_radicand = RadicalOps.simplify_term(coeff, radicand)
    
    # Construct the full answer dict according to task-specific contract
    result_dict = {
        "rational": 6,
        "radical_coefficient": int(simplified_coeff),
        "radicand": int(simplified_radicand),
        "canonical_latex": RadicalOps.format_term(int(simplified_coeff), int(simplified_radicand))
    }

    return {
        "question_text": "一元二次方程式\\n[\\n(x-2)^2=3\\n]的兩根為 \\(a,b\\)，且 \\(a>b\\)。求 \\(2a+b\\)，答案須保持精確根式形式。",
        "correct_answer": {
            "result": result_dict,
        },
        "oracle_payload": {
            "equation": "(x-2)^2=3",
            "order": "a>b",
            "target": "2a+b"
        }
    }