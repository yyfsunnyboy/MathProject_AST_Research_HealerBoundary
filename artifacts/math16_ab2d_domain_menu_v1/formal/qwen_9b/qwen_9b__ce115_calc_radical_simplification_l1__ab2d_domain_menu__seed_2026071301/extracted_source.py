from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    question_text = f"將 \\sqrt{{{radicand}}} 化為最簡根式，其中係數為正整數且被開方數不含大於 1 的完全平方因數。"
    
    coeff, rest = RadicalOps.simplify_term(radicand, radicand)
    
    canonical_latex = RadicalOps.format_expression({rest: coeff})
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": int(coeff),
            "radicand": rest,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"radicand": radicand}
    }