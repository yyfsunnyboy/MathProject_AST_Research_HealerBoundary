def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters as specified in the task description
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    p1_num, p1_den = frozen_params["p1"]
    p2_num, p2_den = frozen_params["p2"]
    
    # Calculate independent probability fraction: (p1 * p2) / (denom1 * denom2)
    numerator = p1_num * p2_num
    denominator = p1_den * p2_den
    
    # Simplify the fraction to irreducible form using GCD
    common_divisor = math.gcd(numerator, denominator)
    
    simplified_numerator = numerator // common_divisor
    simplified_denominator = denominator // common_divisor
    
    # Construct canonical LaTeX for the fraction
    if simplified_denominator == 1:
        canonical_latex = f"{simplified_numerator}"
    else:
        canonical_latex = rf"\frac{{{simplified_numerator}}}{{{simplified_denominator}}}"
    
    question_text = (
        r"Given two independent events with probabilities $\frac{p_1}{q_1}$ and $\frac{p_2}{q_2}$, "
        f"where $P(E_1) = \frac{{p_1}}{{q_1}}$ and $P(E_2) = \frac{{p_2}}{{q_2}}$, calculate the probability of both events occurring. "
        r"The probabilities are given as $\frac{{{p_1}}}{{{q_1}}} = \frac{{{frozen_params['p1'][0]}}}{{{frozen_params['p1'][1]}}}$ and $\frac{{{p_2}}}{{{q_2}}} = \frac{{{frozen_params['p2'][0]}}}{{{frozen_params['p2'][1]}}}$. "
        r"What is the probability of both events occurring, expressed as an irreducible fraction?"
    )

    # Replace placeholders with actual values in question text for clarity and correctness based on frozen params
    p1_val = f"{frozen_params['p1'][0]} / {frozen_params['p1'][1]}"
    p2_val = f"{frozen_params['p2'][0]} / {frozen_params['p2'][1]}"
    
    question_text_cleaned = (
        r"Given two independent events with probabilities $\frac{a}{b}$ and $\frac{c}{d}$, "
        f"where $P(E_1) = \frac{{{frozen_params['p1'][0]}}}{{{frozen_params['p1'][1]}}}$ and $P(E_2) = \frac{{{frozen_params['p2'][0]}}}{{{frozen_params['p2'][1]}}}$. "
        r"What is the probability of both events occurring, expressed as an irreducible fraction?"
    )

    # Reconstruct question text properly with LaTeX delimiters and correct values
    p1_str = rf"\frac{{{{{frozen_params['p1'][0]}}}}}{{{{{frozen_params['p1'][1]}}}}}"
    p2_str = rf"\frac{{{{{frozen_params['p2'][0]}}}}}{{{{{frozen_params['p2'][1]}}}}}"
    
    question_text_final = (
        r"Given two independent events with probabilities $P(A) = " + p1_str + 
        r"$ and $P(B) = " + p2_str + r"$, what is the probability of both A and B occurring? Express your answer as an irreducible fraction."
    )

    correct_answer_dict = {
        "numerator": simplified_numerator,
        "denominator": simplified_denominator,
        "canonical_latex": canonical_latex
    }

    result_dict = {
        "question_text": question_text_final,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }
    
    return result_dict