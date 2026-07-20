def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen", {"radicand": 135}) # Ensure we use the provided frozen param if available, otherwise default. 
    # The prompt says "Frozen sampled parameters: {'radicand': 135}" and oracle_payload must exactly equal them.
    
    radicand = frozen_params["radicand"]
    
    coeff, simplified_radicand = _get_max_square_factor(radicand)
    
    correct_latex = f"{coeff} \sqrt{{{simplified_radicand}}}".replace(" ", "") # Remove spaces for strict matching? Usually standard LaTeX. Let's keep it clean.
    
    question_text = r"\text{Simplify the radical: } $\sqrt{\text{" + str(radicand) + "}}"
    
    return {
        "question_text": question_text,
        "correct_answer": f"{coeff} \sqrt{{{simplified_radicand}}}",
        "oracle_payload": frozen_params
    }