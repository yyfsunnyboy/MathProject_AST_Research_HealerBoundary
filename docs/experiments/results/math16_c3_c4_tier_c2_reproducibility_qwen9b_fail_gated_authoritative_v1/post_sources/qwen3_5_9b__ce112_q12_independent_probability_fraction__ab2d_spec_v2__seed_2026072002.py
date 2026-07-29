# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # 2. Define frozen parameters directly as per specification
    p1_numerator = 2
    p1_denominator = 6
    p2_numerator = 1
    p2_denominator = 5

    # 3. Compute the exact result using FractionOps
    frac_p1 = FractionOps.from_parts(p1_numerator, p1_denominator)
    frac_p2 = FractionOps.from_parts(p2_numerator, p2_denominator)
    
    product_frac = FractionOps.mul(frac_p1, frac_p2)

    # Extract components for the answer object
    ans_num = product_frac.numerator
    ans_den = product_frac.denominator
    
    # Construct canonical LaTeX string: \frac{numerator}{denominator}
    import re
    latex_str = r"\frac{" + str(ans_num) + "}" + r"}" + r"{\dagger" + str(ans_den) + r"}"

    correct_answer = {
        "numerator": ans_num,
        "denominator": ans_den,
        "canonical_latex": latex_str
    }

    question_text = (r"The probability of event $A$ is $\frac{" + str(p1_numerator) + "}{" + 
                      str(p1_denominator) + r"}$, and the probability of independent event $B$ is $\frac{" + 
                      str(p2_numerator) + "}{" + str(p2_denominator) + r"}$. "
                     r"What is the probability that both events occur? Express your answer as an irreducible fraction in LaTeX format.")

    oracle_payload = {
        "p1": [p1_numerator, p1_denominator], 
        "p2": [p2_numerator, p2_denominator]
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }