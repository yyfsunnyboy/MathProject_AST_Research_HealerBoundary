from core.prompts.domain_function_library import FractionOps, Fraction

def generate(level=1, **kwargs):
    # Parse the frozen expression components from kwargs or defaults if not present in a real scenario.
    # Based on task_id 'ce113_q01_negative_fraction_subtraction' and description: 3/7 - (-1/4)
    
    # Define operands based on the problem statement derived from task context
    num1, den1 = 3, 7      # First fraction: 3/7
    num2, den2 = -1, 4     # Second fraction inside parenthesis: -1/4
    
    a = FractionOps.from_parts(num1, den1)
    b = FractionOps.from_parts(num2, den2)
    
    # Perform subtraction: a - b corresponds to (3/7) - (-1/4)
    result = FractionOps.sub(a, b)
    
    return {
        "question_text": r"精確計算 \[ \frac{3}{7}-\left(-\frac{1}{4}\right). \] 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": FractionOps.to_latex(result)
        },
        "oracle_payload": {"expression": "3/7 - (-1/4)"}
    }