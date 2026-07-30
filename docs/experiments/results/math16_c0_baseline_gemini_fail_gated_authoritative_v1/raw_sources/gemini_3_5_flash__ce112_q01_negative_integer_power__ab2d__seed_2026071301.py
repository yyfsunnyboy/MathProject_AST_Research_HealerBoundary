from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    base = -3
    exponent = 3
    
    expr = f"({base}) ** {exponent}"
    correct_answer = IntegerOps.safe_eval(expr)
    
    base_str = IntegerOps.fmt_num(base)
    if base < 0:
        question_text = f"Calculate the value of $({base_str})^{{{exponent}}}$."
    else:
        question_text = f"Calculate the value of ${base_str}^{{{exponent}}}$."
        
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "base": base,
            "exponent": exponent
        }
    }