from core.prompts.domain_function_library import IntegerOps


def generate(level=1, **kwargs):
    base = kwargs.get("base", -3)
    exponent = kwargs.get("exponent", 3)
    
    # Compute the result using safe_eval to ensure correct arithmetic handling of negative bases and powers
    expression = f"{base}**{exponent}"
    result = IntegerOps.safe_eval(expression)

    return {
        "question_text": r"計算\n\[(-3)^3.\]",
        "correct_answer": int(result),
        "oracle_payload": {"base": base, "exponent": exponent},
    }
