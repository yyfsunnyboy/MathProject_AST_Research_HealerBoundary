from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Parse the expression components from frozen_params logic implied by task_id and description
    # Expression: 3/7 - (-1/4) which is equivalent to 3/7 + 1/4
    
    # Create fractions for operands based on the mathematical problem described in 'frozen' context
    # First term: 3/7
    num1 = FractionOps.from_parts(3, 7)
    
    # Second term inside parenthesis: -1/4. 
    # The operation is subtraction of this negative fraction: x - (-y) = x + y
    # We create the magnitude first then handle sign logic or directly compute sum if we treat it as addition.
    # However, to strictly follow "subtraction" API usage for the specific task type 'negative_fraction_subtraction':
    # Let's construct the negative fraction -1/4 explicitly using from_parts with negative numerator? 
    # FractionOps.from_parts expects int; usually handles negatives if passed directly or via create.
    # But let's stick to standard positive parts and logic for subtraction of a negative.
    
    # Constructing -1/4: Numerator -1, Denominator 4
    neg_num = FractionOps.from_parts(-1, 4) 
    
    # The task is "3/7 minus (-1/4)". 
    # We can use the sub API with these two fractions.
    
    term_a = num1          # 3/7
    term_b = neg_num       # -1/4
    
    # Perform subtraction: a - b => (3/7) - (-1/4)
    result_fraction = FractionOps.sub(term_a, term_b)
    
    # Prepare the correct_answer according to Task-specific answer contract
    # canonical_latex using mixed=False as standard for simple fractions unless specified otherwise
    
    latex_str = FractionOps.to_latex(result_fraction, mixed=False)
    
    return {
        "question_text": r"精確計算 \[\frac{3}{7}-\left(-\frac{1}{4}\right).\] 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result_fraction.numerator,
            "denominator": result_fraction.denominator,
            "canonical_latex": latex_str
        },
        "oracle_payload": {
            "expression": "3/7 - (-1/4)"
        }
    }