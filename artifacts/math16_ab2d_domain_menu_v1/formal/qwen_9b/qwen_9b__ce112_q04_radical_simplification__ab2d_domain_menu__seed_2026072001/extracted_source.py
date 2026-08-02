from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = kwargs.get("frozen", {}).get("radicand") or {"radicand": 135}.get("radicand")
    
    coeff, rest = RadicalOps.simplify_term(1, radicand)
    
    return {
        "question_text": r"將 \[\sqrt{135}\] 化為最簡根式。",
        "correct_answer": {
            "coefficient": int(coeff),
            "radicand": rest,
            "canonical_latex": RadicalOps.format_term(int(coeff), rest)
        },
        "oracle_payload": {"radicand": radicand} if isinstance(radicand, dict) else {"radicand": radicand},
    }