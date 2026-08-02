from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # Solve (x-2)^2 = 3 => x - 2 = ±sqrt(3) => x = 2 ± sqrt(3)
    # Roots: a = 2 + sqrt(3), b = 2 - sqrt(3) since a > b.
    # Target expression: 2a + b = 2*(2+sqrt(3)) + (2-sqrt(3))
    #                  = 4 + 2*sqrt(3) + 2 - sqrt(3)
    #                  = 6 + sqrt(3)
    
    # Construct the term for sqrt(3): coefficient=1, radicand=3
    coeff = 1
    radicand = 3
    
    # Simplify to ensure canonical form (though 3 is square-free here)
    simplified_coeff, simplified_radicand = RadicalOps.simplify_term(coeff, radicand)
    
    # Construct the LinearRadical dict for the result term
    linear_radical_result = {
        "rational": 6,      # The integer part (2a+b rational component is 6)
        "radical_coefficient": simplified_coeff, 
        "radicand": simplified_radicand
    }
    
    # Format the canonical LaTeX: "6 + \sqrt{3}"
    canonical_latex = RadicalOps.format_linear_radical(linear_radical_result)
    
    return {
        "question_text": "一元二次方程式\n\\[\n(x-2)^2=3\n\\]\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。",
        "correct_answer": {
            "result": linear_radical_result,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs.get("frozen_params", {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"})
    }