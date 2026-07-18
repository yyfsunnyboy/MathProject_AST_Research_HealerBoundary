from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    base = -3
    exponent = 3
    
    # Calculate correct answer
    ans_val = IntegerOps.safe_eval(f"({base})**{exponent}")
    correct_answer = int(ans_val)
    
    # Format question text using LaTeX delimiters
    formatted_base = IntegerOps.fmt_num(base)
    question_text = f"Evaluate $({formatted_base})^{{{exponent}}}$."
    
    oracle_payload = {
        "base": base,
        "exponent": exponent
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }