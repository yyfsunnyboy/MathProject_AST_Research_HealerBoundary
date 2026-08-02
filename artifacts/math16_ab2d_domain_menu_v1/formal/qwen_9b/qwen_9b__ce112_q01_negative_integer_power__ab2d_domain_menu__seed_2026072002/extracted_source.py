from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    base = kwargs.get("frozen_params", {}).get("base")
    exponent = kwargs.get("frozen_params", {}).get("exponent")
    
    # Compute (-3)^3 using safe_eval to ensure exact integer handling
    expr_str = f"({IntegerOps.fmt_num(base)}) ** {exponent}"
    result = IntegerOps.safe_eval(expr_str)
    
    return {
        "question_text": r"\[(-3)^3.\]",
        "correct_answer": int(result),
        "oracle_payload": kwargs.get("frozen_params", {})
    }