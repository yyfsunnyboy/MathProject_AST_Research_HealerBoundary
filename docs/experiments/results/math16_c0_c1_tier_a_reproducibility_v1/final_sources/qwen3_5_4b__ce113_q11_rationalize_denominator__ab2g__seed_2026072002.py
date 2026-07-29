def generate(level=1, **kwargs):
    import re
    
    # Frozen sampled parameters must be preserved exactly as provided in the task specification context
    # The prompt specifies: {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    frozen_params = {
        "denominator": "4-sqrt(7)", 
        "numerator": 9, 
        "radicand": 7
    }
    
    # Construct the question text using formal LaTeX delimiters
    denominator_str = str(frozen_params["denominator"])
    numerator_val = int(frozen_params["numerator"])
    radicand_val = int(frozen_params["radicand"])
    
    # The task is to rationalize the denominator of a fraction.
    # Given form: (numerator) / (4 - sqrt(radicand))
    # We need to multiply numerator and denominator by the conjugate (4 + sqrt(radicand)).
    # Denominator becomes 16 - radicand = 9.
    
    question_text = r"Rationalize the denominator of the fraction $\frac{\text{" + str(numerator_val) + r"}{4-\sqrt{\text{" + str(radicand_val) + r"}}}$. Express your answer as a single integer."

    # Calculate correct_answer manually to ensure it is an exact integer
    # Expression: (9 * 4) / ((4)^2 - sqrt(7)^2) = 36 / (16 - 7) = 36 / 9 = 4
    numerator_part = int(frozen_params["numerator"]) * 4
    denominator_result = 16 - frozen_params["radicand"] # 16 - 7 = 9
    correct_answer = numerator_part // denominator_result
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }