# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per contract
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }

    # Task: Rationalize denominator of numerator / (a - sqrt(r))
    # Expression: N / (A - sqrt(R)) = N * (A + sqrt(R)) / (A^2 - R)
    # Result form: [N*A/(A^2-R)] + [N*sqrt(R)/(A^2-R)] -> Coefficients for 1 and sqrt(R)
    
    numerator_val = frozen_params["numerator"]      # N = 9
    a_denom_part = int(frozen_params["denominator"].split("-")[0])   # A = 4
    radicand_val = frozen_params["radicand"]        # R = 7
    
    # Calculate denominator rationalization factor (A^2 - R)
    denom_sq_minus_r = a_denom_part ** 2 - radicand_val  # 16 - 7 = 9
    
    # Coefficient for the integer part: N * A / (A^2 - R)
    coeff_a = numerator_val * a_denom_part // denom_sq_minus_r
    
    # Coefficient for the sqrt(R) part: N / (A^2 - R)
    coeff_b = numerator_val // denom_sq_minus_r
    
    # The result is in form a + b*sqrt(7). We need to return integer sum a+b.
    correct_answer = coeff_a + coeff_b

    question_text = r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$ and express it as $a+b\sqrt{7}$ where $a,b \in \mathbb{Z}$. What is the value of $a+b$?"
    
    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }