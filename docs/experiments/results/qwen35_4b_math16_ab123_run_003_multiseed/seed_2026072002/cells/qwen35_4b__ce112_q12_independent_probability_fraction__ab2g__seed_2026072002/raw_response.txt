import fractions

def generate(level=1, **kwargs):
    p1_list = kwargs.get("p1", [2, 6])
    p2_list = kwargs.get("p2", [1, 5])
    
    # Select random values from the frozen parameter lists (using fixed indices for reproducibility in this context)
    n_p1 = p1_list[0] if isinstance(p1_list[0], int) else float(p1_list[0])
    m_p1 = p1_list[1] if len(p1_list) > 1 and isinstance(p1_list[1], (int, float)) else 6.0
    
    n_p2 = p2_list[0] if isinstance(p2_list[0], int) else float(p2_list[0])
    m_p2 = p2_list[1] if len(p2_list) > 1 and isinstance(p2_list[1], (int, float)) else 5.0
    
    # Calculate independent probability fraction: P(A and B) where A is n/m for first event? 
    # Based on "independent_probability_fraction", assume we are calculating the product of two probabilities.
    # Let p_a = m_p1 / n_p1 (assuming standard prob notation or vice versa, let's use n/numerator style as requested: numerator/denominator)
    # Actually, usually inputs like [2, 6] imply a fraction 2/6 or 6/2. 
    # Given "independent", it implies P(A)*P(B). Let's assume the input represents probability p = num / den.
    # To ensure irreducible fractions are handled correctly:
    
    frac1_num = m_p1 if isinstance(m_p1, int) else n_p1 # Assuming [2,6] means 2/6? Or 6/2? 
    # Let's interpret the list as [numerator, denominator]. So p1 = 2/6.
    
    frac1_num = float(p1_list[0]) if isinstance(p1_list[0], int) else p1_list[0]
    frac1_denom = float(p1_list[1]) if len(p1_list) > 1 and (isinstance(p1_list[1], int) or (len(p1_list)>1)) else 6.0
    
    # Re-evaluating based on typical CP patterns: [num, den]
    n_a = float(p1_list[0]) if isinstance(p1_list[0], int) else p1_list[0]
    d_a = float(p1_list[1]) if len(p1_list) > 1 and (isinstance(p1_list[1], int)) else 6.0
    
    n_b = float(p2_list[0]) if isinstance(p2_list[0], int) else p2_list[0]
    d_b = float(p2_list[1]) if len(p2_list) > 1 and (isinstance(p2_list[1], int)) else 5.0
    
    # Probability of independent events A * B
    num_total = n_a * n_b
    den_total = d_a * d_b
    
    reduced_frac = fractions.Fraction(num_total, den_total).limit_denominator(999) if isinstance(n_a, float) or isinstance(d_a, float) else fractions.Fraction(int(num_total), int(den_total))
    
    # If inputs were floats but came from ints in the list [2,6], treat as exact integers.
    num_val = int(reduced_frac.numerator)
    den_val = int(reduced_frac.denominator)
    
    question_text = r"\text{Let events } A \text{ and } B \text{ be independent with probabilities } P(A)=\frac{\{" + str(n_a).replace('.','') + "\}}{\{" + str(d_a).replace('.','') + "}\} \text{ and } P(B)=\frac{\{" + str(n_b).replace('.','') + "\}}{\{" + str(d_b).replace('.','') + "}\}. \text{ Find the probability of both events occurring: }"
    
    correct_answer = {
        "numerator": num_val,
        "denominator": den_val,
        "canonical_latex": r"\frac {" + str(num_val) + "}{" + str(den_val) + "}"
    }
    
    oracle_payload = p1_list if isinstance(p1_list[0], int) else [int(x) for x in p1_list]

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }