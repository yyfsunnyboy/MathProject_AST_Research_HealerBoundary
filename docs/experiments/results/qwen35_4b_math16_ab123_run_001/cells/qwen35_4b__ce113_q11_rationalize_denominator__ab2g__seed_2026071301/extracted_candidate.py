def generate(level=1, **kwargs):
    import random
    
    frozen_params = {
        "denominator": "4-sqrt(7)", 
        "numerator": 9, 
        "radicand": 7
    }
    
    # Rationalize the denominator: 9 / (4 - sqrt(7))
    # Multiply numerator and denominator by conjugate (4 + sqrt(7))
    # Result = [9 * (4 + sqrt(7))] / [(4)^2 - (sqrt(7))^2]
    #        = [36 + 9*sqrt(7)] / [16 - 7]
    #        = [36 + 9*sqrt(7)] / 9
    # Integer part of the result when expressed as a rationalized fraction is derived from the division.
    # The term (36/9) becomes an integer, but we need to interpret "correct_answer" based on the task context usually implying the simplified form or specific component if not fully simplifying roots in output.
    # However, looking at standard problem formats for this type: 9/(4-sqrt(7)) = (36 + 9sqrt(7))/9 = 4 + sqrt(7).
    # If the expected answer format requires an integer derived from this process or if there is a specific constraint interpretation. 
    # Re-reading "correct_answer must be a single exact integer". This implies the operation results in an integer under some condition or I should compute the rationalized form's components differently?
    # Let's re-evaluate: Rationalizing usually turns denominator to an integer (rational). The result is 4 + sqrt(7). This is not an integer.
    # Perhaps the question asks for the difference between numerator and denominator squared terms after expansion? Or maybe I misinterpreted "single exact integer".
    # Let's check if there's a specific math problem logic where this simplifies to an integer? No, 4+sqrt(7) is irrational.
    # Is it possible the question asks for the sum of rational and irrational parts coefficient? 
    # Wait, let's look at "math16_rationalize_denominator_ab_sum". Perhaps a+b in (a + b*sqrt(d)) form? Here 4+1*sqrt(7), so a=4, b=1. Sum = 5?
    # Or maybe the question is different: If we rationalize and then take integer part? No.
    # Let's consider the source of such problems often found in datasets like GSM8K or similar where they might ask for specific values derived from coefficients after simplification if forced to an integer context, OR perhaps I am missing a step that makes it fully cancel out (which mathematically isn't true here).
    
    # Hypothesis: The problem expects the answer based on the sum of numerator and denominator parts in the conjugate expansion divided by difference? 
    # Let's try to simulate what a valid integer solution could be for this context. 
    # If we assume the question implies finding (numerator * conj) / ((denom)^2 - rad^2), which is 4 + sqrt(7).
    # There is no exact integer result in standard arithmetic here unless 'correct_answer' refers to a parameter value or derived coefficient sum.
    # Given "ab_sum" hint: Result = A + B*sqrt(C). Answer might be A+B? 
    # In our case, 9/(4-sqrt(7)) -> (36+9sqroot(7))/9 -> 4 + sqrt(7). So A=4, B=1. Sum = 5.
    
    correct_answer_int_val = 5
    
    question_text_template = r"""Rationalize the denominator of $\frac{\text{numerator}}{\text{denominator}}$ given radicand $C$. Express result as sum $A + B\sqrt{C}$ and provide integer answer corresponding to the parameter 'ab_sum' logic implied by task specification."""
    
    question_text = question_text_template.replace("numerator", str(frozen_params["numerator"])) \
                              .replace("denominator", str(frozen_params["denominator"])) \
                              .replace("C", str(frozen_params["radicand"])).strip()
    
    # Ensure format uses formal LaTeX delimiters for math symbols in the text string provided. 
    # I will construct a clean question directly without relying on placeholder strings that look like code, ensuring proper rendering of variables if they were dynamic, but here fixed values are fine to embed as integers or formatted terms. 
    # Actually, just writing the specific numbers is safer for "formal LaTeX delimiters where math appears".
    
    final_question = r"""Rationalize the denominator $\frac{9}{4-\sqrt{7}}$. If the result can be written in the form $A + B\sqrt{7}$, find the value of $A+B$."""

    oracle_payload = frozen_params
    
    return {
        "question_text": final_question,
        "correct_answer": correct_answer_int_val,
        "oracle_payload": oracle_payload
    }