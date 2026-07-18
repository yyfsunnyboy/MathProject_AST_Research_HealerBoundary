from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    # Frozen parameters
    base = -3
    exponent = 3
    
    # Calculate correct answer
    correct_answer = IntegerOps.safe_eval(f"({base})**{exponent}")
    
    # Format question text
    question_text = f"Calculate $({base})^{{{exponent}}}$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "base": base,
            "exponent": exponent
        }
    }