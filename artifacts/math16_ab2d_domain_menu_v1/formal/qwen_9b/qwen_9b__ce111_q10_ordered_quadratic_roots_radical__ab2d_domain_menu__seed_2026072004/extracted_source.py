from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # Solve (x-2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots: a = 2 + sqrt(3), b = 2 - sqrt(3) since a > b.
    # Target expression: 2a + b = 2*(2+sqrt(3)) + (2-sqrt(3)) 
    #                   = 4 + 2*sqrt(3) + 2 - sqrt(3)
    #                   = 6 + sqrt(3)
    
    # Construct the term for sqrt(3): coefficient=1, radicand=3.
    # Rational part is 6.
    
    rational_part = 6
    
    # Simplify radical: simplify_term expects (coeff, radicand). 
    # We want to represent 'sqrt(3)' which corresponds to coeff=1, radicand=3.
    # However, the API simplifies based on input. Let's pass raw values if needed or just construct directly.
    # The problem asks for exact form 6 + sqrt(3). 
    # We need a LinearRadical dict structure: {"rational": int, "radical_coefficient": int, "radicand": int}
    
    term_dict = {
        "rational": rational_part,
        "radical_coefficient": 1,
        "radicand": 3
    }

    # Use format_linear_radical to get the LaTeX string for this specific structure.
    canonical_latex = RadicalOps.format_linear_radical(term_dict)

    return {
        "question_text": kwargs.get("frozen_params", {}).get("equation") + "\n" + \
                        r"\[(x-2)^2=3\]\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。".replace(r'\[', '').replace(r'\]', '') if 'frozen_params' in kwargs else "一元二次方程式\n(x-2)^2=3\n的兩根為 a,b，且 a>b。求 2a+b，答案須保持精確根式形式。",
        # Actually, the prompt says: use frozen task description as question_text. 
        # The provided text in 'frozen_params' block is just equation info. 
        # I must construct the full stem from the "Frozen task description" section of the prompt instructions if not passed directly?
        # Re-reading: "use as question_text". Usually this means passing the string literal found under ## Frozen task description.
        # Let's use the exact text provided in the '## Task' -> '## Frozen task description' block, cleaning up LaTeX delimiters for standard strings if necessary or keeping them raw? 
        # The example output contract expects a str. I will provide the clean Chinese/English stem derived from the prompt instructions.
        
        "correct_answer": {
            "result": term_dict,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs.get("frozen_params", {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"})
    }