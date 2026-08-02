from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = kwargs.get('frozen_params', {"expression": "3/7 - (-1/4)"})
    
    # Parse the expression: 3/7 and -(-1/4) which is equivalent to adding 1/4.
    # The problem asks for 3/7 - (-1/4). 
    # We can parse this as (Fraction(3, 7)) minus (Fraction(-1, 4)).
    
    numerator_a = frozen_params["expression"].split(" ")[0].replace("-", "") if "-" in frozen_params["expression"] else "3"
    denominator_a = "7"
    
    # Actually, let's parse the expression string directly to be robust.
    # Expression: "3/7 - (-1/4)"
    # Left operand: 3/7 -> num=3, den=7
    a = FractionOps.from_parts(3, 7)
    
    # Right operand in subtraction is -(-1/4). 
    # The term being subtracted is negative one fourth.
    # So we are doing a + (1/4).
    # However, the instruction says "Compute FractionOps.sub(left, right)".
    # Let's interpret the expression as: 3/7 minus (-1/4).
    # Right operand value to subtract: -1/4.
    
    numerator_b = "-1"
    denominator_b = "4"
    b = FractionOps.from_parts(int(numerator_b), int(denominator_b))
    
    result_fraction = FractionOps.sub(a, b)
    
    correct_answer = {
        "numerator": result_fraction.numerator,
        "denominator": result_fraction.denominator,
        "canonical_latex": str(result_fraction).replace('/', '\\frac{').split('\\')[1] if '/' in str(result_fraction) else '0' # This is a hacky way to get latex without the function. 
    }

# Re-evaluating canonical_latex using the allowed API properly based on instructions
result_fraction = FractionOps.sub(a, b)
canonical_latex_str = result_fraction.numerator + '/' + str(result_fraction.denominator).replace('/', '') # No, that's wrong format for latex usually but let's use to_exact or construct string.

# Correct approach using the provided API:
correct_answer = {
    "numerator": int(result_fraction.numerator),
    "denominator": int(result_fraction.denominator),
    "canonical_latex": FractionOps.to_latex(result_fraction) # This returns '\frac{...}{...}' which is standard latex. Wait, the example shows '3/2' for to_exact and '\\frac{2}{7}' for to_latex? 
}

# Let's re-read examples:
# FractionOps.to_exact(Fraction(3, 2)) -> '3/2' (Wait, description says int|str with schema ^-?[0-9]+/[1-9][0-9]*$)
# Actually the example in docs: `FractionOps.to_latex(Fraction(2, 7))` returns `'\\frac{2}{7}'`.

correct_answer = {
    "numerator": int(result_fraction.numerator),
    "denominator": int(result_fraction.denominator),
    "canonical_latex": FractionOps.to_latex(result_fraction) # Assuming to_latex handles the formatting correctly as per example. 
}

# Wait, looking at `FractionOps.to_exact` description: returns_shape includes string_schema "^-?[0-9]+/[1-9][0-9]*$".
# And `to_latex`: returns `'\\frac{2}{7}'`.
# The contract requires "canonical_latex": str. 
# So using to_latex is correct.

question_text = frozen_params["expression"] # Wait, the prompt says use as question_text but also provides a specific Chinese text in Frozen task description.
# Instruction: "Frozen task description (use as question_text)" -> The block contains:
# 精確計算 \[ ... \] 答案須化為最簡分數。

question_text = "精確計算\n\\frac{3}{7}-\\left(-\\frac{1}{4}\\right).\n答案須化為最簡分數。" # Reconstructing from the provided block content.
# Actually, I should just copy the text exactly as given in the frozen_params description section if possible or use the variable name logic? 
# The prompt says: "Frozen task description (use as question_text)". Then below it lists the math and Chinese text.

question_text = f"精確計算\\frac{3}{7}-\\left(-\\frac{1}{4}\\right).答案須化為最簡分數。"

return {
    "question_text": question_text,
    "correct_answer": correct_answer,
    "oracle_payload": frozen_params
}
