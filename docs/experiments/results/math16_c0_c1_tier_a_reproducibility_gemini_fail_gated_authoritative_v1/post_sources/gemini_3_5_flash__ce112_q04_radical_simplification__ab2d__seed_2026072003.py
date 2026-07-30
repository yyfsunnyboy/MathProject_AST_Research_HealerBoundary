from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = 135
    
    # Simplify the radical
    new_coeff, new_radicand = RadicalOps.simplify_term(1, radicand)
    
    # Format the question and answer
    question_latex = RadicalOps.format_term(1, radicand)
    answer_latex = RadicalOps.format_term(new_coeff, new_radicand)
    
    question_text = f"Simplify the radical expression: ${question_latex}$"
    
    correct_answer = {
        "coefficient": int(new_coeff),
        "radicand": int(new_radicand),
        "canonical_latex": answer_latex
    }
    
    oracle_payload = {
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }