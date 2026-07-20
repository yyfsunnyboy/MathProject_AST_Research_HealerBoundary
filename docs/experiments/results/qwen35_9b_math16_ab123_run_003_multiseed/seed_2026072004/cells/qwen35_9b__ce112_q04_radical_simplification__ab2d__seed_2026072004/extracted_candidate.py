def generate(level=1, **kwargs):
    frozen_params = {"radicand": 135}
    
    # Ensure we have a radicand; if not provided in kwargs override or use default? 
    # Spec: "Frozen sampled parameters: {'radicand': 135}". oracle_payload must exactly equal this.
    # question_text generation logic needs to construct LaTeX for sqrt(135).
    
    radicand = frozen_params.get("radicand", kwargs.get('radicand', None)) 
    if radicand is None:
        raise ValueError("No radicand provided")

    # Perform simplification
    coeff, simplified_radicand = RadicalOps.simplify_term(1, radicand) 
    
    # Format the term
    latex_term = RadicalOps.format_term(coeff, simplified_radicand, is_first=True)
    
    # Construct question_text using formal LaTeX delimiters
    # Question text example: "Simplify \sqrt{<radicand>}" or similar. 
    # Let's make it generic based on task type "ce112_q04_radical_simplification".
    # Usually format: Simplify $\sqrt{n}$.
    
    question_text = f"Simplify $\\sqrt{{{radiacnd}}}$." # Typo check
    
    correct_answer = latex_term

    oracle_payload = frozen_params.copy()

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }