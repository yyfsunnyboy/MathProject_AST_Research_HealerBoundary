from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    base = -3
    exponent = 3
    
    correct_answer = IntegerOps.safe_eval(f"({base})**{exponent}")
    
    formatted_base = IntegerOps.fmt_num(base)
    question_text = f"Evaluate $({formatted_base})^{{{exponent}}}$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "base": base,
            "exponent": exponent
        }
    }