from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    expression_str = "9/22 + 11/18 - (23/22 - 7/18)"
    
    f1 = FractionOps.create("9/22")
    f2 = FractionOps.create("11/18")
    f3 = FractionOps.create("23/22")
    f4 = FractionOps.create("-7/18")
    
    inner = FractionOps.add(f3, f4)
    outer1 = FractionOps.add(f1, f2)
    
    neg_inner = FractionOps.create(f"-{inner.numerator}/{inner.denominator}")
    result = FractionOps.add(outer1, neg_inner)
    
    numerator = result.numerator
    denominator = result.denominator
    canonical_latex = FractionOps.to_latex(result)
    
    question_text = (
        "Evaluate the following expression:\n"
        "\\[ \\frac{9}{22} + \\frac{11}{18} - \\left(\\frac{23}{22} - \\frac{7}{18}\\right) \\]"
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "expression": expression_str
        }
    }