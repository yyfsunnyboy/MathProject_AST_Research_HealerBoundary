# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters as per task specification
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    p1_num, p1_den = frozen_params["p1"]
    p2_num, p2_den = frozen_params["p2"]
    
    # Compute product using native Python arithmetic (simplified for difficulty level 1)
    # Result numerator: p1 * p2
    result_numerator = p1_num * p2_num
    
    # Result denominator: lcm(p1_den, p2_den). Since denominators are small integers here, 
    # we can compute LCM manually or use gcd.
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    common_divisor = gcd(p1_den, p2_den)
    
    lcm_result_numerator = (p1_num * p2_num) // common_divisor
    
    # Denominator becomes LCM of original denominators divided by the GCD factor already handled in numerator? 
    # Actually: Result = (n1/n2) * (m/m') = (n*m)/(n'*m').
    # To reduce, we divide both num and den by gcd(num, den).
    
    result_denominator = p1_den * p2_den // common_divisor
    
    final_numerator = lcm_result_numerator
    final_denominator = result_denominator
    
    # Reduce fraction if not already irreducible (though direct multiplication often needs reduction)
    g_final = gcd(final_numerator, final_denominator)
    
    canonical_num = final_numerator // g_final
    canonical_den = final_denominator // g_final

    question_text = r"\text{What is the probability of both independent events occurring? The probabilities are } \frac{\text{" + str(p1_num) + "}}{\text{" + str(p1_den) + "}"} \text{ and } \frac{\text{" + str(p2_num) + "}}{\text{" + str(p2_den) + "}}"
    
    correct_answer = {
        "numerator": canonical_num,
        "denominator": canonical_den,
        "canonical_latex": r"\frac{" + str(canonical_num) + "}{" + str(canonical_den) + "}"
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }