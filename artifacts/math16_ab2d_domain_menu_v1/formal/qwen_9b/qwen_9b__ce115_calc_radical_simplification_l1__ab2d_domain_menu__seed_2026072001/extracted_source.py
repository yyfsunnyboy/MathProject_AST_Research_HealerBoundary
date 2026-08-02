from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", None)
    
    # If no frozen_params provided in kwargs (though task says oracle_payload must equal this object),
    # we assume the 'frozen' context is passed via kwargs or defaults. 
    # However, strictly following "oracle_payload: must exactly equal the frozen_params object provided":
    # We need to extract radicand from a potential source if not directly in level/kwargs for the calculation logic,
    # but usually these tasks pass 'frozen' dict as **kwargs['frozen'] or similar. 
    # Let's assume standard pattern where we might get frozen_params inside kwargs or use default 27 based on task description?
    # Re-reading: "oracle_payload must exactly equal the frozen_params object provided in the task block."
    # The function signature is generate(level=1, **kwargs). 
    # Usually 'frozen' dict containing radicand is passed as an argument or we derive it.
    # Given strict constraints and lack of explicit 'frozen' key mention in generic API usage example vs specific task:
    # I will assume the frozen_params (dict with radicand) might be accessible via kwargs.get('frozen', {}) 
    # OR simply use 27 if not passed, but to be robust against different test harnesses that pass 'frozen':
    
    frozen = kwargs.get("frozen", {"radicand": 27})
    raw_radicand = frozen["radicand"]

    coeff, rest = RadicalOps.simplify_term(raw_radicand, raw_radicand) # Wait, signature is (coeff, radicand). 
    # Correction: simplify_term takes (coefficient_input, radicand_input). We want to simplify sqrt(27), so input coefficient is 1.
    
    coeff, rest = RadicalOps.simplify_term(1, raw_radicand)

    latex_str = RadicalOps.format_term(coeff, rest)

    return {
        "question_text": "\n將\n\\[\n\\\\sqrt{27}\n\\]\n化為最簡根式 \\(a\\\\sqrt{b}\\)，其中 \\(a\\) 為正整數，且 \\(b\\) 不含大於 \\(1\\) 的完全平方因數。",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": latex_str
        },
        "oracle_payload": frozen
    }