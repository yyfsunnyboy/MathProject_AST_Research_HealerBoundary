from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # Solve (x-2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots: a = 2 + sqrt(3), b = 2 - sqrt(3) since a > b.
    # Target expression: 2a + b = 2*(2+sqrt(3)) + (2-sqrt(3))
    #                  = 4 + 2*sqrt(3) + 2 - sqrt(3)
    #                  = 6 + sqrt(3)
    
    # Construct the term for sqrt(3): coefficient=1, radicand=3
    coeff = 1
    radicand = 3
    
    # Simplify to ensure canonical form (though 3 is square-free here)
    simplified_coeff, simplified_radicand = RadicalOps.simplify_term(coeff, radicand)
    
    # The rational part of the result is 6. 
    # We need to represent "6 + sqrt(3)" in the required format:
    # {"rational": int_part, "radical_coefficient": coeff, "radicand": radicand}
    # Here integer part = 6, radical coefficient = 1, radicand = 3.
    
    rational_part = 6
    
    result_dict = {
        "rational": rational_part,
        "radical_coefficient": simplified_coeff,
        "radicand": simplified_radicand
    }
    
    canonical_latex = RadicalOps.format_expression(result_dict)
    
    return {
        "question_text": kwargs.get('frozen_params', {}).get('equation') or "(x-2)^2=3", 
        # Actually, the prompt says use frozen task description as question_text.
        # But I must not read audit payloads. The 'task' block provides a specific string for question_text.
        # However, standard practice in these prompts is to reconstruct from kwargs if available or hardcode based on level/task_id logic implicitly defined by the "frozen_params" provided in the prompt description vs what's passed.
        # Re-reading: "Frozen task description (use as question_text)". 
        # I will use the string explicitly given in the Task section for this specific run, but since I cannot access external state beyond kwargs/frozen_params logic usually injected into generate...
        # Wait, the prompt says "frozen_params" is provided below. The function signature takes **kwargs which likely contains 'frozen_params'.
        # Let's assume frozen_params is in kwargs or we construct it based on task_id if not passed? 
        # Standard pattern: use kwargs.get('frozen_params', {}).get(...) but the instruction says "use as question_text".
        # I will extract from kwargs. If missing, fallback to hardcoded string for this specific ID logic isn't possible without reading audit.
        # However, looking at the provided text block under ## frozen_params... it is part of the prompt description. 
        # Usually in these environments, `generate` receives `frozen_params`. I will use that.
        
        "correct_answer": {
            "result": result_dict,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs.get('frozen_params', {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"})
    }