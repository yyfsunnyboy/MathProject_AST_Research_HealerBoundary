def generate(level=1, **kwargs):
    import random
    
    # Frozen sampled parameters
    p1_range = [2, 6]
    p2_range = [1, 5]
    
    # Sample probabilities (floats between 0 and 1)
    if "p1" in kwargs:
        p_val_1 = float(kwargs["p1"])
    else:
        p_val_1 = random.uniform(0.0, 1.0)
        
    if "p2" in kwargs:
        p_val_2 = float(kwargs["p2"])
    else:
        p_val_2 = random.uniform(0.0, 1.0)

    # Ensure values are within ranges for reproducibility based on frozen params context or simple bounds check
    if not (2 <= p_val_1 <= 6):
        p_val_1 = round(random.uniform(p1_range[0], p1_range[1]), 4)
    if not (1 <= p_val_2 <= 5):
        p_val_2 = round(random.uniform(p2_range[0], p2_range[1]), 4)

    # Independent probability question text using formal LaTeX delimiters
    latex_p1 = f"p_1 = {float(p_val_1)}"
    latex_p2 = f"p_2 = {float(p_val_2)}"
    
    question_text = r"""Calculate the joint probability of two independent events occurring simultaneously.

Given:
$P(A) = $ \text{$latex\_p1$\} and 
$P(B) = $ \text{$latex\_p2$\}.

Find $P(A \cap B)$ as an irreducible fraction in its simplest form."""

    # Compute joint probability (since independent, P(A and B) = P(A) * P(B))
    prob_product = p_val_1 * p_val_2
    
    numerator_str = str(int(round(prob_product))) if abs(float(numerator_str)-round(float(numerator_str))) < 0.000001 else "N/A" # Fallback logic for float conversion to int fraction representation
    denominator_str = str(1)

    # Since inputs are floats, we convert them to rational numbers first assuming they represent simple fractions or use a standard approach if exact input isn't guaranteed but context implies discrete probability space based on frozen params [2,6] and [1,5]. 
    # However, the task specifies "rational_arithmetic". Let's assume p_val_1 and p_val_2 are derived from integers n/d.
    # Re-reading: Frozen sampled parameters {"p1": [2, 6], "p2": [1, 5]}. Usually in these tasks, if not specified otherwise, we treat the input as a fraction representation or simple decimals. 
    # Let's assume p_val_1 and p_val_2 are given as fractions n/d where d=denom? Or simply that the user provides floats which need to be treated exactly.
    
    # To ensure robustness for "rational_arithmetic", let's treat them as exact values provided or generated from simple integer numerators if possible, but since they are sampled floats:
    # We will convert p_val_1 and p_val_2 into a common denominator representation to multiply accurately without floating point error.
    
    def float_to_fraction(f):
        d = 10**6
        n = round(f * d)
        return Fraction(n, d)

    from fractions import Fraction
    
    f_p1 = float_to_fraction(p_val_1)
    f_p2 = float_to_fraction(p_val_2)
    
    joint_frac = f_p1 * f_p2
    
    # Canonical LaTeX for irreducible fraction
    num_joint = int(joint_frac.numerator)
    den_joint = int(joint_frac.denominator)
    
    canonical_latex = rf"\frac{{{num_joint}}}{{\text{$den\_joint$}}}"

    correct_answer_dict = {
        "numerator": str(num_joint),
        "denominator": str(den_joint),
        "canonical_latex": canonical_latex.replace("$", "") # Remove $ from latex string if present in replacement logic, ensure pure mathjax style usually \frac{a}{b}
    }

    oracle_payload = {
        "p1": p_val_1, 
        "p2": p_val_2
    }

    return {
        "question_text": question_text.replace("latex_p1", latex_p1).replace("latex_p2", latex_p2), # Injected variables back into string
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }