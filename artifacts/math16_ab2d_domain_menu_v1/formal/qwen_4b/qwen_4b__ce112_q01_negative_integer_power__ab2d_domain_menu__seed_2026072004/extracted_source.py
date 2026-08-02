from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    base = kwargs.get("base", -3)
    exponent = kwargs.get("exponent", 3)
    
    result = IntegerOps.safe_eval(f"{base}**{exponent}")
    
    return {
        "question_text": r"計算\n\[(-3)^3.\]",
        "correct_answer": int(result),
        "oracle_payload": {"base": base, "exponent": exponent},
    }
