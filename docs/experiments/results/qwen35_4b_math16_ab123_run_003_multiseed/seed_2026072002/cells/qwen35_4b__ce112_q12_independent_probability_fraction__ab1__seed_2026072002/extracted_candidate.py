def generate(level=1, **kwargs):
    p1_min, p1_max = kwargs.get("p1", [2, 6])
    p2_min, p2_max = kwargs.get("p2", [1, 5])
    
    import random
    
    r1 = random.randint(p1_min, p1_max) / (r1 + 3.0) if level == "weighted" else None # Placeholder logic for demo structure only if needed but task implies fixed params usage in payload
    # Actually re-reading: oracle_payload must EXACTLY equal frozen sampled parameters passed or available. 
    # Since kwargs might not have them if they are 'frozen' externally, we should use the provided defaults from spec as fallback if keys missing to ensure deterministic behavior matching "Frozen" concept for this specific task instance logic in a static context.
    
    # To strictly follow "oracle_payload must exactly equal the frozen sampled parameters", 
    # and since these are passed via kwargs or implied by the function signature's default handling of 'frozen' data:
    # We will assume p1 and p2 come from the environment/freeze list provided in spec.
    
    if not isinstance(p1_min, int) or len(kwargs.get("p1", [0])) < 2: 
        # Fallback to specification defaults if kwargs are empty/invalid for this specific frozen task instance simulation
        p1_list = [2] + [6] # Treat as bounds? No, spec says "Frozen sampled parameters". Usually implies the values themselves.
        pass
    
    # Correct interpretation of Frozen Sampled Parameters: They are the actual probability values to be used in the question generation for this run.
    # p1 range [2, 6] likely means value is chosen from that set or those specific integers? 
    # Given "probability fraction", let's assume we pick one integer numerator/denominator pair logic or just use them as parameters P(A)=a/b.
    # Let's interpret the list [x, y] in spec ["p1": [2, 6]] as potential values for p1? Or bounds? 
    # Usually "sampled parameters" means these are the specific constants used to generate THIS question. 
    # If it says [2, 6], maybe P1 is one of them? Let's pick one randomly from the list provided in spec if possible, or treat as range.
    # Safest bet for "fraction": Use p1 and p2 directly as numerators/denominators to form fractions like (p1)/(3+p1) ? 
    # Or simply P(A)=a/b where a,b are derived from the list.
    
    # Let's assume the task asks: Given independent events with probabilities p1 and p2, find P(both).
    # We need specific values for p1 and p2 to generate 'correct_answer'. 
    # The spec says "Frozen sampled parameters": {"p1": [2, 6], "p2": [1, 5]}. 
    # This likely means the generator chooses ONE value from each list.
    
    import random as rnd
    
    val_p1 = rnd.choice([x for x in kwargs.get("p1", [2]) if isinstance(x, int)])
    val_p2 = rnd.choice([x for x in kwargs.get("p2", [1]) if isinstance(x, int)])
    
    # If the list represents a range or specific set? 
    # Let's assume they are sets of allowed values. We pick one.
    p_a = val_p1 / (val_p1 + 3) # Example construction to make it non-trivial fraction math problem
    p_b = val_p2 / (val_p2 + 4) 
    
    num = int(p_numerator := (p_a * p_b).numerator if hasattr((p_a * p_b), 'numerator') else None)
    
    # Let's construct the question based on independent probabilities P(A)=x, P(B)=y. 
    # Question: What is the probability that both A and B occur? Answer = x*y.
    
    final_num_p1 = val_p1 * (val_p2 + 3) # Construct a fraction for p_a like v/(v+3)? No, let's make it simple: P(A)=a/b form from integers directly if possible or derived. 
    # Let's define the probability as an irreducible fraction where numerator/denominator are coprime integers >1 to avoid trivial answers 0/1 etc unless specified otherwise (though standard).
    
    a = val_p1 + 2
    b = val_p1 * 3
    c = val_p2 * 4
    
    # Let's define P(A) = (a+val_p1)/(b+something)? 
    # Simpler: The problem is "Independent events A and B. Prob(A)=p, Prob(B)=q. Find Prob(both)."
    # We generate p and q from the lists provided in 'frozen' parameters? 
    # Let's assume the values IN the list are the numerators/denominators components or just probabilities represented as integers to be converted? 
    # Given "rational_arithmetic", let's treat val_p1, val_p2 as inputs to form fractions.
    
    p_a_num = a := (val_p1 * 5) + 30
    p_a_denom = b := ((val_p1 - 1) * 4) + 6
    
    # Let's just use the integers directly as part of the fraction construction to ensure irreducibility is handled by GCD.
    
    num_prob_a = val_p1 
    den_prob_a = (3 + val_p1) 
    
    num_prob_b = val_p2 
    den_prob_b = (4 + val_p2)
    
    total_num = int(num_prob_a * num_prob_b) # Numerator of product P(A)*P(B)
    total_denom = int(den_prob_a * den_prob_b)   # Denominator
    
    import math as mth
    common_divisor = mth.gcd(total_num, total_denom)
    
    final_num = total_num // common_divisor
    final_denom = total_denom // common_divisor
    
    correct_answer_latex = f"\\frac{{{final_num}}}{{"{total_denom}"}}" # Wait format: canonical latex for irreducible fraction. 
    # LaTeX should be \frac{num}{den}. The variable part in string is tricky.
    
    question_text = r"""Let $A$ and $B$ be independent events with probabilities $P(A) = \frac{\text{{val\_p1}}}{\text{{3 + val\_p1}}} $ and $P(B) = \frac{\text{{val\_p2}}}{\text{{4 + val\_p2}}} $. What is the probability that both $A$ and $B$ occur? Express your answer as an irreducible fraction."""
    
    # Actually, to ensure strict adherence without runtime variable injection issues in LaTeX string: 
    # Use f-string with actual values.
    
    latex_p_a = r"\frac{" + str(num_prob_a) + r"}{" + str(den_prob_a) + r"}"
    latex_p_b = r"\frac{" + str(num_prob_b) + r"}{" + str(den_prob_b) + r"}"
    
    question_text_final = f"""Let events $A$ and $B$ be independent with probabilities ${latex\_p\_a}$ and ${latex\_p\_b}$. Find the probability that both occur."""
    
    correct_answer_latex_final = r"\frac{" + str(final_num) + r"}{" + str(final_denom) + r"}"
    
    return {
        "question_text": question_text_final,
        "correct_answer": {"numerator": final_num, "denominator": final_denom, "canonical_latex": correct_answer_latex_final},
        "oracle_payload": kwargs.get("p1", [2]) + kwargs.get("p2", [5]), # Wait, payload must be the dict exactly. 
    }

# Fixing the return structure to match spec: oracle_payload == frozen sampled parameters {"p1": [...], "p2": [...]}.
# Since we need to generate ONE question per run based on one sample from those lists? Or use all? 
# Task says "Frozen sampled parameters". Usually implies these are THE params for this instance. 
# If the list contains multiple values, it might be a set of possible answers or bounds. 
# Given difficulty 1 and rational arithmetic, let's assume we pick ONE value per key from their respective lists to form the question.
    
    # Re-implementing with proper selection logic inside generate:

def generate(level=1):
    import random as rnd
    
    # Use defaults if not provided in kwargs (simulating frozen state)
    p1_opts = [2, 6] 
    p2_opts = [1, 5] 
    
    # Pick one instance for this question generation to ensure determinism per run seed or just fixed choice? 
    # Let's pick the first available if random is not seeded, but usually frozen params are fixed.
    # If they are "sampled", maybe we sample once. But without a global seed, let's use the lists as provided in spec directly? 
    # Or assume p1=2, p2=1 (first elements)? 
    # Let's try to pick one from each list randomly if allowed by 'frozen' context implying variability within bounds.
    
    val_p = rnd.choice(p1_opts)
    val_q = rnd.choice(p2_opts)
    
    num_a = 3 * val_p + 5
    den_a = 4 * val_p + 7
    
    num_b = 6 * val_q - 2 
    den_b = 8 * val_q + 9
    
    # Probability P(A) = num_a / den_a, P(B) = num_b / den_b.
    total_num = int(num_a * num_b)
    total_denom = int(den_a * den_b)
    
    import math as mth
    gcd_val = mth.gcd(total_num, total_denom)
    
    final_nu = total_num // gcd_val
    final_de = total_denom // gcd_val
    
    latex_ans = r"\frac{" + str(final_nu) + r"}{" + str(final_de) + r"}"
    
    q_str = f"""Let events $A$ and $B$ be independent with probabilities $\frac{{{val\_p}}}{{3{val\_p}+5}}$ and $\frac{{{val\_q}}}{{6{val\_q}-2}}$. What is the probability of both occurring?"""
    
    # Correction: f-string syntax in latex needs to avoid variable names inside math mode if possible or escape properly. 
    # Let's construct string safely.
    
    q_str = r"Let events $A$ and $B$ be independent with probabilities $\frac{\text{{val_p}}}{{3\cdot \text{val\_p}+5}}$ and $\frac{\text{{val_q}}}{{6\cdot \text{val\_q}-2}}$. What is the probability of both occurring?}"
    # Actually, better to hardcode values into string for clean LaTeX.
    
    q_str = f"""Let events $A$ and $B$ be independent with probabilities $\frac{{{num_a}}}{{"{den_a}"}}$ and $\frac{{{num_b}}}{{"{den_b}"}}$. What is the probability of both occurring?"""
    
    return {
        "question_text": q_str,
        "correct_answer": {"numerator": final_nu, "denominator": final_de, "canonical_latex": latex_ans},
        "oracle_payload": {"p1": p1_opts.copy(), "p2": p2_opts.copy()} # Ensure exact match to spec format. 
    }