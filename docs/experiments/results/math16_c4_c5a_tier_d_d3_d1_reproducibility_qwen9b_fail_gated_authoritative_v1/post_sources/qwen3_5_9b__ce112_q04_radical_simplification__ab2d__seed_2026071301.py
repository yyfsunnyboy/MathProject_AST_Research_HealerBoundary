from fractions import Fraction
import random

# Mocking the required imports from a hypothetical library structure as per instructions


# Frozen sampled parameters
frozen_params = {"radicand": 135}

def generate(level=1, **kwargs):
    radicand_input = frozen_params.get("radicand", kwargs.get('radicand', None))
    
    # Task: Radical simplification for sqrt(radicand) -> coeff * sqrt(square_free_radicand)
    if radicand_input is None:
        raise ValueError("No radicand provided.")

    # Initial state: coefficient 1, full radicand input
    initial_coeff = 1
    
    # Simplify the term
    simplified_tuple = RadicalOps.simplify_term(initial_coeff, radicand_input)
    
    coeff_result = simplified_tuple[0]
    radicand_result = simplified_tuple[1]
    
    # Format the LaTeX string. 
    # Note: The prompt implies a single-term answer usually starting with positive sign or just the term.
    # We use format_term with is_first=True to get the standard representation of the first (and only) term in this context.
    latex_string = RadicalOps.format_term(coeff_result, radicand_result, is_first=True)
    
    # Construct correct_answer string. Usually "3\\sqrt{5}" or "\\frac{1}{2}\\sqrt{...}". 
    # Ensure no extra spaces if not needed, but LaTeX requires specific spacing often handled by the formatter logic above.
    # Let's ensure canonical_latex is clean.
    
    question_text = f"Simplify \\sqrt{{{radicand_input}}}."
    
    return {
        "question_text": question_text,
        "correct_answer": latex_string,
        "oracle_payload": frozen_params
    }