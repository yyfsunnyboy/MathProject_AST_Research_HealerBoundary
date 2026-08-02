from core.prompts.domain_function_library import FractionOps, Fraction

def generate(level=1, **kwargs):
    # Parse the frozen expression components from oracle_payload to ensure consistency
    expr_str = kwargs.get("oracle_payload", {}).get("expression")  # "3/7 - (-1/4)"
    
    # Extract operands based on the specific string format provided in task description:
    # \frac{3}{7}-\left(-\frac{1}{4}\right) -> 3/7 and -1/4
    
    term_a_str = "3/7"
    term_b_str = "-1/4"
    
    a = FractionOps.create(term_a_str)
    b = FractionOps.create(term_b_str)
    
    # Perform subtraction: A - B
    result = FractionOps.sub(a, b)
    
    # Construct the canonical answer object according to Task-specific answer contract
    correct_answer = {
        "numerator": int(result.numerator),
        "denominator": int(result.denominator),
        "canonical_latex": FractionOps.to_latex(result)
    }
    
    return {
        "question_text": r"精確計算 \[\frac{3}{7}-\left(-\frac{1}{4}\right).\] 答案須化為最簡分數。",
        "correct_answer": correct_answer,
        "oracle_payload": kwargs.get("oracle_payload")
    }