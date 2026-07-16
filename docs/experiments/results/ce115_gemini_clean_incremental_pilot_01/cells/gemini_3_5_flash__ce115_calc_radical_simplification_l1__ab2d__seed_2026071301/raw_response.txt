from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Frozen parameters
    radicand = 27
    
    # Simplify the radical
    coeff_out, rad_out = RadicalOps.simplify_term(1, radicand)
    
    # Construct question text
    question_text = f"Simplify the radical: \\sqrt{{{radicand}}}"
    
    # Correct answer
    correct_answer = {
        "coefficient": int(coeff_out),
        "radicand": int(rad_out)
    }
    
    # Oracle payload
    oracle_payload = {
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }